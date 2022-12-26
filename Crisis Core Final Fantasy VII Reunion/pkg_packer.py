import zlib
import sys
import os
from pathlib import Path
import glob

def sanitizeFilenames(fileList):
	for i in range(len(fileList)):
		if (Path(fileList[i]).stem.isnumeric() == False):
			print("Files must use numerical names!")
			print("File %s has wrong name!" % Path(fileList[i]).stem)
			sys.exit()
		number = int(Path(fileList[i]).stem, 10)
		if (sanitizeFilenames.IDCheck < number): sanitizeFilenames.IDCheck = number
sanitizeFilenames.IDCheck = 0

def printUsage():
	print(sys.argv)
	print("pkg_packer.py [options] <input folder path>")
	print("Options:")
	print("-r: repack (-e and -m are unavailable if this option is used)")
	print("-o: output file <file path>, default: \"Discimg/discimg_jefigs.pkg\"")
	print("-e: entry count <number>, default: 0x7118")
	print("-m: max chunk size <number>, default: 0x8000")
	print("-l: compression level <number 0-9>, default: 2")
	print("-h: this lowers IO lag at the cost of higher RAM usage (1 GB of free RAM expected)")
	sys.exit()

repack = False
output = "Discimg/discimg_jefigs.pkg"
entry_count = 0x7118
chunk_size = 0x8000
entry_size = 0x10
header_size = 0x10
compression_level = 2
highRAM = False

if (len(sys.argv) < 2):
	printUsage()

i = 1
if (len(sys.argv) > 2):
	while (i < (len(sys.argv) - 1)):
		match(sys.argv[i]):
			case "-r":
				repack = True
				i += 1
			case "-o":
				output = sys.argv[i+1]
				i += 2
			case "-e":
				entry_count = int(sys.argv[i+1])
				i += 2
			case "-m":
				chunk_size = int(sys.argv[i+1])
				i += 2
			case "-l":
				compression_level = int(sys.argv[i+1])
				i += 2
			case "-h":
				highRAM = True
				i += 1
			case _:
				printUsage()

input_folder = sys.argv[len(sys.argv) - 1]

files = glob.glob(f"{input_folder}/*.*")
sanitizeFilenames(files)

assert(sanitizeFilenames.IDCheck <= entry_count)

header = []
header.append(b"FGKP")
header.append(entry_size.to_bytes(4, "little"))
header.append(entry_count.to_bytes(8, "little"))

table = []

data_blob_offset = header_size + (entry_count * entry_size)

os.makedirs(os.path.dirname(output), exist_ok=True)

if repack == False:
	x = 0
	file_count = len(files)
	for i in range(entry_count):
		if (x < file_count) and (i == int(Path(files[x]).stem, base=10)):
			print("Calculating file %d/%d" % (x+1, file_count), end="\r")
			table.append(chunk_size.to_bytes(4, "little"))
			table.append(os.stat(files[x]).st_size.to_bytes(4, "little"))
			x += 1
			table.append(b"\x00" * 8)
		else:
			table.append(b"\x00" * 4)
			table.append(b"\x00" * 4)
			table.append(b"\x00" * 8)
	print("Finished calculating %d files" % file_count)

	size_now = len(b"".join(header) + b"".join(table))
	if (data_blob_offset != size_now):
		print("Writing header + table gone wrong!")
		print("Expected: 0x%x" % data_blob_offset)
		print("Got: 0x%x" % size_now)
		sys.exit()
	
	offset = data_blob_offset

	if (highRAM == True): 
		BLOB = []
		for i in range(file_count):
			print("Compressing file %d/%d" % (i+1, file_count), end="\r")
			filesize = os.stat(files[i]).st_size
			temp_file = open(files[i], 'rb')
			compressed_data = []
			while(temp_file.tell() < filesize):
				compressed_data.append(zlib.compress(temp_file.read(chunk_size), level=compression_level))
			temp_file.close()
			temp_size = 0
			for x in range(len(compressed_data)):
				chunk_temp_size = len(compressed_data[x])
				BLOB.append(chunk_temp_size.to_bytes(4, "little"))
				temp_size += chunk_temp_size + 4
			for x in range(len(compressed_data)):
				BLOB.append(compressed_data[x])
			table[int(Path(files[i]).stem, base=10) * 3 + 2] = offset.to_bytes(8, "little")
			offset += temp_size
		new_file = open(output, "wb")
		new_file.write(b"".join(header))
		new_file.write(b"".join(table))
		new_file.write(b"".join(BLOB))
		new_file.close()
	else:
		new_file = open(output, "wb")
		new_file.write(b"".join(header))
		new_file.write(b"".join(table))
		for i in range(file_count):
			print("Compressing file %d/%d" % (i+1, file_count), end="\r")
			filesize = os.stat(files[i]).st_size
			temp_file = open(files[i], 'rb')
			compressed_data = []
			while(temp_file.tell() < filesize):
				compressed_data.append(zlib.compress(temp_file.read(chunk_size), level=compression_level))
			temp_file.close()
			for x in range(len(compressed_data)):
				new_file.write(len(compressed_data[x]).to_bytes(4, "little"))
			for x in range(len(compressed_data)):
				new_file.write(compressed_data[x])
			new_file.seek(header_size + (int(Path(files[i]).stem, base=10) * entry_size) + 0x8)
			new_file.write(offset.to_bytes(8, "little"))
			new_file.seek(0, 2)
			offset = new_file.tell()
		new_file.close()

	print("Finished executing script!")
else:
	print("Repack not implemented")
	sys.exit()
