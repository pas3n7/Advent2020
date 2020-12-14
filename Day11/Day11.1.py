with open(r'.\Day11\input.txt') as thefile:
    seats = thefile.read().strip()

rowwidth = seats.find("\n")
seats = list(seats.replace("\n", ""))
arealen = len(seats)


def adjindices(index):
	indices = []

	adjacentleft = [-rowwidth, -(rowwidth - 1), +1, rowwidth, rowwidth + 1]
	adcacentright = [-(rowwidth+1), -rowwidth, -1, +(rowwidth-1), rowwidth]
	adjacentmid = [-(rowwidth+1), -rowwidth, -(rowwidth-1), -1, +1, rowwidth-1, rowwidth, rowwidth+1]

	def getindicies(thisindex):
		return index + thisindex


	if (index % rowwidth == 0):
		indices = map(getindicies, adjacentleft)
	elif (index % rowwidth == rowwidth - 1):
		indices = map(getindicies, adcacentright)
	else:
		indices = map(getindicies, adjacentmid)
		
	return [i for i in indices if i >= 0 and i < arealen]

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