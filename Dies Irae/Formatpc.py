#Python 3 script

extracted = open("extract.txt", "r", encoding='utf-16')

data = extracted.read()
extracted.close()

data = data.replace("\x07\x08", "_voice(\x22")
data = data.replace("", "<pause>")

data = data.replace("\x00", "<NULL>")
data = data.replace("","<Break Line>")
data = data.replace("", "<Romaji-over-Kanji>")
data = data.replace("", "<i>")
data = data.replace("", "</i>")
data = data.replace("", "_voiceover();")

for i in range(0, 99):
    data = data.replace("%s<NULL>" % (str(i).zfill(2)), "%s\x22);" % (str(i).zfill(2)))
    data = data.replace("%sa<NULL>" % (str(i).zfill(2)), "%sa\x22);" % (str(i).zfill(2)))
    data = data.replace("%sb<NULL>" % (str(i).zfill(2)), "%sb\x22);" % (str(i).zfill(2)))
    data = data.replace("%s_ef<NULL>" % (str(i).zfill(2)), "%s_ef\x22);" % (str(i).zfill(2)))
    data = data.replace("%s_a<NULL>" % (str(i).zfill(2)), "%s_a\x22);" % (str(i).zfill(2)))

new = open("newpc.txt", "w", encoding='utf-16')
new.write(data)
new.close()
