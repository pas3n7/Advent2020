#### Coordinate system: 
# X coordinates represent rows connecting in the E W direction
# in even numbered rows, moving NE will represent a move of +1y and +0x
# 						 moving NW will represent a move of +1y and -1x
#						 
# 						 moving SW is -1y -1x
#						 moving SE is -1y +0x

# in odd numbered rows, moving NE will represent a move of +1y and +1x
# 						moving NW will represent a move of +1y and +0x
#
#						moving SW is -1y +0x
#						moving SE is -1y +1x

###
###
### let's read in the input 

from collections import Counter

fn = r'.\Day24\testinput.txt'

directions = []
with open(fn) as thefile:
	directions = thefile.read().strip().split('\n')



def interpret(directionline):
	# Directions:  e, se, sw, w, nw, and ne
	dl = directionline
	x = 0
	y = 0
	index = 0
	while index < len(directionline):
		if dl[index] == "n":
			index+=1
			if dl[index] == "w":
				#move nw
				if y % 2 == 0:
					#y is even
					y += 1
					x -= 1
				else:
					y += 1

			else:
				#move ne
				if y % 2 == 0:
					#y is even
					y += 1
				else:
					x += 1
					y += 1
					
		elif dl[index] == "s":
			index+=1
			if dl[index] == "w":
				#move sw
				if y % 2 == 0:
					#y is even
					x -= 1
					y -= 1
				else:
					y -= 1
					
			else:
				#move se
				if y % 2 == 0:
					#y is even
					y -= 1
				else:
					x += 1
					y -= 1

		elif dl[index] == "e":
			#move e
			x += 1
		else:
			#move w
			x -= 1
		index += 1
	return x, y


#### do things

flipcount = Counter(map(interpret, directions))

# print(flipcount)

numblacktiles = 0
initblacktiles = []

for t in flipcount.items():
	if t[1] % 2 == 1:
		#flipped an odd number of times, means it will be black side up
		numblacktiles += 1
		initblacktiles.append(t[0])


print(initblacktiles)
#### game of life... again...
### find out how far the initial tiles stray

farthestx = [coords[0] for coords in initblacktiles]
farthesty = [coords[1] for coords in initblacktiles]
farthestx = min(farthestx), max(farthestx)
farthesty = min(farthesty), max(farthesty)

## Make everything positive
xoffset = abs(farthestx[0])
yoffset = abs(farthesty[0])

initblacktiles = [(x+xoffset, y+yoffset) for x, y in initblacktiles]

print(initblacktiles)

startdim = farthestx[1] + xoffset + 5, farthesty[1] + yoffset + 5  #startdim is traditional x,y


print(startdim)
### initialize a plane:


class afloor:
	def __init__(self, startingset, startdim): #startdim is traditional x,y startingset given in (x,y) tuples
		
		self.thefloor = [["." for _ in range(startdim[0])] for __ in range(startdim[1])]
		### when we add to y, we always need to add 2, to not change even/odd for a row
		### using . for white side up to make it easier to see
		
		for coord in startingset:
			x = coord[0] + 2
			y = coord[1] + 2
			self.thefloor[y][x] = "b"

		self.xdim = startdim[0]
		self.ydim = startdim[1]

	def getbneighbors(self, x, y):
		#returns number of neighboring tiles with black up
		#does not check for edge of board

		#neighbors for an even y (relative to (0,0)) (starting from e side)
		#(1, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)
		#for an odd y:
		#(1, 0), (1, -1), (0, -1), (-1, 0), (0, 1) (1, 1)
		bncount = 0
		yoddset = (1, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)
		yeveset = (1, 0), (1, -1), (0, -1), (-1, 0), (0, 1), (1, 1)  #coords are tradition x, y. Use backwards
		if y % 2 == 0:
			#even
			neighborset = yeveset
		else:
			neighborset = yoddset

		for ncoord in neighborset:
			if self.thefloor[y+ncoord[1]][x+ncoord[0]] == "b":
				bncount += 1
		return bncount
	
	def expandx(self):
		for y in self.thefloor:
			y.insert(0, '.')
			y.append('.')
		self.xdim += 2
	
	def expandy(self):
		#must add 2 to maintain positive/negative per y dimension
		self.thefloor.insert(0, ['.' for _ in range(self.xdim)])
		self.thefloor.insert(0, ['.' for _ in range(self.xdim)])
		self.thefloor.append(['.' for _ in range(self.xdim)])
		self.thefloor.append(['.' for _ in range(self.xdim)])
		self.ydim += 4


	def move(self):
		floorcopy = self.thefloor.copy()
		expandx = False
		expandy = False
		for y in range(1, self.ydim-1):
			for x in range(1, self.xdim-1): #-1, don't want to check outer perimeter. We'll make sure there is always a blank outer
				# Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
				# Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
				numbneigh = self.getbneighbors(x, y)
				if self.thefloor[y][x] == "b":
					if numbneigh == 0 or numbneigh > 2:
						floorcopy[y][x] = "."
				else:
					#white tile
					if numbneigh == 2:
						floorcopy[y][x] = "b"
						if y == self.ydim-2 or y==1:
							expandy = True
						if x == self.xdim-2 or x==1:
							expandx = True
		self.thefloor = floorcopy
		if expandx:
			self.expandx()
		if expandy:
			self.expandy()

		





thefloor = afloor(initblacktiles, startdim)


for row in thefloor.thefloor:
	print(row)

thefloor.move()

print("\n")

for row in thefloor.thefloor:
	print(row)
