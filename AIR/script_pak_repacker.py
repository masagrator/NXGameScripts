import sys
import numpy
import os

Filenames = []
unk0 = []

with open("chapternames.txt", 'r', encoding="ascii") as f:
    Filenames = [line.strip("\r\n").strip("\n").split("\t", -1)[0] for line in f]

file = open(sys.argv[1], "rb")
header_size = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
file_count = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
unk2_int32 = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
round_to = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
file.seek(0,0)

if (file_count != len(Filenames)): raise ValueError("file_count doesn't match. Expected: %d, got from chapternames.txt: %d" % (file_count, len(Filenames)))

new_file = open("%s_NEW.PAK" % (sys.argv[1][:-4]), "wb")
new_file.write(file.read(0x28))

scripts_size = []

for i in range(0, file_count):
    try: 
        script = open("Compiled\%s.dat" % (Filenames[i]), "rb")
    except:
        script = open("new\%s.dat" % (Filenames[i]), "rb")
    script.seek(0, 2)
    scripts_size.append(script.tell())
    script.close()

offset = header_size / 4

for i in range(0, file_count):
    new_file.write(numpy.uint32(offset))
    new_file.write(numpy.uint32(scripts_size[i]))
    offset += int(round((scripts_size[i]+1) / 4))

for i in range(0, file_count):
    new_file.write(Filenames[i].encode("ascii"))
    new_file.write(b"\x00")

while(True):
    if (new_file.tell() == header_size): break
    new_file.write(b"\x00")

for i in range(0, file_count):
    try: 
        script = open("Compiled\%s.dat" % (Filenames[i]), "rb")
    except:
        script = open("new\%s.dat" % (Filenames[i]), "rb")
    temp = script.read()
    new_file.write(temp)
    if (len(temp) != (4 * round((scripts_size[i]+1) / 4))):
        rest = (4 * round((scripts_size[i]+1) / 4) - len(temp))
        for i in range(0, rest):
            new_file.write(b"\x00")

if (new_file.tell() % 16 != 0):
    rest = 16 - (new_file.tell() % 16)
    for i in range(0, rest):
        new_file.write(b"\x00")