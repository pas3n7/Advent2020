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
	inputcode[currentindex].visited = True
	accum = 0
	ReachedLoop = False
	while ReachedLoop is False && currentindex < codelength:
		thisop = inputcode[currentindex]
		inputcode[currentindex].visited = True
		if (thisop.type == "acc"):
			accum += thisop.value
		elif (thisop.type == "jmp"):
			traversefrom(inputcode, currentindex, codelength)
		#print(str(currentindex) + " " +  + " " + str(i.value) + " points to:" + str(i.pointsto) + ", Current accum" + str(accum))
		#need to check if this is the last step before we run again
		# if (thisop.type == 'jmp'):
		# 	print(currentindex)
		# 	numjumps += 1
		ReachedLoop = thisop.visited
		currentindex = thisop.pointsto
	if ReachLoop == True:
		accum = False
	return accum



with open(r'.\Day8\input.txt') as thefile:
	for index, line in enumerate(thefile):
		thecode.append(operation(index, line[0:3], int(line[4:8])))



