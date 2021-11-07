import sys
import numpy
import zlib
import zstandard

def RLE(data):
	output = []
	size = int(bin(int.from_bytes(data[0:3], byteorder="little"))[2:-3], base=2)
	for i in range(0, size):
		output.append(data[3:4])
	return b"".join(output)

def StripBlocks(data):
	size = len(data)
	offset = 0
	buffer = []
	flags = []
	while(offset < size):
		flag = bin(int.from_bytes(data[offset:offset+3], byteorder="little"))[-3:]
		print("Flags: %s" % flag)
		if (flag[0:2] == "01"):
			print("RLE block detected! Experimental conversion")
			output = RLE(data[offset:offset+4])
			buffer.append(output)
			flags.append("00" + flag[2:3])
			offset += 4
		else:
			flags.append(flag)
			size_of_block = int(bin(int.from_bytes(data[offset:offset+3], byteorder="little"))[2:-3], base=2)
			offset += 3
			buffer.append(data[offset:size_of_block+offset])
			offset += size_of_block
	return buffer, flags

def SortOffset(elem):
	return elem["OFFSET"]

def GetFileSize(file):
	temp = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(temp, 0)
	return size

def Compress(file, dec_dict_ID, dec_dicts):
	filesize = GetFileSize(file)
	params = zstandard.ZstdCompressionParameters(compression_level = 15, write_content_size=0, format=zstandard.FORMAT_ZSTD1_MAGICLESS)
	if (dec_dict_ID != -1):
		dictionary = zstandard.ZstdCompressionDict(dec_dicts[dec_dict_ID])
		cctx = zstandard.ZstdCompressor(dict_data = dictionary, compression_params = params).compressobj()
	else:
		cctx = zstandard.ZstdCompressor(compression_params = params).compressobj(size=filesize)
	data_new = []
	chunk_table = []
	flags_array = []
	block_entry = []

	while True:
		in_chunk = file.read(131072)
		if len(in_chunk) < 131072:
			break
		else:
			block_entry.append(cctx.compress(in_chunk))
			block_entry.append(cctx.flush(zstandard.COMPRESSOBJ_FLUSH_BLOCK))
	
	block_entry.append(cctx.compress(in_chunk))
	block_entry.append(cctx.flush())
	if (file.name == "Data/nx64/font/nk2_font2_en/nk2_font.g4tx"):
		file_next = open("output.bin", "wb")
		file_next.write(b"".join(block_entry))
		file_next.close()
	data = b"".join(block_entry)[2:]
	data_temp, flags = StripBlocks(data)
	for i in range(0, len(data_temp)):
		data_new.append(data_temp[i])
	for i in range(0, len(flags)):
		flags_array.append(flags[i])
	if (len(b"".join(data_new)) == 0):
		raise ValueError("Compressed data has 0 B size!")
	for i in range(0, len(data_new)):
		if (flags_array[i][0:1] == "0"):
			size = int(len(data_new[i]) * -1)
		else: 
			size = len(data_new[i])
		chunk_table.append(numpy.int32(size))
	return b"".join(data_new), chunk_table

file = open(sys.argv[1], "rb")

#Read header data
if (file.read(0x4) != b"VFS3"):
	print("WRONG HEADER")
	sys.exit()

header_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
GEN = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

#Here starts folder dictionary
folder_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

#Saving offset where folder dictionary table starts for later
repeat_offset = file.tell()

#Calculating where folder dictionary ends
for i in range(0, folder_count):
	temp = numpy.fromfile(file, dtype=numpy.uint32, count=7)[0]

#Calculating where file dictionary ends
file_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

for i in range(0, file_count):
	Temp = numpy.fromfile(file, dtype=numpy.uint64, count=3)
	Temp = numpy.fromfile(file, dtype=numpy.uint32, count=4)

dictionaries_pointers = file.tell()

# Reading offsets of tables for Chunks, Decompression Dicts and String list
Temp = numpy.fromfile(file, dtype=numpy.uint64, count=3)
Chunk_dictionary_offset = Temp[0]
Decompression_dictionary_offset = Temp[1]
StringListOffset = Temp[2]
while (file.tell() % 16 != 0):
	file.seek(1, 1)

