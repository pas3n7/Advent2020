with open(r'.\Day9\input.txt') as thefile:

    thedata = [int(x) for x in thefile.read().strip().split('\n')]

class sumlist:
	def __init__(self, data):
		self.data = data
		self.sums = []
		
		for index, d in enumerate(self.data):
			if index == 0: #first in data has nothing to add to, will error at index-1
				continue 
			for i in range(max(index - 25, 0), index): #don't need index-1 because range isn't inclusive of the 2nd value
				#print("first looper ", d, " second looper", self.data[i], " index of first: ", index, " index of second ", i)
				summant = self.data[i]
				self.sums.append(d + summant)
		self.sums = set(self.sums)

		


thesums = sumlist(thedata).sums

for i in thedata[24:]:
	if not i in thesums:
		print(i, " is not valid")