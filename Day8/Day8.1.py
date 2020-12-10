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
			self.pointsto = 1
		if (self.pointsto < 0):
			self.pointsto = None

with open(r'.\Day8\input.txt') as thefile:
	for index, line in enumerate(thefile):
		thecode.append(operation(index, line[0,3], int(line[4,8])))