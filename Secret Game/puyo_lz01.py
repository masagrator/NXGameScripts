# Based on QuickBMS source code
# https://github.com/LittleBigBug/QuickBMS/blob/07a65c2555a86a502e9a66a77d06be590ea29a96/src/included/puyo.c
def Decompress(CompressedData, DecompressedSize):
    DestBuffer: list = [0] * 0x1000
    SourcePointer: int = 0
    DestPointer: int = 0
    BufferPointer: int = 0xFEE

    DecompressedBuffer = [0] * DecompressedSize

    CompressedSize = len(CompressedData)

    while (SourcePointer < CompressedSize and DestPointer < DecompressedSize):
        Flag = CompressedData[SourcePointer]
        SourcePointer += 1

        for i in range(8):
            if ((Flag & (1 << i)) > 0): # Data is not compressed
                DecompressedBuffer[DestPointer] = CompressedData[SourcePointer]
                DestBuffer[BufferPointer] = DecompressedBuffer[DestPointer]
                SourcePointer += 1
                DestPointer += 1
                BufferPointer = (BufferPointer + 1) & 0xFFF
            else: # Data is compressed
                Offset = ((((CompressedData[SourcePointer + 1] >> 4) & 0xF) << 8) | CompressedData[SourcePointer])
                Amount = (CompressedData[SourcePointer + 1] & 0xF) + 3
                SourcePointer += 2
                for j in range(Amount):
                    DecompressedBuffer[DestPointer + j] = DestBuffer[(Offset + j) & 0xFFF]
                    DestBuffer[BufferPointer] = DecompressedBuffer[DestPointer + j]
                    BufferPointer = (BufferPointer + 1) & 0xFFF
                DestPointer += Amount
            
            if (SourcePointer >= CompressedSize or DestPointer >= DecompressedSize):
                break

    return bytes(DecompressedBuffer)