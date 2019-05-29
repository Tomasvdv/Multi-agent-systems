import numpy as np
from agent import Agent

TURRET_RANGE = 0

class Turret(Agent):
	def __init__(self, name, x, y, model):
		Agent.__init__(self, name, x, y, model)
		self.agents = [t for t in model.turrets if t.name != self.name]
		self.tracked_planes = []

	def run_epoch(self):
		#resend possibly missed messages
		self.update()

		#check for any new planes
		for plane in self.model.planes:
			if np.linalg.norm(self.pos - plane.pos) <= TURRET_RANGE and plane not in self.tracked_planes: #plane is in range of the turret
				self.broadcast("plane at %d %d" % (plane.pos[0], plane.pos[1]))
				self.tracked_planes.append(plane)