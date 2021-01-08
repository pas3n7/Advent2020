#### okay, just recreate the test case to see if I understand this

SUBJECTNUM = 7
DIVISOR = 20201227

TESTPUBKEYS = 5764801, 17807724
PUZPUBKEYS = 10705932, 12301431

PUBKEYS = PUZPUBKEYS


currentkey = 1
loopnum = 1
while loopnum < 100_000_000:  ##just stop infinite loops
	currentkey = (currentkey * SUBJECTNUM) % DIVISOR
	if currentkey in PUBKEYS:
		print("Reached the public key: ", currentkey, " with loop #", loopnum)
		break
	loopnum+=1

otherpubkey = [key for key in PUBKEYS if key != currentkey][0]

print("Other public key: ", otherpubkey)

encrkey = 1
for loop in range(loopnum):
	encrkey = (encrkey * otherpubkey) % DIVISOR

print("Private Key: ", encrkey)