file_new = open("%s_NEW.vfs" % (sys.argv[1][:-4]), "wb")

end_of_first_part = file.tell()
file.seek(0, 0)
file_new.write(file.read(end_of_first_part))

#Offsets in file dictionary are relative to this position, so we need to save offset.
OldPlace = file.tell()

#Jumping to String List to read folder and file names
file.seek(StringListOffset, 0)
strings_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
File_names = []
Folder_names = []

for i in range(0, strings_count):
	string_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	string = file.read(string_size).decode("UTF-8")
	File_names.append(string)

strings_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

if (strings_count != folder_count):
	print("Folder name count doesn't match!")
	sys.exit()

for i in range(0, strings_count):
	string_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	string = file.read(string_size).decode("UTF-8")
	Folder_names.append(string)

Folders = {}

#Going back to previously saved offset where folder dictionary starts

file.seek(repeat_offset, 0)

#Read all data related to folder dictionary
for i in range(0, folder_count):
	CRC = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	ID = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
	PreviousID = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
	NextID = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
	Folders_inside = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	unk = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	Files_inside = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	if ((PreviousID == -1) or (Folders["0x%x" % PreviousID] == "")):
		Folders["0x%x" % ID] = Folder_names[ID]
	else:
		Folders["0x%x" % ID] = "%s/%s" % (Folders["0x%x" % PreviousID], Folder_names[ID])

#Read all data related to file dictionary and write in the meantime full paths

file_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
file_offset_base = file.tell()

Files = []
for i in range(0, file_count):
	entry = {}
	entry["POINTER"] = file.tell()
	Temp = numpy.fromfile(file, dtype=numpy.uint64, count=3)
	entry["OFFSET"] = Temp[0]
	entry["C_SIZE"] = Temp[1]
	entry["U_SIZE"] = Temp[2]
	entry["CRC"] = file.read(0x4).hex()
	Temp = numpy.fromfile(file, dtype=numpy.uint32, count=2)
	entry["FileID"] = Temp[0]
	entry["FolderID"] = Temp[1]
	entry["COMPRESSION"] = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
	if (entry["COMPRESSION"] != 3): # VFS supports other compressions. In Ni no Kuni 2 all files are compressed with zstd which matches "3"
		print("UNKNOWN COMPRESSION! %d" % entry["COMPRESSION"])
		sys.exit()
	entry["DEC_DICT"] = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
	entry["FULLPATH"] = "%s/%s" % (Folders["0x%x" % Temp[1]], File_names[Temp[0]])
	Files.append(entry)

Files.sort(key=SortOffset)
print("Indexed %d files." % len(Files))

#Read Chunks dictionary
Chunks = []
file.seek(Chunk_dictionary_offset, 0)
ChunkTableSize = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
while (file.tell() < (Chunk_dictionary_offset + ChunkTableSize)):
	entry = {}
	size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0] # Size of chunk size table which is equal to: count of entries * size of int32
	entry["SIZES"] = numpy.fromfile(file, dtype=numpy.int32, count=int(size / 4))
	Chunks.append(entry)

#Read Decompression Dicts dictionary
decompress_dictionary_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
size_dec_dict = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0] # Size of Decompression Dicts dictionary

Dec_dicts = []
for i in range(0, decompress_dictionary_count):
	dict_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0] # Size of one Decompression Dict
	Dec_dicts.append(file.read(dict_size))

print("Indexed %d compression dictionaries." % len(Dec_dicts))

chunk_main_table = []
file_new_offsets = []
file_new_c_sizes = []
file_new_u_sizes = []

Hash_table = []
New_table = {}

