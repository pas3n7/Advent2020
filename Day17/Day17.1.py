FILENAME = r".\Day17\input.txt"
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
		self.expand2() 		#expand by 2, so we don't have to worry about checking indexes later

	def expand1(self):
		self.space[0].insert(0, ['.']*(self.dimension))
		self.space[0].append(['.']*(self.dimension))
		for i in self.space[0]:
			i.insert(0, '.')
			i.append('.')
		self.dimension += 2
		self._expandz()

	def expand2(self):
		self.expand1()
		self.expand1()
	
	def _expandz(self):
		blankspace = [['.']*self.dimension]*self.dimension
		self.space.insert(0, blankspace)
		self.space.append(blankspace)
		self.centersliceref += 1
		self.dimensionz += 2

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

	def rungeneration(self):
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
					elif self.space[z][y][x] == inactivesym and self.countactivenei((z, y, x)) not in [3]:
						tempspace[z][y][x] = activesym
						madechange = True

					if madechange:
						if x in [1, self.dimension - 2] or y in [1, self.dimension - 2] or z in [self.centersliceref -1, self.centersliceref + 1]:
							markedforexpand = True
		self.space[0] = tempspace
		if markedforexpand:
			self.expand1()
	def getcenterslice(self):
		return self.space[self.centersliceref]



	

with open(FILENAME) as thefile:
	rawdata = thefile.read().strip()

myspace = threedgol(rawdata)

for x in myspace.getcenterslice():
	print(x)
print(myspace.countactive())

for i in range(6):
	myspace.rungeneration()
	print("\n")
	for x in myspace.getcenterslice():
		print(x)
	print(myspace.countactive())

print(myspace.countactivenei((7, 3))  in [2, 3])