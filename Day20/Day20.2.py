from math import floor, sqrt
from copy import deepcopy
import re

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
		self.flip = False  ###A flip in the y is equivalent to a flip in the x + a 180 degree rotation
		self.rotation = 0   

		self.neighbors = {"top": None, "right": None, "bottom": None, "left": None} #list of all the neighboring tiles
		self.numneighbors = 0
							
	def __str__(self):
		ret = self.getorientedtile()
		return '\n'.join(ret)
	
	def getorientedtile(self, degrees=None, flip=False):
		if not degrees:
			degrees = self.rotation
		if not flip:
			flip = self.flip
		thistile = [list(row) for row in self.thetile]
		if flip:
			#flip
			ret = [row[::-1] for row in thistile]
		else:
			ret = thistile
		if degrees == 0:
			pass
		elif degrees == 90:
			ret = [[row[col] for row in ret[::-1]] for col in range(len(ret))]
		elif degrees == 180:
			ret = [row[::-1] for row in ret[::-1]]
		elif degrees == 270:
			ret = [[row[col] for row in ret] for col in range(len(ret)-1, 0-1, -1)]
		else:
			print("rotation failed")



		#return as a list of strings
		ret = [''.join(row) for row in ret]

		return ret

	def getorientedstrippedtile(self):
		##strip the borders
		mytile = self.getorientedtile()
		mytile = [row[1:-1] for row in mytile[1:-1]]
		return mytile



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
		if self.flip:
			ret = self.getflipedges()
		else:
			ret = self.edges
		return self.rotate(ret, self.rotation)
	def getedgescompliment(self):
		if self.flip:
			ret = self.getflipedgescomp()
		else:
			ret = self.edgescompliment
		return self.rotate(ret, self.rotation)
	def getflipedges(self):
		#if flip x, we swap positions of l and r, and reverse everything to establish correct direction
		return {"top":self.edgescompliment["top"], "right":self.edgescompliment["left"], "bottom":self.edgescompliment["bottom"], "left":self.edgescompliment["right"]}
	def getflipedgescomp(self):
		#if flip x, we swap positions of l and r, and reverse everything to establish correct direction
		return {"top":self.edges["top"], "right":self.edges["left"], "bottom":self.edges["bottom"], "left":self.edges["right"]}

	def getneighbors(self):
		tempnei = self.neighbors
		#{"top": None, "right": None, "bottom": None, "left": None}
		if self.flip:
			tempnei = {"top": tempnei["top"], "right": tempnei["left"], "bottom": tempnei["bottom"], "left": tempnei["right"]}
		tempnei	= self.rotate(tempnei, self.rotation)
		return tempnei

	def rotate(self, dicttorotate, degrees):
		#do a 90 degree clockwise rotation for now
		#neighbor that was left is now top
		#need to make sure it's in the right order
		tmplist = [dicttorotate["top"], dicttorotate["right"], dicttorotate["bottom"], dicttorotate["left"]]
		for _ in range(degrees %360 //90):
			tmplist.insert(0, (tmplist.pop(-1))) #rotate
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
		tiledim = len(self.tiles[0].getorientedstrippedtile())
		toprint =  []
		for tilerow in self.map:
			for linenum in range(tiledim):
				linenumtoprint=[]
				for atile in tilerow:
					atile = atile.getorientedstrippedtile()
					linenumtoprint.append(''.join(atile[linenum]))
				toprint.append(''.join(linenumtoprint))
		return '\n'.join(toprint)
					
	def printwithlines(self, mymap=None):
		if not mymap:
			mymap=self.map
		tiledim = mymap[0][0].dim[0]
		toprint =  []
		for tilerow in mymap:
			for linenum in range(tiledim):
				linenumtoprint=[]
				if linenum == 1 or linenum == tiledim - 1:
					linenumtoprint.append('\n')
				for atile in tilerow:
					atile = atile.getorientedtile()
					linenumtoprint.append(atile[linenum][0] + "    " + ''.join(atile[linenum][1:-1]) + "    " + atile[linenum][-1])
				toprint.append(''.join(linenumtoprint))
		print('\n'.join(toprint))


	def printdebug(self):
		debuginfo = [[(atile.num, atile.flip, atile.rotation) for atile in row] for row in self.map]
		for row in debuginfo:
			print(row)
	
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
			
	
	def gettilebynum(self, num):
		thistile = None
		for t in self.tiles:
			if t.num == num:
				thistile = t
		return thistile

	
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
		if match[2]:
			#if tile2 needs to be flipped
			torotate.flip = True
			match = self.howmatch(knowngood, torotate) ##howmatch respects the flip flag
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
		for tile in self.tiles:
			neighbors = self.findmatch(tile)
			for i in neighbors:
				hm = self.howmatch(tile, i)
				side = hm[0] #gives us which side of the current tile the match is for
				tile.neighbors[side] = i


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
				break
		#print(topleft.num)
		dim = floor(sqrt(self.numtiles))

		
		#assemble the first column
		#we don't know which way they are rotated, so can't trust their neighbor direction, but can assemble in place
		# based on the number of neighbors. the neighbor with the lowest num neighbors is the next one

		def assemblecolrow(colaslist, length, side):
			#pass in a list with a corner as the only member, and a direction
			#if given a side, just go that direction
			if len(colaslist) < length:
				toadd = self.rotatetile(colaslist[-1], colaslist[-1].getneighbors()[side]) #get next neighbor, rotate it
				colaslist.append(toadd) #add the next one
				colaslist = assemblecolrow(colaslist, length, side)
			return colaslist


		#assemble first column, list comprehension to turn it from a list into a column
		themap = [[rowindzero] for rowindzero in assemblecolrow([topleft], dim, "bottom")]

		for index, rowleader in enumerate(themap):
			themap[index] = assemblecolrow(rowleader, dim, "right")



		self.map = themap


		


		
#fn = r'.\Day20\testinput.txt'
fn = r'.\Day20\input.txt'


with open(fn) as thefile:
	rawdata  = thefile.read()

mymap = amap(rawdata)

def detransform(binnum):
	tmpnum = format(binnum, '010b')
	tmpnum = tmpnum.replace('0', '.').replace('1', '#')
	return tmpnum


tile1 = mymap.tiles[8]

mymap.assemble()

sea = str(mymap)

monsterindex=[]
def seamonstersearch(sea):
	sea = sea.split('\n')
	monsterline1 = r"..................#."
	monsterline2 = r"#....##....##....###"
	monsterline3 = r".#..#..#..#..#..#..."
	
	monstercount = 0
	for index, line in enumerate(sea):
	
		if index == 0:
			continue  #skip the first line, since we are looking for the second monster line
		match = re.finditer(monsterline2, line)
		for s in [m.start() for m in match]:
			if re.match(monsterline1, sea[index-1][s:]) and re.match(monsterline3, sea[index+1][s:]):
				monsterindex.append((index+1, s+1))
				monstercount+= 1

	return monstercount

def fliprotate(sea, *, rotate=False, flip=False):
	if not rotate and not flip:
		return sea
	sea = sea.split('\n')
	if rotate:
		ret = [''.join([row[col] for row in sea[::-1]]) for col in range(len(sea))]
	elif flip:
		ret = [row[::-1] for row in sea]
	else:
		ret = None
	return '\n'.join(ret)

nummonsters = 0
flipped = 0
print(sea)
print("do things --------------------------")
for _ in range(2):
	for _ in range(4):
		#rotate, check, repeat

		nummonsters = seamonstersearch(sea)
		if nummonsters == 0:
			sea = fliprotate(sea, rotate=True)
		else:
			break
	if nummonsters == 0:
		sea = fliprotate(sea, flip=True)
	else:
		break
print(nummonsters)

monsterline1 = r"..................#."
monsterline2 = r"#....##....##....###"
monsterline3 = r".#..#..#..#..#..#..."
numpoundsinmonster = (monsterline1 + monsterline2 + monsterline3).count("#")
numpoundsinsea = sea.count("#")

print(monsterindex)
print(numpoundsinsea-(numpoundsinmonster*nummonsters))