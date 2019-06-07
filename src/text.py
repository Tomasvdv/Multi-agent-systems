import numpy as np
from tkinter import *

class Text():
	def __init__(self,window):
		self.text_window = window
		self.text_canvas = Canvas(self.text_window, width=700, height=700, bg = 'white')
		self.text_canvas.grid(row=0,column=0,columnspan=2)
		self.text_canvas.update()
		self.text_position = 50

	def print(self,message,color):
		self.text_canvas.create_text(400,self.text_position,fill=color, font="Times 12 italic bold",
                        text= message)
		self.text_position += 50
		if self.text_position > 450:
			self.text_canvas.delete("all")
			self.text_position = 50