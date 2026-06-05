import sys
import json


file = open(sys.argv[1], "rb")

dimension_x = int.from_bytes(file.read(2), "little")
dimension_y = int.from_bytes(file.read(2), "little")
glyph_width = int.from_bytes(file.read(2), "little")
glyph_height = int.from_bytes(file.read(2), "little")
max_characters_per_line = dimension_x // glyph_width
version = int.from_bytes(file.read(4), "little")
table_size = int.from_bytes(file.read(4), "little")
unk = int.from_bytes(file.read(8), "little")
character_count = int.from_bytes(file.read(8), "little")
unk = int.from_bytes(file.read(0x8), "little")

CHARACTERS = {}
for i in range(character_count):
    glyph_index = int.from_bytes(file.read(8), "little")
    chara = int.from_bytes(file.read(8), "little")
    num_bytes = (chara.bit_length() + 7) // 8
    raw_bytes = chara.to_bytes(num_bytes, byteorder='big')
    chara = raw_bytes.decode('utf-8')
    number1 = int.from_bytes(file.read(1), "little")
    number2 = int.from_bytes(file.read(1), "little")
    number3 = int.from_bytes(file.read(2), "little")
    number5 = int.from_bytes(file.read(4), "little")
    pos_x = (glyph_index % max_characters_per_line) * glyph_width
    pos_y = glyph_index // max_characters_per_line * glyph_height

    CHARACTERS[glyph_index] = {}
    CHARACTERS[glyph_index]["Glyph"] = chara
    CHARACTERS[glyph_index]["Position"] = [pos_x, pos_y]
    CHARACTERS[glyph_index]["OFFSET_X"] = number1 # represents how many pixels you cut from the left side of glyph
    CHARACTERS[glyph_index]["WIDTH"] = number2
    CHARACTERS[glyph_index]["BASELINE"] = number3
    CHARACTERS[glyph_index]["HEIGHT"] = number5

file.close()
file = open("dump.json", "w", encoding="UTF-8")
json.dump(CHARACTERS, file, indent="\t", ensure_ascii=False)
file.close()