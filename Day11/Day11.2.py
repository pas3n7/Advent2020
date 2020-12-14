class waitingroom:
	def __init__(self, seatdata, rowwidth):
		self.seatdata = seatdata
		self.rowwidth = rowwidth
		self.arealen = len(self.seatdata)

	def indextocoords(self, index):
		x = index % self.rowwidth
		y = -(index // self.rowwidth) #always down
		return x, y

	def coordstoindex(self, x, y):
		return abs((y*self.rowwidth))+x

	def searchdirection(self, index, direction, scaler = 1):
		#direction defined by degrees
		thisarealen = self.arealen
		returnseat = ""

		#convert direction in degrees to a vector as a tuple
		directionkey = {0:(1, 0), 45:(1,1), 90:(0,1), 135:(-1,1), 180:(-1,0), 225:(-1, -1), 270:(0, -1), 315:(1, -1)}

		#edgedetect





with open(r'.\Day11\input.txt') as thefile:
    seats = thefile.read().strip()

rowwidth = seats.find("\n")
seats = list(seats.replace("\n", ""))

theroom = waitingroom(seats, rowwidth)











def getnumoccupiedadj(index, seatlist):
	index = index
	indices = []
	indices = adjindices(index)
	numoccupied = 0
	for i in indices:
		if(seatlist[i] == '#'):
			numoccupied += 1
	return numoccupied

def printseats(numlines):
	toprint = ""
	for i in range(numlines):
		startindex = (i * rowwidth)
		stopindex = ((rowwidth * (i+1)))
		toprint += "\n" + "".join(seats[startindex:stopindex]) #range [:] is not inclusive
	print(toprint, end='\r') 






changemade = True	
numgens = 0
printseats(10)
while (changemade):
	numgens+=1
	occupiedseat = "#"
	vacantseat = "L"
	tempseats = seats.copy()
	changemade = False
	for index, s in enumerate(tempseats):

		## if it's floor, move on
		if (s == "."):
			pass
		##If a seat is unoccupied and all neighboring seats are empty, occupy it
		elif (s == vacantseat) and (getnumoccupiedadj(index, tempseats) == 0):
			seats[index] = occupiedseat
			changemade = True
		##If a seat is occupied, and 4 or more adjacent seats are occupied, empty it
		elif (s == occupiedseat) and (getnumoccupiedadj(index, tempseats) >= 4):
			seats[index] = vacantseat
			changemade = True

	

printseats(10)
print("\n")

print(seats.count("#"))