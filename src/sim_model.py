import random
import numpy as np
from plane import Plane
from turret import Turret

class Model:
	def __init__(self):
		self.turrets = []
		self.planes = []
		self.connections = []

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

		#add turret to set of turrets
		self.turrets.append(new_turret)

	def add_plane(self, name, x, y, dx, dy, isfriendly):
		self.planes.append(Plane(name, x, y, dx, dy, isfriendly, self))

	def add_connection (self):
		idx = len(self.turrets)-1
		name1 = self.turrets[idx-1]
		name2 = self.turrets[idx]
		self.connections.append((name1,name2))

	def run_epoch(self):
		for t in self.turrets:
			t.run_epoch()

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