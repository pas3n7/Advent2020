#### Coordinate system: 
# X coordinates represent rows connecting in the E W direction
# in even numbered rows, moving NE will represent a move of +1y and +0x
# 						 moving NW will represent a move of +1y and -1x
#						 
# 						 moving SW is -1y -1x
#						 moving SE is -1y +0x

# in odd numbered rows, moving NE will represent a move of +1y and +1x
# 						moving NW will represent a move of +1y and +0x
#
#						moving SW is -1y +0x
#						moving SE is -1y +1x

###
###
### let's read in the input 

from collections import Counter

fn = r'.\Day24\input.txt'

directions = []
with open(fn) as thefile:
	directions = thefile.read().strip().split('\n')



def interpret(directionline):
	# Directions:  e, se, sw, w, nw, and ne
	dl = directionline
	x = 0
	y = 0
	index = 0
	while index < len(directionline):
		if dl[index] == "n":
			index+=1
			if dl[index] == "w":
				#move nw
				if y % 2 == 0:
					#y is even
					y += 1
					x -= 1
				else:
					y += 1

			else:
				#move ne
				if y % 2 == 0:
					#y is even
					y += 1
				else:
					x += 1
					y += 1
					
		elif dl[index] == "s":
			index+=1
			if dl[index] == "w":
				#move sw
				if y % 2 == 0:
					#y is even
					x -= 1
					y -= 1
				else:
					y -= 1
					
			else:
				#move se
				if y % 2 == 0:
					#y is even
					y -= 1
				else:
					x += 1
					y -= 1

		elif dl[index] == "e":
			#move e
			x += 1
		else:
			#move w
			x -= 1
		index += 1
	return x, y


#### do things

flipcount = Counter(map(interpret, directions))

# print(flipcount)

numblacktiles = 0

for t in flipcount.items():
	if t[1] % 2 == 1:
		#flipped an odd number of times, means it will be black side up
		numblacktiles += 1

print(numblacktiles)