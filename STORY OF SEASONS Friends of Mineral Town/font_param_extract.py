# STORY OF SEASONS: Friends of Mineral Town font's character table data extractor from *param.bin files
# Generated file is compliant with tsv format which you can import to any program using sheets like Google Sheets or LibreOffice Calc
# For fonts with thousands of characters it can take more than 5 minutes to finish
# Python 3 script
# Author: MasaGratoR @ 2020

import numpy

mainfile = 'SHORHB___param.bin'

param = open(mainfile, 'rb')
paramtxt = open('%s.tsv' % (mainfile), 'w', encoding='utf-16-le')
paramtxt.write('ID\tsign\tUTF-16 hex\tpos x\tpos y\twidth\theight\tunk1\ty shift\tright margin\n')

buffer = numpy.fromfile(param, dtype=numpy.uint16, count=0x10000)

param.seek(0,2)
size = param.tell()
table_offset = size - (size - 0x20000)

for i in range (0, len(buffer)):
    if (buffer[i] != 0xFFFF):
        paramtxt.write(str(buffer[i]))
        paramtxt.write('\t')
        if (i == 0): string = 'NUL'
        elif (i == 1): string = 'SOH'
        elif (i == 2): string = 'STX'
        elif (i == 3): string = 'ETX'
        elif (i == 4): string = 'EOT'
        elif (i == 5): string = 'ENQ'
        elif (i == 6): string = 'ACK'
        elif (i == 7): string = 'BEL'
        elif (i == 8): string = 'BS'
        elif (i == 9): string = 'TAB'
        elif (i == 10): string = 'LF'
        elif (i == 11): string = 'VT'
        elif (i == 12): string = 'FF'
        elif (i == 13): string = 'CR'
        elif (i == 14): string = 'SO'
        elif (i == 15): string = 'SI'
        elif (i == 16): string = 'DLE'
        elif (i == 17): string = 'DC1'
        elif (i == 18): string = 'DC2'
        elif (i == 19): string = 'DC3'
        elif (i == 20): string = 'DC4'
        elif (i == 21): string = 'NAK'
        elif (i == 22): string = 'SYN'
        elif (i == 23): string = 'ETB'
        elif (i == 24): string = 'CAN'
        elif (i == 25): string = 'EM'
        elif (i == 26): string = 'SUB'
        elif (i == 27): string = 'ESC'
        elif (i == 28): string = 'FS'
        elif (i == 29): string = 'GS'
        elif (i == 30): string = 'RS'
        elif (i == 31): string = 'US'
        elif (i == 34): string = "Quotation mark"
        elif (i == 36): string = "Dollar sign"
        else: string = chr(i)
        print(string)
        paramtxt.write(string)
        paramtxt.write('\t')
        paramtxt.write('0x%x' % (i))
        paramtxt.write('\t')
        compare = 0
        table_offset_temp = table_offset - 0xC
        if (i == 0): paramtxt.write('NULL\tNULL\tNULL\tNULL\tNULL\tNULL\tNULL\n')
        else:
            while (compare != i):
                table_offset_temp = table_offset_temp + 0xC
                param.seek(table_offset_temp,0)
                temp = numpy.fromfile(param, dtype=numpy.uint16, count=1)
                compare = temp[0]
            param.seek(table_offset_temp+0x2)
            posx = numpy.fromfile(param, dtype=numpy.uint16, count=1)
            paramtxt.write('%d' % (posx[0]))
            paramtxt.write('\t')
            posy = numpy.fromfile(param, dtype=numpy.uint16, count=1)
            paramtxt.write('%d' % (posy[0]))  
            paramtxt.write('\t')
            width = numpy.fromfile(param, dtype=numpy.uint8, count=1)
            paramtxt.write('%d' % (width[0]))  
            paramtxt.write('\t')
            height = numpy.fromfile(param, dtype=numpy.uint8, count=1)
            paramtxt.write('%d' % (height[0]))  
            paramtxt.write('\t')
            unk1 = numpy.fromfile(param, dtype=numpy.int8, count=1)
            paramtxt.write('%d' % (unk1[0]))  
            paramtxt.write('\t')
            unk2 = numpy.fromfile(param, dtype=numpy.uint8, count=1)
            paramtxt.write('%d' % (unk2[0]))  
            paramtxt.write('\t')
            unk3 = numpy.fromfile(param, dtype=numpy.uint16, count=1)
            paramtxt.write('%d' % (unk3[0]))  
            paramtxt.write('\n')
paramtxt.close()
