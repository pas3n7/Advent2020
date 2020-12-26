## in retrospect, this is a nonsensical solution. My best idea instead is to instead of focusing on a ruleset class, make a rule class, then generate a list 
# of references to that rule to be contained in the rule itself. Then just follow the references around recursively. 
# probably some much better way to do it, but that's the best I can think of while I sit here regretting this approach
## Perhaps part 2 will require a complete rewite anyway, who knows
#
# What lead me to this solution was that on previous days, I was taking too long trying to think of the 'best' way to solve the problem before I got 
# started coding, so for this one I decided to just come up with ANY idea and get stuck in. 
#
## This is not a failure, however. The lessons learned here were worth the cost. 

import re

FILENAME = r'.\Day19\day2testinput.txt'

with open(FILENAME) as thefile:
	rawdata = thefile.read().strip().split('\n\n')
#rawdata will have [ruleset, messages]

class ruleset:
	def __init__(self, rulesetraw):

		self.rulesetraw = rulesetraw.split('\n')
		self.numrules = len(self.rulesetraw)
		self.revref = {} ##we will be able to look up all references to a particular index in ruleset. will init in readindata
		self.letteronlyrules = [] #add just the letters at first, then add any that are newly reduced to just letters
		self.startletterindex = [] #helpful to know where our first 2 letters are
		self.reducedregex = ""

		##Changes for part 2
		#self.linestochange = {8: [[42], [42, 8]], 11: [[42, 31], [42, 11, 31]]}
		#self.linestochange = {8: [[42], [42, 42]], 11: [[42, 31], [42, 42, 31]]}
		self.linestochange = {}

		#init ruleset
		self.ruleset = {}
		self._readindata(self.rulesetraw)
		

	
	def _readindata(self, rulesetraw):

		refregp = r'(\d+): ([\d ]+)(?:\|([\d ]+))?'
		letregp = r'(\d+): "([ab])"'
		for line in rulesetraw:
			match = re.match(refregp, line)
			if match:
				#matched the first regex, so we're looking at a rule with only reference (not a letter rule)
				matchnum = int(match.group(1))
				matchset1 = [int(x) for x in match.group(2).strip().split(' ')]
				#try matchset 2, if there is no | there will be no match
				try:
					matchset2 = [int(x) for x in match.group(3).strip().split(' ')]				
				except:
					matchset2 = []
				if matchnum in self.linestochange:
					##changes for part 2:
					matchset1 = self.linestochange[matchnum][0]
					matchset2 = self.linestochange[matchnum][1]
					print("changing: " + str(matchnum))
				for m in set(matchset1 + matchset2):
					try:
						#try adding to existing dict element, if fails, add a new one
						self.revref[m] += [matchnum]
					except KeyError:
						self.revref[m] = [matchnum]

				
				self.ruleset[matchnum] = [matchset1, matchset2]
			else:
				#didn't match the firt regex, here are our letters
				match = re.match(letregp, line)
				try:
					matchnum = int(match.group(1))
					matchlet = match.group(2)
					self.ruleset[matchnum] = matchlet
					self.startletterindex.append(matchnum)
					self.letteronlyrules = self.startletterindex.copy()
				except:
					print("Failed to parse: " + line)


	def ruletoregex(self, ruleindex):
		##let's take a rule in the format: [3, ['a', 'b'], ['b', 'a']] and make it a regex string
		##does not dereference, rule must only contain letters.
		rule = self.ruleset[ruleindex]
		string = None
		# try: 
		if ruleindex not in self.startletterindex:
			if rule[1]: 
				string = '(' + ''.join(rule[0]) + '|' + ''.join(rule[1]) + ')'
			else:
				string = '(' + ''.join(rule[0]) + ')'
		else: 
			#letter rule, just return the letter
			string = rule
		# except: 
		# 	string = None
		# 	print("ruletoregex failed on ruleindex: " + str(ruleindex) + " : " + str(rule))
		return string
	def reduce(self, indextoreduce):
		#for a given rule, get the regexification
		tempstring = self.ruletoregex(indextoreduce)
		#now find references to this one, and replace them with the string
		if indextoreduce > 0:  
			for ruleref in self.revref[indextoreduce]:
				##for each rule that references this rule
				for sideindex, sideofor in enumerate(self.ruleset[ruleref]):
					if sideofor: #handling if there is no or in this rule
						self.ruleset[ruleref][sideindex] = [tempstring if num == indextoreduce else num for num in sideofor]
				try:##check if fully reduced
					if type(1) not in [type(i) for i in (self.ruleset[ruleref][0] + self.ruleset[ruleref][1])]:
						self.letteronlyrules.append(ruleref)
				except TypeError: #if nothing after the or, will result in an error because nonetype
					if type(1) not in [type(i) for i in self.ruleset[ruleref][0]]:
						self.letteronlyrules.append(ruleref)
		elif indextoreduce == 0: #only one that SHOULD have no references
			self.ruleset[0][1] = tempstring

	def reduceall(self):
		while len(self.letteronlyrules) > 0:
			self.reduce(self.letteronlyrules.pop(0))
		self.reducedregex = self.ruleset[0][1]
		self.reducedregex = r'\b' + self.reducedregex + r'\b'

	def teststring(self, stringtotest):
		#check if a passed in string is a valid rule
		if self.letteronlyrules != "":
			if re.match(self.reducedregex, stringtotest):
				return True
		else:
			return False


myruleset = ruleset(rawdata[0])

# for i in myruleset.ruleset:
# 	print(i)
# 	print(myruleset.ruleset[i])
# #print(myruleset.startletterindex)
myruleset.reduceall()

# print("reducing \n \n")
# for i in myruleset.ruleset:
# 	print(i)
# 	print(myruleset.ruleset[i])

# print(myruleset.reducedregex)




messages = rawdata[1].split('\n')

count = 0
for m in messages:
	print(m)
	if myruleset.teststring(m):
		print("is valid")
		count += 1
	
print(count)

print(myruleset.reducedregex)


# print(myruleset.ruletoregex(42))
# print("\n")
# print(myruleset.ruletoregex(31))

