import os
import glob
import sys

def lib(path):
	files = glob.glob(f"{path}/{path}_*_swizzled.astc")
	os.makedirs("new", exist_ok=True)
	wtp = open(f"new/{sys.argv[1]}.wtp", "wb")
	sizes = []
	for i in range(len(files)):
		temp = open(files[i], "rb")
		temp.seek(0, 2)
		sizes.append(temp.tell())
		temp.seek(0)
		wtp.write(temp.read())
		temp.close()
	wtp.close()
	wta = open(f"{sys.argv[1]}/{sys.argv[1]}.wta", "rb")
	wta.seek(0x1C)
	header_size = int.from_bytes(wta.read(4), "little")
	wta.seek(0xC)
	offsets_table = int.from_bytes(wta.read(4), "little")
	sizes_table = int.from_bytes(wta.read(4), "little")
	wta.seek(0)
	wta_new = open(f"new/{sys.argv[1]}.wta", "wb")
	wta_new.write(wta.read(header_size))
	wta_new.seek(offsets_table)
	base = 0
	for i in range(len(files)):
		wta_new.write(base.to_bytes(4, "little"))
		base += sizes[i]
	wta_new.seek(sizes_table)
	for i in range(len(files)):
		wta_new.write(sizes[i].to_bytes(4, "little"))
	wta_new.seek(0, 2)
	for i in range(len(files)):
		wta_new.write(b".tex")
		wta_new.write(0x79.to_bytes(4, "little"))
		wta_new.write(0x1.to_bytes(4, "little"))
		if (sizes[i] == 0x400000):
			wta_new.write(0x800.to_bytes(4, "little"))
			wta_new.write(0x800.to_bytes(4, "little")) 
		elif (sizes[i] == 0x200000):
			wta_new.write(0x800.to_bytes(4, "little"))
			wta_new.write(0x400.to_bytes(4, "little")) 
		else:
			print("Unknown size")
			sys.exit()
		wta_new.write(0x1.to_bytes(4, "little"))
		wta_new.write(0x1.to_bytes(4, "little"))
		wta_new.write(0x100.to_bytes(4, "little"))
		wta_new.write(sizes[i].to_bytes(4, "little"))
		wta_new.write(b"\x00" * 0xDC)


if __name__ == "__main__":
	lib(sys.argv[1])