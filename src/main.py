import numpy as np
from PIL import Image
from PIL import ImageTk
import time
from tkinter import *
from demo import Demo


SPEED = 0.1 #0.5

if __name__ == '__main()__':

	demo = Demo()
	window = Tk()
	f = GUI(window, demo)

	while True:
		if demo.running:
			demo.drawState()
		time.sleep(SPEED)
		window.update_idletasks()
		window.update()
		demo.text.text_window.update_idletasks()
		demo.text.text_window.update()
		if demo.paused == True:
			demo.running = False
		if demo.step == True:
			demo.running = False
