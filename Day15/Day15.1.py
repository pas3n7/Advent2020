#note, solution is for part 1 and 2, depending on numtostop

numtostop = 30000000
numbers = [0,12,6,13,20,1,17]
allnums = numbers
lastnum = numbers[-1]

numcount = len(numbers) -1

numbers = {num:index for index, num in enumerate(numbers[:-1]) }




while numcount < numtostop - 1: #need to exit one early, we know what the last number will be before we add it. 
		try:
			newnum = numcount - numbers[lastnum]
		except KeyError:
			newnum = 0
		numbers.update({lastnum : numcount})
		numcount += 1
		# if numcount % 10000 == 0:
		# 	print(numcount, end='\r')
		allnums.append(newnum)
		lastnum = newnum
print(lastnum)