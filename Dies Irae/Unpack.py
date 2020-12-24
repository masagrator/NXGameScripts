import numpy

text = open("extract.txt", "w", encoding='shift-jis')
og = open("exec.dat", "rb")

text_offset = 0x389251
table_offset = 0x338CED

og.seek(table_offset, 0)

table_array = numpy.fromfile(og, dtype=numpy.uint32, count=0x14159)

exception = 0
exception2 = 0
exceptionoffset = 0

for i in range(0, 0xA0AC):
    relative_offset = table_array[i*2]
    hard_offset = text_offset + relative_offset
    size = table_array[i*2+1]
    og.seek(hard_offset, 0)
    validation = numpy.fromfile(og, dtype=numpy.uint8, count=size)
    temp_size = size
    for x in range(0, size-1):
        if (validation[x] == 0x87):
            print("detected 0x87")
            if (validation[x+1] == 0x82 or validation[x+1] == 0x95 or validation[x+1] == 0x81):
                continue
            if ((validation[x+1] == 0x55) and (exception != 17) and (exception != 18)):
                exception = 1
            elif ((validation[x+1] == 0x54) and (exception != 17) and (exception != 18)):
                exception = 2
            elif (validation[x+1] == 0x40):
                exception = 3
            elif (validation[x+1] == 0x41):
                exception = 4
            elif (validation[x+1] == 0x42):
                exception = 5
            elif (validation[x+1] == 0x71):
                exception = 6
            elif (validation[x+1] == 0x56):
                exception = 7
            elif (validation[x+1] == 0x5A):
                exception = 8
            elif (validation[x+1] == 0x57):
                exception = 9
            elif (validation[x+1] == 0x58):
                exception = 10
            elif (validation[x+1] == 0x59):
                exception = 11
            elif (validation[x+1] == 0x70):
                exception = 12
            elif (validation[x+1] == 0x5b):
                exception = 13
            elif (validation[x+1] == 0x75):
                exception = 14
            elif (validation[x+1] == 0x5C):
                exception = 15
            elif (validation[x+1] == 0x5D):
                if ((validation[x+2] == 0x87) and (validation[x+3] == 0x54)): exception = 17
                elif ((validation[x+2] == 0x87) and (validation[x+3] == 0x55)): exception = 18
                else: exception = 16
            if (exception > 0):
                print("alarm: %x, offset: 0x%x, iteration: 0x%x, exception: %d" % (validation[x+1], hard_offset, x+1, exception))
                if ((exception == 17) or (exception == 18)): 
                    temp_size = temp_size - (temp_size-x) - 2
                    exceptionoffset = x
                else: 
                    temp_size = temp_size - (temp_size-x)
                    exceptionoffset = x
            else: print("false alarm: %x, offset: 0x%x, iteration: 0x%x" % (validation[x+1], hard_offset, x+1))
    
    og.seek(hard_offset)
    text.write(og.read(temp_size).decode('shift-jis'))
    if (exception == 1):
        text.write(">>0x8755<<")
    elif (exception == 2):
        text.write(">>0x8754<<")
    elif (exception == 3):
        text.write(">>0x8740<<")
    elif (exception == 4):
        text.write(">>0x8741<<")
    elif (exception == 5):
        text.write(">>0x8742<<")
    elif (exception == 6):
        text.write(">>0x8771<<")
    elif (exception == 7):
        text.write(">>0x8756<<")
    elif (exception == 8):
        text.write(">>0x875A<<")
    elif (exception == 9):
        text.write(">>0x8757<<")
    elif (exception == 10):
        text.write(">>0x8758<<")
    elif (exception == 11):
        text.write(">>0x8759<<")
    elif (exception == 12):
        text.write(">>0x8770<<")
    elif (exception == 13):
        text.write(">>0x875B<<")
    elif (exception == 14):
        text.write(">>0x8775<<")
    elif (exception == 15):
        text.write(">>0x875C<<")
    elif (exception == 16):
        text.write(">>0x875D<<")
    elif (exception == 17):
        text.write(">>0x875D<<>>0x8754<<")
    elif (exception == 18):
        text.write(">>0x875D<<>>0x8755<<")
    if (exception > 0):
        if ((exception == 17) or (exception == 18)):
            current_offset = og.tell() + 4
            temp_size = size - exceptionoffset - 2
        else: 
            current_offset = og.tell() + 2
            temp_size = size - exceptionoffset - 2
        og.seek(current_offset, 0)
        text.write(og.read(temp_size).decode('shift-jis'))
        exception = 0
    text.write("\n\n>-NEW LINE-<\n\n")

text.close()