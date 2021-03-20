import numpy

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

f = open("localization.bin", "rb")

Column = []

Columns_count = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
for i in range(0, Columns_count):
    Column.append([])

for i in range(0, Columns_count):
    ID = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
    IDString_size = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
    Column[i].append(f.read(IDString_size).decode("UTF-8"))
    unk1 = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
    row_count = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
    row_offset = numpy.fromfile(f, dtype=numpy.uint32, count = row_count+1)
    offset_master = f.tell()
    for x in range(0, row_count):
        f.seek(offset_master + row_offset[x], 0)
        Column[i].append(readString(f).replace("\x0D\x0A", "<break_line>"))
    character_table_size = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
    character_table = f.read(character_table_size).decode("UTF-8")

f.close()

f = open("Extracted.tsv", "w", encoding="UTF-8")
for i in range(0, row_count):
    for x in range(0, Columns_count):
        f.write(Column[x][i])
        if (x < Columns_count-1): f.write("\t")
    if (i < row_count-1): f.write("\n")

f.close()