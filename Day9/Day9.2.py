with open(r'.\Day9\input.txt') as thefile:

    thedata = [int(x) for x in thefile.read().strip().split('\n')]

NUM_TO_SEARCH = 675280050

minset = 2
maxset = 200
datalen = len(thedata)
Foundnum = False #this is probably sloppy, idk
smallnum = 0
bignum = 0

for i in range(minset, maxset + 1):
	setlen = i
	for startwith in range(0, datalen - setlen + 1):  #where we will start the sum(). Need the plus 1 to include the final index, range and below set are not inclusive
		if sum(thedata[startwith:(startwith + setlen)]) == NUM_TO_SEARCH:
			smallnum = min(thedata[startwith:(startwith + setlen - 1)])
			bignum = max(thedata[startwith:(startwith + setlen - 1)])
			Foundnum = True
			break
	if Foundnum:
		break

print(smallnum, " ", bignum, " sum:", smallnum + bignum)
