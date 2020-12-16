### function defs
from math import prod


## returns the next multiple of num larger than mustbeafter
## numaway will give subsequent multiples of num
def findmultipleafter(num, mustbeafter, numaway = 1):
	nextmult = num *((mustbeafter // num ) + numaway)
	return nextmult

def findmultipleprev(num, mustbebefore, numaway = 1):
	prevmult = num *((mustbebefore // num ) - numaway)
	return prevmult

### open the file

with open(r'.\Day13\input.txt') as thefile:
	busses = thefile.read()[7:].strip().split(',')

# with open(r'.\Day13\inputtest.txt') as thefile:
# 	busses = thefile.read().strip().split(',')

#get a list of tuples, with bus and their index
busses = [ (int(bus), index) for index, bus in enumerate(busses) if bus != "x"]

# just, whatevs, let's just search
numbusses = len(busses)
timestamp = None
i = 1
incrementby = 1
lockedin = 0 #once we find a match for a given bus, we are locked in and don't need to keep checking it


for bus in busses[lockedin:numbusses]:
	while timestamp is None:
		if ((i+bus[1]) % bus[0] == 0): #if the current i is divisible by the current bus number and 
			if bus[0] == busses[numbusses-1][0]:
				#found the final match, record timestamp
				timestamp = i
			else:
				lockedin += 1
				incrementby = prod([bus[0] for bus in busses[0:lockedin]]) #start incrementing by the product of all busses matched
			break

		i += incrementby

print(timestamp)