'''
Tic Tac Toe with tkinter module
Human player and artificial player with Minimax algorithm

Author : Ghali Boucetta (Netero)
Date : 21/06/2019
'''

import tkinter as tk
from players import *
from basics import *

window = tk.Tk()

game = Game(window)

window.mainloop()

