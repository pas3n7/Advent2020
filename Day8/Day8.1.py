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

while ReachedLoop is False:
	ReachedLoop = thecode[currentop].visited
	thecode[currentop].visited = True
	if (thecode[currentop].type == "acc"):
		accum += thecode[currentop].value

	currentop = thecode[currentop].pointsto

print(accum)