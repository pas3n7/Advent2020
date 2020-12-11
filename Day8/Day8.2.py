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
	Gotoend = False
	while ReachedLoop is False and currentindex < codelength:
		print(ReachedLoop)
		thisop = inputcode[currentindex]
		nextindex = thisop.pointsto
		if (thisop.type == "acc"):
			accum += thisop.value
		elif (thisop.type == "jmp" and Gotoend is False):
			#traverse from the current index if we encounter a jump. Follow the jump. If that returns a good value, it found the path to the end. If not, it means we 
			#eliminate this jmp operation and go to the end, because this is the one. 
			tempaccum = traversefrom(inputcode, currentindex, codelength)
			if tempaccum is not False:
				#this means we got the value in a deeper recursion
				#add its result to whatever we got and break
				accum += tempaccum
				break
			else:
				#didn't find it in a deeper recursion. skip and go to end
				Gotoend = True
				nextindex = currentindex + 1
		

		#print(str(currentindex) + " " +  + " " + str(i.value) + " points to:" + str(i.pointsto) + ", Current accum" + str(accum))
		#need to check if this is the last step before we run again
		# if (thisop.type == 'jmp'):
		# 	print(currentindex)
		# 	numjumps += 1
		ReachedLoop = thisop.visited
		inputcode[currentindex].visited = True
		currentindex = nextindex
	if ReachedLoop == True:
		accum = False
	return accum



with open(r'.\Day8\input.txt') as thefile:
	for index, line in enumerate(thefile):
		thecode.append(operation(index, line[0:3], int(line[4:8])))



print(traversefrom(thecode, 0, len(thecode)))