import re

FILENAME = r'.\Day19\testinput.txt'

with open(FILENAME) as thefile:
	rawdata = thefile.read().strip().split('\n\n')
#rawdata will have [ruleset, messages]

class ruleset:
	def __init__(self, rulesetraw):

		self.rulesetraw = rulesetraw.split('\n')
		self.numrules = len(self.rulesetraw)
		self.revref = [set() for _ in range(self.numrules)] ##we will be able to look up all references to a particular index in ruleset. will init in readindata
		
		#init ruleset
		self.ruleset = []
		self._readindata(self.rulesetraw)
		

	
	def _readindata(self, rulesetraw):

		refregp = r'(\d): ([\d ]+)(?:\|([\d ]+))?'
		letregp = r'(\d): "([ab])"'
		for line in rulesetraw:
			match = re.match(refregp, line)
			if match:
				matchnum = int(match.group(1))
				matchset1 = [int(x) for x in match.group(2).strip().split(' ')]
				for n in matchset1:
					self.revref[n].add(matchnum) #add references to matchnum
				try:
					matchset2 = [int(x) for x in match.group(3).strip().split(' ')]
					for n in matchset2:
						self.revref[n].add(matchnum) #add references to matchnum
				except:
					matchset2 = None
				self.ruleset.append([matchnum, matchset1, matchset2])
			else:
				match = re.match(letregp, line)
				try:
					matchnum = int(match.group(1))
					matchlet = match.group(2)
					self.ruleset.append([matchnum, matchlet])
				except:
					print("Failed to parse: " + line)
		


myruleset = ruleset(rawdata[0])

for rule in myruleset.ruleset:
	print(rule)

print(myruleset.revref)
print(myruleset.numrules)