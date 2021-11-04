import sys
import numpy
import os
import zstandard

ZSTD_MAGIC_header = b"\x28\xB5\x2F\xFD"

def DebugOutput(string):
	if (DebugOutput.Flag == False): 
		file = open("Debug.txt", "w", encoding="UTF-8")
		DebugOutput.Flag = True
	else: file = open("Debug.txt", "a", encoding="UTF-8")
	file.write(string)
	file.write("\n")
	file.close()
DebugOutput.Flag = False

def MakeHeader(chunk_size, iterator):
	buffer_temp = []
	if (iterator == 0):
		buffer_temp.append(ZSTD_MAGIC_header)
		buffer_temp.append(0x0.to_bytes(1, byteorder="little"))
		buffer_temp.append(0x48.to_bytes(1, byteorder="little"))
	compressed_block_flag = "100"
	bin_c_size = bin(chunk_size)[2:]
	bin_compress_size = bin_c_size + compressed_block_flag
	com_size = int(bin_compress_size, base=2).to_bytes(3, byteorder="little")
	buffer_temp.append(com_size)
	return b"".join(buffer_temp)

	
def Decompress(data, u_size, chunks, dec_dict_ID, dec_dicts):
	if (dec_dict_ID != -1):
		dictionary = zstandard.ZstdCompressionDict(dec_dicts[dec_dict_ID])
		dctx = zstandard.ZstdDecompressor(dict_data = dictionary)
	else:
		dctx = zstandard.ZstdDecompressor()
	list = []
	sumarum = 0
	for i in range(0, len(chunks)):
		temp_list = []
		data_temp = data[sumarum:sumarum+chunks[i]]
		sumarum += chunks[i]
		temp_list.append(MakeHeader(len(data_temp), i))
		temp_list.append(data_temp)
		list.append(b"".join(temp_list))
	list.append(b"\x01\x00\x00")
	return dctx.decompress(b"".join(list), max_output_size=u_size)

file = open("preload_zstd.vfs", "rb")

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

# Reading offsets of tables for Chunks, Decompression Dicts and String list
Temp = numpy.fromfile(file, dtype=numpy.uint64, count=3)
Chunk_dictionary_offset = Temp[0]
Decompression_dictionary_offset = Temp[1]
StringListOffset = Temp[2]
file.seek(4, 1)

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

Files = {}
for i in range(0, file_count):
	entry = {}
	Temp = numpy.fromfile(file, dtype=numpy.uint64, count=3)
	entry["OFFSET"] = Temp[0]
	entry["C_SIZE"] = Temp[1]
	entry["U_SIZE"] = Temp[2]
	entry["CRC"] = file.read(0x4).hex()
	Temp = numpy.fromfile(file, dtype=numpy.uint32, count=2)
	entry["FolderID"] = Temp[1]
	entry["COMPRESSION"] = numpy.fromfile(file, dtype=numpy.int16, count=1)[0] #Compression method
	if (entry["COMPRESSION"] != 3):
		print("UNKNOWN FLAG! %d" % entry["COMPRESSION"])
		sys.exit()
	entry["DEC_DICT"] = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
	entry["FULLPATH"] = "%s/%s" % (Folders["0x%x" % Temp[1]], File_names[Temp[0]])
	Files["0x%x" % Temp[0]] = entry

#Read Chunks dictionary
Chunks = []
file.seek(Chunk_dictionary_offset, 0)
ChunkTableSize = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
while (file.tell() < (Chunk_dictionary_offset + ChunkTableSize)):
	entry = {}
	size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	entry["SIZES"] = numpy.fromfile(file, dtype=numpy.uint32, count=int(size / 4))
	Chunks.append(entry)

#Read Decompression Dicts dictionary
decompress_dictionary_count = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
size_dec_dict = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

Dec_dicts = []
for i in range(0, decompress_dictionary_count):
	dict_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
	Dec_dicts.append(file.read(dict_size))

Files_SUCCESS = 0
Files_FAIL = 0
# Write Data
for i in range(0, len(Files)):
	Offset = OldPlace + int(Files["0x%x" % i]["OFFSET"])
	file.seek(Offset, 0)
	if ((Files["0x%x" % i]["C_SIZE"] == 0) or (Files["0x%x" % i]["C_SIZE"] == Files["0x%x" % i]["U_SIZE"])):
		data.append(file.read(Files["0x%x" % i]["U_SIZE"]))
	else:
		buffer_temp = (file.read(Files["0x%x" % i]["C_SIZE"]))
		try:
			data = Decompress(buffer_temp, Files["0x%x" % i]["U_SIZE"], Chunks[i]["SIZES"], Files["0x%x" % i]["DEC_DICT"], Dec_dicts)
		except Exception as Exception_handle:
			DebugOutput("%s, %s, chunks=%d, dec_dict=%d" % (Files["0x%x" % i]["FULLPATH"], Exception_handle, len(Chunks[i]["SIZES"]), Files["0x%x" % i]["DEC_DICT"]))
			Files_FAIL += 1
			continue

	Files_SUCCESS += 1
	os.makedirs(os.path.dirname(Files["0x%x" % i]["FULLPATH"]), exist_ok=True)
	file_new = open(Files["0x%x" % i]["FULLPATH"], "wb")
	file_new.write(data)
	file_new.close()

print("Finished executing script!")
print("TOTAL / SUCCESS / FAIL")
print("%d / %d / %d" % (Files_SUCCESS+Files_FAIL, Files_SUCCESS, Files_FAIL))
if (Files_FAIL > 0): print("You can find list of failed files in Debug.txt!")