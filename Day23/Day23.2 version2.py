class cupcircle:
	def __init__(self, cupinit, numtotal=0):
		self.thecups = []
		self.cupindexmemory = dict()
		self.currentcupind = 0  ###the index, not the cup num
		self.numcups = max(len(cupinit), numtotal) #note that because numbers start a 1 and not 0, this is also the highest cupnum
		self.needtoupdate = (0, self.numcups-1) #given in terms of the index

		tempcups = [int(i) for i in input]
		self.thecups = tempcups + list(range(max(tempcups) + 1, numtotal + 1))

		##init the dictionary index
		self.updatememory()
	
	def updateneedtoupdate(self, updatedtuple):
		##this function is to be called when a function updates thecups
		##updatedtuple should be a tuple of the lowest index modified, and the highest index modified

		#Actually, idk if we need this
		pass

	def updatememory(self, firstcupindex=None, lastcupindex=None):
		#if given, only update everything from firstcupindex to lastcupindex
		if lastcupindex != 0:
			tmpdict = {cupnum:index for index, cupnum in enumerate(self.thecups[self.needtoupdate[0]:self.needtoupdate[1]+1])}
			self.cupindexmemory.update(tmpdict)
		self.needtoupdate = (0, 0)

	def movetonextcup(self):
		if self.currentcupind < self.numcups -1:
			self.currentcupind += 1
		elif self.currentcupind == self.numcups -1:
			self.currentcupind = 0
		else:
			raise UserWarning("currentcupind is already out of range, this shouldn't happen")
	
	def pickupcups(self):
		tmpstack = []
		updatedindexes = []
		indtopop = self.currentcupind + 1
		for _ in range(3):
			if indtopop >= len(self.thecups): #len is changing as we pop
				indtopop = 0
			tmpstack.append(self.thecups.pop(indtopop))
			updatedindexes.append(indtopop)
		return tmpstack, updatedindexes

	def insertcups(self, cupstack, index):
		for cup in cupstack:
			self.thecups.insert(index, cup)

	def move(self):
		updatedindexes = [] #keep track of what's been moved around
		tmpstack = []
		##pick up cups to the right of the currently selected cup:
		tmpstack, updatedindexes = self.pickupcups()

		#find the target, can't be in the tmpstack, can't be 0 (there is no cup number 0)
		target = self.thecups[self.currentcupind] -1
		while target == 0 or target in tmpstack:
			target = (target -1 ) % (self.numcups + 1) #need the +1, because need -1% () to come out to be numcups
		##at this point, everything to the right of min(updatedindexes) (to take into account wrapping) is at index -3 of where 
		#cupindexmemory thinks it 
	

		targetindexunadjusted = self.cupindexmemory[target]
		#don't need to worry about cases where we wrapped(everything is off) or pulled the last 3 (nothing is off)
		if targetindexunadjusted >= min(updatedindexes): 
			targetindex = targetindexunadjusted + 3
		else:
			targetindex = targetindexunadjusted

		self.insertcups(tmpstack, targetindex+1) #insert to the right of the target
		updatedindexes.extend(range(targetindex, targetindex+3))  ##add the targetindex to the indexes we have changed

		#No, need to update anything between the lowest index we've modified (anything lower wasn't moved)
		# and the highest index we've modified (anything to the right of that got moved back when we inserted)
		self.needtoupdate = (min(updatedindexes), max(updatedindexes))
		self.updatememory()
		





####### Main 

###### 
# Constants

testinput = True

if not testinput:
	#real input
	input = "219347865"
else: 
	#test input
	input = "389125467"


crabbycups = cupcircle(input)

print(crabbycups.thecups)
print(crabbycups.cupindexmemory)

crabbycups.move()

print(crabbycups.thecups)
print(crabbycups.cupindexmemory)





# ###idk, let's just try brute forcing it
# mil = 1000000
# numtoextendto = 9
# nummoves = 100# 10 * numtoextendto
# input.extend(range(max(input) + 1, numtoextendto + 1))

# def move(cups, nummoves):
# 	for _ in range(nummoves):
# 		stack = deque()
# 		cups.rotate(-1)
# 		nexttarget = input[-1] -1
# 		for _ in range(3):
# 			stack.append(cups.popleft())
# 		while nexttarget == 0 or nexttarget in stack:
# 			nexttarget = nexttarget - 1
# 			if nexttarget == -1:
# 				nexttarget = numtoextendto
# 		#print("destination", nexttarget, end='\r')
# 		nexttarget = cups.index(nexttarget)
# 		#rotate, extend, rotate back
# 		cups.rotate(-(nexttarget+1))
# 		cups.extend(stack)
# 		cups.rotate(nexttarget+4)
		


# move(input, nummoves)


# print('\n')

# def solforp2(cups):
# 	oneindex = cups.index(1)
# 	nums = cups[(oneindex+1)%numtoextendto] , cups[(oneindex+2)%numtoextendto]
# 	return nums

# print(solforp2(input))