for i in range(0, file_count):
	chunk_table = []
	Repeated = 0
	for x in range(0, len(Chunks[i]["SIZES"])):
		chunk_table.append(numpy.int32(Chunks[i]["SIZES"][x]))
	try:
		file_handle = open(Files[i]["FULLPATH"], "rb")
	except:
		if (i % 1024 == 0):
			print("%d/%d" % (i+1, file_count))
		file.seek(int(Files[i]["OFFSET"]) + OldPlace, 0)
		data = file.read(Files[i]["C_SIZE"])
		crc = zlib.crc32(data)
		if (crc in Hash_table):
			Repeated = Hash_table.index(crc)
		Hash_table.append(crc)
		file_new_u_sizes.append(Files[i]["U_SIZE"])
	else:
		print("%d/%d %s detected. Packing..." % (i+1, file_count, Files[i]["FULLPATH"]))
		file_new_u_sizes.append(GetFileSize(file_handle))
		data, chunk_table2 = Compress(file_handle, Files[i]["DEC_DICT"], Dec_dicts)
		print("Compression comparison ### Original: %d B / %0.2f MB, New: %d B / %0.2f MB. Ratio: %0.2f" % (Files[i]["C_SIZE"], Files[i]["C_SIZE"] / 1024 / 1024, len(data), len(data) / 1024 / 1024, (len(data) / Files[i]["C_SIZE"]) * 100) + "%")
		print("ID: %d, iterator: %d" % (Files[i]["FileID"], i))
		print("Chunk size offset: 0x%x" % len(b"".join(chunk_main_table)))
		file_handle.close()
		crc = zlib.crc32(data)
		if (crc in Hash_table):
			Repeated = Hash_table.index(crc)
		Hash_table.append(crc)
		entry2 = []
		chunk_count = int(len(chunk_table2)*4).to_bytes(4, byteorder="little")
		entry2.append(chunk_count)
		entry2.append(b"".join(chunk_table2))
		New_table["%d" % Files[i]["FileID"]] = b"".join(entry2)
	print("%d: FileID: %d, %s" % (i, Files[i]["FileID"], Files[i]["FULLPATH"]) + str(chunk_table))
	file_new_c_sizes.append(len(data))
	if (Files[i]["FULLPATH"] == "Data/nx64/event/ev_pic/ev_pic_e3thankyou/ev_pic_e3thankyou.g4tx"):
		file_2 = open("output2.bin", "wb")
		file_2.write(data)
		file_2.close()
	chunk_count = int(len(chunk_table)*4).to_bytes(4, byteorder="little")
	entry = []
	entry.append(chunk_count)
	entry.append(b"".join(chunk_table))
	chunk_main_table.append(b"".join(entry))
	if (Repeated == 0):
		file_new_offsets.append(file_new.tell() - OldPlace)
	else:
		file_new_offsets.append(file_new_offsets[Repeated])
	if (Repeated == 0):
		file_new.write(data)
	while(file_new.tell() % 16 != 0):
		file_new.write(b"\x00")

for i in range(0, file_count):
	try:
		get = New_table["%d" % i]
	except:
		continue
	else:
		chunk_main_table[i] = New_table["%d" % i]
temp_offset = file_new.tell()
file_new.seek(dictionaries_pointers, 0)
file_new.write(numpy.uint64(temp_offset))
file_new.seek(temp_offset, 0)
file_new.write(numpy.uint32(len(b"".join(chunk_main_table))))
file_new.write(b"".join(chunk_main_table))

temp_offset = file_new.tell()
file_new.seek(dictionaries_pointers + 8, 0)
file_new.write(numpy.uint64(temp_offset))
file_new.seek(temp_offset, 0)
file.seek(Decompression_dictionary_offset, 0)
dict_size = numpy.fromfile(file, dtype=numpy.uint32, count=2)[1]
file.seek(Decompression_dictionary_offset, 0)
file_new.write(file.read(dict_size + 8))

temp_offset = file_new.tell()
file_new.seek(dictionaries_pointers + 16, 0)
file_new.write(numpy.uint64(temp_offset))
file_new.seek(temp_offset, 0)
file_new.write(file.read())

for i in range(0, file_count):
	file_new.seek(Files[i]["POINTER"], 0)
	file_new.write(numpy.uint64(file_new_offsets[i]))
	file_new.write(numpy.uint64(file_new_c_sizes[i]))
	file_new.write(numpy.uint64(file_new_u_sizes[i]))
