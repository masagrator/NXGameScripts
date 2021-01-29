import numpy
import sys

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)


f = open(sys.argv[1], 'rb')

Entry_count = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
text_block_start = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
text_block_size = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
text_count = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]

Entry_typeID = []
offset = []
entry_type = []
entry_value = []
string_offset = []

f.seek(text_block_start)

x = False

new = open("%s.txt" % (sys.argv[1]), "w", encoding="UTF-8")

while(True):
    new.write("0x%x\t%s" % (f.tell()-text_block_start, readString(f)))
    new.write("\n")
    if (f.tell() == text_block_start + text_block_size): break

new.close()
f.close()