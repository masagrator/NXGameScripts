import os
import numpy
import threading
import time
import glob
import sys
import shutil
import xml.etree.ElementTree as ET

def ReturnIndex(dec_buffer, dec_indx, window_size, file_size):
	dec_offset = dec_indx - window_size
	assert(window_size < 255)
	if (dec_offset < 0):
		dec_offset = 0
	old_dec_indx = dec_indx
	Size = 0
	Offset = 0
	iterator = 3
	if (dec_indx+iterator >= (file_size - iterator)):
		pass
	elif (dec_buffer.find(dec_buffer[dec_indx:dec_indx+iterator], dec_offset, dec_indx) != -1):
		while(True):
			iterator += 1
			idx = dec_buffer.rfind(dec_buffer[dec_indx:dec_indx+iterator], dec_offset, dec_indx)
			if (idx != -1):
				Size = iterator
				Offset = idx
			else:
				break
			if (dec_indx+iterator >= file_size):
				break


	if (Size == 0):
		return None, None, dec_indx
	else:
		dec_indx = old_dec_indx + Size
		return (Offset, Size, dec_indx)
	

def GetFileSize(src):
	src.seek(0, 2)
	size = src.tell()
	src.seek(0)
	return size

def printStatus():
	while(printStatus.close == False):
		print("%d%s, %d/%d" % ((LZ77Compress.dec_itr / LZ77Compress.dec_buffer_size ) * 100, "%", LZ77Compress.dec_itr, LZ77Compress.dec_buffer_size ), end="\r")
printStatus.close = False

def LZ77Compress(src, window_size = 254):
	dec_buffer = src.read()
	LZ77Compress.dec_buffer_size = len(dec_buffer)
	dec_buffer2 = numpy.frombuffer(dec_buffer, dtype=numpy.uint8)
	unique = numpy.unique(dec_buffer2)
	array_sub = numpy.array(range(0, 256), dtype=numpy.uint8)
	difference = numpy.array([i for i in array_sub if i not in unique], dtype=numpy.uint8)
	if (difference.size != 0):
		flag = numpy.amin(difference)
	else:
		counts = numpy.bincount(dec_buffer2)
		flag = numpy.argmin(counts)

	output = bytearray(b"\0" * (LZ77Compress.dec_buffer_size + 256))
	output[0] = flag
	output_itr = 4
	LZ77Compress.dec_itr = 0

	t1 = threading.Thread(name="PrintStatus", target=printStatus, daemon=True)
	t1.start()

	while(LZ77Compress.dec_itr < LZ77Compress.dec_buffer_size):
		byte = dec_buffer[LZ77Compress.dec_itr]
		if (byte == flag):
			LZ77Compress.dec_itr += 1
			output[output_itr] = flag
			output[output_itr+1] = byte
			output_itr += 2
		else:
			(Offset, Size, new_index) = ReturnIndex(dec_buffer, LZ77Compress.dec_itr, window_size, LZ77Compress.dec_buffer_size)
			if (Offset != None):
				output[output_itr] = flag
				output[output_itr+1] = LZ77Compress.dec_itr - Offset
				if (flag <= (LZ77Compress.dec_itr - Offset)):
					output[output_itr+1] += 1
				LZ77Compress.dec_itr = new_index
				output[output_itr+2] = Size
				output_itr += 3
			else:				
				output[output_itr] = dec_buffer[LZ77Compress.dec_itr]
				output_itr += 1
				LZ77Compress.dec_itr += 1

	printStatus.close = True
	t1.join()
	printStatus.close = False

	return output[0:output_itr]
LZ77Compress.dec_itr = 0
LZ77Compress.dec_buffer_size = 0

if (len(sys.argv) != 2):
	print("USAGE:")
	print("Compresspkg.py [folder_path]")
	sys.exit()

tree = ET.parse("%s/asset_GNX.xml" % sys.argv[1])
root = tree.getroot()
files = ["asset_GNX.xml"]
for x in range(0, len(root)):
	for y in range(0, len(root[x])):
		files.append(os.path.basename(root[x][y].attrib["path"]))

os.makedirs("tmp", exist_ok=True)

for i in range(0, len(files)):
	print("---->%s" % files[i])
	file_new = open("%s/%s" % (sys.argv[1], files[i]), "rb")
	uncompressed_size = GetFileSize(file_new)
	file_new2 = open("tmp/%s" % files[i], "wb")
	start_time = time.time()
	file_new2.write(LZ77Compress(file_new))
	print("Time: %s s" % (time.time() - start_time))
	print("Compression ratio: %0.2f%s" % ((file_new2.tell() / uncompressed_size) * 100, "%"))
	file_new.close()
	file_new2.close()

print("Packing PKG")
os.makedirs("NEW_PKG", exist_ok=True)
pkg_new = open("NEW_PKG/%s.pkg" % os.path.basename(os.path.dirname(sys.argv[1] + "/")), "wb")
pkg_new.write(b"\x00\x00\x81\x60")
pkg_new.write(numpy.uint32(len(files)))
header_block = []
blob_offset = 8 + (0x50 * len(files))
blob_sizes = []
for i in range(0, len(files)):
	entry = []
	unc_file = open("%s/%s" % (sys.argv[1], files[i]), "rb")
	com_file = open("tmp/%s" % files[i], "rb")
	unc_size = GetFileSize(unc_file)
	com_size = GetFileSize(com_file) + 8
	unc_file.close()
	com_file.close()
	string = os.path.basename(files[i]).encode("ASCII")
	if (len(string) < 0x40):
		string += b"\x00" * (0x40 - len(string))
	entry.append(string)
	entry.append(numpy.uint32(unc_size))
	entry.append(numpy.uint32(com_size))
	entry.append(numpy.uint32(blob_offset))
	blob_offset += com_size
	entry.append(numpy.uint32(1))
	header_block.append(b"".join(entry))
	blob_sizes.append((numpy.uint32(unc_size), numpy.uint32(com_size)))
pkg_new.write(b"".join(header_block))
for i in range(0, len(files)):
	com_file = open("tmp/%s" % files[i], "rb")
	pkg_new.write(blob_sizes[i][0])
	pkg_new.write(blob_sizes[i][1])
	pkg_new.write(com_file.read())
	com_file.close()
pkg_new.close()
shutil.rmtree("tmp")