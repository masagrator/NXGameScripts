from wand import image
import glob
import os
import sys

files = glob.glob("UNPACKED/*/*.dds.header")
files = glob.glob("UNPACKED/*/*.png.header")

os.makedirs("REPACKED", exist_ok=True)

for i in range(0, len(files)):
    print(files[i][9:])
    file = open(files[i], "rb")
    file.seek(0, 2)
    file.seek((0x42) * -1, 1)
    width = int.from_bytes(file.read(4), byteorder="little")
    height = int.from_bytes(file.read(4), byteorder="little")
    file.seek(0, 2)
    file.seek((0x4A) * -1, 1)
    mipmaps = int.from_bytes(file.read(1), byteorder="little")
    file.seek(0x1F, 1)
    type = file.read(4).decode("ASCII")
    file.seek(0, 0)
    header = file.read()
    file.close()

    print(width)
    print(height)
    img = image.Image(filename="%s.png" % files[i][:-11])
    if (img.width != width):
        print("PNG width is wrong!")
        print("EXPECTED: %d px, GOT: %d px" % (width, img.width))
        sys.exit()
    elif (img.height != height):
        print("PNG height is wrong!")
        print("EXPECTED: %d px, GOT: %d px" % (height, img.height))
        sys.exit()
    
    img.flip()
    img.compression = type.lower()
    img.format = "dds"
    print(mipmaps)
    img.options['dds:mipmaps'] = "%d" % mipmaps
    blob = img.make_blob()
    img.close()

    os.makedirs("REPACKED/%s" % os.path.dirname(files[i][9:]), exist_ok=True)
    file = open("REPACKED/%s.phyre" % files[i][9:-7], "wb")
    file.write(header)
    if (type == "RGBA"):
        file.write(blob[0x94:])
    else:
        file.write(blob[0x80:])
    file.close()