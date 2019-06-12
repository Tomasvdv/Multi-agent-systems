class Message_manager:

	def __init__(self,text):
		self.text = text
		self.tracked_plane = ""
		self.counter = 0
		self.messages =[]

	def set_tracked(self,name):
		self.tracked = name
		self.counter = 0
		self.remove()
	
	def print(self):
		for message in self.messages:
			self.text.print(message,"")
		self.messages = []

	def add_message(self,text):
		self.messages.append(text)
		self.counter += 1

	def remove(self):
		for idx in range(0,self.counter):
			self.text.remove()
		self.messages = []
		self.counter = 0