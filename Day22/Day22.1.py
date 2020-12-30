# fn = r'.\Day22\testinput.txt'
fn = r'.\Day22\input.txt'


with open(fn) as thefile:
	p1, p2 = thefile.read().strip().split('\n\n')
p1, p2 = map(lambda x : x.split('\n')[1:], (p1, p2))
p1, p2 = map(lambda y : [int(x) for x in y], (p1, p2))

while len(p1) > 0 and len(p2) > 0:
	thisround = p1.pop(0), p2.pop(0)
	if thisround[0] > thisround[1]:
		p1.extend(thisround)
	else:
		p2.extend(reversed(thisround))


def scoregen(deck):
	i=1
	for c in deck:
		yield c*i
		i+=1
print(sum(scoregen(reversed(max(p1, p2)))))