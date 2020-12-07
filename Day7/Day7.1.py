import re
class bagrule:
	def __init__(self, bagcolor, contains):
		self.color = bagcolor
		self.contains = contains

def findcancontain(ruleset, checkcolor):
	cancontainme = []
	for i in ruleset:
		if(checkcolor in (x[1] for x in i.contains)):
			cancontainme.append(i.color)
			for y in findcancontain(ruleset, i.color):
				cancontainme.append(y)

	return cancontainme

	

ruleset = []
with open(r'.\Day7\input.txt') as thefile:
	for line in thefile:
		thisbagcolor = (re.match(r'.+(?= bags contain)', line).group())
		thisbagcontains = re.findall(r'(\d)\s([a-z\s]+)(?= bag(?:s?))', line)
		ruleset.append(bagrule(thisbagcolor, thisbagcontains))


cancontaingold = findcancontain(ruleset, 'shiny gold')

print len(set(cancontaingold))

