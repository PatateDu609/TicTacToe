'''
Player classes and the copy function

	- copy(game): copy a list of 3 lists of 3 elements
	- the class Player:
		- __init__(game, symbol): initialize the human player to make him play when the function play is called
		- play(event): principal function of the class, it make the player a player... it takes in parameter the event.
	- the class PlayerMinMax:
		- __init__(game, symbol): initialize the human player to make him play when the function play is called
		- play(): principal function of the class, it make the player an AI
		- test(a, b, c): compare a, b and c to the symbol of the player, when we have a position favorable to the player it returns 5 and -5 when it's not. If it's favorable to anybody so it returns 0
		- eval(game, end, canContinue): evaluate the game. It returns a tuple (max, min) where max is the player and min it's opponent.
		- max(game, depht) and min(game, depht): they are used to simulate the choice of a player.
			- max is going to maximize the first element of the eval term and minimize the second. It calls min for each child node and take the maximum child
			- min do the exact opposite
		- possibleMoves(game, symbol): generate the possible child nodes from a situation given in parameter.
		- play(): call max and put the starter depht at self.depht
'''



from random import randint
import math

def copy(game):
	result = []
	for i in range(3):
		result.append([])
		for j in range(3):
			result[i].append(game[i][j])
	return result

class Player:

	def __init__(self, game, symbol):
		self.game = game
		self.symbol = symbol
		self.w = self.game.w
		self.h = self.game.h
		self.squareW = self.game.squareW
		self.squareH = self.game.squareH
	
	def play(self, event):
		played = False
		if event.x < 1 * self.squareW:
			x = 0
		elif event.x < 2 * self.squareW:
			x = 1
		else:
			x = 2

		if event.y < 1 * self.squareH:
			y = 0
		elif event.y < 2 * self.squareH:
			y = 1
		else:
			y = 2

		if self.game.game[x][y] == None and self.game.playable:
			played = True
			self.game.game[x][y] = self.symbol
			if self.symbol == "cross":
				self.game.cross(x, y)
			else:
				self.game.circle(x, y)

		result = self.game.end(self.game.game)
		if result == "cross":
			print("Player 1 won")
			self.game.playable = False
		elif result == "circle":
			print("Player 2 won")
			self.game.playable = False
		else:
			if self.game.canContinue(self.game.game) == False:
				print("Tie")
				self.game.playable = False

		if played == True:
			self.game.player += 1


class PlayerMinMax(Player):

	def __init__(self, game, symbol, depht):
		Player.__init__(self, game, symbol)

		self.depht = depht

		if self.symbol == "cross":
			self.other = "circle"
		else:
			self.other = "cross"
	
	def possibleMoves(self, game, symbol):
		result = []

		for i in range(3):
			for j in range(3):
				if game[i][j] == None:
					temp = copy(game)
					temp[i][j] = symbol
					result.append(temp)

		return result

	def test(self, a, b, c):
		if a == None and b == c == self.symbol \
			or b == None and a == c == self.symbol \
			or c == None and a == b == self.symbol:
			return 5
		elif a == None and b == c == self.other \
			or b == None and a == c == self.other \
			or c == None and a == b == self.other:
			return -5
		else:
			return 0

	def eval(self, game, end, canContinue):
		if end == self.symbol:
			return (1000, -1000)
		elif end == self.other:
			return (-1000, 1000)
		elif canContinue == False:
				return (0, 0)

		tMax = 0
		tMin = 0
		
		if self.test(game[0][0], game[0][1], game[0][2]) == 5:
			tMax += 5
		if self.test(game[1][0], game[1][1], game[1][2]) == 5:
			tMax += 5
		if self.test(game[2][0], game[2][1], game[2][2]) == 5:
			tMax += 5
		if self.test(game[0][0], game[1][0], game[2][0]) == 5:
			tMax += 5
		if self.test(game[0][1], game[1][1], game[2][1]) == 5:
			tMax += 5
		if self.test(game[0][2], game[1][2], game[2][2]) == 5:
			tMax += 5
		if self.test(game[0][0], game[1][1], game[2][2]) == 5:
			tMax += 5
		if self.test(game[0][2], game[1][1], game[2][0]) == 5:
			tMax += 5


		if self.test(game[0][0], game[0][1], game[0][2]) == -5:
			tMin += 5
		if self.test(game[1][0], game[1][1], game[1][2]) == -5:
			tMin += 5
		if self.test(game[2][0], game[2][1], game[2][2]) == -5:
			tMin += 5
		if self.test(game[0][0], game[1][0], game[2][0]) == -5:
			tMin += 5
		if self.test(game[0][1], game[1][1], game[2][1]) == -5:
			tMin += 5
		if self.test(game[0][2], game[1][2], game[2][2]) == -5:
			tMin += 5
		if self.test(game[0][0], game[1][1], game[2][2]) == -5:
			tMin += 5
		if self.test(game[0][2], game[1][1], game[2][0]) == -5:
			tMin += 5
		
		return (tMax, tMin)

	def max(self, game, depht):
		end = self.game.end(game)
		canContinue = self.game.canContinue(game)
		if depht == 0 or end != False or canContinue == False: #Test if it's the end of game or if we reached the maximal depht
			return self.eval(game, end, canContinue)
		else:
			u = (-8000, 8000)
			a = None
			moves = self.possibleMoves(game, self.symbol)
			same = []

			for i in range(len(moves)):
				tMin = self.min(moves[i], depht - 1)
				if i > 0 and tMin == u:
					same.append(moves[i])
				if tMin[0] > u[0] and tMin[1] < u[1]:
					a = moves[i]
					u = tMin
					same = [a]

			if same != [a]:
				i = randint(0, len(same) - 1)
				self.actualMax = moves[i]
			else:
				self.actualMax = a
			
			return u

	def min(self, game, depht):
		end = self.game.end(game)
		canContinue = self.game.canContinue(game)
		if depht == 0 or end != False or canContinue == False:
			return self.eval(game, end, canContinue)
		else:
			u = (8000, -8000)
			a = None
			moves = self.possibleMoves(game, self.other)

			for i in range(len(moves)):
				tMax = self.max(moves[i], depht - 1)
				if i > 0 and tMax == u:
					same.append(moves[i])
				if tMax[0] < u[0] and tMax[1] > u[1]:
					a = moves[i]
					u = tMax
					same = [a]

			if same != [a]:
				i = randint(0, len(same) - 1)
				self.actualMax = moves[i]
			else:
				self.actualMax = a

			return u
	
	def play(self):
		print("Player 2 Thinking")
		self.max(self.game.game, self.depht)
		move = self.actualMax
		for i in range(3):
			for j in range(3):
				if self.game.game[i][j] != move[i][j]:
					x = i
					y = j

		if self.symbol == "cross":
			self.game.cross(x, y)
			self.game.game[x][y] = "cross"
		else:
			self.game.circle(x, y)
			self.game.game[x][y] = "circle"

		result = self.game.end(self.game.game)
		if result == "cross":
			print("Player 1 won")
			self.game.playable = False
		elif result == "circle":
			print("Player 2 won")
			self.game.playable = False
		else:
			if self.game.canContinue(self.game.game) == False:
				print("Tie")
				self.game.playable = False

		self.game.player += 1