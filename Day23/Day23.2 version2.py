from collections import deque

testinput = True

if not testinput:
	#real input
	input = "219347865"
else: 
	#test input
	input = "389125467"
input = deque([int(i) for i in input])

###idk, let's just try brute forcing it
mil = 1000000
numtoextendto = 9
nummoves = 100# 10 * numtoextendto
input.extend(range(max(input) + 1, numtoextendto + 1))

def move(cups, nummoves):
	for _ in range(nummoves):
		stack = deque()
		cups.rotate(-1)
		nexttarget = input[-1] -1
		for _ in range(3):
			stack.append(cups.popleft())
		while nexttarget == 0 or nexttarget in stack:
			nexttarget = nexttarget - 1
			if nexttarget == -1:
				nexttarget = numtoextendto
		#print("destination", nexttarget, end='\r')
		nexttarget = cups.index(nexttarget)
		#rotate, extend, rotate back
		cups.rotate(-(nexttarget+1))
		cups.extend(stack)
		cups.rotate(nexttarget+4)
		


move(input, nummoves)


print('\n')

def solforp2(cups):
	oneindex = cups.index(1)
	nums = cups[(oneindex+1)%numtoextendto] , cups[(oneindex+2)%numtoextendto]
	return nums

print(solforp2(input))