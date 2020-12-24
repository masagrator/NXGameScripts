import numpy

translation = open("reformatted.txt", 'r', encoding='shift-jis', newline='')
data = translation.read()
translation.close()
data = data.replace(">>0x875D<<", "\x87\x5d")
data = data.replace(">>0x8755<<", "\x87\x55")
data = data.replace(">>0x875C<<", "\x87\x5C")
data = data.replace(">>0x8775<<", "\x87\x75")
data = data.replace(">>0x875B<<", "\x87\x5B")
data = data.replace(">>0x8770<<", "\x87\x70")
data = data.replace(">>0x8759<<", "\x87\x59")
data = data.replace(">>0x8758<<", "\x87\x58")
data = data.replace(">>0x8757<<", "\x87\x57")
data = data.replace(">>0x875A<<", "\x87\x5A")
data = data.replace(">>0x8756<<", "\x87\x56")
data = data.replace(">>0x8771<<", "\x87\x71")
data = data.replace(">>0x8742<<", "\x87\x42")
data = data.replace(">>0x8741<<", "\x87\x41")
data = data.replace(">>0x8740<<", "\x87\x40")
data = data.replace(">>0x8754<<", "\x87\x54")
texts = data.split("\n\n>-NEW LINE-<\n\n", -1)
offset = 0;
offset_table = open("temp1.txt", "wb")
text_table = open("temp2.txt", "wb")

exception = 0

for i in range(0, len(texts)-1):
    if (offset == 0x2C927B): print (texts[i])
    offset_table.write(numpy.uint32(offset))
    tempbuffer = texts[i]
    temp_size = len(tempbuffer)
    tempbuffer = tempbuffer.replace("\x87\x55", "$#").replace("\x87\x54", "$%").replace("\x87\x40", "$&").replace("\x87\x41", "$;").replace("\x87\x42", "$(").replace("\x87\x71", "$)").replace("\x87\x56", "$*").replace("\x87\x5A", "$+").replace("\x87\x57", "$-").replace("\x87\x58", "$/").replace("\x87\x59", "$:").replace("\x87\x70", "$<").replace("\x87\x5b", "$>").replace("\x87\x75", "$=").replace("\x87\x5C", "$@").replace("\x87\x5D", "$^")
    temp_size = len(tempbuffer.encode('shift-jis'))
    offset_table.write(numpy.uint32(len(tempbuffer.encode('shift-jis'))))
    text_table.write(tempbuffer.encode('shift-jis').replace(b'$^', b'\x87\x5D').replace(b'$@', b'\x87\x5C').replace(b'$=', b'\x87\x75').replace(b'$>', b'\x87\x5b').replace(b'$<', b'\x87\x70').replace(b'$:', b'\x87\x59').replace(b'$/', b'\x87\x58').replace(b'$-', b'\x87\x57').replace(b'$+', b'\x87\x5A').replace(b'$*', b'\x87\x56').replace(b'$)', b'\x87\x71').replace(b'$(', b'\x87\x42').replace(b'$;', b'\x87\x41').replace(b'$&', b'\x87\x40').replace(b'$%', b'\x87\x54').replace(b'$#', b'\x87\x55'))
    text_table.write(numpy.uint8(0x0))
    offset = offset + temp_size + 1

offset_table.write(numpy.uint32(offset))
offset_table.close()
text_table.close()
offset_table = open("temp1.txt", "rb")
text_table = open("temp2.txt", "rb")
execdata = open("exec.dat", "rb")
result = open("result.dat", "wb")
result.write(execdata.read(0x338CED))
result.write(offset_table.read())
result.write(text_table.read())
offset_table.close()
text_table.close()
result.close()