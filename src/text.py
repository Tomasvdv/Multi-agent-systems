'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Handles showing text regarding the knowledge of turrets.  
'''
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
		self.insert(END, str(message + "\n"))
		self.pack()

	def remove(self):
		self.delete(1.0,END)

	def print_KB(self, KB):
		for fact in KB:
			self.print(str(fact), 0)