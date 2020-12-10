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

with open(r'.\Day8\input.txt') as thefile:
	for index, line in enumerate(thefile):
		thecode.append(operation(index, line[0:3], int(line[4:8])))

# for i in thecode:
# 	print(str(i.position) + " " + i.type + " " + str(i.value) + " points to:" + str(i.pointsto))

currentop = 0
accum = 0
ReachedLoop = False
# numjumps = 0 

while ReachedLoop is False:
	thisop = thecode[currentop]
	thecode[currentop].visited = True
	if (thisop.type == "acc"):
		accum += thisop.value
	#print(str(currentop) + " " +  + " " + str(i.value) + " points to:" + str(i.pointsto) + ", Current accum" + str(accum))
	#need to check if this is the last step before we run again
	# if (thisop.type == 'jmp'):
	# 	print(currentop)
	# 	numjumps += 1
	ReachedLoop = thecode[thisop.pointsto].visited
	currentop = thisop.pointsto

#print("num jumps: " + str(numjumps))	
print(accum)
