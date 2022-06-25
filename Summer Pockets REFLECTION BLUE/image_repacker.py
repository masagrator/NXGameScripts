import sys
import numpy
import os

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

file = open(sys.argv[1], "rb")
header_size = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
file_count = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
unk2_int32 = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
round_to = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
reserved0 = file.read(0x10)
flag0 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag1 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag2 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag3 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
offset_start_file_names = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

if (flag0 != 0):
    print("UNSUPPORTED PAK TYPE")
    sys.exit()

if (flag1 not in [2, 3]):
    print("UNSUPPORTED PAK TYPE")
    sys.exit()

file_table = {}
file_table['offset'] = []
file_table['size'] = []

for i in range(0, file_count):
	file_table['offset'].append(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]*round_to)
	file_table['size'].append(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])

if (flag1 == 2):
	assert(file.tell() == offset_start_file_names)
else:
	file.seek(offset_start_file_names)

filename_table = []

for i in range(0, file_count):
	filename_table.append(readString(file))

if (len(sys.argv) == 3):
	new_file = open("%s" % (sys.argv[2]), "wb")
else:
	new_file = open("%s_NEW.PAK" % (sys.argv[1][:-4]), "wb")
file.seek(0)
new_file.write(file.read(header_size))
file.seek(0)
new_file.seek(0x28)

scripts_size = []

for i in range(0, file_count):
	if (file_table["offset"][i] == 0):
		try:
			script = open("%s\%s.dat" % (sys.argv[1][:-4], filename_table[i]), "rb")
		except:
			scripts_size.append(0)
			continue
	else:
		script = open("%s\%s.dat" % (sys.argv[1][:-4], filename_table[i]), "rb")
	script.seek(0, 2)
	scripts_size.append(script.tell())
	script.close()

offset = header_size / round_to

for i in range(0, file_count):
	if (scripts_size[i] == 0):
		new_file.write(numpy.uint64(0))
		continue
	new_file.write(numpy.uint32(offset))
	new_file.write(numpy.uint32(scripts_size[i]))
	offset += int(round((scripts_size[i]+(round_to/2-1)) / round_to))

new_file.seek(offset_start_file_names)

for i in range(0, file_count):
	new_file.write(filename_table[i].encode("shift_jis_2004"))
	new_file.write(b"\x00")

file.seek(new_file.tell(), 0)
while(True):
	if (new_file.tell() == header_size): break
	new_file.write(file.read(0x1))

for i in range(0, file_count):
	if (scripts_size[i] == 0):
		continue
	script = open("%s\%s.dat" % (sys.argv[1][:-4], filename_table[i]), "rb")
	temp = script.read()
	new_file.write(temp)
	if (len(temp) != (round_to * round((scripts_size[i]+(round_to/2-1)) / round_to))):
		rest = (round_to * round((scripts_size[i]+(round_to/2-1)) / round_to) - len(temp))
		for i in range(0, rest):
			new_file.write(b"\x00")

if (new_file.tell() % 16 != 0):
	rest = 16 - (new_file.tell() % 16)
	for i in range(0, rest):
		new_file.write(b"\x00")