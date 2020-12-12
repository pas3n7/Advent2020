from collections import Counter
with open(r'.\Day10\input.txt') as thefile:

    adapters = [int(x) for x in thefile.read().strip().split('\n')]

adapters.append(0)
adapters.sort()
adapters.append(3 + adapters[len(adapters) - 1])
differences = []

last = None
for i in adapters:
	if last is not None:
		differences.append(i-last)
	last = i

counts = Counter(differences)
print(counts[1]*(counts[3]))
print(zip(adapters, differences))
print(Counter(differences))