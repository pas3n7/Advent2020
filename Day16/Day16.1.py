import re
with open(r'.\Day16\input.txt') as thefile:
	rawfiledata = thefile.read().strip().split('\n\n')


ruledata = rawfiledata[0].split("\n")
myticket = rawfiledata[1].split("\n")[1]
NUM_TICKET_ENTIRES = 20
nearbytickets = [[int(line.split(",")[i]) for i in range(NUM_TICKET_ENTIRES)] for line in rawfiledata[2].split("\n")[1:]] 


class ruleset:
	#pass in ruledata, one rule per line
	def __init__(self, ruledata):
		self._ruledata = ruledata
		self.ruleset = []
		self._parsedata()
	
	def _parsedata(self):
		for line in self._ruledata:
			searchob = re.search(r'([\w\s]*)(?:: )(\d{1,3})(?:-)(\d{1,3})(?: or )(\d{1,3})(?:-)(\d{1,3})', line)
			thisrule = searchob.group(1), int(searchob.group(2)), int(searchob.group(3)), int(searchob.group(4)), int(searchob.group(5))
			self.ruleset.append(thisrule)
			#index 0 = rule name
			#index 1 = lower lower bound
			#index 2 = upper lower bound
			#index 3 = lower upper bound
			#index 4 = upper upper bound
			#bounds are inclusive

	def cumuvalidrange(self):
		#pretty sure this would break if any lower range was completely below any other (etc)
		lowerlower = min([i[1] for i in self.ruleset])
		upperlower = max([i[2] for i in self.ruleset])
		lowerupper = min([i[3] for i in self.ruleset])
		upperupper = max([i[4] for i in self.ruleset])
		if upperlower >= lowerupper: #overlapping ranges, return a tuple of 2 values
			return lowerlower, upperupper
		else:
			return lowerlower, upperlower, lowerupper, upperupper
	def scanforinvalid(self, ticketdata):
		#not searching for if any 2 or more entries are only valid for the same field
		#because the prompt says I don't need to
		validrange = self.cumuvalidrange()
		allticketvalues = []
		for i in ticketdata:
			allticketvalues += i
		invalidentries = [value for value in allticketvalues if value < validrange[0] or value > validrange[1]]
		return invalidentries


		




myruleset = ruleset(ruledata)
print(sum(myruleset.scanforinvalid(nearbytickets)))
