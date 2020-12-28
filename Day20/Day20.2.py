from math import floor

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
		self.edges = None #will be a dict of edges top, right, bottom, left 
		self.edgescompliment = None #will be a dict, with reverses of edges
		
		self._calcedges()

		self.iscorner = None
		self.isedge = None
		self.isflipped = None
		self.flipx = None  ###I don't want to actually modify the tile, just mark if it needs to be flipped in either direction
		self.flipy = None
		self.rotation = 0   ##note that flipping in both x and y is equivalent to a 180 degree rotation
							
	def __str__(self):
		return '\n'.join(self.thetile)

	def _calcedges(self):
		width, height = self.dim
		tmptedge = self.thetile[0]
		tmpredge = ''.join([line[width-1] for line in self.thetile])
		tmpbedge = self.thetile[height-1][::-1]
		tmpledge = ''.join([line[0] for line in self.thetile][::-1])

		#get the compliment (edges backwards)

		ctmptedge = tmptedge[::-1]
		ctmpredge = tmpredge[::-1]
		ctmpbedge = tmpbedge[::-1]
		ctmpledge = tmpledge[::-1]
			
		
		def edgetobin(edge):
			edge = edge.replace('.', '0').replace('#', '1')
			edge = int(edge, 2)
			return edge
		
		##always top, right, bottom, left. evaluated clockwise
		self.edges = {"top": edgetobin(tmptedge), "right": edgetobin(tmpredge), "bottom": edgetobin(tmpbedge), "left": edgetobin(tmpledge)}
		self.edgescompliment = {"top":edgetobin(ctmptedge), "right":edgetobin(ctmpredge), "bottom":edgetobin(ctmpbedge), "left":edgetobin(ctmpledge)}

	def getedges(self):
		return self.edges
	def getedgescompliment(self):
		return self.edgescompliment
	def getflipxedges(self):
		#if flip x, we swap positions of l and r, and reverse everything to establish correct direction
		return {"top":self.edgescompliment["top"], "right":self.edgescompliment["left"], "bottom":self.edgescompliment["bottom"], "left":self.edgescompliment["right"]}
	def getflipyedges(self):
		#if flipping in y, we swap positions of top and bottom and reverse everything to establish correct direction
		return {"top":self.edgescompliment["bottom"], "right":self.edgescompliment["right"], "bottom":self.edgescompliment["top"], "left":self.edgescompliment["left"]}
	def detransform(self, num):
		#will take a num and transform back to the form edges take in the input, for troubleshooting
		tmpnum = format(num, '010b')
		tmpnum = tmpnum.replace('0', '.').replace('1', '#')
		return tmpnum

class amap:
	def __init__(self, rawmapdata=None):
		#rawmapdata should be provided as a string of tiles (format given in tile class) separated by a blank line
		self.tiles = []
		self.numtiles = 0
		self.alledges = []
		self.alledgescomp = []
		self.corners = []
		self.edges = []
		if rawmapdata:
			self.readindata(rawmapdata)
	
	def readindata(self, rawmapdata):
		#rawmapdata should be provided as a string of tiles (format given in tile class) separated by a blank line
		self.tiles.extend([tile(t) for t in rawmapdata.strip().split('\n\n')])
		self.update()

	def addtile(self, tile):
		self.tiles.append(tile)
		self.numtiles += 1
		self.alledges.extend(tile.getedges().values())
		self.alledges.extend(tile.getedgescompliment().values())

	def update(self):
		self.numtiles = len(self.tiles)
		self.alledges = [value for atile in self.tiles for value in atile.getedges().values()]
		self.alledgescomp = [value for atile in self.tiles for value in atile.getedgescompliment().values()]
	

	def print(self, numtoprint):
		for i in range(numtoprint):
			print(self.tiles[i])
			print('\n') ##for now, to make it easier
	
	def gettilebynum(self, num):
		thistile = None
		for t in self.tiles:
			if t.num == num:
				thistile = t
		return thistile



	def findcorners(self):
		#corners should be the tiles for which 2 edges have no match after checking all orientations
		#per the prompt: but the outermost edges won't line up with any other tiles.
		#this is not even remotely optimal, but let's just get it done

		#flipping the tile reverses the order of the numbers
		#Need to compare to compiment and non compliment because others might be flipped
		#with tile to test, check compliment (which represents matches if it is not flipped), and non compliment (which represent maches if flipped)
		#whichever has more matches should be correct.
		#This approach might match more than one edge on our tile to another single tile, but let's hope not
		
		corners = []
		for index, atile in enumerate(self.tiles):
			matches = 0
			allotheredges = self.alledges[:index*4] + self.alledges[(index*4)+4:] + self.alledgescomp[:index*4] + self.alledgescomp[(index*4)+4:]
			matches = len([edge for edge in atile.getedgescompliment().values() if edge in allotheredges])
			
			if matches == 2:
				self.tiles[index].iscorner = True
				self.tiles[index].isedge = False
				corners.append(atile.num)
				self.corners.append(atile.num)
			elif matches == 3:
				self.tiles[index].isedge = True
				self.tiles[index].iscorner = False
				self.edges.append(atile.num)
			elif matches < 2:
				print("finding corners is probably broken for tile: " + str(atile.num))
			elif matches > 4:
				print(str(atile.num) + " is matching more than 4 edges")
		return self.corners
		
	def assembleborder(self):
		if self.corners == []:
			print("Run findcorners first")
			return None
	
	def findmatch(self, atile):
		#just find the matching tile, don't care about orientation
		##if fed an int, turn it into a tile
		if isinstance(atile, int):
			atile = self.gettilebynum(atile)
		matchtiles = []
		thistileedges = atile.edgescompliment.values()
		matchedges = [index for index, edge in enumerate(self.alledges + self.alledgescomp) if edge in thistileedges]
		matchtiles = [floor(x%len(self.alledges)/4) for x in matchedges]
		matchtiles = [self.tiles[i] for i in matchtiles if self.tiles[i] is not atile]
		return matchtiles
		

		


with open(r'.\Day20\testinput.txt') as thefile:
	rawdata  = thefile.read()

mymap = amap(rawdata)

def detransform(binnum):
	tmpnum = format(binnum, '010b')
	tmpnum = tmpnum.replace('0', '.').replace('1', '#')
	return tmpnum


print("numtiles: "+ str(mymap.numtiles))
print("numedges:" + str(len(mymap.edges)))
print("numedges matches numtiles?: " + "Yes!" if (((len(mymap.edges)/4) + 2)**2 == mymap.numtiles) else "no :(")
