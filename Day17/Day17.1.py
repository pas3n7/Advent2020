FILENAME = r".\Day17\testinput.txt"
from copy import deepcopy

class threedgol:
	def __init__(self, inputdata):
		self.dimension = 0
		self.dimensionz = 1
		self.centersliceref = 0
		self.space = [[[]]]
		self._readinspace(inputdata)

	
	def _readinspace(self, inputdata):
		tempspaceslice = inputdata.split("\n")
		self.dimension = len(tempspaceslice)
		self.space[0] = [list(row) for row in tempspaceslice] #list(row) turns the string into a list of chars
		self.expand(2) 		#expand by 2, so we don't have to worry about checking indexes later

	def expand(self, num):
		#add all-off z slices to top and bottom
		for num in range(num):
			dimension = self.dimension
			self.space.insert(0, [[ '.' for i in range(dimension) ] for j in range(dimension)])
			self.space.append([[ '.' for i in range(dimension) ] for j in range(dimension)])
			self.centersliceref += 1
			self.dimensionz += 2
			for zslice in self.space:
				zslice.insert(0, ['.' for i in range(dimension)])
				zslice.append(['.' for i in range(dimension)])
				for i in zslice:
					i.insert(0, '.')
					i.append('.')
			self.dimension += 2

	def countactivenei(self, dimension):
		#pass in dimension as a tuple (z, y, x)
		z = dimension[0]
		y = dimension[1]
		x = dimension[2]
		activesym = '#'
		neighbors = [self.space[z+k][y+j][x+i] for i in [-1,0,1] for j in [-1,0,1] for k in [-1,0,1] if (i != 0)|(j != 0)|(k != 0)]
		activenei = neighbors.count(activesym)
		return activenei
	
	def countactive(self):
		#flatten the space and count
		active = [y for x in self.space for y in x]
		active = [y for x in active for y in x].count("#")
		return active

	def rungeneration(self, gens= 1):
		for _ in range(gens):
			tempspace = deepcopy(self.space)
			activesym = '#'
			inactivesym = '.'
			markedforexpand = False
			#if active and 2 or 3 neighbors are active, keep active, otherwise make inactive
			#if inactive but 3 neighbors active, stays inactive, otherwise make active
			#outside is always empty, don't need to check,
			for z in range(1, self.dimensionz-1):
				for y in range(1, self.dimension-1):
					for x in range(1, self.dimension-1):
						madechange = False
						if self.space[z][y][x] == activesym and self.countactivenei((z, y, x)) not in [2, 3]:
							tempspace[z][y][x] = inactivesym
							madechange = True
						elif self.space[z][y][x] == inactivesym and self.countactivenei((z, y, x)) in [3]:
							tempspace[z][y][x] = activesym
							madechange = True

						if madechange:
							if x in [1, self.dimension - 1] or y in [1, self.dimension - 1] or z in [1, self.dimensionz - 1]:
								markedforexpand = True
			self.space = tempspace
			if markedforexpand:
				self.expand(1)

	def getcenterslice(self):
		return self.space[self.centersliceref]

	def printall(self):
		for z in range(self.dimensionz):
			for x in self.space[z]:
				print(x)
			print('\n')
	
	def printcenter(self):
		for row in self.getcenterslice():
			print(row)



	

with open(FILENAME) as thefile:
	rawdata = thefile.read().strip()

myspace = threedgol(rawdata)

myspace.rungeneration(6)
myspace.printall()


print(myspace.countactive())




# for x in myspace.getcenterslice():
# 	print(x)

# print("\n")


# for i in range(2):
# 	myspace.rungeneration()
# 	print("\n")
# 	for x in myspace.getcenterslice():
# 		print(x)
# 	print(myspace.countactive())
