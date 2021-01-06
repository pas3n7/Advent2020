class cupcircle:
	def __init__(self, cupinit, numtotal=0):
		self.thecups = []
		self.currentcupind = 0  ###the index, not the cup num
		self.numcups = max(len(cupinit), numtotal) #note that because numbers start a 1 and not 0, this is also the highest cupnum
		self.needtoupdate = (0, self.numcups-1) #given in terms of the index
		self.updatelast5 = [0, 0, 0, 0, 0]
		self.movenum = 0
		self.cupindexmemory = [0 for _ in range(self.numcups+1)]

		tempcups = [int(i) for i in input]
		self.thecups = tempcups + list(range(max(tempcups) + 1, numtotal + 1))

		##init the dictionary index
		self.updatememory()

		## initial rotation to avoid some of the initial stuff where it updates either side of the list over and over
		self.rotate(self.numcups//2)

	def rotate(self, num):
		self.thecups = self.thecups[num:] + self.thecups[:num]
		self.currentcupind = (self.currentcupind + num + 1) % self.numcups
		self.updateallmem()

	def updatememory(self):
		#if given, only update everything from firstcupindex to lastcupindex
		# if self.movenum % 100 == 0:
		needtoupdate = self.needtoupdate
		# updatenum = needtoupdate[1]-needtoupdate[0]
		# # print("updating: ", updatenum, end="\r")
		# self.updatelast5.pop(0)
		# self.updatelast5.append(updatenum)
		# if sum(self.updatelast5)/5 > self.numcups/2:
		# 	self.rotate(self.numcups//4)

		if needtoupdate[1] != 0:
			# tmpdict = {cupnum:index for index, cupnum in enumerate(self.thecups[self.needtoupdate[0]:self.needtoupdate[1]+1], self.needtoupdate[0])}
			# self.cupindexmemory.update(tmpdict)
			for index, cup in enumerate(self.thecups[needtoupdate[0]:needtoupdate[1]+1], needtoupdate[0]):
				self.cupindexmemory[cup] = index
		self.needtoupdate = (0, 0)

	def updateallmem(self):
		self.needtoupdate = (0, self.numcups-1) #given in terms of the index
		for index, cup in enumerate(self.thecups):
			self.cupindexmemory[cup] = index


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
		# print("starting")
		# print(self.thecups)
		# print(self.cupindexmemory)
		# print("memcheck passed: ", self.memcheck())
		for _ in range(nummoves):
			updatedindexes = [] #keep track of what's been moved around
			tmpstack = []
			currentcupval = self.thecups[self.currentcupind]
			##pick up cups to the right of the currently selected cup:
			tmpstack, updatedindexes = self.pickupcups()
			#print("picked up: ", tmpstack)
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
			self.movenum += 1

			# print(_)
			# print(self.thecups)
			# print(self.cupindexmemory)
			# print("memcheck passed: ", self.memcheck())



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

numtoextendto = 1000000

crabbycups = cupcircle(input, numtoextendto)

# import cProfile
# import re
# cProfile.run('crabbycups.move(10000)')

crabbycups.move(10000)

# crabbycups.move(10000)


# crabbycups = cupcircle(input)
# crabbycups.move(10)
# print(crabbycups.thecups)



# print(crabbycups.thecups)
# print(crabbycups.cupindexmemory)

def solforp2(cups):
	oneindex = cups.index(1)
	nums = cups[(oneindex+1)%numtoextendto] , cups[(oneindex+2)%numtoextendto]
	return nums

print(solforp2(crabbycups.thecups))