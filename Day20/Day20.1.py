class tile:
	def __init__(self, rawdata):
		##rawdata should be a string with Tile \d{4}: at the top, and then the tile data, one line per line
		self.thetile = rawdata.split('\n')[1:]
		#All the tile numbers are 4 digits in this input
		self.num = int(rawdata[5:9])
		self.dim = (len(self.thetile[1]), len(self.thetile))  ##dimension of the tile in (width, height)
		#we'll calc the binary equiv of the edges such that '.' is a 0 and '#' is a 1
		#direction will be (from most significant bit to least) in the clockwise direction around the edge
		#l to right on the top, top to bottom on the right, right to left on the bottom, bottom to top on the left
		#this way the vaue of the edges does not change with rotation, just the position
		self.edges = None #will be a tuple of edges (self.tedge, self.redge, self.bedge, self.ledge) 
		self.edgescompliment = None #will be the edges, but backwards, as this is how we will find a matching edge
		
		self._calcedges()

	def __str__(self):
		return '\n'.join(self.thetile)

	def _calcedges(self):
		width, height = self.dim
		tmptedge = self.thetile[0]
		tmpredge = [line[width-1] for line in self.thetile]
		tmpbedge = self.thetile[height-1][::-1]
		tmpledge = [line[0] for line in self.thetile][::-1]

		#get the compliment (edges backwards)

		ctmptedge = tmptedge[::-1]
		ctmpredge = tmpredge[::-1]
		ctmpbedge = tmpbedge[::-1]
		ctmpledge = tmpledge[::-1]
			
		
		def edgetobin(edge):
			edge = ''.join(edge)
			edge = edge.replace('.', '0').replace('#', '1')
			edge = int(edge, 2)
			return edge
		
		self.edges = (edgetobin(tmptedge), edgetobin(tmpredge), edgetobin(tmpbedge), edgetobin(tmpledge))
		self.edgescompliment = (edgetobin(ctmptedge), edgetobin(ctmpredge), edgetobin(ctmpbedge), edgetobin(ctmpledge))

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
		#really needs to be 2 adjacent matches and no more
		alledges = [ edge for t in self.tiles	for edge in t.edges]
			#will end up being all edges, in the same order as the tiles, 4 per. Can use that to step through efficiently
		corners = []
		for index, atile in enumerate(self.tiles):
			matches = 0
			matches = len([index for index, edge in enumerate(atile.edgescompliment) if edge in alledges[:index*4] + alledges[(index*4)+4:]])
			if matches == 2:
				corners.append(atile.num)
			elif matches < 2:
				print("finding corners is probably broken for tile: " + str(atile.num))
		return corners
			



with open(r'.\Day20\testinput.txt') as thefile:
	rawdata  = thefile.read()

mymap = map(rawdata)

def detransform(binnum):
	tmpnum = bin(binnum)[1:]


mymap.print(1)
print('\n')
print(mymap.tiles[0].edges)
print(mymap.tiles[0].edgescompliment)
print(mymap.findcorners())
print(mymap.numtiles)

