import sys

file = open(f"{sys.argv[1]}.wta", "rb")
blob = open(f"{sys.argv[1]}.wtp", "rb")

if file.read(4) != b"WTB\x00":
    print("WRONG MAGIC!")
    sys.exit()

flags = int.from_bytes(file.read(4), "little")
file_count = int.from_bytes(file.read(4), "little")
offset_table = int.from_bytes(file.read(4), "little")
sizes_table = int.from_bytes(file.read(4), "little")
random_IDs = int.from_bytes(file.read(4), "little")
info_table = int.from_bytes(file.read(4), "little")

offsets = []
sizes = []

file.seek(offset_table)
for i in range(file_count):
    offsets.append(int.from_bytes(file.read(4), "little"))

file.seek(sizes_table)
for i in range(file_count):
    sizes.append(int.from_bytes(file.read(4), "little"))

for i in range(file_count):
    new_file = open(f"{sys.argv[1]}_{i}.dds", "wb")
    blob.seek(offsets[i])
    new_file.write(blob.read(sizes[i]))
    new_file.close()

blob.close()
file.close()