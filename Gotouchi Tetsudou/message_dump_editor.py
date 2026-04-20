"""
    python message_dump_editor.py
"""

import configparser, json, os, re, sys
import tkinter as tk
from tkinter import filedialog, messagebox

# ── Config path (next to this script) ────────────────────────────────────────
CFG_PATH = os.path.abspath(__file__) + ".cfg"

# ── Regex: all recognised tag types ──────────────────────────────────────────
_SEG_RE = re.compile(
    r'(\[([^\]/]+)/RUBY/([^\]]*)\])'                     # 1-3  ruby
    r'|(\[/BR/\])'                                        # 4    break
    r'|(\[/VO/([^\]]*)\])'                               # 5-6  voice
    r'|(%[-+0 #]*\d*(?:\.\d+)?[sdifgGxXoObceEu%])'     # 7    printf
)

def parse_segments(text: str) -> list:
    out, last = [], 0
    for m in _SEG_RE.finditer(text):
        if m.start() > last:
            out.append({"type":"plain","value":text[last:m.start()],
                        "start":last,"end":m.start()})
        if m.group(1):
            out.append({"type":"ruby","main":m.group(2),"ruby_text":m.group(3),
                        "raw":m.group(1),"start":m.start(),"end":m.end()})
        elif m.group(4):
            out.append({"type":"br","raw":m.group(4),
                        "start":m.start(),"end":m.end()})
        elif m.group(5):
            out.append({"type":"vo","filename":m.group(6),"raw":m.group(5),
                        "start":m.start(),"end":m.end()})
        else:
            out.append({"type":"printf","value":m.group(7),"raw":m.group(7),
                        "start":m.start(),"end":m.end()})
        last = m.end()
    if last < len(text):
        out.append({"type":"plain","value":text[last:],
                    "start":last,"end":len(text)})
    return out

def tk_idx(text: str, offset: int) -> str:
    before = text[:offset]
    line   = before.count('\n') + 1
    col    = len(before) - (before.rfind('\n') + 1)
    return f"{line}.{col}"

# ── Colour palette ────────────────────────────────────────────────────────────
BG          = "#1e1f2b"
BG_PANEL    = "#252636"
BG_CARD     = "#2d2e42"
BG_LIST     = "#1a1b27"
BG_ENTRY    = "#12131c"
ACCENT      = "#7c6af7"
ACCENT_DARK = "#5a4fc4"
FG          = "#e2e4f0"
FG_DIM      = "#8889a8"
FG_ORIG     = "#a0c4ff"
HIGHLIGHT   = "#3d3e5c"
MODIFIED    = "#f5a623"   # orange  – edited in this session
TRANSLATED  = "#5dba7d"   # green   – TEXT already differs from ORIGINAL
SAVED_OK    = "#4caf50"
BORDER      = "#3a3b52"
SEL_FILE    = "#33344f"
DANGER_BG   = "#c0392b"
DANGER_HV   = "#922b21"

# tag highlight colours
HL_RB_BRKT  = "#6666aa"
HL_RB_SEP   = "#aa88ff"   # bright purple — clearly visible /RUBY/
HL_RB_MAIN  = "#b8c0ff"
HL_RB_RT    = "#7090e0"
HL_PF_FG    = "#ffaa44"
HL_PF_BG    = "#2a1800"
HL_BR_FG    = "#ff6b8a"
HL_BR_BG    = "#3a0020"
HL_VO_FG    = "#00d4d4"
HL_VO_BG    = "#002a2a"
PV_RUBY_MAIN = "#c8d0ff"

# ── Shortcut definitions ──────────────────────────────────────────────────────
# Maps action_id → default tkinter binding string (or "" for none)
DEFAULT_SHORTCUTS = {
    "open"       : "<Control-o>",
    "save"       : "<Control-s>",
    "save_all"   : "<Control-Shift-s>",
    "save_as"    : "",
    "close_file" : "",
    "apply"      : "",
    "apply_next" : "<Control-Return>",
    "prev_entry" : "<Alt-Up>",
    "next_entry" : "<Alt-Down>",
    "revert"     : "",
    "add_ruby"   : "",
    "shortcuts"  : "",
}

SHORTCUT_LABELS = {
    "open"       : "Open file(s)",
    "save"       : "Save current file",
    "save_all"   : "Save all files",
    "save_as"    : "Save As...",
    "close_file" : "Close current file",
    "apply"      : "Apply edit",
    "apply_next" : "Apply & go to next",
    "prev_entry" : "Previous entry",
    "next_entry" : "Next entry",
    "revert"     : "Revert entry to original",
    "add_ruby"   : "Insert Ruby annotation...",
    "shortcuts"  : "Open shortcuts editor",
}

def _tk_to_display(tk_str: str) -> str:
    """Convert '<Control-Shift-s>' → 'Ctrl+Shift+S' for display."""
    if not tk_str:
        return "—"
    inner = tk_str.strip("<>")
    parts = inner.split("-")
    out        = []
    has_shift  = False
    for p in parts:
        if   p == "Control": out.append("Ctrl")
        elif p == "Alt":     out.append("Alt")
        elif p == "Shift":   out.append("Shift"); has_shift = True
        elif len(p) == 1 and p.isupper() and p.isalpha():
            # Uppercase letter in binding → implies Shift was required
            if not has_shift:
                out.append("Shift")
                has_shift = True
            out.append(p)
        elif len(p) == 1:    out.append(p.upper())
        else:                out.append(p)   # Return, F1, Up, Down …
    return "+".join(out)

# Keys that are themselves modifiers — ignore as solo presses
_MODIFIER_SYMS = frozenset({
    "Control_L","Control_R","Alt_L","Alt_R","Shift_L","Shift_R",
    "Super_L","Super_R","Meta_L","Meta_R","ISO_Level3_Shift",
    "Mode_switch","","??","VoidSymbol",
})

# Modifier state bit masks — cover Windows, X11, macOS Tk variants
# On X11: Ctrl=4, Shift=1, Mod1(Alt)=8
# On Windows: Ctrl=4, Shift=1, Alt=131072 (0x20000)
# On macOS: Command=8(?), Option/Alt=16 or 0x80
_MOD_SHIFT = 0x0001
_MOD_CTRL  = 0x0004
# Alt: Mod1=0x0008, Mod3=0x0080, Windows Alt=0x20000, sometimes 0x10000
_MOD_ALT   = 0x0008 | 0x0080 | 0x10000 | 0x20000

def _event_to_tk(event) -> str:
    """Build a canonical '<Modifier-key>' string from a KeyPress event.
    Handles Ctrl, Alt, Shift and all three-key combinations.
    Always normalises letter keys to lowercase with explicit Shift modifier."""
    keysym = event.keysym
    if not keysym or keysym in _MODIFIER_SYMS:
        return ""

    state    = event.state
    has_ctrl  = bool(state & _MOD_CTRL)
    has_shift = bool(state & _MOD_SHIFT)

    # Alt detection: check state bits AND check if Alt-keysym was generated
    # (some platforms set different bits)
    has_alt = bool(state & _MOD_ALT)

    # Tk sometimes encodes Shift into the keysym for letter keys (gives "S" not "s").
    # Normalise: make letter lowercase, record Shift explicitly.
    if len(keysym) == 1 and keysym.isalpha():
        if keysym.isupper():
            has_shift = True
        keysym = keysym.lower()

    mods = []
    if has_ctrl:  mods.append("Control")
    if has_alt:   mods.append("Alt")
    if has_shift: mods.append("Shift")

    # Must have at least one modifier (bare key → rejected by caller)
    if not mods:
        return ""

    return "<" + "-".join(mods + [keysym]) + ">"


# ── Cross-platform flat button (Label-based, macOS-safe) ──────────────────────
class FlatButton(tk.Label):
    """tk.Label styled as a button — respects bg on macOS unlike tk.Button."""
    def __init__(self, master, text, command=None,
                 bg=BG_CARD, fg=FG, hover_bg=HIGHLIGHT,
                 font_size=10, padx=10, pady=4, **kw):
        super().__init__(master, text=text, bg=bg, fg=fg,
                         font=("Segoe UI", font_size),
                         padx=padx, pady=pady, cursor="hand2", **kw)
        self._bg   = bg
        self._hv   = hover_bg
        self._cmd  = command
        self.bind("<Button-1>", lambda e: self._fire())
        self.bind("<Enter>",    lambda e: self.config(bg=self._hv))
        self.bind("<Leave>",    lambda e: self.config(bg=self._bg))

    def _fire(self):
        if self._cmd:
            self._cmd()

    def update_command(self, cmd):
        self._cmd = cmd


def _btn(parent, text, command,
         accent=False, small=False, large=False, danger=False, **kw):
    bg = (DANGER_BG if danger else ACCENT) if (accent or danger) else BG_CARD
    hv = (DANGER_HV if danger else ACCENT_DARK) if (accent or danger) else HIGHLIGHT
    sz = 9 if small else (11 if large else 10)
    py = 2 if small else (6 if large else 4)
    px = 8 if small else (16 if large else 10)
    return FlatButton(parent, text=text, command=command,
                      bg=bg, fg=FG, hover_bg=hv,
                      font_size=sz, padx=px, pady=py, **kw)


# ── Per-file state ────────────────────────────────────────────────────────────
class FileState:
    def __init__(self, path: str, data: dict):
        self.path             = path
        self.data             = data
        self.entries: list    = data.get("TEXTS", [])
        self.modified: set    = set()
        self.dirty            = False
        self.current_index    = None
        self.filtered_indices : list = []
        self.search_query     = ""

    @property
    def basename(self): return os.path.basename(self.path)
    @property
    def label(self): return ("● " if self.dirty else "  ") + self.basename


