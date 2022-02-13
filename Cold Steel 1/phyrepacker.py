from wand import image
import glob
import os
import sys

def SortElem(elem):
    return elem

files = glob.glob("UNPACKED/*/*.png.header")
files += glob.glob("UNPACKED/*/*.dds.header")
files.sort(key=SortElem)

os.makedirs("REPACKED", exist_ok=True)

for i in range(0, len(files)):
    print(files[i][9:])
    file = open(files[i], "rb")
    file.seek(0, 2)
    if (files[i][-10:-7] == "png"):
        file.seek((0x43) * -1, 1)
    else:
        file.seek((0x42) * -1, 1)
    width = int.from_bytes(file.read(4), byteorder="little")
    height = int.from_bytes(file.read(4), byteorder="little")
    file.seek(0, 2)
    if (files[i][-10:-7] == "png"):
        file.seek((0x4C) * -1, 1)
    else:
        file.seek((0x4B) * -1, 1)
    mipmaps = int.from_bytes(file.read(1), byteorder="little")
    file.seek(0x20, 1)
    type = file.read(4).decode("ASCII")
    if (type == "RGBA"): type = "no"
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
    blob = blob[0x80:]
    if (type == "no"):
        new_blob = []
        print("Repacking from BGRA to RGBA... Please wait a while.")
        for x in range(0, int(len(blob) / 4)):
            new_blob.append(blob[2+(4*x):3+(4*x)])
            new_blob.append(blob[1+(4*x):2+(4*x)])
            new_blob.append(blob[0+(4*x):1+(4*x)])
            new_blob.append(blob[3+(4*x):4+(4*x)])
        file.write(b"".join(new_blob))
    else:
        file.write(blob)
    file.close()