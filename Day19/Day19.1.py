import re

FILENAME = r'.\Day19\testinput.txt'

with open(FILENAME) as thefile:
	rawdata = thefile.read().strip().split('\n\n')
#rawdata will have [ruleset, messages]

class ruleset:
	def __init__(self, rulesetraw):
		#init ruleset
		self.ruleset = []
		self._readindata(rulesetraw)
	
	def _readindata(self, rulesetraw):
		rulesetraw = rulesetraw.split()
		refregp = r'(\d): ([\d ]+)(?:\|([\d ]+))?'
		letregp = r'(\d): "([ab])"'
		for line in rulesetraw:
			match = re.match(refregp, line)
			if match:
				matchnum = int(match.group(1))
				matchset1 = [int(x) for x in match.group(2).strip().split(' ')]
				try:
					matchset2 = [int(x) for x in match.group(3).strip().split(' ')]
				except:
					matchset2 = None
				ruleset.append([matchnum, matchset1, matchset2])
			else:
				match = re.match(letregp, line)
				try:
					matchnum = int(match.group(1))
					matchlet = match.group(2)
					ruleset.append([matchnum, matchlet])
				except:
					print("Failed to parse: " + line)
		


myruleset = ruleset(rawdata[0])
