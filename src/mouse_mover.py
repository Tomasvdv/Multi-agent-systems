'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Redundant code
'''

from tkinter import *
from PIL import ImageTk, Image

class mouseMover():
  
	def __init__(self):
		self.item = 0; self.previous = (0, 0)
		self.x = 0; self.y =0;

		
	def select(self, event):
		widget = event.widget                       # Get handle to canvas 
		# Convert screen coordinates to canvas coordinates

		xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
		self.item = widget.find_closest(xc, yc)[0]        # ID for closest
		self.x = xc
		self.y = yc
		