import numpy

Columns = []

with open("Extracted.tsv", 'r', encoding='utf-8') as f:
    Columns.append([line.split("\t", -1)[0] for line in f])
    f.seek(0,0)
    Columns.append([line.split("\t", -1)[1] for line in f])
    f.seek(0,0)
    Columns.append([line.split("\t", -1)[2] for line in f])
    f.seek(0,0)
    Columns.append([line.split("\t", -1)[3] for line in f])
    f.seek(0,0)
    Columns.append([line.split("\t", -1)[4] for line in f])
    f.seek(0,0)
    Columns.append([line.split("\t", -1)[5] for line in f])
    f.seek(0,0)
    Columns.append([line.split("\t", -1)[6] for line in f])

print(Columns[0])

with open("localization_new.bin", "wb") as f:
    f.write(numpy.uint32(7))
    for i in range(0, 7):
        f.write(numpy.uint32(i))
        f.write(numpy.uint32(len(Columns[i][0])))
        f.write(bytes(Columns[i][0].encode("UTF-8")))
        if (bytes(Columns[i][0].encode("UTF-8")) == bytes("Spanish".encode("UTF-8"))): f.write(numpy.uint32(6))
        elif (bytes(Columns[i][0].encode("UTF-8")) == bytes("German".encode("UTF-8"))): f.write(numpy.uint32(5))
        else: f.write(numpy.uint32(0))
        f.write(numpy.uint32(len(Columns[i])-1))
        master_size = 0
        f.write(numpy.uint32(master_size))
        for x in range(1, len(Columns[i])):
            master_size = master_size + len(Columns[i][x].replace("<break_line>", "\x0D\x0A").encode("UTF-8")) + 1
            f.write(numpy.uint32(master_size))
        for x in range(1, len(Columns[i])):
            f.write(bytes(Columns[i][x].replace("<break_line>", "\x0D\x0A").encode("UTF-8")))
            f.write(numpy.uint8(0))
        character_table = []
        size = 0
        for x in range(1, len(Columns[i])):
            lista = list(Columns[i][x].replace("<break_line>", "\x0D\x0A"))
            for y in range(0, len(lista)):
                temp = lista[y].encode("UTF-8")
                if temp not in character_table:
                    character_table.append(temp)
                    size = size + len(temp)
        f.write(numpy.uint32(size+1))
        for x in range(0, len(character_table)):
            f.write(bytes(character_table[x]))
        f.write(numpy.uint8(0))