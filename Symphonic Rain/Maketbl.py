import glob
import numpy

files = glob.glob("New_KGO/*.kgo")

Size = 0x1912
Count = 0xE4
MaxFuncSize = 0
MaxDataSize = 512
MaxTextSize = 0
MaxTextCount = 0

Table = open("New_KGO/Scene.tbl", "wb")
Table.write(b"SR10") #0x0
Table.write(numpy.uint32(Size)) # 0x4
Table.write(numpy.uint32(Count)) # 0x8
Table.write(numpy.uint32(MaxFuncSize)) #0xC
Table.write(numpy.uint32(MaxDataSize)) #0x10
Table.write(numpy.uint32(MaxTextSize)) #0x14
Table.write(numpy.uint32(MaxTextCount)) #0x18

for i in range(0, len(files)):
    file = open(files[i], "rb")
    file.seek(0x10)
    registration_offset = int.from_bytes(file.read(0x4), byteorder="little")
    file.seek(0x18)
    registration_count = int.from_bytes(file.read(0x4), byteorder="little")
    file.seek(registration_offset)
    for i in range(0, registration_count):
        temp = file.tell()
        entry_size = int.from_bytes(file.read(0x2), byteorder="little")
        file.seek(-2, 1)
        Table.write(file.read(entry_size))
        file.seek(temp+entry_size)
    file.seek(0x20)
    Funcs_size = int.from_bytes(file.read(0x4), byteorder="little")
    if (MaxFuncSize < Funcs_size):
        MaxFuncSize = Funcs_size
    file.seek(0x38)
    Text_blob_size = int.from_bytes(file.read(0x4), byteorder="little")
    if (MaxTextSize < Text_blob_size):
        MaxTextSize = Text_blob_size
    Text_count = int.from_bytes(file.read(0x4), byteorder="little")
    if (MaxTextCount < Text_count):
        MaxTextCount = Text_count
    file.close()
Table.seek(0xC)
Table.write(numpy.uint32(MaxFuncSize)) #0xC
Table.write(numpy.uint32(MaxDataSize)) #0x10
Table.write(numpy.uint32(MaxTextSize)) #0x14
Table.write(numpy.uint32(MaxTextCount)) #0x18
Table.close()