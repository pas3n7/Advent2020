from collections import deque

testinput = False

if not testinput:
	#real input
	input = "219347865"
else: 
	#test input
	input = "389125467"
input = deque([int(i) for i in input])

largest = max(input)


def move(cups):
	stack = deque()
	cups.rotate(-1)
	nexttarget = input[-1] -1
	for _ in range(3):
		stack.append(cups.popleft())
	while nexttarget == 0 or nexttarget in stack:
		nexttarget = (nexttarget - 1) % 10
	print("destination", nexttarget)
	nexttarget = cups.index(nexttarget)
	#rotate, extend, rotate back
	cups.rotate(-(nexttarget+1))
	cups.extend(stack)
	cups.rotate(nexttarget+4)

nummoves = 100

for i in range(nummoves):
	move(input)
	# printable = input.copy()  #make a copy to rotate so printed output will align with example, for now
	# printable.rotate(1)
	# print(printable)
	print(input)

def orderforp1(cups):
	cups = cups.copy()
	cups.rotate(-cups.index(1))
	cups.popleft()
	return ''.join([str(x) for x in cups])

print(orderforp1(input))