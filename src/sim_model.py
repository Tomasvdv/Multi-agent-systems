'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Constructs a model of the scene with turrets and planes. 
'''
import random
import numpy as np
from plane import Plane
from turret import Turret
from statistics import Statistics
from message_manager import Message_manager
from message_sender import Message_sender
class Model:
	def __init__(self):
		self.turret_enemy_threshold = 2 #Number of turrets that need to identify a plane as enemy before any of the turrets start to shoot
		self.turrets = []
		self.planes = []
		self.connections = []
		self.failprob = 0.1
		self.numepochs = 20
		self.draw_shots = False
		self.messageprotocol = 'A1'
		self.message_manager = Message_manager(self)
		self.message_sender = Message_sender(self)
		# self.text

	## allows for some late binding to the gui
	def setText(self, text):
		self.text = text

	def set_protocol(self, protocol):
		if protocol == self.messageprotocol: ## do nothing
			return
		elif protocol == 'A1' or protocol == 'TCP': ## set protocol
			# for agent in self.turrets:
			# 	agent.inbox = []
			# 	agent.confirmed = {}
			# for agent in self.planes:
			# 	agent.inbox = []
			# 	agent.confirmed = {}
			[agent.empty_messages() for agent in self.turrets]
			[agent.empty_messages() for agent in self.planes]
			self.messageprotocol = protocol


			



	def getKB():
		kb = {}
		for t in self.turrets:
			kb[t.name] = t.knowledge

		for p in planes:
			kb[p.name] = p.knowledge			

	def add_turret(self, name, x, y):
		new_turret = Turret(name, x, y, self)
		#add connections to existing turrets
		for t in self.turrets:
			t.agents.append(new_turret)
			self.add_connection(t, new_turret)

		#add turret to set of turrets
		self.turrets.append(new_turret)

	def add_plane(self, name, x, y, dx, dy, isfriendly):
		self.planes.append(Plane(name, x, y, dx, dy, isfriendly, self))

	def add_connection (self, turret1, turret2):
		self.connections.append((turret1, turret2))

	def run_epoch(self,statistics):
		for t in self.turrets:
			t.run_epoch(statistics,self.numepochs)

		for p in self.planes:
			p.run_epoch()



if __name__ == "__main__":

	m = Model()
	# m.add_turret("A", 0, 1)
	# m.add_turret("B", 1, 0)
	# m.add_turret("C", 1, 1)

	# m.add_plane("P", 0, 6, 0, -1, False) #plane spawns south of the turrets, moves north

	# for idx in range(10):
	# 	# m.turrets[0].broadcast("plane")
	# 	m.run_epoch()