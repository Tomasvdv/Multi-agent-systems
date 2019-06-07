'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		This class handles the GUI for interaction between the user and the program. 
'''

from demo import Demo
from text import TextCanvas
import time
from tkinter import *
from PIL import Image
from PIL import ImageTk
from statistics import Statistics
class GUI(Frame):
	def __init__(self, master, demo):
		Frame.__init__(self, master)

		self.buttonwidth = 40
		self.buttonheight = 40

		self.demo = demo

		self.build_canvas()
		self.add_buttons()

		self.button_canvas.pack(side=LEFT, expand=True)
		self.app_canvas.pack(side=LEFT)
		self.text_canvas.pack(side=LEFT)
		self.pack(expand=True)
		self.update()


	def build_canvas(self):
		#instantiate 
		self.app_canvas = Canvas(self, width=500,height=500)
		self.text_canvas = Canvas(self, width=500,height=500)
		self.button_canvas = Canvas(self, width=50,height=500)

		#give demo class pointers to the GUI
		self.demo.canvas = self.app_canvas
		self.demo.text = TextCanvas(self.text_canvas)
		self.demo.statistics = Statistics(self.demo.text)

	def add_buttons(self):
		## TODO, make labels and entryfields in seperate canvases

		self.numplanes_entry_canvas = Canvas(self.button_canvas)
		self.numplanes_entry_canvas.pack(side=TOP)
		self.numPlanes_text = StringVar()
		self.numPlanes_text.set("Number of planes:")
		self.numplanes_label = Label(self.numplanes_entry_canvas, textvariable=self.numPlanes_text)
		self.numplanes_label.pack(side=LEFT)
		self.numplanes_entry = Entry(self.numplanes_entry_canvas, text="numplanes")
		self.numplanes_entry.pack(side=LEFT)


		self.updatebutton = Button(self.button_canvas, text = "Update sim", command = self.update_demo_parameters)
		self.updatebutton.pack(side=TOP)


		self.speed_control_canvas = Canvas(self.button_canvas)
		self.speed_control_canvas.pack(side=BOTTOM)

		self.play_img = image=self.load_button_art("../img/play.png")
		self.play_button =Button(self.speed_control_canvas, command=self.demo.play_handler, image=self.play_img)
		self.play_button.pack(side=LEFT)


		self.pause_img = self.load_button_art("../img/pause.png")
		self.pause_button=Button(self.speed_control_canvas, command=self.demo.pause_handler, image= self.pause_img)
		self.pause_button.pack(side=LEFT)

		self.ff_img = self.load_button_art("../img/ff.png")
		self.ff_button=Button(self.speed_control_canvas, command=self.demo.step_handler, image=self.ff_img)
		self.ff_button.pack(side=LEFT)

	def load_button_art(self, path):
		button_img = Image.open(path)
		button_img = button_img.resize((self.buttonwidth,self.buttonheight), Image.ANTIALIAS)
		button_img = ImageTk.PhotoImage(button_img)
		return button_img


	def update_demo_parameters(self):
		try:
			self.demo.numPlanes = int(self.numplanes_entry.get())
		except:
			pass
			

if __name__ == "__main__":
	demo = Demo()
	window=Tk()
	f = GUI(window, demo)