# ── Ruby edit / insert dialog ─────────────────────────────────────────────────
class RubyDialog(tk.Toplevel):
    def __init__(self, parent, *, mode="insert", main_val="", ruby_val=""):
        super().__init__(parent)
        self.result = None
        self.transient(parent)
        self.title("Edit Ruby Annotation" if mode=="edit" else "Insert Ruby Annotation")
        self.configure(bg=BG_PANEL)
        self.resizable(False, False)
        self.grab_set()

        def lbl(text): return tk.Label(self, text=text, bg=BG_PANEL, fg=FG_DIM,
                                        font=("Segoe UI",9), anchor="w")
        def entry(var, fg=FG):
            e = tk.Entry(self, textvariable=var, bg=BG_ENTRY, fg=fg,
                         insertbackground=FG, font=("Segoe UI",12), relief=tk.FLAT,
                         width=34, highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
            return e

        lbl("Ruby text  (small text shown above):").pack(fill=tk.X, padx=16, pady=(16,2))
        self.ruby_var = tk.StringVar(value=ruby_val)
        entry(self.ruby_var, HL_RB_RT).pack(fill=tk.X, padx=16, ipady=5)

        lbl("Main text:").pack(fill=tk.X, padx=16, pady=(10,2))
        self.main_var = tk.StringVar(value=main_val)
        entry(self.main_var).pack(fill=tk.X, padx=16, ipady=5)

        # preview
        pf = tk.Frame(self, bg=BG_CARD)
        pf.pack(fill=tk.X, padx=16, pady=10)
        tk.Label(pf, text="Preview:", bg=BG_CARD, fg=FG_DIM,
                 font=("Segoe UI",8)).pack(pady=(8,4))
        inner = tk.Frame(pf, bg=BG_CARD)
        inner.pack(pady=(0,8))
        self.pv_ruby = tk.Label(inner, text=ruby_val or " ",
                                 bg=BG_CARD, fg=HL_RB_RT, font=("Segoe UI",9))
        self.pv_ruby.pack()
        tk.Frame(inner, height=1, bg="#555577", width=100).pack()
        self.pv_main = tk.Label(inner, text=main_val or " ",
                                 bg=BG_CARD, fg=FG, font=("Segoe UI",14))
        self.pv_main.pack()

        lbl("Raw tag:").pack(anchor="w", padx=16)
        self.raw_lbl = tk.Label(self, text=self._tag(), bg=BG_PANEL,
                                 fg=FG_DIM, font=("Courier New",9))
        self.raw_lbl.pack(anchor="w", padx=16, pady=(0,10))

        self.ruby_var.trace_add("write", self._refresh)
        self.main_var.trace_add("write", self._refresh)

        bf = tk.Frame(self, bg=BG_PANEL, padx=16, pady=10)
        bf.pack(fill=tk.X)
        label = "Apply" if mode=="edit" else "Insert"
        _btn(bf, label, self._apply, accent=True).pack(side=tk.LEFT, padx=(0,6))
        if mode == "edit":
            _btn(bf, "Delete Ruby (keep main)", self._del_ruby).pack(side=tk.LEFT, padx=(0,6))
            _btn(bf, "Delete All",  self._del_all, danger=True).pack(side=tk.LEFT)
        _btn(bf, "Cancel", self.destroy).pack(side=tk.RIGHT)

        self.bind("<Return>", lambda e: self._apply())
        self.bind("<Escape>", lambda e: self.destroy())
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  - self.winfo_width())  // 2
        py = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(0,px)}+{max(0,py)}")
        parent.wait_window(self)

    def _tag(self): return f"[{self.main_var.get()}/RUBY/{self.ruby_var.get()}]"
    def _refresh(self, *_):
        self.pv_ruby.config(text=self.ruby_var.get() or " ")
        self.pv_main.config(text=self.main_var.get() or " ")
        self.raw_lbl.config(text=self._tag())
    def _apply(self):
        self.result = ("apply", self.main_var.get(), self.ruby_var.get()); self.destroy()
    def _del_ruby(self):
        self.result = ("del_ruby", self.main_var.get(), ""); self.destroy()
    def _del_all(self):
        if messagebox.askyesno("Confirm", "Remove entire tag including main text?", parent=self):
            self.result = ("del_all","",""); self.destroy()


# ── Shortcuts editor dialog ───────────────────────────────────────────────────
class ShortcutsDialog(tk.Toplevel):
    """Modal dialog to view and reassign keyboard shortcuts."""

    def __init__(self, parent, shortcuts: dict, on_save):
        super().__init__(parent)
        self.title("Keyboard Shortcuts")
        self.configure(bg=BG_PANEL)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._shortcuts  = dict(shortcuts)
        self._on_save    = on_save
        self._recording  = None             # action_id currently being recorded
        self._row_widgets = {}              # action_id → (disp_lbl, change_btn, clear_btn)

        # ── Header ──────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG_PANEL)
        hdr.pack(fill=tk.X, padx=16, pady=(14, 4))
        tk.Label(hdr, text="Keyboard Shortcuts", bg=BG_PANEL, fg=FG,
                 font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)

        tk.Label(self,
                 text="Shortcut must include Ctrl or Alt, but not both together (Ctrl+Alt is reserved for AltGr on many keyboards).  "
                      "Click Change, then press the desired combo.  Click Clear to unassign.",
                 bg=BG_PANEL, fg=FG_DIM, font=("Segoe UI", 9),
                 wraplength=480, justify=tk.LEFT).pack(
                 anchor="w", padx=16, pady=(0, 6))

        tk.Frame(self, height=1, bg=BORDER).pack(fill=tk.X)

        # ── Table ────────────────────────────────────────────────────────────
        table = tk.Frame(self, bg=BG_PANEL)
        table.pack(fill=tk.BOTH, padx=16, pady=8)

        # Column headers
        for col, (txt, w) in enumerate([("Action",28),("Shortcut",16),("","7"),("","7")]):
            tk.Label(table, text=txt, bg=BG_PANEL, fg=FG_DIM,
                     font=("Segoe UI",8,"bold"), width=w, anchor="w").grid(
                     row=0, column=col, sticky="w", padx=(0,6), pady=(0,4))

        tk.Frame(table, height=1, bg=BORDER).grid(
            row=1, column=0, columnspan=4, sticky="ew", pady=(0,6))

        for r, action_id in enumerate(SHORTCUT_LABELS, start=2):
            current = self._shortcuts.get(action_id, "")

            tk.Label(table, text=SHORTCUT_LABELS[action_id],
                     bg=BG_PANEL, fg=FG, font=("Segoe UI",10),
                     anchor="w", width=30).grid(row=r, column=0, sticky="w",
                                                padx=(0,8), pady=2)

            disp_lbl = tk.Label(table, text=_tk_to_display(current),
                                 bg=BG_ENTRY, fg=ACCENT,
                                 font=("Segoe UI",10,"bold"),
                                 width=18, anchor="w", padx=8)
            disp_lbl.grid(row=r, column=1, sticky="w", padx=(0,6), pady=2)

            chg_btn = FlatButton(table, text="Change",
                                 command=lambda aid=action_id: self._start_record(aid),
                                 bg=BG_CARD, hover_bg=HIGHLIGHT,
                                 font_size=9, padx=8, pady=3)
            chg_btn.grid(row=r, column=2, sticky="w", padx=(0,4), pady=2)

            clr_btn = FlatButton(table, text="Clear",
                                 command=lambda aid=action_id: self._clear_shortcut(aid),
                                 bg=BG_CARD, hover_bg=HIGHLIGHT,
                                 font_size=9, padx=8, pady=3)
            clr_btn.grid(row=r, column=3, sticky="w", pady=2)

            self._row_widgets[action_id] = (disp_lbl, chg_btn, clr_btn)

        # ── Status ───────────────────────────────────────────────────────────
        tk.Frame(self, height=1, bg=BORDER).pack(fill=tk.X, pady=(4,0))
        self._status_lbl = tk.Label(self, text="", bg=BG_PANEL, fg=MODIFIED,
                                     font=("Segoe UI",9,"italic"), pady=4)
        self._status_lbl.pack(fill=tk.X, padx=16)

        # ── Bottom buttons ───────────────────────────────────────────────────
        tk.Frame(self, height=1, bg=BORDER).pack(fill=tk.X)
        bf = tk.Frame(self, bg=BG_PANEL, padx=16, pady=10)
        bf.pack(fill=tk.X)
        _btn(bf, "Save",           self._save,            accent=True).pack(side=tk.LEFT, padx=(0,6))
        _btn(bf, "Reset Defaults", self._reset_defaults              ).pack(side=tk.LEFT)
        _btn(bf, "Cancel",         self.destroy                      ).pack(side=tk.RIGHT)

        self.bind("<KeyPress>", self._on_keypress)
        self.bind("<Escape>",   self._on_escape)

        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  - self.winfo_width())  // 2
        py = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(0,px)}+{max(0,py)}")
        parent.wait_window(self)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_display(self, action_id, tk_str):
        disp_lbl, _, _ = self._row_widgets[action_id]
        disp_lbl.config(text=_tk_to_display(tk_str), fg=ACCENT, bg=BG_ENTRY)

    # ── Recording ────────────────────────────────────────────────────────────

    def _start_record(self, action_id: str):
        if self._recording:
            self._cancel_record(self._recording)
        self._recording = action_id
        disp_lbl, chg_btn, _ = self._row_widgets[action_id]
        disp_lbl.config(text="[ press key combo... ]", fg=MODIFIED, bg=HIGHLIGHT)
        chg_btn.config(text="Cancel")
        chg_btn.update_command(lambda aid=action_id: self._cancel_record(aid))
        self._status_lbl.config(
            text=f'Recording "{SHORTCUT_LABELS[action_id]}"  —  press combo or Esc to cancel')
        self.focus_set()

    def _cancel_record(self, action_id: str):
        self._recording = None
        _, chg_btn, _ = self._row_widgets[action_id]
        self._set_display(action_id, self._shortcuts.get(action_id, ""))
        chg_btn.config(text="Change")
        chg_btn.update_command(lambda aid=action_id: self._start_record(aid))
        self._status_lbl.config(text="")

    def _clear_shortcut(self, action_id: str):
        if self._recording == action_id:
            self._cancel_record(action_id)
        self._shortcuts[action_id] = ""
        self._set_display(action_id, "")
        self._status_lbl.config(text=f'Cleared "{SHORTCUT_LABELS[action_id]}".')

    def _on_escape(self, event=None):
        if self._recording:
            self._cancel_record(self._recording)
        else:
            self.destroy()
        return "break"

    def _on_keypress(self, event):
        if not self._recording:
            return
        tk_str = _event_to_tk(event)
        if not tk_str:
            return "break"

        # Parse what modifiers are present
        has_ctrl  = "Control" in tk_str
        has_alt   = "Alt"     in tk_str
        has_shift = "Shift"   in tk_str
        # Extract the actual (non-modifier) key — last component
        bare_key  = tk_str.strip("<>").split("-")[-1]

        # Rule: must have Ctrl or Alt (Shift alone, or bare key, is not allowed)
        if not (has_ctrl or has_alt):
            self._status_lbl.config(
                text="Invalid: shortcut must include Ctrl or Alt.")
            return "break"

        # Rule: Ctrl+Alt (with or without Shift) is not allowed — on many
        # European keyboards Ctrl+Alt equals AltGr, causing conflicts.
        if has_ctrl and has_alt:
            self._status_lbl.config(
                text="Invalid: Ctrl+Alt combinations are not allowed.")
            return "break"

        action_id = self._recording

        # Conflict check
        conflict = next(
            (aid for aid, b in self._shortcuts.items()
             if b == tk_str and aid != action_id), None)
        if conflict:
            ans = messagebox.askyesno(
                "Conflict",
                f"{_tk_to_display(tk_str)} is already used by\n"
                f'"{SHORTCUT_LABELS[conflict]}".\n\n'
                f'Reassign to "{SHORTCUT_LABELS[action_id]}"?',
                parent=self)
            if not ans:
                self._cancel_record(action_id)
                return "break"
            self._shortcuts[conflict] = ""
            self._set_display(conflict, "")

        self._shortcuts[action_id] = tk_str
        self._recording = None
        self._set_display(action_id, tk_str)
        _, chg_btn, _ = self._row_widgets[action_id]
        chg_btn.config(text="Change")
        chg_btn.update_command(lambda aid=action_id: self._start_record(aid))
        self._status_lbl.config(
            text=f'Set "{SHORTCUT_LABELS[action_id]}" → {_tk_to_display(tk_str)}')
        return "break"

    # ── Actions ───────────────────────────────────────────────────────────────

    def _reset_defaults(self):
        if not messagebox.askyesno("Reset", "Reset all shortcuts to defaults?", parent=self):
            return
        self._shortcuts = dict(DEFAULT_SHORTCUTS)
        for aid in self._row_widgets:
            self._set_display(aid, self._shortcuts.get(aid, ""))
        self._status_lbl.config(text="All shortcuts reset to defaults.")

    def _save(self):
        self._on_save(dict(self._shortcuts))
        self.destroy()


