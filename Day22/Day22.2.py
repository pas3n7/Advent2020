#fn = r'.\Day22\testinput.txt'
fn = r'.\Day22\input.txt'


with open(fn) as thefile:
	p1, p2 = thefile.read().strip().split('\n\n')
p1, p2 = map(lambda x : x.split('\n')[1:], (p1, p2))
p1, p2 = map(lambda y : [int(x) for x in y], (p1, p2))


def statehash(p1deck, p2deck):
	return int(''.join([str(x) for x in p1deck+p2deck]))

def gamestate(p1card, p2card, p1deck, p2deck, gameround, gamedepth):
	toprint = "\n-- Round {round} (Game {depth}) -- \nPlayer1 Deck: {p1d}\nPlayer2 Deck: {p2d}\nPlayer1 Plays: {p1}\nPlayer2 Plays: {p2}"
	return toprint.format(round = gameround, depth = gamedepth, p1d = p1deck, p2d = p2deck, p1 = p1card, p2=p2card)


	


def game(p1deck, p2deck, gamedepth=0):
	gameround = 0
	gameover = False
	gamehistory = []
	while len(p1deck) > 0 and len(p2deck) > 0 and gameover == False:
		p1wins = False
		p2wins = False
		startinghash = statehash(p1deck, p2deck)
		if startinghash in gamehistory: #rule #1
			p1wins = True
			gameover = True
		else:
			p1card, p2card= p1deck.pop(0), p2deck.pop(0)
		# print(gamestate(p1card, p2card, p1deck, p2deck, gameround, gamedepth))
		#print("game: " + str(gamedepth) + "   round: " + str(gameround) + " size of history: " + str(len(gamehistory)), end="\r")
		if not gameover:
			if len(p1deck) >= p1card and len(p2deck) >= p2card:
				#print("Playing a subgame to determine round winner")
				subwinner, _ = game(p1deck[:p1card], p2deck[:p2card], gamedepth+1)  #don't need the deck of the winner
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
				#print("Player1 Wins!")
			elif p2wins:
				p2deck.extend((p2card, p1card))
				#print("Player2 Wins!")
			else:
				print("Oh no, nobody won")
		gamehistory.append(startinghash)
		gameround += 1


	if gameover or p1deck>p2deck:
		#only way we set gameover true is if something matched in the game history, p1 wins
		winner = 1
		winnerdeck = p1deck
		#print("Player 1 wins game " + str(gamedepth))
	else:
		winner = 2
		winnerdeck = p2deck
		#print("Player 2 wins game " + str(gamedepth))

	return winner, winnerdeck

def calcscore(deck):
	def scoregen(deck):
		i=1
		for c in deck:
			yield c*i
			i+=1
	return sum(scoregen(reversed(deck)))


#####################################Do things ####################################

winner, winnerdeck = game(p1, p2)

print("player " + str(winner) + " wins!")
print("score: " + str(calcscore(winnerdeck)))
print("winning deck: " + str(winnerdeck))
