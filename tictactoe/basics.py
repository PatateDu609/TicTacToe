import tkinter as tk
from players import Player, PlayerMinMax

class TicTacToe:
	
	def __init__(self):
		self.game = [[None, None, None], [None, None, None], [None, None, None]]
		self.playable = True
		self.player = 0

	def end(self, game):
		if game[0][0] == "cross" and game[0][1] == "cross" and game[0][2] == "cross" \
		or game[1][0] == "cross" and game[1][1] == "cross" and game[1][2] == "cross" \
		or game[2][0] == "cross" and game[2][1] == "cross" and game[2][2] == "cross" \
		or game[0][0] == "cross" and game[1][0] == "cross" and game[2][0] == "cross" \
		or game[0][1] == "cross" and game[1][1] == "cross" and game[2][1] == "cross" \
		or game[0][2] == "cross" and game[1][2] == "cross" and game[2][2] == "cross" \
		or game[0][0] == "cross" and game[1][1] == "cross" and game[2][2] == "cross" \
		or game[2][0] == "cross" and game[1][1] == "cross" and game[0][2] == "cross":
			return "cross"
		elif game[0][0] == "circle" and game[0][1] == "circle" and game[0][2] == "circle" \
		or game[1][0] == "circle" and game[1][1] == "circle" and game[1][2] == "circle" \
		or game[2][0] == "circle" and game[2][1] == "circle" and game[2][2] == "circle" \
		or game[0][0] == "circle" and game[1][0] == "circle" and game[2][0] == "circle" \
		or game[0][1] == "circle" and game[1][1] == "circle" and game[2][1] == "circle" \
		or game[0][2] == "circle" and game[1][2] == "circle" and game[2][2] == "circle" \
		or game[0][0] == "circle" and game[1][1] == "circle" and game[2][2] == "circle" \
		or game[2][0] == "circle" and game[1][1] == "circle" and game[0][2] == "circle":
			return "circle"

		return False

	def canContinue(self, game):
		for i in range(3):
			for j in range(3):
				if game[i][j] == None:
					return True
		return False

class Game(TicTacToe):

	def __init__(self, window):
		TicTacToe.__init__(self)
		
		self.w, self.h = 600, 600
		self.squareW, self.squareH = self.w / 3, self.h / 3
		
		self.player1 = PlayerMinMax(self, "cross", 9)
		self.player2 = PlayerMinMax(self, "circle", 9)

		self.offset = 10
		self.canvas = tk.Canvas(window, width=self.w, height=self.h, background='white')
		self.canvas.bind("<Button-1>", self.play)

		self.drawBasics()
		self.canvas.pack()

	def cross(self, x, y):
		self.canvas.create_line(x * self.squareW + self.offset, y * self.squareH + self.offset, x * self.squareW + 200 - self.offset, y * self.squareH + 200 - self.offset)
		self.canvas.create_line(x * self.squareW + 200 - self.offset, y * self.squareH + self.offset, x * self.squareW + self.offset, y * self.squareH + 200 - self.offset)

	def circle(self, x, y):
		self.canvas.create_oval(x * self.squareW + self.offset, y * self.squareH + self.offset, x * self.squareW + 200 - self.offset, y * self.squareH + 200 - self.offset)

	def drawBasics(self):
		self.canvas.create_line(self.squareW, 0, self.squareW, self.h)
		self.canvas.create_line(2 * self.squareW, 0, 2 * self.squareW, self.h)

		self.canvas.create_line(0, self.squareH, self.w, self.squareH)
		self.canvas.create_line(0, 2 * self.squareH, self.w, 2 * self.squareH)

	def clean(self):
		self.canvas.delete("all")
		self.drawBasics()
		self.player = 0
		self.playable = True

		for i in range(3):
			for j in range(3):
				self.game[i][j] = None

	def play(self, event = -1):
		if self.player % 2 == 0:
			if type(self.player1) is Player:
				self.player1.play(event)
			else:
				self.player1.play()
		else:
			if type(self.player2) is Player:
				self.player2.play(event)
			else:
				self.player2.play()

		if self.playable == False:
			self.clean()