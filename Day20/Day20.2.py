from math import floor, sqrt
from copy import deepcopy

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
		self.flipx = False  ###I don't want to actually modify the tile, just mark if it needs to be flipped in either direction
		self.flipy = False
		self.rotation = 0   ##note that flipping in both x and y is equivalent to a 180 degree rotation

		self.neighbors = {"top": None, "right": None, "bottom": None, "left": None} #list of all the neighboring tiles
		self.numneighbors = 0
							
	def __str__(self):
		ret = self.getrotatedtile()
		return '\n'.join(ret)
	
	def getrotatedtile(self, degrees=None):
		if not degrees:
			degrees = self.rotation
		thistile = self.thetile
		if degrees == 0:
			ret = thistile
		elif degrees == 90:
			ret = [[row[col] for row in thistile[::-1]] for col in range(len(thistile))]
		elif degrees == 180:
			ret = [row[::-1] for row in thistile[::-1]]
		elif degrees == 270:
			ret = [[row[col] for row in thistile] for col in range(len(thistile)-1, 0-1, -1)]
		else:
			print("rotation failed")

		return ret

	def _calcedges(self):
		width, height = self.dim
		tmptedge = self.thetile[0]
		tmpredge = ''.join([line[width-1] for line in self.thetile])
		tmpbedge = self.thetile[height-1][::-1]
		tmpledge = ''.join([line[0] for line in self.thetile][::-1])

		ed = (tmptedge, tmpredge, tmpbedge, tmpledge)
		ced = tuple(map(self._compedge, ed))

		#get the compliment (edges backwards)
		
		def edgetobin(edge):
			edge = edge.replace('.', '0').replace('#', '1')
			edge = int(edge, 2)
			return edge

		ed = tuple(map(edgetobin, ed))
		ced = tuple(map(edgetobin, ced))
		
		##always top, right, bottom, left. evaluated clockwise
		self.edges = {"top": ed[0], "right": ed[1], "bottom": ed[2], "left": ed[3]}
		self.edgescompliment = {"top":ced[0], "right":ced[1], "bottom":ced[2], "left":ced[3]}

	def getedges(self):
		if self.flipx:
			return self.getflipxedges()
		elif self.flipy:
			return self.getflipyedges()
		else:
			return self.edges
	def getedgescompliment(self):
		if self.flipx:
			return self.getflipxedgescomp()
		elif self.flipy:
			return self.getflipyedgescomp()
		else:
			return self.edgescompliment
	def getflipxedges(self):
		#if flip x, we swap positions of l and r, and reverse everything to establish correct direction
		return {"top":self.edgescompliment["top"], "right":self.edgescompliment["left"], "bottom":self.edgescompliment["bottom"], "left":self.edgescompliment["right"]}
	def getflipyedges(self):
		#if flipping in y, we swap positions of top and bottom and reverse everything to establish correct direction
		return {"top":self.edgescompliment["bottom"], "right":self.edgescompliment["right"], "bottom":self.edgescompliment["top"], "left":self.edgescompliment["left"]}
	def getflipxedgescomp(self):
		#if flip x, we swap positions of l and r, and reverse everything to establish correct direction
		return {"top":self.edges["top"], "right":self.edges["left"], "bottom":self.edges["bottom"], "left":self.edges["right"]}
	def getflipyedgescomp(self):
		#if flipping in y, we swap positions of top and bottom and reverse everything to establish correct direction
		return {"top":self.edges["bottom"], "right":self.edges["right"], "bottom":self.edges["top"], "left":self.edges["left"]}

	def getneighbors(self):
		tempnei = self.neighbors
		#{"top": None, "right": None, "bottom": None, "left": None}
		if self.flipx:
			tempnei = {"top": tempnei["top"], "right": tempnei["left"], "bottom": tempnei["bottom"], "left": tempnei["right"]}
		elif self.flipy:
			tempnei = {"top": tempnei["top"], "right": tempnei["left"], "bottom": tempnei["bottom"], "left": tempnei["right"]}
		tempnei	= self.rotate(tempnei, self.rotation)
		return tempnei

	def rotate(self, neighbordict, degrees):
		#do a 90 degree clockwise rotation for now
		#neighbor that was left is now top
		#need to make sure it's in the right order
		tmplist = [neighbordict["top"], neighbordict["right"], neighbordict["bottom"], neighbordict["left"]]
		for _ in range(degrees %360 //90):
			tmplist.append(tmplist.pop(1)) #rotate
		return {"top": tmplist[0], "right":tmplist[1], "bottom": tmplist[2], "left": tmplist[3]}

	def detransform(self, num):
		#will take a num and transform back to the form edges take in the input, for troubleshooting
		tmpnum = format(num, '010b')
		tmpnum = tmpnum.replace('0', '.').replace('1', '#')
		return tmpnum
	def _compedge(self, edge):
		return edge[::-1]

class amap:
	def __init__(self, rawmapdata=None):
		#rawmapdata should be provided as a string of tiles (format given in tile class) separated by a blank line
		self.tiles = []
		self.numtiles = 0
		self.alledges = []
		self.alledgescomp = []
		self.corners = []
		self.edges = []
		self.map = []
		if rawmapdata:
			self.readindata(rawmapdata)
	def __str__(self):
		tiledim = self.tiles[0].dim[0]
		lines = []
		for row in self.map:
			for linenum in range(tiledim):
				thisline = ""
				for tile in row:
					thisline += tile.thetile[linenum]
				lines.append(thisline)
		return '\n'.join(lines)
		

	
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
		#this is pointless now, but I'll remove it later
		raise UserWarning("don't use findcorners")

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
		# return self.corners
		return False  #this function is pointless now. Will remove it later
	
	def findmatch(self, atile, side = None):
		#just find the matching tile, don't care about orientation
		##if fed an int, turn it into a tile
		if isinstance(atile, int):
			atile = self.gettilebynum(atile)
		#if we are given a side, only check that side, otherwise, check all
		if side:
			thistileedges = [atile.getedgescompliment()[side]]
		else:
			thistileedges = atile.getedgescompliment().values()

		matchedges = [index for index, edge in enumerate(self.alledges + self.alledgescomp) if edge in thistileedges]
		matchtiles = [floor(x%len(self.alledges)/4) for x in matchedges]
		matchtiles = [self.tiles[i] for i in matchtiles if self.tiles[i] is not atile]
		return matchtiles

	def howmatch(self, tile1, tile2):
		#why am I doing this separately from findmatch? idk just get it done
		#allow passing in a tile number
		if isinstance(tile1, int):
			tile1 = self.gettilebynum(tile1)
		if isinstance(tile2, int):
			tile2 = self.gettilebynum(tile2)
		##given 2 tiles, return (tile1 matching edge, tile2matchingedge, does tile2 need to be flipped)
		returnval = None
		tile1edges = tile1.getedgescompliment()
		for edge in tile1edges.items():
			for t2edge in tile2.getedges().items():
				if edge[1] == t2edge[1]:
					returnval = (edge[0], t2edge[0], False)
					break
			for t2edge in tile2.getedgescompliment().items():
				if edge[1] == t2edge[1]:
					returnval = (edge[0], t2edge[0], True)
					break
		return returnval
	
	def rotatetile(self, knowngood, torotate):
		#feed 2 connected tiles, second will be rotated to connect appropriately with the first
		match = self.howmatch(knowngood, torotate)
		sideref = {"top" : 0, "right" :1, "bottom" : 2, "left": 3}
		goodsidenum = sideref[match[0]]
		testsidenum = sideref[match[1]] + 2 % 4  #rotate the number indexes by 2 places
		#if goodsidenum - testsidenum is negative, wants a counterclockwise rotation
		#to convert to clockwise, just add 4
		diff = goodsidenum - testsidenum
		if diff < 0:
			diff += 4
		torotate.rotation = (diff * 90) %360
		return torotate

	def settile(self, atile):
		##for a tile which is passed in, if it exists in tiles array (as determined by tile number), replace it
		for index, t in enumerate(self.tiles):
			if t.num == atile.num:
				self.tiles[index] = atile
		else:
			print("settile did not find a tile to replace")
				

	def matchall(self):
		temptilelist = []
		isflip = {}
		for tile in self.tiles:
			neighbors = self.findmatch(tile)
			for i in neighbors:
				hm = self.howmatch(tile, i)
				side = hm[0] #gives us which side of the current tile the match is for
				otherside = hm[1]
				if hm[2]: ##true if flipped
					isflip[i] = otherside #store for now, add flipped flag when we come to it
				tile.neighbors[side] = i

			if tile in isflip:
				if isflip[i] in ["left", "right"]:
					tile.flipx = True
				else:
					tile.flipy = True


			temptilelist.append(tile)
			tile.numneighbors = len(neighbors)
		self.tiles = temptilelist

	def assemble(self):
		self.matchall()
		corners = [tile for tile in self.tiles if tile.numneighbors == 2]
		topleft = None #keep in mind the whole thing could be flipped or rotated
		for i in corners:
			if i.neighbors["right"] and i.neighbors["bottom"]:
				topleft = i
		#print(topleft.num)
		dim = floor(sqrt(self.numtiles))

		
		#assemble the first column
		#we don't know which way they are rotated, so can't trust their neighbor direction, but can assemble in place
		# based on the number of neighbors. the neighbor with the lowest num neighbors is the next one

		def assemblecolrow(colaslist, length, side=None):
			#pass in a list with a corner as the only member, and a direction
			#if given a side, just go that direction
			if side:
				toadd = self.rotatetile(colaslist[-1], colaslist[-1].getneighbors()[side]) #get next neighbor, rotate it
				colaslist.append(toadd) #add the next one
				colaslist = assemblecolrow(colaslist, length)
			elif len(colaslist) < length:
				neighbors = { side : tile for side, tile in colaslist[-1].getneighbors().items() if tile and tile not in colaslist}
				nexttile = neighbors[min(neighbors, key= lambda n : neighbors[n].numneighbors)]
				nexttile = self.rotatetile(colaslist[-1], nexttile)
				colaslist.append(nexttile)
				colaslist = assemblecolrow(colaslist, length)
			return colaslist


		#assemble first column
		themap = [[rowindzero] for rowindzero in assemblecolrow([topleft], dim, "bottom")]
		self.map = themap


		


		
fn = r'.\Day20\testinput.txt'
#fn = r'.\Day20\input.txt'


with open(fn) as thefile:
	rawdata  = thefile.read()

mymap = amap(rawdata)

def detransform(binnum):
	tmpnum = format(binnum, '010b')
	tmpnum = tmpnum.replace('0', '.').replace('1', '#')
	return tmpnum


print("numtiles: "+ str(mymap.numtiles))
print("numedges:" + str(len(mymap.edges)))
print("numedges matches numtiles?: " + "Yes!" if (((len(mymap.edges)/4) + 2)**2 == mymap.numtiles) else "no :(")

tile1 = mymap.tiles[8]



mymap.assemble()
print(mymap)