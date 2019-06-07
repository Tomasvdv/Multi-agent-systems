from text import Text
class Statistics():

	def __init__(self,text):
		self.friendly_planes_generated = 0
		self.enemy_planes_generated = 0
		self.friendly_planes_shot = 0
		self.enemy_planes_shot = 0
		self.text = text

	def showStatistics(self):
		self.text.refresh = 0
		self.text.text_canvas.delete("all")
		self.text.text_position = 50
		color = 'black'
		self.text.print("Statistics",color)
		self.text.print("Total of planes generated: "+str(self.friendly_planes_generated + self.enemy_planes_generated),color)
		self.text.print("Friendly planes generated: "+str(self.friendly_planes_generated),color)
		self.text.print("Enemy planes generated: "+str(self.enemy_planes_generated),color)
		self.text.print("Friendly planes shot: "+str(self.friendly_planes_shot),color)
		self.text.print("Enemy planes shot: "+str(self.enemy_planes_shot),color)
