new = open("new.txt", "r", encoding='shift-jis', newline='')
data = new.read()
new.close()

data = data.replace("<SPECIAL_CASE_3>", "")

for i in range(0, 99):
    data = data.replace("%sb\x22);" % (str(i).zfill(2)), "%sb<NULL>" % (str(i).zfill(2)))
    data = data.replace("%sa\x22);" % (str(i).zfill(2)), "%sa<NULL>" % (str(i).zfill(2)))
    data = data.replace("%s\x22);" % (str(i).zfill(2)), "%s<NULL>" % (str(i).zfill(2)))
    data = data.replace("%s_ef\x22);" % (str(i).zfill(2)), "%s_ef<NULL>" % (str(i).zfill(2)))
    data = data.replace("%s_a\x22);" % (str(i).zfill(2)), "%s_a<NULL>" % (str(i).zfill(2)))

data = data.replace("_voiceover();","")
data = data.replace("<Break Line>","")
data = data.replace("<NULL>","\x00")
data = data.replace("<Romaji-over-Kanji_start>", "\x0A")

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