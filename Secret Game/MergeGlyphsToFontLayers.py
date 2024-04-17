from PIL import Image
import sys
import glob
from pathlib import Path
import os

def CalculatePos(value: int):
	if (0x20 <= value <= 0x7F):
		value += 0x300 - 0x31
	elif (value & 0xFF < 0x40 or value & 0xFF in [0x7F, 0xFD, 0xFE, 0xFF]):
		return -1, -1, -1
	elif (0x9FFC >= value >= 0x8140):
		value -= 0x8140
		remainder = value % 0x100
		value = int(value / 0x100) * 188 + remainder
		if (remainder > 0x3E): value -= 1
	elif (0xFC4B >= value >= 0xE040):
		value -= 0xE040
		remainder = value % 0x100
		value = int(value / 0x100) * 188 + remainder
		if (remainder > 0x3E): value -= 1
		value += 5828
	else: return -1, -1, -1
		
	X = ((value >> 2) & 0x1F) * 48
	Y = (value >> 7) * 48
	layer = value % 4
	return X, Y, layer

def sort_fun(key):
	return key

files = glob.glob(f"{sys.argv[1]}/*.png")

img1 = Image.new('RGBA', (1536, 3072), (0, 0, 0, 0))
img2 = Image.new('RGBA', (1536, 3072), (0, 0, 0, 0))
img3 = Image.new('RGBA', (1536, 3072), (0, 0, 0, 0))
img4 = Image.new('RGBA', (1536, 3072), (0, 0, 0, 0))

file_count = len(files)

for i in range(len(files)):
	if (Path(files[i]).stem.isnumeric() != True):
		print("Badly named glyph detected! Remove or change name for:\n%s" % files[i])
		sys.exit()
	index = int(Path(files[i]).stem, base=10)
	print(f"File: {i}/{file_count}", end="\r")
	im = Image.open(files[i])

	width, height = im.size

	column_count = int(width / 48)
	row_count = int(height / 48)

	X, Y, layer = CalculatePos(index)
	if (X == -1):
		print("Number %d is not correct!" % index)
		sys.exit()
	match(layer):
		case 0:
			img1.paste(im, (X, Y))
		case 1:
			img2.paste(im, (X, Y))
		case 2:
			img3.paste(im, (X, Y))
		case 3:
			img4.paste(im, (X, Y))

	im.close()

os.makedirs("new_layers", exist_ok=True)
img1.save("new_layers/0.png")
img2.save("new_layers/1.png")
img3.save("new_layers/2.png")
img4.save("new_layers/3.png")