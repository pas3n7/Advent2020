FILENAME = r".\Day17\input.txt"
from copy import deepcopy

class threedgol:
	def __init__(self, inputdata):
		self.dimension = 0
		self.dimensionz = 1
		self.centersliceref = 0
		self.homecuberef = 0
		self.space = [[[[]]]]
		self._readinspace(inputdata)

	
	def _readinspace(self, inputdata):
		tempspaceslice = inputdata.split("\n")
		self.dimension = len(tempspaceslice)
		self.space[0][0] = [list(row) for row in tempspaceslice] #list(row) turns the string into a list of chars
		self.expand(2) 		#expand by 2, so we don't have to worry about checking indexes later

	def expand(self, num):
		#add all-off z slices to top and bottom
		for num in range(num):
			dimension = self.dimension
			dimensionz = self.dimensionz
			#expand in t
			self.space.insert(0, [[[ '.' for i in range(dimension) ] for j in range(dimension)] for k in range(dimensionz)])
			self.space.append([[[ '.' for i in range(dimension) ] for j in range(dimension)] for k in range(dimensionz)])
			self.homecuberef += 1
			#expand in z 
			for cube in self.space:
				cube.insert(0, [[ '.' for i in range(dimension) ] for j in range(dimension)])
				cube.append([[ '.' for i in range(dimension) ] for j in range(dimension)])
				self.centersliceref += 1
				for zslice in cube:
					#expand in y
					zslice.insert(0, ['.' for i in range(dimension)])
					zslice.append(['.' for i in range(dimension)])
					#expand in x
					for i in zslice:
						i.insert(0, '.')
						i.append('.')
			self.dimensionz += 2
			self.dimension += 2
		return None

	def countactivenei(self, dimension):
		#pass in dimension as a tuple (t, z, y, x)
		t = dimension[0]
		z = dimension[1]
		y = dimension[2]
		x = dimension[3]
		activesym = '#'
		neighbors = [self.space[t+l][z+k][y+j][x+i] for i in [-1,0,1] for j in [-1,0,1] for k in [-1,0,1] for l in [-1,0,1]if (i != 0)|(j != 0)|(k != 0)|(l != 0)]
		activenei = neighbors.count(activesym)
		return activenei
	
	def countactive(self):
		#flatten the space and count
		active = [x for t in self.space for z in t for y in z for x in y].count("#")
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
			for t in range(1, self.dimensionz-1):
				for z in range(1, self.dimensionz-1):
					for y in range(1, self.dimension-1):
						for x in range(1, self.dimension-1):
							madechange = False
							if self.space[t][z][y][x] == activesym and self.countactivenei((t, z, y, x)) not in [2, 3]:
								tempspace[t][z][y][x] = inactivesym
								madechange = True
							elif self.space[t][z][y][x] == inactivesym and self.countactivenei((t, z, y, x)) in [3]:
								tempspace[t][z][y][x] = activesym
								madechange = True

							if madechange:
								if markedforexpand == False and (x in [1, self.dimension - 1] or y in [1, self.dimension - 1] or z in [1, self.dimensionz - 1] or t in [1, self.dimensionz -1]):
									markedforexpand = True
			self.space = deepcopy(tempspace)
			if markedforexpand:
				self.expand(1)

	def getcenterslice(self):
		return self.space[self.homecuberef][self.centersliceref]

	def printall(self):
		for z in range(self.dimensionz):
			for x in self.space[self.homecuberef][z]:
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

print("measuredlen")
print(len(myspace.space))
print("dimension var")
print(myspace.dimension)


# for x in myspace.getcenterslice():
# 	print(x)

# print("\n")


# for i in range(2):
# 	myspace.rungeneration()
# 	print("\n")
# 	for x in myspace.getcenterslice():
# 		print(x)
# 	print(myspace.countactive())
