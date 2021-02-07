# Original algorithm by gdkchan
# Ported and improved (a tiny bit) by Stella/AboodXD
# Small changes by MasaGratoR

import sys

BCN = {71, 74, 77, 95, 98}

FORMATS =   {   "RGBA8": 28,
                "R8": 61,
                "A8": 65,
                "BC1": 71,
                "DXT1": 71,
                "BC2": 74,
                "DXT3": 74,
                "BC3": 77,
                "DXT5": 77,
                "BGRA8": 87,
                "BC6H": 95,
                "BC7": 98
                }

bpps = {    28: 4,
            61: 1,
            71: 8,
            74: 16,
            77: 16,
            87: 4,
            95: 16,
            98: 16
            }

xBases = {  1: 4,
            2: 3,
            4: 2,
            8: 1,
            16: 0
            }

padds = {   1: 64,
            2: 32,
            4: 16,
            8: 8,
            16: 4
            }


def roundSize(size, pad):
    mask = pad - 1
    if size & mask:
        size &= ~mask
        size +=  pad

    return size


def pow2RoundUp(v):
    v -= 1

    v |= (v+1) >> 1
    v |= v >>  2
    v |= v >>  4
    v |= v >>  8
    v |= v >> 16

    return v + 1


def isPow2(v):
    return v and not v & (v - 1)


def countZeros(v):
    numZeros = 0

    for i in range(32):
        if v & (1 << i):
            break

        numZeros += 1

    return numZeros


def deswizzle(width, height, format_, data):
    pos_ = 0

    bpp = bpps[format_]

    origin_width = width
    origin_height = height

    if format_ in BCN:
        origin_width = (origin_width + 3) & ~3
        origin_height = (origin_height + 3) & ~3

    xb = countZeros(pow2RoundUp(origin_width))
    yb = countZeros(pow2RoundUp(origin_height))

    hh = pow2RoundUp(origin_height) >> 1;

    if not isPow2(origin_height) and origin_height <= hh + hh // 3 and yb > 3:
        yb -= 1

    width = roundSize(origin_width, padds[bpp])

    result = bytearray(data)

    xBase = xBases[bpp]

    for y in range(origin_height):
        for x in range(origin_width):
            pos = getAddr(x, y, xb, yb, width, xBase) * bpp

            if pos_ + bpp <= len(data) and pos + bpp <= len(data):
                result[pos_:pos_ + bpp] = data[pos:pos + bpp]

            pos_ += bpp

    return result


def swizzle(width, height, format_, data):
    pos_ = 0

    bpp = bpps[format_]

    origin_width = width
    origin_height = height

    if format_ in BCN:
        origin_width = (origin_width + 3) & ~3
        origin_height = (origin_height + 3) & ~3

    xb = countZeros(pow2RoundUp(origin_width))
    yb = countZeros(pow2RoundUp(origin_height))

    hh = pow2RoundUp(origin_height) >> 1;

    if not isPow2(origin_height) and origin_height <= hh + hh // 3 and yb > 3:
        yb -= 1

    width = roundSize(origin_width, padds[bpp])

    result = bytearray(data)

    xBase = xBases[bpp]

    for y in range(origin_height):
        for x in range(origin_width):
            pos = getAddr(x, y, xb, yb, width, xBase) * bpp

            if pos + bpp <= len(data) and pos_ + bpp <= len(data):
                result[pos:pos + bpp] = data[pos_:pos_ + bpp]

            pos_ += bpp

    return result


def getAddr(x, y, xb, yb, width, xBase):
    xCnt    = xBase
    yCnt    = 1
    xUsed   = 0
    yUsed   = 0
    address = 0

    while (xUsed < xBase + 2) and (xUsed + xCnt < xb):
        xMask = (1 << xCnt) - 1
        yMask = (1 << yCnt) - 1

        address |= (x & xMask) << xUsed + yUsed
        address |= (y & yMask) << xUsed + yUsed + xCnt

        x >>= xCnt
        y >>= yCnt

        xUsed += xCnt
        yUsed += yCnt

        xCnt = max(min(xb - xUsed, 1), 0)
        yCnt = max(min(yb - yUsed, yCnt << 1), 0)

    address |= (x + y * (width >> xUsed)) << (xUsed + yUsed)

    return address


if (len(sys.argv) != 6 and len(sys.argv) != 8): raise ValueError("Wrong command.\nSwizzler.py [de]swizzle image.raw width_dec height_dec format_str_short (start_offset_hex, size_dec)")

file = open(sys.argv[2], "rb")
buffer = file.read()
file.close()

start_offset = 0
size = 0

if (len(sys.argv) == 8):
    file = open(sys.argv[2], "rb")
    start_offset = int(sys.argv[6], 16)
    file.seek(start_offset)
    size = int(sys.argv[7])
    if (size == 0): buffer = file.read()
    else: buffer = file.read(size)
    file.close()

if (sys.argv[1] == "swizzle"):
    data = swizzle(int(sys.argv[3]), int(sys.argv[4]), FORMATS[sys.argv[5]], buffer)
    file = open("result.dat", "wb")
    file.write(data)
    file.close()

elif (sys.argv[1] == "deswizzle"):
    data = deswizzle(int(sys.argv[3]), int(sys.argv[4]), FORMATS[sys.argv[5]], buffer)
    file = open("result.dat", "wb")
    file.write(data)
    file.close()
