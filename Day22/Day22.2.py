# fn = r'.\Day22\testinput.txt'
fn = r'.\Day22\input.txt'

from copy import deepcopy


with open(fn) as thefile:
	p1, p2 = thefile.read().strip().split('\n\n')
p1, p2 = map(lambda x : x.split('\n')[1:], (p1, p2))
p1, p2 = map(lambda y : [int(x) for x in y], (p1, p2))

# debugprint = print

def debugprint(a, *args, **kwargs):
	pass

def statehash(p1deck, p2deck):
	return int(''.join([str(x) for x in p1deck+p2deck]))

def gamestate(p1card, p2card, p1deck, p2deck, gameround, gamedepth):
	toprint = "\n-- Round {round} (Game {depth}) -- \nPlayer1 Deck: {p1d}\nPlayer2 Deck: {p2d}\nPlayer1 Plays: {p1c}\nPlayer2 Plays: {p2c}"
	return toprint.format(round = gameround, depth = gamedepth, p1d = p1deck, p2d = p2deck, p1c = p1card, p2c=p2card)


def game(p1deck, p2deck, gamedepth=0):
	gameround = 0
	gameover = False
	gamehistory = []
	while len(p1deck) > 0 and len(p2deck) > 0 and gameover == False:
		p1wins = False
		p2wins = False
		startinghash = int(''.join([str(x) for x in p1deck+p2deck]))
		if startinghash in gamehistory: #rule #1
			p1wins = True
			gameover = True
			break
		else:
			p1card, p2card= p1deck[0], p2deck[0]
			p1deck = p1deck[1:]
			p2deck = p2deck[1:]
		debugprint(gamestate(p1card, p2card, p1deck, p2deck, gameround, gamedepth))
		#debugprint("game: " + str(gamedepth) + "   round: " + str(gameround) + " size of history: " + str(len(gamehistory)), end="\r")
		if not gameover:
			if len(p1deck) >= p1card and len(p2deck) >= p2card:
				debugprint("Playing a subgame to determine round winner")
				subwinner, _ = game(p1deck.copy()[:p1card+1], p2deck.copy()[:p2card+1], gamedepth+1)  #don't need the deck of the winner
				if subwinner == 1:
					p1wins = True
				else:
					p2wins = True
			elif p1card > p2card:
				p1wins = True
			else:
				p2wins = True
		
			if p1wins:
				p1deck.extend((p1card, p2card))
				debugprint("Player1 Wins!")
			elif p2wins:
				p2deck.extend((p2card, p1card))
				debugprint("Player2 Wins!")
			else:
				print("Oh no, nobody won")
		gamehistory.append(startinghash)
		gameround += 1


	if gameover or len(p2deck)==0:
		#only way we set gameover true is if something matched in the game history, p1 wins
		winner = 1
		winnerdeck = p1deck
		debugprint("Player 1 wins game " + str(gamedepth))
	elif len(p1deck) == 0:
		winner = 2
		winnerdeck = p2deck
		debugprint("Player 2 wins game " + str(gamedepth))
	else:
		print("oh no, nobody won the game")

	return winner, winnerdeck

def calcscore(deck):
	def scoregen(deck):
		i=1
		for c in deck:
			yield c*i
			i+=1
	return sum(scoregen(reversed(deck)))


#####################################Do things ####################################
print(len(p1), len(p2))
winner, winnerdeck = game(p1.copy(), p2.copy())
print(len(p1), len(p2))

print("player " + str(winner) + " wins!")
print("score: " + str(calcscore(winnerdeck)))
print("winning deck: " + str(winnerdeck))
