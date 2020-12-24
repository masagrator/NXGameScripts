extracted = open("extract.txt", "r", encoding='shift-jis', newline='')

data = extracted.read()
extracted.close()

data = data.replace("", "<SPECIAL_CASE_2>")
data = data.replace("\r", "<SPECIAL CASE>")
data = data.replace("\x07\x08", "_voice(\x22")
data = data.replace("\x00「", "\x22);「")
data = data.replace("\x00『","\x22);『")
data = data.replace("", "<Romaji-over-Kanji>")
data = data.replace("", "<pause>")

for i in range(0x3001, 0x30FE):
    data = data.replace("\x0A %s" % (chr(i)), "<Romaji-over-Kanji_start> %s" % (chr(i)))
    data = data.replace("\x0A%s" % (chr(i)), "<Romaji-over-Kanji_start>%s" % (chr(i)))

for i in range(0x32D0, 0x32FE):
    data = data.replace("\x0A %s" % (chr(i)), "<Romaji-over-Kanji_start> %s" % (chr(i)))
    data = data.replace("\x0A%s" % (chr(i)), "<Romaji-over-Kanji_start>%s" % (chr(i)))

for i in range(0xFF65, 0xFF9F):
    data = data.replace("\x0A %s" % (chr(i)), "<Romaji-over-Kanji_start> %s" % (chr(i)))
    data = data.replace("\x0A%s" % (chr(i)), "<Romaji-over-Kanji_start>%s" % (chr(i)))

data = data.replace("\x00", "<NULL>")
data = data.replace("","<Break Line>")
data = data.replace("", "_voiceover();")

for i in range(0, 9999):
    data = data.replace("%s<NULL>" % (str(i).zfill(4)), "%s\x22);" % (str(i).zfill(4)))
    data = data.replace("%sa<NULL>" % (str(i).zfill(4)), "%s\x22);" % (str(i).zfill(4)))
    data = data.replace("%sb<NULL>" % (str(i).zfill(4)), "%s\x22);" % (str(i).zfill(4)))


data = data.replace("\n<Romaji-over-Kanji_start>", "\n\n")

data = data.replace("", "<SPECIAL_CASE_3>")

new = open("new.txt", "w", encoding='shift-jis', newline='')
new.write(data)
new.close()