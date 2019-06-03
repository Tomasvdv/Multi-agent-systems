import numpy as np
from agent import Agent

class Turret(Agent):
	def __init__(self, name, x, y, model):
		Agent.__init__(self, name, x, y, model)
		self.agents = [t for t in model.turrets if t.name != self.name]
		self.tracked_planes = []
		self.turret_range = 2

	def run_epoch(self):
		#resend possibly missed messages
		self.update()

		#check for any new planes
		for plane in self.model.planes:
			if np.linalg.norm(self.pos - plane.pos) <= self.turret_range and plane.isvisible: #plane is visible and in range of the turret
				if plane not in self.tracked_planes: #plane is not yet being tracked
					print("turret %s spotted plane %s at loc (%d, %d)" % (self.name, plane.name, plane.pos[0], plane.pos[1]))

					#tell other turrets that there is a plane
					self.broadcast("plane at %d %d" % (plane.pos[0], plane.pos[1]))
					self.tracked_planes.append(plane)

					#send message to plane
					self.send_new_message(plane, "indentify")
				else:
					#check if there was a message from the plane
					for (message, identifier, sender) in self.received_messages:
						if sender == plane and "not_friendly" in message:
							self.shoot(plane)

	def shoot(self, plane):
		if np.linalg.norm(self.pos - plane.pos) <= self.turret_range+0.5: #plane is in range of the turret
			print("\nPLANE DESTROYED!\n")
			if not plane.isdestroyed:
				print("plane %s shot down by %s" % (plane.name, self.name))
				plane.destroy()
				self.broadcast("%s destroyed" % (plane.name))
				self.tracked_planes.remove(plane)
		else:
			print("plane %s out of range of %s" % (plane.name, self.name))