# ── Font selector dialog ──────────────────────────────────────────────────────
class FontDialog(tk.Toplevel):
    """Simple dialog to pick editor font family and size."""

    def __init__(self, parent, family: str, size: int, on_apply):
        super().__init__(parent)
        self.title("Font Settings")
        self.configure(bg=BG_PANEL)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._on_apply = on_apply
        self._selected_family = family   # tracks current choice; starts as the active font

        import tkinter.font as tkfont
        all_families = sorted(tkfont.families(), key=str.lower)

        # ── Family ────────────────────────────────────────────────────────
        tk.Label(self, text="Search font family:", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",9), anchor="w").pack(fill=tk.X, padx=16, pady=(14,2))

        # Search box is ONLY a filter — it is never pre-filled with the font
        # name and listbox clicks never write to it.
        search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=search_var,
                                bg=BG_ENTRY, fg=FG, insertbackground=FG,
                                font=("Segoe UI",10), relief=tk.FLAT,
                                highlightthickness=1,
                                highlightbackground=BORDER, highlightcolor=ACCENT)
        search_entry.pack(fill=tk.X, padx=16, ipady=4)

        lb_frame = tk.Frame(self, bg=BG_LIST)
        lb_frame.pack(fill=tk.BOTH, padx=16, pady=(3,0))
        lb_sb = tk.Scrollbar(lb_frame, orient=tk.VERTICAL, bg=BG_PANEL,
                              troughcolor=BG_ENTRY, activebackground=ACCENT)
        lb_sb.pack(side=tk.RIGHT, fill=tk.Y)
        lb = tk.Listbox(lb_frame, bg=BG_LIST, fg=FG, selectbackground=ACCENT,
                        selectforeground=FG, activestyle="none",
                        font=("Segoe UI",10), relief=tk.FLAT, bd=0,
                        highlightthickness=0, yscrollcommand=lb_sb.set, height=8)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lb_sb.config(command=lb.yview)

        # Label showing which font is currently chosen
        self._sel_lbl = tk.Label(self, text=f"Selected: {family}",
                                  bg=BG_PANEL, fg=ACCENT,
                                  font=("Segoe UI", 9, "bold"), anchor="w")
        self._sel_lbl.pack(fill=tk.X, padx=16, pady=(4, 0))

        self._all_families = all_families
        self._lb = lb

        def refresh_list(*_):
            q = search_var.get().lower()
            lb.delete(0, tk.END)
            for f in all_families:
                if q in f.lower():
                    lb.insert(tk.END, f)
            # Re-highlight selected font if it's still visible
            for i in range(lb.size()):
                if lb.get(i) == self._selected_family:
                    lb.selection_clear(0, tk.END)
                    lb.selection_set(i)
                    lb.see(i)
                    break

        def on_lb_select(_=None):
            sel = lb.curselection()
            if sel:
                self._selected_family = lb.get(sel[0])
                self._sel_lbl.config(text=f"Selected: {self._selected_family}")
                self._update_preview()

        search_var.trace_add("write", refresh_list)
        lb.bind("<<ListboxSelect>>", on_lb_select)
        self._family_var = search_var   # kept for _update_preview fallback
        refresh_list()   # populate list (shows all fonts since search is empty)
        # Scroll the listbox to the currently active font
        for i in range(lb.size()):
            if lb.get(i) == family:
                lb.selection_set(i)
                lb.see(i)
                break

        # ── Size ──────────────────────────────────────────────────────────
        sz_frame = tk.Frame(self, bg=BG_PANEL)
        sz_frame.pack(fill=tk.X, padx=16, pady=(10,0))
        tk.Label(sz_frame, text="Size:", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",9)).pack(side=tk.LEFT, padx=(0,8))
        self._size_var = tk.IntVar(value=size)
        sb = tk.Spinbox(sz_frame, from_=6, to=48, textvariable=self._size_var,
                        bg=BG_ENTRY, fg=FG, insertbackground=FG,
                        buttonbackground=BG_CARD, relief=tk.FLAT,
                        font=("Segoe UI",11), width=5)
        sb.pack(side=tk.LEFT)
        self._size_var.trace_add("write", lambda *_: self._update_preview())

        # ── Preview ───────────────────────────────────────────────────────
        tk.Label(self, text="Preview:", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",9), anchor="w").pack(fill=tk.X, padx=16, pady=(10,2))
        pv_box = tk.Frame(self, bg=BG_ENTRY,
                          highlightthickness=1, highlightbackground=BORDER)
        pv_box.pack(fill=tk.X, padx=16)
        self._pv_lbl = tk.Label(pv_box, text="The quick brown fox  |  ABC abc 123",
                                 bg=BG_ENTRY, fg=FG, pady=10, padx=10, anchor="w")
        self._pv_lbl.pack(fill=tk.X)

        tk.Label(self, text="Note: font will fall back to Segoe UI if not found on system.",
                 bg=BG_PANEL, fg=FG_DIM, font=("Segoe UI",8),
                 wraplength=360, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(6,0))

        # ── Buttons ───────────────────────────────────────────────────────
        tk.Frame(self, height=1, bg=BORDER).pack(fill=tk.X, pady=(10,0))
        bf = tk.Frame(self, bg=BG_PANEL, padx=16, pady=10)
        bf.pack(fill=tk.X)
        _btn(bf, "Apply", self._apply, accent=True).pack(side=tk.LEFT, padx=(0,6))
        _btn(bf, "Cancel", self.destroy).pack(side=tk.RIGHT)

        self._update_preview()
        self.bind("<Return>", lambda e: self._apply())
        self.bind("<Escape>", lambda e: self.destroy())

        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  - self.winfo_width())  // 2
        py = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(0,px)}+{max(0,py)}")

    def _update_preview(self):
        fam = self._selected_family or "Segoe UI"
        try:
            sz = int(self._size_var.get())
        except (tk.TclError, ValueError):
            sz = 12
        try:
            self._pv_lbl.config(font=(fam, sz))
        except Exception:
            self._pv_lbl.config(font=("Segoe UI", sz))

    def _apply(self):
        import tkinter.font as tkfont
        fam = (self._selected_family or "Segoe UI").strip()
        try:
            sz = max(6, min(48, int(self._size_var.get())))
        except (tk.TclError, ValueError):
            sz = 12
        if fam not in tkfont.families():
            fam = "Segoe UI"
        self._on_apply(fam, sz)
        self.destroy()


