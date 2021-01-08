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

fn = r'.\Day24\testinput.txt'

directions = []
with open(fn) as thefile:
	directions = thefile.read().strip().split('\n')

print(directions)
