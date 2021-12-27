import sys
import numpy

file = open(sys.argv[1], "rb+")

halfwidth = ["!", "#", "$", "%", "&", "(", ")", "*", "+", ",", "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
fullwidth = ["！", "＃", "＄", "％", "＆", "（", "）", "＊", "＋", "，", "－", "．", "０", "１", "２", "３", "４", "５", "６", "７", "８", "９", "：", "；", "＜", "＝", "＞", "？", "＠", "Ａ", "Ｂ", "Ｃ", "Ｄ", "Ｅ", "Ｆ", "Ｇ", "Ｈ", "Ｉ", "Ｊ", "Ｋ", "Ｌ", "Ｍ", "Ｎ", "Ｏ", "Ｐ", "Ｑ", "Ｒ", "Ｓ", "Ｔ", "Ｕ", "Ｖ", "Ｗ", "Ｘ", "Ｙ", "Ｚ", "ａ", "ｂ", "ｃ", "ｄ", "ｅ", "ｆ", "ｇ", "ｈ", "ｉ", "ｊ", "ｋ", "ｌ", "ｍ", "ｎ", "ｏ", "ｐ", "ｑ", "ｒ", "ｓ", "ｔ", "ｕ", "ｖ", "ｗ", "ｘ", "ｙ", "ｚ"]
halfwidth_IDs = {}
fullwidth_IDs = {}
buffer = numpy.fromfile(file, dtype=numpy.uint16, count=4)
texture_width = buffer[0]
texture_height = buffer[1]
block_width = buffer[2]
block_height = buffer[3]
file.seek(0x4, 1)
table_character_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
file.seek(8, 1)
character_count = numpy.fromfile(file, dtype=numpy.uint64, count=1)[0]
file.seek(8, 1)
DUMP = []
for i in range(0, character_count):
    entry = {}
    entry["OFFSET"] = file.tell()
    entry["ID"] = int(numpy.fromfile(file, dtype=numpy.uint64, count=1)[0])
    string = file.read(0x8)
    entry["string"] = int.from_bytes(string, byteorder="little")
    string = int.from_bytes(string, byteorder="little")
    if (string < 256): size = 1
    elif (string < 65536): size = 2
    else: size = 3
    string = string.to_bytes(size, byteorder="big")
    entry["CHARACTER"] = string.decode("UTF-8")
    buffer = numpy.fromfile(file, dtype=numpy.int8, count=2)
    entry["ANCHOR"] = int(buffer[0])
    entry["WIDTH"] = int(buffer[1])
    entry["UNK2"] = int(numpy.fromfile(file, dtype=numpy.int16, count=1)[0])
    buffer = numpy.fromfile(file, dtype=numpy.int8, count=2)
    entry["UNK3"] = int(buffer[0])
    entry["UNK4"] = int(buffer[1])
    file.seek(2, 1)
    DUMP.append(entry)
    if (entry["CHARACTER"] in halfwidth):
        halfwidth_IDs["%d" % halfwidth.index(entry["CHARACTER"])] = entry
    elif (entry["CHARACTER"] in fullwidth):
        fullwidth_IDs["%d" % fullwidth.index(entry["CHARACTER"])] = entry

for i in range(0, len(DUMP)):
    if (DUMP[i]["CHARACTER"] in halfwidth):
        index = halfwidth.index(DUMP[i]["CHARACTER"])
        file.seek(DUMP[i]["OFFSET"])
        file.write(numpy.uint64(fullwidth_IDs["%d" % index]["ID"]))
        file.seek(8, 1)
        file.write(numpy.int8(fullwidth_IDs["%d" % index]["ANCHOR"]))
        file.write(numpy.int8(fullwidth_IDs["%d" % index]["WIDTH"]))
        file.write(numpy.int16(fullwidth_IDs["%d" % index]["UNK2"]))
        file.write(numpy.int8(fullwidth_IDs["%d" % index]["UNK3"]))
        file.write(numpy.int8(fullwidth_IDs["%d" % index]["UNK4"]))
        
    elif (DUMP[i]["CHARACTER"] in fullwidth):
        index = fullwidth.index(DUMP[i]["CHARACTER"])
        file.seek(DUMP[i]["OFFSET"])
        file.write(numpy.uint64(halfwidth_IDs["%d" % index]["ID"]))
        file.seek(8, 1)
        file.write(numpy.int8(halfwidth_IDs["%d" % index]["ANCHOR"]))
        file.write(numpy.int8(halfwidth_IDs["%d" % index]["WIDTH"]))
        file.write(numpy.int16(halfwidth_IDs["%d" % index]["UNK2"]))
        file.write(numpy.int8(halfwidth_IDs["%d" % index]["UNK3"]))
        file.write(numpy.int8(halfwidth_IDs["%d" % index]["UNK4"]))

file.close()