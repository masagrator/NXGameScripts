import glob
import os
import json
import sys
import numpy

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

files = glob.glob("database\*.dat")

if (len(files) == 0):
    print("No files detected! Be sure to unpack database.dat!")
    sys.exit()

exceptions = ["database\\common_story.dat", "database\\story.dat", "database\\00_logic.dat", "database\\00_tree.dat", "database\\nmlcodelabel.dat", "database\\screenposadvps4.dat", "database\\tipadv.dat", "database\\tiplogic.dat"]

os.makedirs("strings", exist_ok=True)
for i in range(0, len(files)):
    if (files[i] in exceptions):
        print("%s in in exceptions! Ignoring..." % files[i])
        continue
    file = open(files[i], "rb")
    buffer = numpy.fromfile(file, dtype=numpy.uint32, count=4)
    entry_count = buffer[0]
    entry_size = buffer[1]
    data_blob_start = buffer[2]
    header_size = buffer[3]
    file.seek(header_size)
    match(files[i]):
        case "database\\characterdatabase.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[2])
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\extracg.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[4] + data_blob_start)
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\extraendinglist.dat":
            Dump = {}
            for x in range(0, entry_count):
                entry2 = {}
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[4] + data_blob_start)
                entry2["String1"] = readString(file)
                file.seek(buffer[8] + data_blob_start)
                entry2["String2"] = readString(file)
                file.seek(buffer[10] + data_blob_start)
                entry2["String3"] = readString(file)
                file.seek(buffer[12] + data_blob_start)
                entry2["String4"] = readString(file)
                file.seek(buffer[14] + data_blob_start)
                entry2["String5"] = readString(file)
                file.seek(buffer[16] + data_blob_start)
                entry2["String6"] = readString(file)
                file.seek(buffer[18] + data_blob_start)
                entry2["String7"] = readString(file)
                file.seek(buffer[20] + data_blob_start)
                entry2["String8"] = readString(file)
                file.seek(buffer[22] + data_blob_start)
                entry2["String9"] = readString(file)
                Dump["%d" % buffer[0]] = entry2
                file.seek(pos)
        case "database\\extrasidestory.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[2] + data_blob_start)
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\flagdatabase.dat":
            Dump = []
            for x in range(0, entry_count):
                entry = {}
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                if (buffer[1] > 0):
                    entry["START_ID"] = int(buffer[0])
                    entry["END_ID"] = int(buffer[1])
                else:
                    entry["ID"] = int(buffer[0])
                pos = file.tell()
                file.seek(buffer[2] + data_blob_start)
                entry["STRING"] = readString(file)
                file.seek(pos)
                Dump.append(entry)
        case "database\\foafdatabase.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[4] + data_blob_start)
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\foafdatabasetext.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[4] + data_blob_start)
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\gamestring.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[2])
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\keyword.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[2] + data_blob_start)
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\liarsart.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(buffer[4] + data_blob_start)
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\paramdatabase.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[2])
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\selecter.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[2])
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\selectinfo.dat":
            Dump = {}
            for x in range(0, entry_count):
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[4])
                Dump["%d" % buffer[0]] = readString(file)
                file.seek(pos)
        case "database\\soundbgm.dat":
            Dump = {}
            for x in range(0, entry_count):
                entry2 = {}
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[4])
                entry2["Type"] = readString(file)
                file.seek(data_blob_start + buffer[8])
                entry2["String1"] = readString(file)
                file.seek(data_blob_start + buffer[10])
                entry2["String2"] = readString(file)
                file.seek(data_blob_start + buffer[12])
                entry2["String3"] = readString(file)
                file.seek(data_blob_start + buffer[14])
                entry2["String4"] = readString(file)
                Dump["%d" % buffer[0]] = entry2
                file.seek(pos)
        case "database\\soundse.dat":
            Dump = {}
            for x in range(0, entry_count):
                entry2 = {}
                buffer = numpy.fromfile(file, dtype=numpy.uint32, count=int(entry_size / 4))
                pos = file.tell()
                file.seek(data_blob_start + buffer[4])
                entry2["Type"] = readString(file)
                file.seek(data_blob_start + buffer[8])
                entry2["String1"] = readString(file)
                file.seek(data_blob_start + buffer[10])
                entry2["String2"] = readString(file)
                file.seek(data_blob_start + buffer[12])
                entry2["String3"] = readString(file)
                file.seek(data_blob_start + buffer[14])
                entry2["String4"] = readString(file)
                Dump["%d" % buffer[0]] = entry2
                file.seek(pos)
        case _:
            print("Ignoring...")
            continue
    if Dump: 
        file_new = open("strings/%s.json" % os.path.basename(files[i])[:-4], "w", encoding="UTF-8")
        json.dump(Dump, file_new, indent="\t", ensure_ascii=False)
        file_new.close()