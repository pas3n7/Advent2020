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

	def updatememory(self):
		#if given, only update everything from firstcupindex to lastcupindex
		if self.needtoupdate[1] != 0:
			tmpdict = {cupnum:index for index, cupnum in enumerate(self.thecups[self.needtoupdate[0]:self.needtoupdate[1]+1], self.needtoupdate[0])}
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
		indtoappend = indtopop
		for i in range(3):
			if indtopop >= len(self.thecups): #len is changing as we pop
				indtopop = 0
			tmpstack.append(self.thecups.pop(indtopop))
			updatedindexes.append((indtoappend + i) % self.numcups)
		return tmpstack, updatedindexes

	def insertcups(self, cupstack, index):
		for cup in cupstack[::-1]:
			self.thecups.insert(index, cup)

	def move(self, nummoves=1):
		print("starting")
		print(self.thecups)
		print(self.cupindexmemory)
		print("memcheck passed: ", self.memcheck())
		for _ in range(nummoves):
			updatedindexes = [] #keep track of what's been moved around
			tmpstack = []
			currentcupval = self.thecups[self.currentcupind]
			##pick up cups to the right of the currently selected cup:
			tmpstack, updatedindexes = self.pickupcups()
			print("picked up: ", tmpstack)
			#find the target, can't be in the tmpstack, can't be 0 (there is no cup number 0)
			target = currentcupval -1
			while target == 0 or target in tmpstack:
				target = (target -1 ) % (self.numcups + 1) #need the +1, because need -1% () to come out to be numcups
			##at this point, everything to the right of min(updatedindexes) (to take into account wrapping) is at index -3 of where 
			#cupindexmemory thinks it 
		

			targetindexunadjusted = self.cupindexmemory[target]
			
			#find how many items have been removed left of the target
			numpoppedleftoftarget = len([x for x in updatedindexes if x < targetindexunadjusted])

			targetindex = targetindexunadjusted - numpoppedleftoftarget

			self.insertcups(tmpstack, targetindex+1) #insert to the right of the target
			updatedindexes.extend(range(targetindex, targetindex+4))  ##add the targetindex to the indexes we have changed

			#No, need to update anything between the lowest index we've modified (anything lower wasn't moved)
			# and the highest index we've modified (anything to the right of that got moved back when we inserted)
			self.needtoupdate = (min(updatedindexes), max(updatedindexes))
			self.updatememory()
			#current cup may have moved
			self.currentcupind = self.cupindexmemory[currentcupval]

			self.movetonextcup()

			print(_)
			print(self.thecups)
			print(self.cupindexmemory)
			print("memcheck passed: ", self.memcheck())



	def memcheck(self):
		for index, cup in enumerate(self.thecups):
			if self.cupindexmemory[cup] != index:
				return False
		return True



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

crabbycups.move(10)



# print(crabbycups.thecups)
# print(crabbycups.cupindexmemory)