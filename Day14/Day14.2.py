import re
FILENAME = r'.\Day14\input.txt'


def addall(bits):
	resultset = []
	numbits = len(bits)
	bits.sort()

	#count in binary, AND the number with the binary itterator, add results to a temp int
	#if there are x bits, we need to count (in decimal) to (2^x) -1
	for x in range(2**numbits):
		tempnum = 0
		for index, i in enumerate(bits):
			# AND 2^i with the current x in binary, shifted i  bits to the left and add to tempnum
			tempnum += 2**i & (x << (i - index))
		resultset.append(tempnum)
	return resultset

#an instruction group will represent a bitmask and a set of memory write instructions
class instructiongroup:
	def __init__(self, setdata):
		#init vars
		self.mask = 0
		self.tempmask = 0
		self.instrlist = []  #for each instruction, will be a tuple of (address, data)
		self.numinstr = 0
		self.maskadders = [] #this will be the numbers we need to add to the base memory addresses, to get all addresses to write

		#initialize the masks
		self._initmasks(setdata)
		self._initinstr(setdata)

	def _initmasks(self, setdata):
		#because the mask has 0, 1, and X, I'm making a mask for the mask, called maskmask
		#maskmask will have a 1 if mask has an X, and a 0 if the mask has a 0 or 1
		#I will then replace the Xs in the mask with 0

		#read in the mask data
		tempmask = re.match(r'(?:mask = )([01X]{36})', setdata).group(1)
		tempmaskmask = tempmask
		#replace Xs with 0s, convert to int (base 2)
		tempmask = int(tempmask.upper().replace('X', '0'), 2)

		#make the mask mask, so that any bit in the mask is represented here by a 1, any x a 0.
		#  replace any Xs with 0s, and any 0s with 1s.
		#convert to an in (base 2)
		tempmaskmask = int(tempmaskmask.upper().replace('1', '0').replace('X', '1'), 2)
		self.mask = tempmask
		self.maskmask = tempmaskmask

		## we will calculate all addresses as the set of the given address, or'd with the base mask
		## plus the sum of all the set bits in mask mask
		## find the set bits buy anding with a 1 shifted up to 33 places (and remove 0's)
		setbits = [i for i in range(36) if (self.maskmask & (1 << i)) != 0] 
		self.maskadders = addall(setbits) 
	
	def _initinstr(self, setdata):
		tempinstrlist = re.findall(r'mem\[(\d+)\] = (\d+)', setdata)
		self.instrlist = [(int(x), int(y)) for x, y in tempinstrlist]
		self.numinstr = len(self.instrlist)
	
	def execute(self):
		#Value is just the data, only need to calulate the address set
		#to get the base address, we ~maskmask &(addr + mask)
		#then need to add all combinations of the mask mask set (for all bits == x)
		#reminder, instructions come in tuple (address, data)

		tempmems = {(~self.maskmask & (i[0] | self.mask))+maskadder : i[1] for i in self.instrlist for maskadder in self.maskadders}
		return tempmems



def readdata():
	with open(FILENAME) as thefile:
		rawinput = thefile.read().strip()

	#split up the data into chunks including the mask and the instructions
	return re.findall(r"mask.+(?:\nmem\[\d+\] = \d+)+", rawinput)

dataset = [instructiongroup(thisgroup) for thisgroup in readdata()]

memory = {}
for instgroup in dataset:
	memory.update(instgroup.execute())
	#repeated addresses will be overwritten

print(sum(memory.values()))

