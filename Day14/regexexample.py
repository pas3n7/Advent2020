# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

# mask = ([01X]{36})(?:\nmem\[(?P<maddr0>\d+)\] = (?P<data0>\d+))?(?:\nmem\[(?P<maddr1>\d+)\] = (?P<data1>\d+))?


import re

#regex = r"(mask.+(?:\n.+)+?)(?=\nmask|$)"

regex = r'mask = ([01X]{36})' + ''.join([r'(?:\nmem\[(?P<maddr' + str(i) + r'>\d+)\] = (?P<data' + str(i) + r'>\d+))?'  for i in range(5)])

test_str = ("mask = 01111X0011X11110XX11X110111001X00001\n"
	"mem[26252] = 2785\n"
	"mem[5529] = 156\n"
	"mem[43194] = 29224\n"
	"mem[64799] = 11208\n"
	"mem[1727] = 138064713\n"
	"mem[51786] = 67480\n"
	"mask = 00010000011011101X0000X001X01001X0X0\n"
	"mem[8820] = 143936540\n"
	"mem[33783] = 33161\n"
	"mem[60979] = 17936311\n"
	"mem[19136] = 48558314\n"
	"mem[55023] = 718791450\n"
	"mem[1315] = 258018313\n"
	"mem[1093] = 104780852\n"
	"mask = 10111X1000X0001XX11011X11X0011100X00\n"
	"mem[31605] = 115835374\n"
	"mem[50005] = 5\n"
	"mask = 1X011000XX101X101X0011100010X0100001\n"
	"mem[42546] = 58538740\n"
	"mem[42808] = 3851323\n"
	"mem[54043] = 1022\n"
	"mem[45712] = 43197369\n"
	"mem[10795] = 2548035\n"
	"mem[57363] = 1159\n"
	"mem[54202] = 412819")

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
