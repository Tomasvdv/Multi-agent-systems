'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Handles the movement, existence and message sending of turrets.
					A turret is an air defense unit that is able to shoot down planes fly in its range.
					Superclass of Agent. 
'''

import numpy as np
from agent import Agent
from model import Kripke_model

class Turret(Agent):
	def __init__(self, name, x, y, model):
		Agent.__init__(self, name, x, y, model)
		Kripke_model.__init__(self)
		self.agents = [t for t in model.turrets if t.name != self.name]
		self.tracked_planes = []
		self.turret_range = 2

	def run_epoch(self,message_manager,statistics):
		#resend possibly missed messages
		self.update(message_manager)

		#check for any new planes
		for plane in self.model.planes:
			print (self.name, plane.name, self.pos, plane.pos, np.linalg.norm(self.pos - plane.pos))
			if np.linalg.norm(self.pos - plane.pos) <= (self.turret_range + 0.5) and plane.isvisible: #plane is visible and in range of the turret

				if plane not in self.tracked_planes: #plane is not yet being tracked
					# print("turret %s spotted plane %s at loc (%d, %d)" % (self.name, plane.name, plane.pos[0], plane.pos[1]))

					#tell other turrets that there is a plane
					self.broadcast("plane at %d %d" % (plane.pos[0], plane.pos[1]),message_manager)
					self.tracked_planes.append(plane)

					#send message to plane
					self.send_new_message(plane, "indentify",message_manager)
				else:
					#check if there was a message from the plane
					for (message, identifier, sender) in self.received_messages:
						self.to_model()
						if sender == plane and not "friendly" in message:
							print(plane.isfriendly)
							self.shoot(plane,statistics,message_manager)
								

	def shoot(self, plane, statistics,message_manager):
		if np.linalg.norm(self.pos - plane.pos) <= self.turret_range+0.5: #plane is in range of the turret
			print("\nPLANE DESTROYED!\n")

			if not plane.isdestroyed:
				print("plane %s shot down by %s" % (plane.name, self.name))
				plane.destroy()
				if plane.isfriendly == False:
					statistics.enemy_planes_shot += 1
				else:
					statistics.friendly_planes_shot += 1
				self.broadcast("%s destroyed" % (plane.name),message_manager)
				self.tracked_planes.remove(plane)
		
