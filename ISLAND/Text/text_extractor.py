import numpy
import json
import os
import sys

try:
    os.mkdir("json")
except:
    pass

SUBCMD_EXCEPTIONS = [0x14, 0xB, 0x3]

Filenames = []

Dump = {}
Dump['Main'] = []

with open("chapternames.txt", 'r', encoding="ascii") as f:
    Filenames = [line.strip("\r\n").strip("\n").split("\t", -1)[0] for line in f]

for i in range(0, len(Filenames)):
    file = open("new\%s.dat" % (Filenames[i]), "rb")
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0, 0)
    while (file.tell() < file_size):
        if (file.read(1) == b"\x23"):
            if (file.read(1) == b"\x03"):
                file.seek(-4, 1)
                current_offset = file.tell()
                command_size = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
                if (file.read(2) == b"\x23\x03"):
                    entry = {}
                    subcommand = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
                    if (subcommand >= 0xFF00 or subcommand in SUBCMD_EXCEPTIONS): continue
                    entry['SUBCMD'] = subcommand
                    entry['MSGID'] = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
                    temp_numb = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
                    if (temp_numb != 0): entry['VOICEID'] = temp_numb
                    string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
                    if (string_size == 0): continue
                    if (string_size > 0):
                        string_size = string_size * 2
                        entry['JPN'] = file.read(string_size).decode("UTF-16-LE")
                        file.seek(2, 1)
                    else:
                        entry['JPN'] = file.read(string_size).decode("UTF-8")
                        file.seek(1, 1)
                    string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
                    if (string_size > 0): 
                        string_size = string_size * 2
                        entry['ENG'] = file.read(string_size).decode("UTF-16-LE")
                        file.seek(2, 1)
                    else:
                        string = file.read(abs(string_size))
                        try:
                            entry['ENG'] = string.decode("UTF-8")
                        except Exception as err:
                            raise Exception("Something went wrong. String:\n%s\nError: %s" % (string, err))
                            input("Press ENTER")
                            sys.exit()
                        file.seek(1, 1)   
                    Dump['Main'].append(entry)
                else: raise Exception("Something went horribly wrong.")
                file.seek(current_offset + command_size, 0)
    file.close()
    if (Dump['Main'] != []):
        jsonfile = open("json\%s.json" % (Filenames[i]), "w", encoding="UTF-8")
        json.dump(Dump, jsonfile, indent=4, ensure_ascii=False)
        jsonfile.close()
        Dump['Main'] = []
    else: print("No messages were found in %s" % (Filenames[i]))