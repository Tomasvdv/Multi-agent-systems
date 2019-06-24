class Message_manager:

	def __init__(self, model):
		self.model = model
		self.tracked_plane = ""
		self.counter = 0
		self.messages =[]

	def set_tracked(self,name):
		self.tracked = name
		self.counter = 0
		self.remove()
	
	def print(self):
		for message in self.messages:
			self.model.text.print(message,"")
		self.messages = []

	def add_message(self,message):
		self.messages.append(message)
		self.counter += 1

	def remove(self):
		for idx in range(0,self.counter):
			self.model.text.remove()
		self.messages = []
		self.counter = 0