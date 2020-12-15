with open(r'.\Day12\input.txt') as thefile:
	navlist = thefile.read().strip().split('\n')
lennavlist = len(navlist)
shippos = (0,0)
waypointpos = (10, 1) #start position from the prompt



#make some transformations to reduce if statements later
#transform the R instruction into L instructions
navlist = ["L"+str((-int(item[1:5])) % 360) if item[0]=="R" else item for item in navlist]
#transform S to -N instructions
navlist = ["N-"+item[1:5] if item[0]=="S" else item for item in navlist]
#transform W to -E instructions
navlist = ["E-"+item[1:5] if item[0]=="W" else item for item in navlist]




for i in navlist:
	instruction = i[0]
	magnitude = int(i[1:5])

	if instruction == 'L':
		#rotate the waypoint about the ship. If I want to use math to do this, I have to introduce rounding errors
		#will never be an instruction 0 or 360
		if magnitude == 90:
			#flip x and y, then make x negative
			waypointpos = -waypointpos[1], waypointpos[0]
		elif magnitude == 180:
			#don't flip, make negative
			waypointpos = tuple(map(lambda x: -x, waypointpos)) #is this faster than by index? idk
		elif magnitude == 270:
			#flip x and y, then make y negative
			waypointpos = waypointpos[1], -waypointpos[0]
		else:
			print("rotation magnitude error for: " + str(magnitude))
	elif instruction == "N":
		#move waypoint N by magnitude (add magnitude to y)
		waypointpos = waypointpos[0], waypointpos[1]+magnitude
	elif instruction == "E":
		#move waypoint E by magnitude (add magnitude to x)
		waypointpos = waypointpos[0] + magnitude , waypointpos[1]
	elif instruction == 'F':
		#move the ship in the direction of the waypoint vector, magnitude times
		shippos = waypointpos[0]*magnitude + shippos[0], waypointpos[1]*magnitude + shippos[1]
	else:
		print("unrecognized instruction: " + instruction)

print("Ship Position: " + str(shippos) + "\n")
print("Manhattan distance: " + str((abs(shippos[0])+abs(shippos[1]))) + "\n")

