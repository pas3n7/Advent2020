import re
from collections import defaultdict
fn = r'.\Day21\input.txt'
#fn = r'.\Day21\testinput.txt'

with open(fn) as thefile:
	rawdata = thefile.read().strip().split("\n")

justallergens = [re.search(r"\(contains (.+)\)", x).group(1) for x in rawdata]
justfoods = [re.match(r'.+(?= \()', x).group() for x in rawdata]

allergenlist = set([aler for alerline in justallergens for aler in alerline.split(", ")])
foodslist = set([food for foodline in justfoods for food in foodline.split(" ")])

lines = []
for line in rawdata:
	thisline = line.split(' (contains ')
	thisline = thisline[0].split(' '), thisline[1].strip(')').split(', ')
	lines.append(thisline)

lines.sort(key= lambda x: len(x[0]))

allergencantbein = defaultdict(set)

for line in lines:
	for allergen in line[1]:
		allergencantbein[allergen].update([food for food in foodslist if food not in line[0]])


possiblelist = []

for allergen in list(allergencantbein.items()):
	possiblelist.append([allergen[0], foodslist.difference(allergen[1])])


print(possiblelist)
knownlist = []
i = 0
while len(possiblelist) > 0 and i < 3000:
	knownlistnew = [al for al in possiblelist if len(al[1]) == 1] #add any currently known to knownlist
	knownlist.extend(knownlistnew)
	possiblelist = [pl for pl in possiblelist if len(pl[1])> 1] #remove any currently known from possiblelist
	for new in knownlistnew:
		for pos in possiblelist:
			pos[1].difference_update(new[1])
	# possiblelist = [[p[0], p[1].difference(x)] for p in possiblelist for x in [new[1] for new in knownlistnew]]
	print(len(possiblelist), end='\r')
	i += 1

	
print(knownlist)

allknown = set().union(*[known[1] for known in knownlist])

unknownlist = foodslist.difference(allknown)

print(unknownlist)

print(sum([[food for foodline in justfoods for food in foodline.split(" ")].count(x) for x in unknownlist]))

print(','.join([known[1].pop() for known in sorted(knownlist)]))