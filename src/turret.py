import numpy as np
from agent import Agent
from model import Kripke_model
from text import Text
class Turret(Agent):
	def __init__(self, name, x, y, model):
		Agent.__init__(self, name, x, y, model)
		Kripke_model.__init__(self)
		self.agents = [t for t in model.turrets if t.name != self.name]
		self.tracked_planes = []
		self.turret_range = 2

	def run_epoch(self,text):
		#resend possibly missed messages
		self.update(text)

		#check for any new planes
		for plane in self.model.planes:
			print (self.name, plane.name, self.pos, plane.pos, np.linalg.norm(self.pos - plane.pos))
			if np.linalg.norm(self.pos - plane.pos) <= (self.turret_range + 0.5) and plane.isvisible: #plane is visible and in range of the turret

				if plane not in self.tracked_planes: #plane is not yet being tracked
					self.last_message = ("turret %s spotted plane %s at loc (%d, %d)" % (self.name, plane.name, plane.pos[0], plane.pos[1]))
					text.print(self.last_message,'red')
					#tell other turrets that there is a plane
					self.broadcast("plane at %d %d" % (plane.pos[0], plane.pos[1]),text)
					self.tracked_planes.append(plane)

					#send message to plane
					self.send_new_message(plane, "indentify",text)
				else:
					#check if there was a message from the plane
					for (message, identifier, sender) in self.received_messages:
						self.to_model()
						if sender == plane and "not_friendly" in message:
							text.print(Agent.printKB(self),'green')
							#self.shoot(plane,text)
							pass

	def shoot(self, plane, text):
		if np.linalg.norm(self.pos - plane.pos) <= self.turret_range+0.5: #plane is in range of the turret
			print("\nPLANE DESTROYED!\n")

			if not plane.isdestroyed:
				print("plane %s shot down by %s" % (plane.name, self.name))
				plane.destroy()
				self.broadcast("%s destroyed" % (plane.name),text)
				self.tracked_planes.remove(plane)
		else:
			print("plane %s out of range of %s" % (plane.name, self.name))