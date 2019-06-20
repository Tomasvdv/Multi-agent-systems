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
		#Kripke_model.__init__(self)
		self.agents = [t for t in model.turrets if t.name != self.name]
		self.tracked_planes = []
		self.turret_range = 2
		self.broadcasted_pos = False
		self.closest = False
		self.planecounters = {} ## dict of planes with a counter for each plane
		self.max_message_count = 20
		self.max_epochs = 4
		self.shoot_plane = False

	def determine_closest_turret(self,plane):
		for (message, identifier, sender) in self.received_messages:
			if 'x' and 'y' in message:
				for idx in range(0,len(message)):
					if message[idx] == 'x':
						x = int(message [idx+1])
						y = int(message [idx+3])
						pos = np.array((x, y))
						if np.linalg.norm(pos - plane.pos) <= (self.turret_range + 0.5):
							self.send_new_message(sender,"shoot"+plane.name)
							return
							# print("broadcast: "+str(sender.name)+ "is closest to "+plane.name)
		
	def update_plane_knowledge(self,plane):
		self.planecounters[plane] += 1 ## set nr of messages sent to 1
		self.knowledge.add("K_"+str(self.name)+"("+str(plane.name)+"is in sight for "+str(self.planecounters[plane])+"epochs)")

	#Verifies how many turrets have decided that a particular plane should be shot
	def verify_turret_identifications(self, shoot_command):
		count = 0
		for turret in self.model.turrets:
			if shoot_command in turret.knowledge:
				count += 1
		print("COUNT: ", count)
		return count

	def run_epoch(self, statistics):
		if not self.broadcasted_pos:
			self.broadcast(str(self.name) + "x"+ str(self.x) + "y"+ str(self.y))
			self.broadcasted_pos = True

		#resend possibly missed messages
		self.update()
		#check for any new planes
		for plane in self.model.planes:
			reason = ""
			# print (self.name, plane.name, self.pos, plane.pos, np.linalg.norm(self.pos - plane.pos))
			if np.linalg.norm(self.pos - plane.pos) <= (self.turret_range + 0.5) and plane.isvisible: #plane is visible and in range of the turret

				if plane not in self.tracked_planes: #plane is not yet being tracked
					# print("turret %s spotted plane %s at loc (%d, %d)" % (self.name, plane.name, plane.pos[0], plane.pos[1]))

					#tell other turrets that there is a plane
					self.broadcast("plane at %d %d" % (plane.pos[0], plane.pos[1]))
					self.tracked_planes.append(plane)


					#send message to plane
					self.send_new_message(plane, "indentify")
					self.planecounters[plane] = 1 ## set nr of messages sent to 1
				
				else:
					self.update_plane_knowledge(plane)
					#check if there was a message from the plane
					for (message, identifier, sender) in self.received_messages:
						# print(message)
						self.to_model()
											
						
						if sender == plane and  "key"+str(plane.name) in message  and not "K_%s(indentified as friendly)" % self.name in self.knowledge:
							self.send_new_message(plane, "indentified as friendly")
						
						if sender == plane:
							if "" in message:
								reason = "no response"
							if "K_"+str(self.name)+"("+str(plane.name)+"is in sight for "+str(self.max_epochs)+"epochs)" in self.knowledge:
								reason = "max epochs"

							if not "K_%s(friendly)" % plane.name in self.knowledge or "" in message or "K_"+str(self.name)+"("+str(plane.name)+"is in sight for "+str(self.max_epochs)+"epochs)" in self.knowledge :
									self.determine_closest_turret(plane)
				shoot_command = "shoot"+str(plane.name)
				#Shoot will be done in next round, first draw shots
				if self.shoot_plane and (shoot_command in self.knowledge): #Last check is in case a plane crashed into the side of the window
					self.shoot(plane,statistics,reason)
				self.shoot_plane = (shoot_command in self.knowledge) and (self.verify_turret_identifications(shoot_command) >= self.model.turret_enemy_threshold)
				if self.shoot_plane:
					self.model.draw_shots = True
			

	def shoot(self, plane, statistics,reason):
		if np.linalg.norm(self.pos - plane.pos) <= self.turret_range+0.5: #plane is in range of the turret
			print("\nPLANE DESTROYED!\n")

			if not plane.isdestroyed:
				print("plane %s shot down by %s. Reason: %s" % (plane.name, self.name, reason))
				plane.destroy()
				for turret in self.model.turrets:
					turret.clean_up_messages(plane)
				self.model.draw_shots = False
				if plane.isfriendly == False and reason is "max epochs":
					statistics.enemy_planes_shot_epoch_counter += 1
				else:
					statistics.enemy_planes_shot_no_reponse += 1
				if plane.isfriendly == True:
					statistics.friendly_planes_shot_epoch_counter +=1
					self.broadcast("Identification of %s took too long" % (plane.name))
				
				self.broadcast("%s destroyed" % (plane.name))
				self.tracked_planes.remove(plane)
		
