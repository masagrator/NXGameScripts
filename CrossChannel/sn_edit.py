import numpy
import os

def GetFileSize(file):
	pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(pos)
	return size

file = open("sn_new_dec.bin", "rb")

size = GetFileSize(file)

file.close()

file_old = open("0100735012AAE000/romfs/sn_new.bin", "rb")
dump = file_old.read()
file_old.close()

file_new = open("0100735012AAE000/romfs/sn.bin", "wb")
file_new.write(numpy.uint32(size))
file_new.write(dump)
file_new.close()

os.remove("0100735012AAE000/romfs/sn_new.bin")