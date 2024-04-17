from PIL import Image
import sys
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

os.makedirs("Splitted", exist_ok=True)

for i in range(4):
	print(f"Layer {i}")
	im = Image.open(f"{i}.png")

	width, height = im.size

	column_count = int(width / 48)
	row_count = int(height / 48)

	for y in range(row_count):
		for x in range(column_count):
			im1 = im.crop((x * 48, y * 48, (x + 1) * 48, (y + 1) * 48))
			info = (x*48, y*48, i)
			index = 0
			for iter in range(0x20, 0xFC4C):
				if (iter > 0x7F and iter < 0x8140):
					continue
				X, Y, layer = CalculatePos(iter)
				new_info = (X, Y, layer)
				if (info == new_info):
					index = iter
					break
			if (index == 0):
				print("Failed! X: %d, Y: %d, layer: %d" % (info[0], info[1], info[2]))
				sys.exit()
			im1.save("Splitted/%05d.png" % (index))

	im.close()