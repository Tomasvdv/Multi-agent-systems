from text import Text
class Statistics():

	def __init__(self,text = ""):
		self.friendly_planes_generated = 0
		self.enemy_planes_generated = 0
		self.friendly_planes_shot_epoch_counter = 0
		self.enemy_planes_shot_no_reponse = 0
		self.text = text
		self.init = 1

	def showStatistics(self):
		if self.init != 1:
			self.text.remove()
		self.sentence = "Statistics \nTotal of planes generated: "+str(self.friendly_planes_generated + self.enemy_planes_generated)+"\nFriendly planes generated: "+str(self.friendly_planes_generated)+"\nEnemy planes generated: "+str(self.enemy_planes_generated)+ "\nFriendly planes shot max epochs: "+str(self.friendly_planes_shot_epoch_counter)+"\nEnemy planes shot no reponse: "+str(self.enemy_planes_shot_no_reponse)
		self. init = 0
		self.text.print(self.sentence,"")