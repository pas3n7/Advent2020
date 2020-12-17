import re


#an instruction group will represent a bitmask and a set of memory write instructions
class instructiongroup:
    def __init__(self, setdata):
        #init vars
        self.mask = 0
        self.tempmask = 0
        self.instrlist = []
        self.numinstr = 0

        #initialize the masks
        self._initmasks(setdata)
        self._initinstr(setdata)

    def _initmasks(self, setdata):
        #because the mask has 0, 1, and X, I'm making a mask for the mask, called maskmask
        #maskmask will have a 0 if mask has an X, and a 1 if the mask has a 0 or 1
        #I will then replace the Xs in the mask with 1

        #read in the mask data
        tempmask = re.match(r'(?:mask = )([01X]{36})', setdata).group(1)
        tempmaskmask = tempmask
        #replace Xs with 1s, convert to int (base 2)
        tempmask = int(tempmask.upper().replace('X', '1'), 2)

        #make the mask mask, so that any bit in the mask is represented here by a 1, any x a 0.
        #  replace any Xs with 0s, and any 0s with 1s.
        #convert to an in (base 2)
        tempmaskmask = int(tempmaskmask.upper().replace('0', '1').replace('X', '0'), 2)
        self.mask = tempmask
        self.maskmask = tempmaskmask
    
    def _initinstr(self, setdata):
        tempinstrlist = re.findall(r'mem\[(\d+)\] = (\d+)', setdata)
        self.instrlist = [(int(x), int(y)) for x, y in tempinstrlist]
        self.numinstr = len(self.instrlist)
    
    def execute(self):
        #returns a list of tuples. memory address , data
        tempmems = [(add, self.mask & (self.maskmask | ((~self.maskmask)&)) ) for add, data in self.instrlist]



def readdata():
    with open(r'.\Day14\input.txt') as thefile:
        rawinput = thefile.read().strip()

    #split up the data into chunks including the mask and the instructions
    return re.findall(r"mask.+(?:\nmem\[\d+\] = \d+)+", rawinput)

dataset = [instructiongroup(thisgroup) for thisgroup in readdata()]

