import re
class bagrule:
	def __init__(self, color, contains):
		self.color = color
		self.contains = contains

ruleset = []
with open(r'.\Day7\input.txt') as thefile:
	for line in thefile:
		thisbagcolor = (re.match(r'.+(?= bags contain)', line).group())
		thisbagcontains = re.findall(r'(\d)\s([a-z\s]+)(?= bag(?:s?))', line)
		ruleset.append(bagrule(thisbagcolor, thisbagcontains))


def icontain(ruleset, bagcolor):
	contentscount = 0
	thisbag = next((x for x in ruleset if x.color == bagcolor), None)
	for i in thisbag.contains:
		print(i)
		contentscount += int(i[0]) #index 0 of the contains list should be the number contained
		contentscount += int(i[0]) * icontain(ruleset, i[1])
	return contentscount

print(icontain(ruleset, 'shiny gold'))