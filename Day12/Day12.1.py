INITIAL_HEADING = 0 #East = 0 degrees here, because math
from math import sin, cos, radians

with open(r'.\Day12\input.txt') as thefile:
	navlist = thefile.read().strip().split('\n')
lennavlist = len(navlist)


#can split off the cardinal direction instructions


northinstructions = sum([int(item[1:5]) for item in navlist if item[0] == "N"])
southinstructions = sum([int(item[1:5]) for item in navlist if item[0] == "S"])
eastinstructions = sum([int(item[1:5]) for item in navlist if item[0] == "E"])
westinstructions = sum([int(item[1:5]) for item in navlist if item[0] == "W"])

#extract all the turn instructions in order
turninstructions = [item for item in navlist if item[0] in ('R', 'L', 'F')]

#transform the R instruction into negative L instructions
turninstructions = ["L-"+item[1:5] if item[0]=="R" else item for item in turninstructions]



nbyturn = 0
ebyturn = 0 #just using north and east, will make them positive or negative


heading = INITIAL_HEADING

for i in turninstructions:
	instruction = i[0]
	magnitude = int(i[1:5])

	if instruction == 'L':
		heading += magnitude
		heading = heading % 360
	elif instruction == 'F':
		ebyturn += magnitude * round(cos(radians(heading)))
		nbyturn += magnitude * round(sin(radians(heading)))
	else:
		print("unrecognized instruction: " + instruction)

x = ebyturn + eastinstructions - westinstructions
y = nbyturn + northinstructions - southinstructions

print(x)
print(y)
print(abs(x)+abs(y))