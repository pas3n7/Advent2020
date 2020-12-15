### function defs

def findmultipleafter(num, mustbeafter):
	nextmult = num *((mustbeafter // num ) + 1)
	return nextmult

### open the file

with open(r'.\Day13\input.txt') as thefile:
	departtimestamp = int(thefile.readline().strip())
	busses = thefile.readline().strip().split(',')


#filter out the x's, make the others ints
busses = [ int(bus) for bus in busses if bus != "x"]



## actually do things

nextarrival = [ findmultipleafter(bus, departtimestamp) for bus in busses]
arriving = min(nextarrival)
arrivingin = arriving - departtimestamp
thebus = busses[nextarrival.index(arriving)]


print("bus number: " + str(thebus))
print("arriving in: " + str(arrivingin) + " minutes")
print("prompt answer: " + str(thebus * arrivingin))