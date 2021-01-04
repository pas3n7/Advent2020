import time

testinput = True

if not testinput:
	#real input
	input = "219347865"
else: 
	#test input
	input = "389125467"
input = [int(i) for i in input]

###idk, let's just try brute forcing it
mil = 1000000
numtoextendto = 9
nummoves = 10

def move(cups, nummoves):
	def numgen(direction):
		numr = len(cups) + 1
		numl = numtoextendto
		while True and numl > numr and numl > 0 and numr < numtoextendto:
			if direction == 1:
				yield numr
				numr += 1
			if direction == -1:
				yield numl
				numl -= 1
		else:
			yield None
	cups.extend(range(len(cups)+1, numtoextendto+1))
	move = 0
	selectedindex = 0
	while move < nummoves:
		print(cups, end='\n')
		time.sleep(.25)
		stack = []
		target = cups[selectedindex] -1 
		tomoveindex = selectedindex + 1
		for i in range(3):
			tomoveindex = tomoveindex % (numtoextendto - i)
			stack.insert(0, (cups.pop(tomoveindex)))
		while target in stack or target == 0:
			if target == 0:
				target = numtoextendto
			target = target - 1

		targetindex = cups.index(target) % (numtoextendto - 2 )

		for i in stack:
			cups.insert(targetindex+1, i) #insert to the right of target
		print("selected", cups[selectedindex], "destination", target, "dest index", targetindex, "stack", list(reversed(stack)))
		#iterate, move over by 4 if we put the 3 new ones to the right
		print(selectedindex)
		if targetindex < selectedindex:
			selectedindex = (selectedindex+4) % numtoextendto
		else:
			selectedindex = (selectedindex+1) % numtoextendto
		move+= 1



		



# import cProfile
# import re
# cProfile.run('move(input, nummoves)')

move(input, nummoves)

def solforp2(cups):
	oneindex = cups.index(1)
	nums = cups[(oneindex+1)%numtoextendto] , cups[(oneindex+2)%numtoextendto]
	return nums

print(solforp2(input))