# ── Main application ──────────────────────────────────────────────────────────
class TextEditorApp(tk.Tk):
    def __init__(self, paths=None):
        super().__init__()
        self.title("JSON Text Editor")
        self.configure(bg=BG)
        self.geometry("1380x780")
        self.minsize(960, 580)

        self.open_files   = []
        self.active_file  = None
        self._suppress    = False
        self._hl_job      = None
        self._prev_frames = []
        self._saved_sash  = {}
        self.shortcuts    = dict(DEFAULT_SHORTCUTS)
        self._active_bindings = {}   # binding_str → funcid (for reliable unbind)

        # Editor font (applied to text boxes; falls back to Segoe UI)
        self.editor_font_family = "Segoe UI"
        self.editor_font_size   = 12

        self.search_var  = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        self.status_var  = tk.StringVar(value="Open one or more JSON files to begin.")
        self.hide_br_var = tk.BooleanVar(value=False)
        self.hide_vo_var = tk.BooleanVar(value=False)
        self.hide_br_var.trace_add("write", lambda *_: self._schedule_hl())
        self.hide_vo_var.trace_add("write", lambda *_: self._schedule_hl())

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._load_settings()           # may update self.shortcuts / fonts
        self._bind_shortcuts()
        # Apply loaded font to text widgets (need widgets to exist first)
        self.after(50, lambda: self._apply_editor_font(
            self.editor_font_family, self.editor_font_size))
        self.after(150, self._restore_sashes)

        for p in (paths or []):
            self._load_file(p)

    # ══════════════════════════════════════════════════════════════════════
    # UI BUILD
    # ══════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        self._build_menu()

        self._main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=BG,
                                          sashwidth=5, sashrelief=tk.FLAT)
        self._main_pane.pack(fill=tk.BOTH, expand=True)

        self._main_pane.add(self._build_file_panel(self._main_pane),  minsize=200)
        self._main_pane.add(self._build_entry_panel(self._main_pane), minsize=220)
        self._main_pane.add(self._build_editor_panel(self._main_pane),minsize=400)

        self._main_pane.sash_place(0, 260, 0)
        self._main_pane.sash_place(1, 560, 0)
        self._build_statusbar()

    # ── Menu ─────────────────────────────────────────────────────────────
    def _build_menu(self):
        bar = tk.Menu(self, bg=BG_PANEL, fg=FG,
                      activebackground=ACCENT, activeforeground=FG, relief=tk.FLAT)
        self.config(menu=bar)

        self._file_menu = tk.Menu(bar, tearoff=False, bg=BG_PANEL, fg=FG,
                                   activebackground=ACCENT, activeforeground=FG)
        # Each entry: (base_label, action_id, command)
        self._fm_entries = [
            ("Open file(s)...", "open",       self._open_files_dialog),
            ("Save current",    "save",        self._save_current),
            ("Save As...",      "save_as",     self._save_as),
            ("Save All",        "save_all",    self._save_all),
            ("Close file",      "close_file",  self._close_current_file),
        ]
        for lbl, _, cmd in self._fm_entries:
            self._file_menu.add_command(label=lbl, command=cmd)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Exit", command=self._on_close)
        bar.add_cascade(label="File", menu=self._file_menu)

        em = tk.Menu(bar, tearoff=False, bg=BG_PANEL, fg=FG,
                     activebackground=ACCENT, activeforeground=FG)
        em.add_command(label="Insert Ruby annotation...", command=self._open_ruby_wizard)
        em.add_command(label="Revert entry to original",  command=self._revert_entry)
        em.add_separator()
        em.add_command(label="Keyboard Shortcuts...",     command=self._open_shortcuts_dialog)
        em.add_command(label="Font Settings...",          command=self._open_font_dialog)
        bar.add_cascade(label="Edit", menu=em)

    def _update_menu_labels(self):
        """Refresh File menu shortcut hints after shortcuts change."""
        for i, (base_lbl, aid, _) in enumerate(self._fm_entries):
            sc   = self.shortcuts.get(aid, "")
            hint = _tk_to_display(sc) if sc else ""
            self._file_menu.entryconfigure(i, label=base_lbl, accelerator=hint)

    # ── File panel ────────────────────────────────────────────────────────
    def _build_file_panel(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)

        hdr = tk.Frame(frame, bg=BG_PANEL, pady=8, padx=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="FILES", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",8,"bold")).pack(side=tk.LEFT)

        row1 = tk.Frame(frame, bg=BG_PANEL, padx=6)
        row1.pack(fill=tk.X, pady=(0,3))
        _btn(row1, "+ Open",  self._open_files_dialog).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0,3))
        _btn(row1, "✕ Close", self._close_current_file).pack(
            side=tk.LEFT, fill=tk.X, expand=True)

        row2 = tk.Frame(frame, bg=BG_PANEL, padx=6)
        row2.pack(fill=tk.X, pady=(0,4))
        _btn(row2, "💾  Save All Files", self._save_all, accent=True).pack(fill=tk.X)

        tk.Frame(frame, height=1, bg=BORDER).pack(fill=tk.X)

        lbf = tk.Frame(frame, bg=BG_LIST)
        lbf.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        sb = tk.Scrollbar(lbf, orient=tk.VERTICAL, bg=BG_PANEL,
                          troughcolor=BG_ENTRY, activebackground=ACCENT)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox = tk.Listbox(
            lbf, bg=BG_LIST, fg=FG, selectbackground=SEL_FILE,
            selectforeground=FG, activestyle="none",
            font=("Segoe UI",10), relief=tk.FLAT, bd=0,
            highlightthickness=0, yscrollcommand=sb.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.config(command=self.file_listbox.yview)
        self.file_listbox.bind("<<ListboxSelect>>", self._on_file_select)

        self.file_count_lbl = tk.Label(frame, text="No files open",
                                        bg=BG_PANEL, fg=FG_DIM,
                                        font=("Segoe UI",8), anchor="center", pady=4)
        self.file_count_lbl.pack(fill=tk.X)
        return frame

    # ── Entry panel ───────────────────────────────────────────────────────
    def _build_entry_panel(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)

        hdr = tk.Frame(frame, bg=BG_PANEL, pady=8, padx=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="ENTRIES", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",8,"bold")).pack(side=tk.LEFT)
        _btn(hdr, "Save", self._save_current, accent=True).pack(side=tk.RIGHT)

        sf = tk.Frame(frame, bg=BG_PANEL)
        sf.pack(fill=tk.X, padx=8, pady=(0,4))
        tk.Label(sf, text="Search:", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",9)).pack(side=tk.LEFT)
        tk.Entry(sf, textvariable=self.search_var,
                 bg=BG_ENTRY, fg=FG, insertbackground=FG, relief=tk.FLAT,
                 font=("Segoe UI",10), highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT).pack(
                 side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0), ipady=4)

        self.count_label = tk.Label(frame, text="", bg=BG_PANEL, fg=FG_DIM,
                                     font=("Segoe UI",8), anchor="e", padx=10, pady=2)
        self.count_label.pack(fill=tk.X)
        tk.Frame(frame, height=1, bg=BORDER).pack(fill=tk.X)

        lbf = tk.Frame(frame, bg=BG_LIST)
        lbf.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        sb2 = tk.Scrollbar(lbf, orient=tk.VERTICAL, bg=BG_PANEL,
                            troughcolor=BG_ENTRY, activebackground=ACCENT)
        sb2.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_listbox = tk.Listbox(
            lbf, bg=BG_LIST, fg=FG, selectbackground=ACCENT,
            selectforeground=FG, activestyle="none",
            font=("Segoe UI",10), relief=tk.FLAT, bd=0,
            highlightthickness=0, yscrollcommand=sb2.set)
        self.entry_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb2.config(command=self.entry_listbox.yview)
        self.entry_listbox.bind("<<ListboxSelect>>", self._on_entry_select)
        self.entry_listbox.bind("<Up>",   lambda e: self.after(10, self._on_entry_select))
        self.entry_listbox.bind("<Down>", lambda e: self.after(10, self._on_entry_select))
        return frame

    # ── Editor panel ──────────────────────────────────────────────────────
    def _build_editor_panel(self, parent):
        frame = tk.Frame(parent, bg=BG)

        # ── ID badge (fixed, above the paned window) ──────────────────────
        id_bar = tk.Frame(frame, bg=BG_PANEL, padx=16, pady=10)
        id_bar.pack(fill=tk.X)
        tk.Label(id_bar, text="Global ID", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",9)).grid(row=0, column=0, sticky="w")
        self.global_id_lbl = tk.Label(id_bar, text="--", bg=BG_PANEL,
                                       fg=ACCENT, font=("Segoe UI",16,"bold"))
        self.global_id_lbl.grid(row=1, column=0, sticky="w")
        tk.Frame(id_bar, width=2, bg=BORDER).grid(row=0, column=1, rowspan=2,
                                                    padx=20, sticky="ns")
        tk.Label(id_bar, text="Internal ID", bg=BG_PANEL, fg=FG_DIM,
                 font=("Segoe UI",9)).grid(row=0, column=2, sticky="w")
        self.internal_id_lbl = tk.Label(id_bar, text="--", bg=BG_PANEL,
                                         fg=FG, font=("Segoe UI",16,"bold"))
        self.internal_id_lbl.grid(row=1, column=2, sticky="w")
        id_bar.columnconfigure(3, weight=1)
        self.modified_badge = tk.Label(id_bar, text="✎ MODIFIED", bg=BG_PANEL,
                                        fg=MODIFIED, font=("Segoe UI",9,"bold"))
        self.modified_badge.grid(row=0, column=4, sticky="e")
        self.modified_badge.grid_remove()

        # ── Action buttons — packed FIRST so they are always visible ────────
        btn_bar = tk.Frame(frame, bg=BG)
        btn_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=8)
        _btn(btn_bar, "Apply & Next", self._apply_and_next,
             accent=True, large=True).pack(side=tk.LEFT, padx=(0,8))
        _btn(btn_bar, "Apply", self._apply_current,
             large=True).pack(side=tk.LEFT)
        _btn(btn_bar, "< Prev", self._go_prev).pack(side=tk.RIGHT, padx=(6,0))
        _btn(btn_bar, "Next >", self._go_next).pack(side=tk.RIGHT)

        # ── Vertical PanedWindow: ORIGINAL / TEXT / PREVIEW ───────────────
        self._editor_vpane = tk.PanedWindow(
            frame, orient=tk.VERTICAL, bg=BORDER,
            sashwidth=6, sashpad=0, sashrelief=tk.FLAT, relief=tk.FLAT)
        self._editor_vpane.pack(fill=tk.BOTH, expand=True, padx=10, pady=(6,0))

        # -- ORIGINAL TEXT section --
        orig_frame = tk.Frame(self._editor_vpane, bg=BG)
        orig_frame.pack(fill=tk.BOTH, expand=True)
        orig_hdr = tk.Frame(orig_frame, bg=BG)
        orig_hdr.pack(fill=tk.X)
        tk.Label(orig_hdr, text="ORIGINAL TEXT  (read-only)",
                 bg=BG, fg=FG_DIM, font=("Segoe UI",9,"bold"),
                 anchor="w").pack(side=tk.LEFT, pady=(4,2))
        orig_box = tk.Frame(orig_frame, bg=BG_CARD,
                             highlightthickness=1, highlightbackground=BORDER)
        orig_box.pack(fill=tk.BOTH, expand=True)
        orig_sb = tk.Scrollbar(orig_box, orient=tk.VERTICAL, bg=BG_PANEL,
                               troughcolor=BG_ENTRY, activebackground=ACCENT)
        orig_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.orig_text = tk.Text(
            orig_box, bg=BG_CARD, fg=FG_ORIG,
            font=("Segoe UI",11), wrap=tk.WORD, relief=tk.FLAT, bd=8,
            state=tk.DISABLED, highlightthickness=0,
            yscrollcommand=orig_sb.set)
        self.orig_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        orig_sb.config(command=self.orig_text.yview)
        self._setup_hl_tags(self.orig_text)
        self._editor_vpane.add(orig_frame, minsize=50)

        # -- TEXT EDITOR section --
        edit_frame = tk.Frame(self._editor_vpane, bg=BG)
        edit_frame.pack(fill=tk.BOTH, expand=True)
        edit_hdr = tk.Frame(edit_frame, bg=BG)
        edit_hdr.pack(fill=tk.X)
        tk.Label(edit_hdr, text="TEXT  (editable)",
                 bg=BG, fg=FG_DIM, font=("Segoe UI",9,"bold"),
                 anchor="w").pack(side=tk.LEFT, pady=(4,2))
        _btn(edit_hdr, "+ Add Ruby...", self._open_ruby_wizard,
             accent=True, small=True).pack(side=tk.RIGHT, padx=(4,0), pady=2)
        _btn(edit_hdr, "Revert to original", self._revert_entry,
             small=True).pack(side=tk.RIGHT, pady=2)
        edit_box = tk.Frame(edit_frame, bg=BG_ENTRY,
                             highlightthickness=1, highlightbackground=BORDER)
        edit_box.pack(fill=tk.BOTH, expand=True)
        edit_sb = tk.Scrollbar(edit_box, orient=tk.VERTICAL, bg=BG_PANEL,
                               troughcolor=BG_ENTRY, activebackground=ACCENT)
        edit_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.edit_text = tk.Text(
            edit_box, bg=BG_ENTRY, fg=FG,
            font=("Segoe UI",12), wrap=tk.WORD, relief=tk.FLAT, bd=10,
            insertbackground=FG, highlightthickness=0, undo=True,
            yscrollcommand=edit_sb.set)
        self.edit_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        edit_sb.config(command=self.edit_text.yview)
        self._setup_hl_tags(self.edit_text)
        # real-time highlight + preview on every keystroke/paste/undo
        for ev in ("<KeyRelease>","<<Paste>>","<<Cut>>","<<Undo>>","<<Redo>>"):
            self.edit_text.bind(ev, self._schedule_hl)
        self.edit_text.bind("<Control-z>", lambda e: (self.edit_text.edit_undo(), self._schedule_hl()))
        self.edit_text.bind("<Control-y>", lambda e: (self.edit_text.edit_redo(), self._schedule_hl()))
        self._editor_vpane.add(edit_frame, minsize=50)

        # -- PREVIEW section --
        prev_frame = tk.Frame(self._editor_vpane, bg=BG)
        prev_frame.pack(fill=tk.BOTH, expand=True)
        prev_hdr = tk.Frame(prev_frame, bg=BG)
        prev_hdr.pack(fill=tk.X)
        tk.Label(prev_hdr, text="PREVIEW  (click a ruby to edit)",
                 bg=BG, fg=FG_DIM, font=("Segoe UI",9,"bold"),
                 anchor="w").pack(side=tk.LEFT, pady=(4,2))
        # Hide toggles (right-aligned, using Checkbutton with custom colours)
        tk.Checkbutton(prev_hdr, text="Hide BR", variable=self.hide_br_var,
                       bg=BG, fg=FG_DIM, selectcolor=BG_CARD,
                       activebackground=BG, activeforeground=FG,
                       font=("Segoe UI",8)).pack(side=tk.RIGHT, padx=(4,0))
        tk.Checkbutton(prev_hdr, text="Hide VO", variable=self.hide_vo_var,
                       bg=BG, fg=FG_DIM, selectcolor=BG_CARD,
                       activebackground=BG, activeforeground=FG,
                       font=("Segoe UI",8)).pack(side=tk.RIGHT, padx=(4,0))
        prev_box = tk.Frame(prev_frame, bg=BG_ENTRY,
                             highlightthickness=1, highlightbackground=BORDER)
        prev_box.pack(fill=tk.BOTH, expand=True)
        prev_sb = tk.Scrollbar(prev_box, orient=tk.VERTICAL, bg=BG_PANEL,
                               troughcolor=BG_ENTRY, activebackground=ACCENT)
        prev_sb.pack(side=tk.RIGHT, fill=tk.Y)
        # Use a plain Canvas so we position every element ourselves —
        # no Tk "align" heuristics, baselines are just explicit y coordinates.
        self.preview_canvas = tk.Canvas(
            prev_box, bg=BG_ENTRY, highlightthickness=0,
            yscrollcommand=prev_sb.set)
        self.preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prev_sb.config(command=self.preview_canvas.yview)
        self.preview_canvas.bind("<Configure>", lambda e: self._schedule_hl())
        self.preview_canvas.bind("<MouseWheel>",
            lambda e: self.preview_canvas.yview_scroll(-1*(e.delta//120), "units"))
        self.preview_canvas.bind("<Button-4>",
            lambda e: self.preview_canvas.yview_scroll(-1, "units"))
        self.preview_canvas.bind("<Button-5>",
            lambda e: self.preview_canvas.yview_scroll( 1, "units"))
        self._editor_vpane.add(prev_frame, minsize=50)



        return frame

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=BG_PANEL)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Frame(bar, height=1, bg=BORDER).pack(fill=tk.X)
        self.status_lbl = tk.Label(bar, textvariable=self.status_var,
                                    bg=BG_PANEL, fg=FG_DIM,
                                    font=("Segoe UI",9), anchor="w",
                                    padx=12, pady=5)
        self.status_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.mod_count_lbl = tk.Label(bar, text="", bg=BG_PANEL, fg=MODIFIED,
                                       font=("Segoe UI",9,"bold"), padx=12, pady=5)
        self.mod_count_lbl.pack(side=tk.RIGHT)

    # ══════════════════════════════════════════════════════════════════════
    # SHORTCUTS
    # ══════════════════════════════════════════════════════════════════════

    # Maps action_id → the callable it should invoke
    _ACTION_MAP = None   # built lazily (needs self)

    def _action_map(self) -> dict:
        return {
            "open"       : self._open_files_dialog,
            "save"       : self._save_current,
            "save_all"   : self._save_all,
            "save_as"    : self._save_as,
            "close_file" : self._close_current_file,
            "apply"      : self._apply_current,
            "apply_next" : self._apply_and_next,
            "prev_entry" : self._go_prev,
            "next_entry" : self._go_next,
            "revert"     : self._revert_entry,
            "add_ruby"   : self._open_ruby_wizard,
            "shortcuts"  : self._open_shortcuts_dialog,
        }

    def _bind_shortcuts(self):
        """Unbind all previously active shortcuts, bind the current set, update menus."""
        # Unbind every binding that was active before this call.
        # We store the funcid returned by bind() so we can unbind precisely —
        # calling unbind(seq) without a funcid can silently fail in some Tk versions.
        for binding, funcid in list(self._active_bindings.items()):
            try: self.unbind(binding, funcid)
            except Exception: pass
        self._active_bindings.clear()

        am = self._action_map()
        for action_id, binding in self.shortcuts.items():
            if not binding:
                continue
            fn = am.get(action_id)
            if fn:
                funcid = self.bind(binding, lambda e, f=fn: (f(), "break")[1])
                self._active_bindings[binding] = funcid

        self._update_menu_labels()

    def _open_shortcuts_dialog(self):
        def on_save(new_shortcuts):
            self.shortcuts = new_shortcuts
            self._bind_shortcuts()   # unbinds old (tracked in _active_bindings), binds new
            self._save_settings()
            self.status_var.set("Shortcuts updated and saved.")
        ShortcutsDialog(self, self.shortcuts, on_save)

    def _open_font_dialog(self):
        FontDialog(self,
                   family=self.editor_font_family,
                   size=self.editor_font_size,
                   on_apply=self._apply_editor_font)

    # ══════════════════════════════════════════════════════════════════════
    # SETTINGS SAVE / LOAD
    # ══════════════════════════════════════════════════════════════════════

    def _save_settings(self):
        cfg = configparser.ConfigParser()
        cfg["window"] = {"geometry": self.geometry()}
        try:
            cfg["sash"] = {
                "main0":  str(self._main_pane.sash_coord(0)[0]),
                "main1":  str(self._main_pane.sash_coord(1)[0]),
                "edit0":  str(self._editor_vpane.sash_coord(0)[1]),
                "edit1":  str(self._editor_vpane.sash_coord(1)[1]),
            }
        except Exception:
            pass
        cfg["shortcuts"] = {k: v for k, v in self.shortcuts.items()}
        cfg["preview"] = {
            "hide_br": str(self.hide_br_var.get()),
            "hide_vo": str(self.hide_vo_var.get()),
        }
        cfg["font"] = {
            "family": self.editor_font_family,
            "size":   str(self.editor_font_size),
        }
        try:
            with open(CFG_PATH, "w", encoding="utf-8") as f:
                cfg.write(f)
        except Exception:
            pass

    def _load_settings(self):
        if not os.path.exists(CFG_PATH):
            return
        cfg = configparser.ConfigParser()
        try:
            cfg.read(CFG_PATH, encoding="utf-8")
        except Exception:
            return
        if "window" in cfg:
            try: self.geometry(cfg["window"].get("geometry", "1380x780"))
            except Exception: pass
        if "sash" in cfg:
            self._saved_sash = dict(cfg["sash"])
        if "shortcuts" in cfg:
            for action_id in DEFAULT_SHORTCUTS:
                if action_id in cfg["shortcuts"]:
                    self.shortcuts[action_id] = cfg["shortcuts"][action_id]
        if "preview" in cfg:
            try: self.hide_br_var.set(cfg["preview"].getboolean("hide_br", False))
            except Exception: pass
            try: self.hide_vo_var.set(cfg["preview"].getboolean("hide_vo", False))
            except Exception: pass
        if "font" in cfg:
            fam = cfg["font"].get("family", "Segoe UI")
            try:
                sz = int(cfg["font"].get("size", "12"))
            except ValueError:
                sz = 12
            # Validate font family exists; fall back to Segoe UI silently
            import tkinter.font as tkfont
            available = tkfont.families()
            if fam in available:
                self.editor_font_family = fam
                self.editor_font_size   = sz

    # ══════════════════════════════════════════════════════════════════════
    # FONT SETTINGS
    # ══════════════════════════════════════════════════════════════════════

    def _recalc_preview_metrics(self):
        """Recompute font metrics used by the canvas-based preview renderer."""
        self._pv_main_font.config(family=self.editor_font_family,
                                   size=self.editor_font_size)
        self._pv_ruby_font.config(family=self.editor_font_family, size=7)
        mm = self._pv_main_font.metrics()
        rm = self._pv_ruby_font.metrics()
        self._pv_ruby_zone = rm["ascent"] + rm["descent"] + 4  # height reserved above main text
        self._pv_main_asc  = mm["ascent"]
        self._pv_main_desc = mm["descent"]

    def _apply_editor_font(self, family: str, size: int):
        """Apply a new editor font to all text widgets and refresh."""
        self.editor_font_family = family
        self.editor_font_size   = size

        font_spec      = (family, size)
        font_spec_orig = (family, max(8, size - 1))   # original text slightly smaller
        font_spec_tags = (family, max(7, size - 4))   # tag ruby annotation text

        for w in (self.edit_text, self.orig_text):
            w.config(font=font_spec)

        # Update highlight tag fonts that embed explicit font specs
        for w in (self.edit_text, self.orig_text):
            w.tag_config("hl_rb_rt", font=(family, max(7, size - 4)))

        # Invalidate cached preview fonts so they're rebuilt on next render
        if hasattr(self, "_pv_main_font"):
            self._recalc_preview_metrics()

        self._save_settings()
        self._do_hl()   # re-highlight with new font

    def _restore_sashes(self):
        s = self._saved_sash
        try:
            self._main_pane.sash_place(0, int(s.get("main0",260)), 0)
            self._main_pane.sash_place(1, int(s.get("main1",560)), 0)
        except Exception: pass
        try:
            h = self._editor_vpane.winfo_height()
            y0 = int(s["edit0"]) if "edit0" in s else max(80,  int(h*0.20))
            y1 = int(s["edit1"]) if "edit1" in s else max(200, int(h*0.52))
            self._editor_vpane.sash_place(0, 0, y0)
            self._editor_vpane.sash_place(1, 0, y1)
        except Exception: pass

    # ══════════════════════════════════════════════════════════════════════
    # SYNTAX HIGHLIGHTING
    # ══════════════════════════════════════════════════════════════════════

    def _setup_hl_tags(self, w: tk.Text):
        w.tag_config("hl_rb_brk",  foreground=HL_RB_BRKT)
        w.tag_config("hl_rb_sep",  foreground=HL_RB_SEP)
        w.tag_config("hl_rb_main", foreground=HL_RB_MAIN, underline=True)
        w.tag_config("hl_rb_rt",   foreground=HL_RB_RT,  font=("Segoe UI",9))
        w.tag_config("hl_printf",  foreground=HL_PF_FG,  background=HL_PF_BG)
        w.tag_config("hl_br",      foreground=HL_BR_FG,  background=HL_BR_BG,
                     font=("Segoe UI",10,"bold"))
        w.tag_config("hl_vo",      foreground=HL_VO_FG,  background=HL_VO_BG)

    def _apply_hl(self, w: tk.Text, text: str):
        for tag in ("hl_rb_brk","hl_rb_sep","hl_rb_main","hl_rb_rt",
                    "hl_printf","hl_br","hl_vo"):
            w.tag_remove(tag, "1.0", tk.END)
        for seg in parse_segments(text):
            s0, e0 = seg["start"], seg["end"]
            if seg["type"] == "ruby":
                ms = s0+1;       me = ms+len(seg["main"])
                ss = me;         se = ss+6          # "/RUBY/"
                rs = se;         re_ = e0-1
                w.tag_add("hl_rb_brk",  tk_idx(text,s0),  tk_idx(text,s0+1))
                w.tag_add("hl_rb_main", tk_idx(text,ms),  tk_idx(text,me))
                w.tag_add("hl_rb_sep",  tk_idx(text,ss),  tk_idx(text,se))
                w.tag_add("hl_rb_rt",   tk_idx(text,rs),  tk_idx(text,re_))
                w.tag_add("hl_rb_brk",  tk_idx(text,re_), tk_idx(text,e0))
            elif seg["type"] == "printf":
                w.tag_add("hl_printf", tk_idx(text,s0), tk_idx(text,e0))
            elif seg["type"] == "br":
                w.tag_add("hl_br",     tk_idx(text,s0), tk_idx(text,e0))
            elif seg["type"] == "vo":
                w.tag_add("hl_vo",     tk_idx(text,s0), tk_idx(text,e0))

    def _schedule_hl(self, _event=None):
        if self._hl_job:
            self.after_cancel(self._hl_job)
        self._hl_job = self.after(80, self._do_hl)

    def _do_hl(self):
        raw = self._get_edit_text()
        self._apply_hl(self.edit_text, raw)
        self._render_preview(raw)

    # ══════════════════════════════════════════════════════════════════════
    # PREVIEW RENDERING
    # ══════════════════════════════════════════════════════════════════════

    def _render_preview(self, text: str):
        import tkinter.font as tkfont

        pc = self.preview_canvas
        pc.delete("all")
        # destroy any legacy embedded frames (guard for old references)
        for f in self._prev_frames:
            try: f.destroy()
            except Exception: pass
        self._prev_frames.clear()

        # ── Font objects (cached, recreated on font change) ────────────────
        if not hasattr(self, "_pv_main_font"):
            self._pv_main_font = tkfont.Font(family=self.editor_font_family,
                                              size=self.editor_font_size)
            self._pv_ruby_font = tkfont.Font(family=self.editor_font_family, size=7)
            self._recalc_preview_metrics()

        segs    = parse_segments(text)
        hide_br = self.hide_br_var.get()
        hide_vo = self.hide_vo_var.get()

        # ── Layout constants ───────────────────────────────────────────────
        PAD_X = 10
        PAD_Y = 8
        GAP   = 6                           # extra pixels between lines
        ma    = self._pv_main_asc           # font ascent
        md    = self._pv_main_desc          # font descent
        rz    = self._pv_ruby_zone          # height of ruby annotation zone
        lh    = rz + ma + md + GAP         # total line height

        pc.update_idletasks()
        usable_w = max(pc.winfo_width() - 2 * PAD_X, 60)

        # Cursor x and baseline y.
        # Text drawn with anchor="nw" at (x, bl - ma):
        #   top of bounding-box = bl - ma  (= baseline - ascent)
        #   baseline             = bl                               ← the reference
        #   bottom of bounding-box = bl + md
        # Same y is used for BOTH plain text and ruby main text, so they
        # are always on the same baseline with zero Tk alignment involvement.
        x  = PAD_X
        bl = PAD_Y + rz + ma               # first-line baseline

        ruby_idx = [0]   # mutable counter for unique canvas tag names

        def newline():
            nonlocal x, bl
            x   = PAD_X
            bl += lh

        def wrap_if_needed(w):
            """Advance to next line if a token of pixel-width w won't fit."""
            if x > PAD_X and x + w > PAD_X + usable_w:
                newline()

        for seg in segs:
            t = seg["type"]

            # ── Plain text ─────────────────────────────────────────────────
            if t == "plain":
                val = seg["value"]
                # Handle explicit newlines in the source text
                for li, line_chunk in enumerate(val.split("\n")):
                    if li > 0:
                        newline()
                    # Word-wrap: split preserving whitespace tokens
                    for tok in re.split(r'(\s+)', line_chunk):
                        if not tok:
                            continue
                        tw = self._pv_main_font.measure(tok)
                        wrap_if_needed(tw)
                        pc.create_text(x, bl - ma, text=tok,
                                       anchor="nw", fill=FG,
                                       font=self._pv_main_font)
                        x += tw

            # ── Printf placeholder ─────────────────────────────────────────
            elif t == "printf":
                val = seg["value"]
                tw  = self._pv_main_font.measure(val)
                wrap_if_needed(tw)
                # Highlight box behind the token
                pc.create_rectangle(x, bl - ma, x + tw, bl + md,
                                    fill=HL_PF_BG, outline="")
                pc.create_text(x, bl - ma, text=val,
                               anchor="nw", fill=HL_PF_FG,
                               font=self._pv_main_font)
                x += tw

            # ── Ruby annotation ────────────────────────────────────────────
            elif t == "ruby":
                ruby_text = seg["ruby_text"] or ""
                main_text = seg["main"]
                mw   = self._pv_main_font.measure(main_text)
                rw   = self._pv_ruby_font.measure(ruby_text) if ruby_text else 0
                slot = max(mw, rw) + 6     # total horizontal slot
                wrap_if_needed(slot)

                cx = x + slot // 2         # horizontal centre of slot

                # Ruby annotation — drawn so its BOTTOM is at (bl - ma - 2),
                # i.e. just above the top of the main text bounding box.
                if ruby_text:
                    pc.create_text(cx, bl - ma - 2, text=ruby_text,
                                   anchor="s", fill=HL_RB_RT,
                                   font=self._pv_ruby_font)

                # Thin separator
                sep_y = bl - ma - 1
                pc.create_line(x, sep_y, x + slot, sep_y, fill="#555577")

                # Main text — anchor="n" centres horizontally, top at (bl - ma).
                # baseline = (bl - ma) + ma = bl  ← identical to plain text ✓
                pc.create_text(cx, bl - ma, text=main_text,
                               anchor="n", fill=PV_RUBY_MAIN,
                               font=self._pv_main_font)

                # Invisible hit-rectangle over the whole ruby slot
                ruby_idx[0] += 1
                htag = f"rh{ruby_idx[0]}"
                pc.create_rectangle(x, bl - ma - rz, x + slot, bl + md,
                                    outline="", fill="", tags=htag)
                raw_s, m_v, r_v = seg["raw"], seg["main"], seg["ruby_text"]
                pc.tag_bind(htag, "<Button-1>",
                            lambda e, m=m_v, r=r_v, raw=raw_s:
                                self._edit_ruby_from_preview(m, r, raw))
                pc.tag_bind(htag, "<Enter>",
                            lambda e: pc.config(cursor="hand2"))
                pc.tag_bind(htag, "<Leave>",
                            lambda e: pc.config(cursor=""))

                x += slot

            # ── Line break ─────────────────────────────────────────────────
            elif t == "br":
                if not hide_br:
                    bsz = 18
                    wrap_if_needed(bsz + 4)
                    bx = x;  by = bl - bsz + md
                    pc.create_rectangle(bx, by, bx + bsz, by + bsz,
                                        fill=HL_BR_BG, outline=HL_BR_FG)
                    pc.create_text(bx + bsz // 2, by + bsz // 2, text="||",
                                   fill=HL_BR_FG,
                                   font=("Segoe UI", 8, "bold"), anchor="center")
                    x += bsz + 4
                newline()

            # ── Voice-over ─────────────────────────────────────────────────
            elif t == "vo":
                if not hide_vo:
                    fname = os.path.basename(seg["filename"]) or seg["filename"]
                    label = f"\u266a  {fname}"
                    lw2   = self._pv_main_font.measure(label) + 16
                    lh2   = ma + md + 6
                    wrap_if_needed(lw2)
                    vy = bl - ma - 3
                    pc.create_rectangle(x, vy, x + lw2, vy + lh2,
                                        fill=HL_VO_BG, outline="#005555")
                    pc.create_text(x + lw2 // 2, vy + lh2 // 2, text=label,
                                   fill=HL_VO_FG,
                                   font=("Segoe UI", 9), anchor="center")
                    x += lw2 + 8
                newline()

        # Expand scroll region to fit all drawn content
        total_h = bl + md + PAD_Y
        pc.config(scrollregion=(0, 0, PAD_X * 2 + usable_w, total_h))

    # ══════════════════════════════════════════════════════════════════════
    # RUBY OPERATIONS
    # ══════════════════════════════════════════════════════════════════════

    def _edit_ruby_from_preview(self, main_val, ruby_val, raw_original):
        dlg = RubyDialog(self, mode="edit", main_val=main_val, ruby_val=ruby_val)
        if dlg.result is None: return
        action, new_main, new_ruby = dlg.result
        current = self._get_edit_text()
        if   action == "apply":   replacement = f"[{new_main}/RUBY/{new_ruby}]"
        elif action == "del_ruby": replacement = new_main
        else:                     replacement = ""
        new_text = current.replace(raw_original, replacement, 1)
        self._suppress = True
        self.edit_text.delete("1.0", tk.END)
        self.edit_text.insert("1.0", new_text)
        self._suppress = False
        self._do_hl()

    def _open_ruby_wizard(self):
        try:    selected = self.edit_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError: selected = ""
        dlg = RubyDialog(self, mode="insert", main_val=selected, ruby_val="")
        if dlg.result is None: return
        _, new_main, new_ruby = dlg.result
        tag = f"[{new_main}/RUBY/{new_ruby}]"
        try: self.edit_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError: pass
        self.edit_text.insert(tk.INSERT, tag)
        self._do_hl()

    # ══════════════════════════════════════════════════════════════════════
    # FILE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════

    def _open_files_dialog(self):
        paths = filedialog.askopenfilenames(
            title="Open JSON file(s)",
            filetypes=[("JSON files","*.json"),("All files","*.*")])
        for p in paths: self._load_file(p)

    def _load_file(self, path: str):
        for i, fs in enumerate(self.open_files):
            if fs.path == path:
                self._switch_to_file(i); return
        try:
            with open(path,"r",encoding="utf-8") as f: data = json.load(f)
        except Exception as exc:
            messagebox.showerror("Error", f"Could not open:\n{exc}"); return
        self.open_files.append(FileState(path, data))
        self._refresh_file_list()
        self._switch_to_file(len(self.open_files)-1)

    def _save_current(self):
        if not self.active_file: return
        self._apply_current()
        self._write_file(self.active_file, self.active_file.path)

    def _save_as(self):
        if not self.active_file: return
        self._apply_current()
        path = filedialog.asksaveasfilename(
            title="Save As", initialfile=self.active_file.basename,
            defaultextension=".json",
            filetypes=[("JSON files","*.json"),("All files","*.*")])
        if path:
            self.active_file.path = path
            self._write_file(self.active_file, path)
            self._refresh_file_list()

    def _save_all(self):
        self._apply_current()
        saved = 0
        for fs in self.open_files:
            if fs.dirty:
                if self._write_file(fs, fs.path): saved += 1
        msg = f"Saved {saved} file(s)." if saved else "All files already up to date."
        self.status_var.set(msg)

    def _write_file(self, fs: FileState, path: str) -> bool:
        try:
            with open(path,"w",encoding="utf-8") as f:
                json.dump(fs.data, f, ensure_ascii=False, indent="\t")
            fs.dirty = False
            self._refresh_file_list()
            self.status_var.set(f"Saved → {path}")
            self.status_lbl.config(fg=SAVED_OK)
            self.after(3000, lambda: self.status_lbl.config(fg=FG_DIM))
            return True
        except Exception as exc:
            messagebox.showerror("Save error", f"Could not save:\n{exc}")
            return False

    def _close_current_file(self):
        if not self.active_file: return
        fs = self.active_file
        if fs.dirty:
            ans = messagebox.askyesnocancel(
                "Unsaved changes",
                f"{fs.basename} has unsaved changes.\nSave before closing?")
            if ans is None: return
            if ans: self._write_file(fs, fs.path)
        idx = self.open_files.index(fs)
        self.open_files.remove(fs)
        self.active_file = None
        self._refresh_file_list()
        if self.open_files:
            self._switch_to_file(min(idx, len(self.open_files)-1))
        else:
            self._suppress = True
            self.search_var.set("")
            self._suppress = False
            self.entry_listbox.delete(0, tk.END)
            self.count_label.config(text="")
            self._clear_editor()
            self.status_var.set("Open one or more JSON files to begin.")
            self.title("JSON Text Editor")

    # ══════════════════════════════════════════════════════════════════════
    # FILE LIST
    # ══════════════════════════════════════════════════════════════════════

    def _refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for fs in self.open_files:
            self.file_listbox.insert(tk.END, fs.label)
            if fs.dirty:
                self.file_listbox.itemconfig(tk.END, fg=MODIFIED)
        n = len(self.open_files)
        self.file_count_lbl.config(
            text=f"{n} file{'s' if n!=1 else ''} open" if n else "No files open")
        if self.active_file in self.open_files:
            idx = self.open_files.index(self.active_file)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(idx)
            self.file_listbox.see(idx)

    def _on_file_select(self, _=None):
        sel = self.file_listbox.curselection()
        if not sel: return
        idx = sel[0]
        if idx < len(self.open_files) and self.open_files[idx] is not self.active_file:
            self._apply_current()
            self._switch_to_file(idx)

    def _switch_to_file(self, idx: int):
        self.active_file = self.open_files[idx]
        fs = self.active_file
        self.file_listbox.selection_clear(0, tk.END)
        self.file_listbox.selection_set(idx)
        self.file_listbox.see(idx)
        self._suppress = True
        self.search_var.set(fs.search_query)
        self._suppress = False
        self._rebuild_entry_list(fs.search_query)
        self._update_mod_count()
        self.title(f"JSON Text Editor  —  {fs.basename}")
        if fs.current_index is not None and fs.current_index in fs.filtered_indices:
            self._select_entry_item(fs.filtered_indices.index(fs.current_index))
        elif fs.filtered_indices:
            self._select_entry_item(0)
        else:
            self._clear_editor()

    # ══════════════════════════════════════════════════════════════════════
    # ENTRY LIST
    # ══════════════════════════════════════════════════════════════════════

    def _entry_color(self, fs: FileState, i: int) -> str:
        entry = fs.entries[i]
        if i in fs.modified:
            return MODIFIED
        if entry.get("TEXT","") != entry.get("ORIGINAL_TEXT",""):
            return TRANSLATED
        return FG

    def _rebuild_entry_list(self, query: str = ""):
        fs = self.active_file
        self.entry_listbox.delete(0, tk.END)
        if not fs:
            self.count_label.config(text=""); return
        fs.filtered_indices = []
        q = query.strip().lower()
        for i, entry in enumerate(fs.entries):
            gid  = entry.get("global_id","")
            iid  = entry.get("internal_id","")
            text = entry.get("TEXT","")
            if q and q not in str(gid).lower() \
                  and q not in str(iid).lower() \
                  and q not in text.lower():
                continue
            fs.filtered_indices.append(i)
            dot     = "✎ " if i in fs.modified else "  "
            preview = text.replace("\n"," ")[:40]
            self.entry_listbox.insert(tk.END, f"{dot}#{gid} / {iid}   {preview}")
            self.entry_listbox.itemconfig(tk.END, fg=self._entry_color(fs, i))
        shown = len(fs.filtered_indices)
        self.count_label.config(text=f"{shown} / {len(fs.entries)} entries")

    def _select_entry_item(self, pos: int):
        self.entry_listbox.selection_clear(0, tk.END)
        self.entry_listbox.selection_set(pos)
        self.entry_listbox.activate(pos)
        self.entry_listbox.see(pos)
        fs = self.active_file
        if fs and pos < len(fs.filtered_indices):
            self._load_entry(fs.filtered_indices[pos])

    def _on_entry_select(self, _=None):
        sel = self.entry_listbox.curselection()
        if not sel or not self.active_file: return
        fs   = self.active_file
        real = fs.filtered_indices[sel[0]]
        if real != fs.current_index:
            self._load_entry(real)

    def _refresh_entry_item(self, real_index: int):
        fs = self.active_file
        if not fs or real_index not in fs.filtered_indices: return
        pos   = fs.filtered_indices.index(real_index)
        entry = fs.entries[real_index]
        dot   = "✎ " if real_index in fs.modified else "  "
        prev  = entry.get("TEXT","").replace("\n"," ")[:40]
        label = f"{dot}#{entry.get('global_id')} / {entry.get('internal_id')}   {prev}"
        self.entry_listbox.delete(pos)
        self.entry_listbox.insert(pos, label)
        self.entry_listbox.itemconfig(pos, fg=self._entry_color(fs, real_index))
        self.entry_listbox.selection_set(pos)

    # ══════════════════════════════════════════════════════════════════════
    # ENTRY EDITING
    # ══════════════════════════════════════════════════════════════════════

    def _load_entry(self, index: int):
        fs = self.active_file
        if not fs: return
        self._suppress = True
        fs.current_index = index
        entry = fs.entries[index]

        self.global_id_lbl.config(text=str(entry.get("global_id","--")))
        self.internal_id_lbl.config(text=str(entry.get("internal_id","--")))

        orig = entry.get("ORIGINAL_TEXT","")
        self.orig_text.config(state=tk.NORMAL)
        self.orig_text.delete("1.0", tk.END)
        self.orig_text.insert("1.0", orig)
        self._apply_hl(self.orig_text, orig)
        self.orig_text.config(state=tk.DISABLED)

        text = entry.get("TEXT","")
        self.edit_text.delete("1.0", tk.END)
        self.edit_text.insert("1.0", text)
        self.edit_text.edit_reset()
        self.edit_text.edit_modified(False)

        if index in fs.modified: self.modified_badge.grid()
        else:                     self.modified_badge.grid_remove()

        self._suppress = False
        self._apply_hl(self.edit_text, text)
        self._render_preview(text)

    def _clear_editor(self):
        self._suppress = True
        self.global_id_lbl.config(text="--")
        self.internal_id_lbl.config(text="--")
        self.orig_text.config(state=tk.NORMAL)
        self.orig_text.delete("1.0", tk.END)
        self.orig_text.config(state=tk.DISABLED)
        self.edit_text.delete("1.0", tk.END)
        self.modified_badge.grid_remove()
        self.count_label.config(text="")
        self._render_preview("")
        self._suppress = False

    def _get_edit_text(self) -> str:
        raw = self.edit_text.get("1.0", tk.END)
        return raw.rstrip("\n") if not raw.endswith("\n\n") else raw[:-1]

    def _apply_current(self):
        fs = self.active_file
        if not fs or fs.current_index is None: return
        new_text = self._get_edit_text()
        entry    = fs.entries[fs.current_index]
        if new_text == entry.get("TEXT",""): return
        entry["TEXT"] = new_text
        fs.modified.add(fs.current_index)
        fs.dirty = True
        self.edit_text.edit_modified(False)
        self._refresh_entry_item(fs.current_index)
        self._refresh_file_list()
        self.modified_badge.grid()
        self._update_mod_count()
        self.status_var.set(
            f"{fs.basename}  —  entry #{entry.get('global_id')} updated (unsaved).")

    def _apply_and_next(self):
        self._apply_current(); self._go_next()

    def _revert_entry(self):
        fs = self.active_file
        if not fs or fs.current_index is None: return
        entry    = fs.entries[fs.current_index]
        original = entry.get("ORIGINAL_TEXT","")
        self._suppress = True
        self.edit_text.delete("1.0", tk.END)
        self.edit_text.insert("1.0", original)
        self.edit_text.edit_modified(False)
        self._suppress = False
        entry["TEXT"] = original
        fs.modified.discard(fs.current_index)
        self.modified_badge.grid_remove()
        self._refresh_entry_item(fs.current_index)
        self._update_mod_count()
        self._apply_hl(self.edit_text, original)
        self._render_preview(original)
        self.status_var.set("Entry reverted to original.")

    def _go_prev(self):
        fs = self.active_file
        if not fs or not fs.filtered_indices: return
        sel = self.entry_listbox.curselection()
        self._select_entry_item(max(0, (sel[0] if sel else 0)-1))

    def _go_next(self):
        fs = self.active_file
        if not fs or not fs.filtered_indices: return
        sel = self.entry_listbox.curselection()
        self._select_entry_item(
            min(len(fs.filtered_indices)-1, (sel[0] if sel else -1)+1))

    # ══════════════════════════════════════════════════════════════════════
    # MISC
    # ══════════════════════════════════════════════════════════════════════

    def _on_search_change(self, *_):
        if self._suppress or not self.active_file: return
        q = self.search_var.get()
        self.active_file.search_query = q
        self._rebuild_entry_list(q)
        fs = self.active_file
        if not fs or not fs.filtered_indices: self._clear_editor(); return
        if fs.current_index in fs.filtered_indices:
            self._select_entry_item(fs.filtered_indices.index(fs.current_index))
        else:
            self._select_entry_item(0)

    def _update_mod_count(self):
        fs = self.active_file
        n  = len(fs.modified) if fs else 0
        self.mod_count_lbl.config(text=f"✎ {n} modified" if n else "")

    def _on_close(self):
        dirty = [fs for fs in self.open_files if fs.dirty]
        if dirty:
            names = "\n".join(f"  {fs.basename}" for fs in dirty)
            ans = messagebox.askyesnocancel(
                "Unsaved changes",
                f"These files have unsaved changes:\n{names}\n\nSave all before exiting?")
            if ans is None: return
            if ans:
                self._apply_current()
                for fs in dirty: self._write_file(fs, fs.path)
        self._save_settings()
        self.destroy()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    TextEditorApp(paths=sys.argv[1:]).mainloop()