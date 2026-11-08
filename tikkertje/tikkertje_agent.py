import torch
import random
import numpy as np
from collections import deque
from tikkertje_game import Tikkertje
#from model import Linear_QNet, QTrainer
#from helper import plot
from datetime import datetime
import pygame
import numpy as np
import sys
import math

MAX_MEMORY = 100_000	#aantal items die kunnen worden opgeslagen
BATCH_SIZE = 1000	#
LR = 0.001	#a.k.a. α

game = Tikkertje()

class Agent:

	def __init__(self):
		self.n_games = 0 	#aantal games die zijn gespeeld
		self.epsilon = 0	#randomness rate
		self.gamma = 0.9 	#discount rate, balances immediate rewards with future rewards
		self.memory = deque(maxlen=MAX_MEMORY)	#popleft() d.w.z. als memory te groot wordt word deel ervan verwijderd
#		self.model = #Linear_QNet(11, 256, 3)	#11 inputs, 256 hidden, 3 outputs
#		self.trainer = #QTrainer(self.model, lr=LR, gamma=self.gamma)

	def get_state_r(self):
		rcoord = (2*game.renner.x)*(2*game.renner.y+1)
		jcoord = (2*game.jager.x)*(2*game.jager.y+1)
		rvel = game.richting_r[1]
		jvel = game.richting_j[1]
		if game.richting_r[0] == 'Noord': rdir = 0
		if game.richting_r[0] == 'Zuid': rdir = 1
		if game.richting_r[0] == 'Oost': rdir = 2
		if game.richting_r[0] == 'West': rdir = 3

		if game.richting_j[0] == 'Noord': jdir = 0
		if game.richting_j[0] == 'Zuid': jdir = 1
		if game.richting_j[0] == 'Oost': jdir = 2
		if game.richting_j[0] == 'West': jdir = 3
		touch = int(game.renner.colliderect(game.muur))

		state = [	# 7 inputs
			rcoord, jcoord,
			rvel, jvel,
			rdir, jdir,
			touch]

		print(state)

		return np.array(state, dtype=int)

agent = Agent()

if __name__ == '__main__':
	agent.get_state_r()
	print(state)