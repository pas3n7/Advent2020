class waitingroom:
	def __init__(self, seatdata, rowwidth):
		self.seatdata = seatdata
		self.rowwidth = rowwidth
		self.arealen = len(self.seatdata)
		self.numrows = self.arealen / self.rowwidth

	def indextocoords(self, index):
		x = index % self.rowwidth
		y = -(index // self.rowwidth) #always downs
		return x, y

	def coordstoindex(self, coords):
		#pass in coordinates in an (x, y) tuple
		return abs((coords[1]*self.rowwidth))+coords[0]

	def getbyindexvector(self, index, vector):
		#vector is a tuple
		startcoords = self.indextocoords(index)
		coords = startcoords[0] + vector[0], startcoords[1] + vector[1]
		if self.coordisvalid(coords):
			return self.seatdata[self.coordstoindex(coords)]
		else:
			return None

	def coordisvalid(self, coord):
		if coord[0] >= 0 and coord[0] < self.rowwidth and coord[1] >= 0 and coord[1] < self.numrows:
			return True
		else:
			return False

	def getbycoords(self, coords):
		return self.seatdata[self.coordstoindex(coords)]

	def searchdirection(self, index, direction, scaler = 1):
		#just return a bool, if an occupied seat in that direction, return true
		#direction defined by degrees
		occupiedseat = "#"
		vacantseat = "L"
		floortile = "."


		#convert direction in degrees to a vector as a tuple
		directionkey = {0:(1, 0), 45:(1,1), 90:(0,1), 135:(-1,1), 180:(-1,0), 225:(-1, -1), 270:(0, -1), 315:(1, -1)}
		dirunitvector = directionkey.get(direction)
		dirvector = dirunitvector[0]*scaler, dirunitvector[1]*scaler

		#okay search now
		targetval = self.getbyindexvector(index, dirvector)

		if targetval == occupiedseat:
			return True
		elif targetval == None or targetval == vacantseat:
			return False
		elif targetval == floortile:
			return self.searchdirection(index, direction, scaler+1)

	def countoccupied(self, index):
		#given an index, returns how many in line of sight are occupied
		directions = [0, 45, 90, 135, 180 ,225, 270, 315]
		numoccupied = 0
		for i in directions:
			if self.searchdirection(index, i) == True:
				numoccupied += 0
		return numoccupied
	def printseats(self, numlines):
		toprint = ""
		for i in range(numlines):
			startindex = (i * self.rowwidth)
			stopindex = ((self.rowwidth * (i+1)))
			toprint += "\n" + "".join(self.seatdata[startindex:stopindex]) #range [:] is not inclusive
		print(toprint, end='\r') 

	def rungeneration(self):
		#return True if there was a change, false if there was no change
		occupiedseat = "#"
		vacantseat = "L"
		floortile = "."
		tempseats = self.seatdata.copy()
		changemade = False

		for index, s in enumerate(tempseats):

			## if it's floor, move on
			if (s == floortile):
				pass
			else:
				numoccupied = self.countoccupied(index)
				if(s == occupiedseat and numoccupied >= 5):
					##occupied and >= 5 visible occupied seats, so vacate
					self.seatdata[index] = vacantseat
					changemade = True
				elif(s == vacantseat and numoccupied == 0):
					##vacant and nobody visible adjacent, occupy it
					self.seatdata[index] = occupiedseat
					changemade = True
		return changemade

	def totaloccupied(self):
		return self.seatdata.count("#")








with open(r'.\Day11\input.txt') as thefile:
    seats = thefile.read().strip()

rowwidth = seats.find("\n")
seats = list(seats.replace("\n", ""))

theroom = waitingroom(seats, rowwidth)


