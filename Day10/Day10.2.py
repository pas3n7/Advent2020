#thanks to https://pietroppeter.github.io/adventofnim/2020/day10hints.html for the hints (only needed the first 3, honest)

#after sorting, any sequence of numbers with difference 3 between them, have to be included in their original order. 
#By definition, the numbers between them must be a consecutive sequence of integers
#In the dataset given, no sequence of consecutive integers greater than count 3. 
#combos of those are 7 for runs of 3, 4 for runs of 2 and 2 for runs of 1
#difference between the higher number of a lower set of diff 3 group, and the lower number of the higher one is n+1 of the number of 'adapters' between them
# 0 is also a special case, first one has to be included.
#need to multiply all together in the end

from collections import Counter

def listdifferences(thelist):
	outputlist = []
	last = None
	for i in thelist:
		if last is not None:
			outputlist.append(i-last)
		last = i
	return outputlist



with open(r'.\Day10\input.txt') as thefile:

    adapters = [int(x) for x in thefile.read().strip().split('\n')]

adapters.append(0)
adapters.sort()
adapters.append(3 + adapters[len(adapters) - 1])
differences = listdifferences(adapters)




threeindicies = []
lastn = None
for index, n in enumerate(differences):
	if (n == 3 and lastn == 1) or lastn == 3: #account for the back side, want the index for all bordering a 3 diff
		threeindicies.append(index)

	lastn = n
threeindicies.insert(0, 0) #hacky garbage, accounting for the 0
threeindicies.append(len(adapters)-1)#last is the "device" and by definition 3 apart
print(threeindicies)
last = None
threedistances = []
for i in threeindicies:
	if last is not None and i-last > 1:
		threedistances.append(i-last -1)
	last = i

print(threedistances)

print(Counter(threedistances))
count = Counter(threedistances)

#lengths of 3 => 7 combos
#lengths of 2 => 4 combos
#lengths of 1 => 2 combos
combos = (7**count[3])*(4**count[2])*(2**count[1])
print(combos)