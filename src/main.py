'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		The main loop of the program. Handles play, pause and stop functionality 
					of the demo.
'''

from tkinter import *
import numpy as np
from PIL import Image
from PIL import ImageTk
import time
from demo import Demo
from NewGUI import GUI


SPEED = 0.1 #0.5

if __name__ == '__main__':

	demo = Demo()
	window = Tk()
	f = GUI(window, demo)
	while True:
		if demo.running:
			demo.drawState()
		time.sleep(SPEED)
		window.update_idletasks()
		window.update()
		# demo.text.text_window.update_idletasks()
		# demo.text.text_window.update()
		if demo.paused == True:
			demo.running = False
		if demo.step == True:
			demo.running = False
