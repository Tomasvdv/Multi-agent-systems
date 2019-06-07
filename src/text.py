import numpy as np
from tkinter import *

class TextCanvas(Text): #text is already a tkinter class. 
	def __init__(self,canvas):
		Text.__init__(self, canvas)
		# self.text_window = window
		self.text_canvas = canvas#Canvas(self.text_window, width=1000, height=1000, bg = 'white')
		# self.text_canvas.grid(row=0,column=0,columnspan=2)
		# self.text_canvas.update()
		# self.text_position = 50
		self.insert(INSERT, "---Hello world---")
		self.pack()

	def print(self,message,color):
		# self.text_canvas.create_text(400,self.text_position,fill=color, font="Times 12 italic bold",
  #                       text= message)
		# self.text_position += 50
		# if self.text_position > 450:
		# 	self.text_canvas.delete("all")
		# 	self.text_position = 50

		self.insert(END, str(message + "\n"))

	def print_KB(self, KB):
		for fact in KB:
			self.print(str(fact), 0)