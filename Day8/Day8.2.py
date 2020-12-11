thecode = []

class operation:
	def __init__(self, position, type, value = 0):
		self.type = type
		self.position = position
		if (self.type != "nop"):
			self.value = value
		else:
			self.value = None
		if (type == "jmp"):
			self.pointsto = position + value
		else:
			self.pointsto = self.position + 1
		if (self.pointsto < 0):
			self.pointsto = None
		self.visited = False

def traversefrom(inputcode, startindex, codelength):

	thisop = inputcode[startindex]
	currentindex = startindex
	accum = 0
	ReachedLoop = False
	ReachedEnd = False
	Gotoend = False
	while ReachedLoop is False and ReachedEnd is False:
	
		thisop = inputcode[currentindex]
		inputcode[currentindex].visited = True
		nextindex = thisop.pointsto #assigning to a variable so we can ignore a jump if we want

		#need to check if we are at the end, checking [nextindex] will fail if it doesn't exist
		if (nextindex == codelength):
			ReachedEnd = True
		else:
			ReachedLoop = inputcode[nextindex].visited
			#if we reached the end, we don't need to set this

		
		if (thisop.type == "acc"):
			accum += thisop.value
		elif (thisop.type == "jmp" and Gotoend is False and ReachedEnd is False):
			#traverse from the current index if we encounter a jump. Follow the jump. If that returns a good value, it found the path to the end. If not, it means we 
			# skip this jmp operation and go to the end, because this is the one. 
			tempaccum = traversefrom(inputcode, nextindex, codelength)
			if tempaccum is not False:
				#this means we got the value in a deeper recursion
				#add its result to whatever we got and break
				accum += tempaccum
				ReachedEnd = True
			else:
				#didn't find it in a deeper recursion. skip and go to end
				Gotoend = True
				nextindex = currentindex + 1
		

		#print(str(currentindex) + " " +  + " " + str(i.value) + " points to:" + str(i.pointsto) + ", Current accum" + str(accum))
		#need to check if this is the last step before we run again
		# if (thisop.type == 'jmp'):
		# 	print(currentindex)
		# 	numjumps += 1
		
		currentindex = nextindex

	if ReachedLoop == True:
		accum = False
	return accum



with open(r'.\Day8\input.txt') as thefile:
	for index, line in enumerate(thefile):
		thecode.append(operation(index, line[0:3], int(line[4:8])))



print(traversefrom(thecode, 0, len(thecode)))