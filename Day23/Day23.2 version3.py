#### Okay, one more time. Thanks to https://github.com/frerich/aoc2020 for posting a solution and giving me something to wrap my head around
### going to try doing it a little different, with a list of objects. I love objects


## input ##
TESTINPUT = True

if not TESTINPUT:
	#real input
	INPUT = [int(x) for x in "219347865"]
else: 
	#test input
	INPUT = [int(x) for x in "389125467"]




####
#Constants
NUMTOEXTENDTO = 1_000_000
NUMMOVES = 10_000


###### class def

class cup:
	def __init__(self, cupnum, nextcup):
		self.cupnum = cupnum
		self.nextcup = nextcup

	def __str__(self):
		return "I am a cup with number: " + str(self.cupnum) + ". and next in line is: " + str(self.nextcup)

def readinput(cupinput):
	### make our list to hold the cups

	thecups = [0] * (len(cupinput)+1)
	currentcup = INPUT[0] #start at the start, then take it away.

	for index, incupnum in enumerate(cupinput):
		#put a cup (numbered x) at thecups[x] so we can call it by its index
		# its nextcup will be equal to the next one in the input
		thecups[incupnum] = cup(incupnum, cupinput[(index+1)%len(cupinput)])

	return currentcup, thecups

def extend(listofcups, numtoextendto, firstcupnum, lastcupnum):
	extendfrom = max(listofcups[1:], key=lambda x: x.cupnum).cupnum
	# listofcups = listofcups + [cup()]
	if numtoextendto > extendfrom:
		listofcups[lastcupnum].nextcup = extendfrom + 1
		extension = [cup(index, index+1) for index in range(extendfrom+1, numtoextendto)]
		extension.append(cup(numtoextendto, firstcupnum))
		listofcups.extend(extension)


def reassemble(listofcups):
	##for testing
	currentcup = listofcups[1]
	orderedlist = []
	for _ in range(len(listofcups) -1):
		orderedlist.append(currentcup.cupnum)
		currentcup = listofcups[currentcup.nextcup]

	return orderedlist

def move(currentcup, listofcups):
	#find our cups to pick up
	n1=listofcups[currentcup].nextcup
	n2=listofcups[n1].nextcup
	n3=listofcups[n2].nextcup

	#find our destination
	dest = currentcup - 1 

	while dest ==0 or dest in [n1, n2, n3]:
		if dest == 0:
			dest = NUMTOEXTENDTO
		else:
			dest -=1

	#connect currentcup to nextcup
	listofcups[currentcup].nextcup = listofcups[n3].nextcup

	#connect dest to the cups we picked up
	listofcups[n3].nextcup = listofcups[dest].nextcup
	listofcups[dest].nextcup = n1


def calcscorep2(listofcups):
	return listofcups[1].nextcup * listofcups[listofcups[1].nextcup].nextcup


currentcup, thecups = readinput(INPUT)

##### REMEMBER, AND DON'T FORGET
#### thecups[0] is just the number 0
#### because there is no cup with number 0

extend(thecups, NUMTOEXTENDTO, INPUT[0], INPUT[-1])

# print(reassemble(thecups))

for _ in range(NUMMOVES):
	move(currentcup, thecups)
	currentcup = thecups[currentcup].nextcup

print(calcscorep2(thecups))

