#### okay, just recreate the test case to see if I understand this

SUBJECTNUM = 7
DIVISOR = 20201227

TESTPUBKEYS = 5764801, 17807724


PUBKEYS = TESTPUBKEYS


currentkey = 1
loopnum = 1
while loopnum < 100:  ##just stop infinite loops
	currentkey = (currentkey * SUBJECTNUM) % DIVISOR
	print(currentkey)
	if currentkey in PUBKEYS:
		print("Reached the public key: ", currentkey, " with loop #", loopnum)
		break
	loopnum+=1

otherpubkey = [key for key in PUBKEYS if key != currentkey][0]

print(otherpubkey)

privkey = 1
for loop in range(loopnum):
	privkey = (privkey * otherpubkey) % DIVISOR
	print(loop)

print(privkey)
