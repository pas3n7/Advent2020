import re
with open(r'.\Day16\input.txt') as thefile:
	rawfiledata = thefile.read().strip().split('\n\n')

NUM_TICKET_ENTIRES = 20
ruledata = rawfiledata[0].split("\n")
myticket = [int(rawfiledata[1].split("\n")[1].split(",")[i]) for i in range(NUM_TICKET_ENTIRES)]

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
	def removeinvalid(self, ticketdata):
		#not searching for if any 2 or more entries are only valid for the same field
		#because the prompt says I don't need to
		validrange = self.cumuvalidrange()
		validtickets = [ticket for ticket in ticketdata if min(ticket)>= validrange[0] and max(ticket)<=validrange[1]]
		return validtickets
	def matchrule(self, fieldset):
		matchingrules = []
		for rule in self.ruleset:
			testset = [value for value in fieldset if value < rule[1] or (value > rule[2] and value < rule[3]) or value > rule[4]]
			if len(testset) == 0:
				matchingrules.append(rule[0])
		return matchingrules
		
	
		

def tsettofieldvalueset(ticketdata):
	#transform the list of tickets to a list of fields for a given position in the input data
	tempset = [[field[i] for field in ticketdata] for i in range(NUM_TICKET_ENTIRES)]
	tempset = list(map(lambda x: sorted(list(set(x))), tempset))
	return tempset

def elimination(fieldlist):
	#perform process of elimination on a list containing list of possible fields for each index
	#return a list in the same order 
	#orderdict so we can work from the entry which can only be one thing, etc, without sorting and losing track of indexing
	orderdict = {len(fields) : index for index, fields in enumerate(fieldlist)}
	
	taken = []
	for i in range(1, NUM_TICKET_ENTIRES): #start at 1 because len
		thisfieldname = fieldlist[orderdict.pop(i)][0]
		taken.append(thisfieldname)
		for x in orderdict.values():
			fieldlist[x].remove(thisfieldname)
	return fieldlist

		
#create a ruleset based on the file input
myruleset = ruleset(ruledata)
#remove invalid tickets if they have any fields that cannot match any rules
nearbytickets = myruleset.removeinvalid(nearbytickets)
#transform frome list of ticket to list of data for a given position in the input data
fieldvals = tsettofieldvalueset(nearbytickets)
#see which rules could possibly match data from each position
fieldindexmatches = [myruleset.matchrule(field) for field in fieldvals]
#perform process of elimination to get the field names in the order the appear
fieldnames = elimination(fieldindexmatches)


product = 1
for index, field in enumerate(fieldnames):
	if field[0][0:9] == "departure":
		print(index)
		print(myticket[index])
		product = product * myticket[index]

print(product)