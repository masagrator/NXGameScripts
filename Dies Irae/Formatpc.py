#Python 3 script

extracted = open("extract.txt", "r", encoding='utf-16')

data = extracted.read()
extracted.close()

data = data.replace("\x07\x08", "_voice(\x22")
data = data.replace("", "<pause>")

data = data.replace("\x00", "<NULL>")
data = data.replace("","<Break Line>")
data = data.replace("", "_voiceover();")

for i in range(0, 9999):
    data = data.replace("%s<NULL>" % (str(i).zfill(4)), "%s\x22);" % (str(i).zfill(4)))
    data = data.replace("%sa<NULL>" % (str(i).zfill(4)), "%s\x22);" % (str(i).zfill(4)))
    data = data.replace("%sb<NULL>" % (str(i).zfill(4)), "%s\x22);" % (str(i).zfill(4)))
    
data = data.replace("", "<SPECIAL_CASE_3>")

data = data.replace("\x22_voiceover();", "<Romaji-over-Kanji>")

new = open("new.txt", "w", encoding='utf-16')
new.write(data)
new.close()
