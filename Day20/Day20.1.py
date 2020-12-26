class tile:
	def __init__(self, rawdata):
		##rawdata should be a string with Tile \d{4}: at the top, and then the tile data, one line per line
		self.thetile = rawdata.split('\n')[1:]
		#All the tile numbers are 4 digits in this input
		self.num = int(rawdata[5:9])
		self.dim = (len(self.thetile[1]), len(self.thetile))  ##dimension of the tile in (width, height)
		#we'll calc the binary equiv of the edges such that '.' is a 0 and '#' is a 1
		#direction will be (from most significant bit to least) left to right and top to bottom
		self.redge = 0
		self.ledge = 0
		self.bedge = 0
		self.tedge = 0
		self._calcedges()
		self.edges = (self.tedge, self.redge, self.bedge, self.ledge) #starting at the top going clockwise is logical, right?

	def __str__(self):
		return '\n'.join(self.thetile)

	def _calcedges(self):
		width, height = self.dim
		tmpredge = [line[width-1] for line in self.thetile]
		tmpledge = [line[0] for line in self.thetile]
		tmptedge = self.thetile[0]
		tmpbedge = self.thetile[height-1]
		
		def edgetobin(edge):
			edge = ''.join(edge)
			edge = edge.replace('.', '0').replace('#', '1')
			edge = int(edge, 2)
			return edge
		
		self.redge = edgetobin(tmpredge)
		self.ledge = edgetobin(tmpledge)
		self.tedge = edgetobin(tmptedge)
		self.bedge = edgetobin(tmpbedge)

class map:
	def __init__(self, rawmapdata):
		#rawmapdata should be provided as a string of tiles (format given in tile class) separated by a blank line
		self.tiles = [tile(t) for t in rawmapdata.strip().split('\n\n')]
		self.numtiles = len(self.tiles)

	

	def print(self, numtoprint):
		for i in range(numtoprint):
			print(self.tiles[i])
			print('\n') ##for now, to make it easier

	def findcorners(self):
		#corners should (hopefully) be the tiles for which 2 edges have no match 
		#this is not even remotely optimal, but let's just get it done
		alledges = [ edge for t in self.tiles	for edge in t.edges]
			#will end up being all edges, in the same order as the tiles, 4 per. Can use that to step through efficiently
		corners = []
		for index, atile in enumerate(self.tiles):
			nomatch = 0
			nomatch = len([edge	for edge in atile.edges if edge not in alledges[:index*4] + alledges[(index*4)+4:]])
			if nomatch == 2:
				corners.append(atile.num)
			elif nomatch > 2:
				print("finding corners is probably broken for tile: " + str(atile.num))
		return corners
			



with open(r'.\Day20\testinput.txt') as thefile:
	rawdata  = thefile.read()

mymap = map(rawdata)

print(mymap.findcorners())
print(mymap.numtiles)