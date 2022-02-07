import os

Texts = [
	"MAIN",
	"CC_30A",
	"CC0TOU",
	"CC1MIS",
	"CC2KIR",
	"CC3MIK",
	"CC4YOU",
	"CC5TOM",
	"CC6SAK",
	"CCA0001",
	"CCA0002",
	"CCA0003",
	"CCA0004",
	"CCA0005A",
	"CCA0005B",
	"CCA0006",
	"CCA0007",
	"CCA0008",
	"CCA0009A",
	"CCA0009B",
	"CCA0009C",
	"CCA0010",
	"CCA0011A",
	"CCA0011B",
	"CCA0011C",
	"CCA0012",
	"CCA0013",
	"CCA0014A",
	"CCA0014B",
	"CCA0015",
	"CCA0016",
	"CCA0017A",
	"CCA0017B",
	"CCA0018",
	"CCA0019",
	"CCA0020",
	"CCA0021",
	"CCA0022",
	"CCA0023",
	"CCA0024",
	"CCA0025A",
	"CCA0025B",
	"CCA0025C",
	"CCA0025D",
	"CCA0026",
	"CCA0027",
	"CCA0028",
	"CCA0029",
	"CCA0030",
	"CCB0001",
	"CCB0002",
	"CCB0003",
	"CCB0004B",
	"CCB0004C",
	"CCB0005",
	"CCB0006",
	"CCB0007",
	"CCB0008A",
	"CCB0008B",
	"CCB0009",
	"CCB0010A",
	"CCB0010B", # Not Used accoring to debug menu
	"CCB0011",
	"CCB0012",
	"CCB0013",
	"CCB0014",
	"CCB0015B",
	"CCB0015C",
	"CCB0016",
	"CCB0017",
	"CCB0018",
	"CCB0019",
	"CCB0020",
	"CCB0021",
	"CCB0022",
	"CCB0023",
	"76",
	"CCB1001",
	"CCB1002A",
	"CCB1002B",
	"CCB1003",
	"CCB1004",
	"CCB1005",
	"CCB1006",
	"CCB1007A",
	"CCB1007B",
	"CCB1008",
	"CCB1009",
	"CCB1010",
	"CCB1011",
	"CCB1012",
	"CCB1013",
	"CCB1014A",
	"CCB1014B",
	"CCB1014C",
	"CCB1014D",
	"CCB1015",
	"CCB1016",
	"CCB1017", # Not Used accoring to debug menu
	"CCB1101", # Not Used accoring to debug menu
	"CCB1102",
	"CCB2001",
	"CCB2002",
	"CCB2003A",
	"CCB2003B", # Not Used accoring to debug menu
	"CCB2005",
	"CCB2006",
	"CCB2007",
	"CCB2008",
	"CCB2009",
	"CCB2010",
	"CCB2011",
	"CCB2012",
	"CCB2013",
	"CCB2014",
	"CCB2015",
	"CCB2016",
	"CCB2017",
	"CCB2018", # Not Used accoring to debug menu
	"CCB2019",
	"CCB2020",
	"CCB2021",
	"CCB2101",
	"CCB2102",
	"CCC0000",
	"CCC0001",
	"CCC0002",
	"CCC0003A",
	"CCC0003B",
	"CCC0004A",
	"CCC0004B",
	"CCC0005",
	"CCC0006A",
	"CCC0006B",
	"CCC0006C",
	"CCC0006D",
	"CCC0007",
	"CCC0008A",
	"CCC0008B",
	"CCC0009",
	"CCC0010A",
	"CCC0010B",  # Not Used accoring to debug menu
	"CCC0011A",
	"CCC0011B",
	"CCC0011C",
	"CCC0013A",
	"CCC0013B",
	"CCC0014",
	"CCC0015",
	"CCC0016A",
	"CCC0016B",
	"CCC0017",
	"CCC0018A",
	"CCC0018B",
	"CCC0019",
	"CCC0020",
	"CCC0021",
	"CCC0022",
	"CCC0023A",
	"CCC0023B",
	"CCC0024",
	"CCC0025",
	"CCC0026",
	"CCC0027",
	"CCC0028",
	"CCC0029A",
	"CCC0029B",
	"CCC0029C",
	"CCC0030",
	"CCC0031A",
	"CCC0031B",
	"CCC0031C",
	"CCC0032",
	"CCC0033A",
	"CCC0033B",
	"CCC0034",
	"CCC0035A",
	"CCC0035B",
	"CCC0036A",
	"CCC0036B",
	"CCC0037",
	"CCC0038A",
	"CCC0038B",
	"CCC0039",
	"CCC0040",
	"CCC0041",
	"CCC0042",
	"CCC0043",
	"CCC0044",
	"CCC0045A",
	"CCC0045B",
	"CCC0101",
	"CCC3001",
	"CCC3002",
	"CCC3003",
	"CCC3004",
	"CCC3005",
	"CCC3006",
	"CCC3007",
	"CCC3008",
	"CCC3009",
	"CCC3010",
	"CCC3011",
	"CCC3012A",
	"CCC3012B",
	"CCC3013",
	"CCC3014",
	"CCC3015",
	"CCC3016",
	"CCC3017",
	"CCC3018",
	"CCC3019A",
	"CCC3019B",
	"CCC3020",
	"CCC3021",
	"CCC3022",
	"CCC3023",
	"CCC3024",
	"CCC3025",
	"CCC3026",
	"CCC3027",
	"CCC3028",
	"CCC3029",
	"CCC3030",
	"CCC4001",
	"CCC4002",
	"CCC4003",
	"CCC4004",
	"CCC4005",
	"CCC4006",
	"CCC4007",
	"CCC4008",
	"CCC4009",
	"CCC4010",
	"CCC4011",
	"CCC4012",
	"CCC4013", # Not Used accoring to debug menu
	"CCC4014",
	"CCC4015",
	"CCC4016",
	"CCC4017",
	"CCC4018",
	"CCC4019",
	"CCC4020",
	"CCC4021",
	"CCC4022",
	"CCC4023",
	"CCC4024",
	"CCC4025",
	"CCD0001",
	"CCD0002",
	"CCD0003",
	"CCD0004",
	"CCD0005A",
	"CCD0005B", # Not Used accoring to debug menu
	"CCD0005C",
	"CCD0006",
	"CCD0007",
	"CCD0008A",
	"CCD0008B",
	"CCD0008C",
	"CCD0008D",
	"CCD0008E",
	"CCD0009",
	"CCD0010",
	"265",
	"CCD0012",
	"CCD0013",
	"CCD0014A",
	"CCD0014B",
	"CCD0014C",
	"CCD0015A",
	"CCD0015B",
	"CCD0016A",
	"CCD0016B",
	"CCD0017",
	"CCD0018",
	"CCD0019",
	"CCD0020A",
	"CCD0020B",
	"CCD0020C",
	"CCD0021",
	"CCD0022A",
	"CCD0022B",
	"CCD0023",
	"CCD0101",
	"CCD0102",
	"CCD0201",
	"CCD1001A",
	"CCD1001B",
	"CCD1001C",
	"CCD1001D",
	"CCD2001",
	"CCD2002A",
	"CCD2002B",
	"CCD3001",
	"CCD3002A",
	"CCD3002B",
	"CCD3003A",
	"CCD3003B",
	"CCD3003C",
	"CCD3003D",
	"CCD3099",
	"CCD4001",
	"CCD4002A",
	"CCD4002B",
	"CCD4003A",
	"CCD4003B", # Not Used accoring to debug menu
	"CCD5001A",
	"CCD5001B",
	"CCD6001",
	"CCE0001",
	"312",
	"CCX0001",
	"314",
	"315"
]

for i in range(1, 316):
	try:
		os.rename("Text_extracted/%s.json" % Texts[i], "Text_extracted/%04d.json" % i)
	except:
		pass