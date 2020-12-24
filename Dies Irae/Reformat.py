new = open("new.txt", "r", encoding='shift-jis', newline='')
data = new.read()
new.close()

data = data.replace("<SPECIAL_CASE_3>", "")

for i in range(0, 9999):
    data = data.replace("%sb\x22);" % (str(i).zfill(4)), "%s<NULL>" % (str(i).zfill(4)))
    data = data.replace("%sa\x22);" % (str(i).zfill(4)), "%s<NULL>" % (str(i).zfill(4)))
    data = data.replace("%s\x22);" % (str(i).zfill(4)), "%s<NULL>" % (str(i).zfill(4)))

data = data.replace("_voiceover();","")
data = data.replace("<Break Line>","")
data = data.replace("<NULL>","\x00")

for i in range(0xFF65, 0xFF9F):
    data = data.replace("<Romaji-over-Kanji_start>%s" % (chr(i)), "\x0A%s" % (chr(i)))
    data = data.replace("<Romaji-over-Kanji_start> %s" % (chr(i)), "\x0A %s" % (chr(i)))
    
for i in range(0x32D0, 0x32FE):
    data = data.replace("<Romaji-over-Kanji_start>%s" % (chr(i)), "\x0A%s" % (chr(i)))
    data = data.replace("<Romaji-over-Kanji_start> %s" % (chr(i)), "\x0A %s" % (chr(i)))

for i in range(0x3001, 0x30FE):
    data = data.replace("<Romaji-over-Kanji_start>%s" % (chr(i)), "\x0A%s" % (chr(i)))
    data = data.replace("<Romaji-over-Kanji_start> %s" % (chr(i)), "\x0A %s" % (chr(i)))

data = data.replace("<pause>", "")
data = data.replace("<Romaji-over-Kanji>", "")
data = data.replace("\x22);『", "\x00『")
data = data.replace("\x22);「", "\x00「")
data = data.replace("_voice(\x22", "\x07\x08")
data = data.replace("<SPECIAL CASE>", "\r")
data = data.replace("<SPECIAL_CASE_2>", "")

reformatted = open("reformatted.txt", "w", encoding='shift-jis', newline='')
reformatted.write(data)
reformatted.close()