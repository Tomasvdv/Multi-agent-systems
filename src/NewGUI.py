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
from message_manager import Message_manager
class GUI(Frame):
	def __init__(self, master, demo):
		Frame.__init__(self, master)

		self.buttonwidth = 40
		self.buttonheight = 40

		self.demo = demo

		self.build_canvas()
		self.add_buttons()

		self.add_mouse_listener()

		self.button_canvas.pack(side=LEFT, expand=True)
		self.app_canvas.pack(side=LEFT)
		self.text_button_canvas.pack(side=BOTTOM)
		self.text_canvas.pack(side=LEFT)
		self.pack(expand=True)
		self.update()

	def mouse_callback(self, event):
		self.demo.text.print("clicked at %d %d" % ( int(event.x), int(event.y)), 1)
		KB = self.demo.get_KB_from_click(int(event.x), int(event.y))
		self.demo.text.print_KB(KB)

	def add_mouse_listener(self):
		self.app_canvas.bind("<Button-1>", self.mouse_callback)



	def build_canvas(self):
		#instantiate 
		self.app_canvas = Canvas(self, width=500,height=500)
		self.text_canvas = Canvas(self, width=500,height=500)
		self.button_canvas = Canvas(self, width=50,height=500)
		self.text_button_canvas = Canvas(self, width=50,height=40)
		
		#give demo class pointers to the GUI
		self.demo.canvas = self.app_canvas
		self.demo.text = TextCanvas(self.text_canvas)
		self.demo.statistics = Statistics(self.demo.text)
		self.demo.message_manager = Message_manager(self.demo.text)

	def add_buttons(self):
		## TODO, make labels and entryfields in seperate canvases

		self.numplanes_entry_canvas = Canvas(self.button_canvas)
		self.numplanes_entry_canvas.pack(side=TOP)
		self.numturrets_entry_canvas = Canvas(self.button_canvas)
		self.numturrets_entry_canvas.pack(side=TOP)
		self.numPlanes_text = StringVar()
		self.numPlanes_text.set("Number of planes:")
		self.numTurrets_text = StringVar()
		self.numTurrets_text.set("Number of turrets:")
		self.numplanes_label = Label(self.numplanes_entry_canvas, textvariable=self.numPlanes_text)
		self.numplanes_label.pack(side=LEFT)
		self.numturrets_label = Label(self.numturrets_entry_canvas, textvariable=self.numTurrets_text)
		self.numturrets_label.pack(side=LEFT)
		self.numplanes_entry = Entry(self.numplanes_entry_canvas, text="numplanes")
		self.numplanes_entry.pack(side=LEFT)
		self.numturrets_entry = Entry(self.numturrets_entry_canvas, text="numturrets")
		self.numturrets_entry.pack(side=LEFT)


		self.update_planes = Button(self.button_canvas, text = "Update planes", command = self.update_demo_planes)
		self.update_planes.pack(side=TOP)
		self.update_turrets = Button(self.button_canvas, text = "Update turrets", command = self.update_demo_turrets)
		self.update_turrets.pack(side=TOP)


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

		self.statistics_button = Button(self.text_button_canvas, command=self.demo.statisics_handler, text = "Show statistics")
		self.statistics_button.pack(side = LEFT)

		self.turret_kb_button = Button(self.text_button_canvas, command=self.demo.turret_kb_handler, text = "Show knowledge base")
		self.turret_kb_button.pack(side = LEFT)

		self.messages_button = Button(self.text_button_canvas, command=self.demo.messages_handler, text = "Show messages")
		self.messages_button.pack(side = LEFT)

	def load_button_art(self, path):
		button_img = Image.open(path)
		button_img = button_img.resize((self.buttonwidth,self.buttonheight), Image.ANTIALIAS)
		button_img = ImageTk.PhotoImage(button_img)
		return button_img


	def update_demo_planes(self):
		try:
			new_num = int(self.numplanes_entry.get())
			if new_num > 1:
				self.demo.numPlanes = new_num
			else:
				print("Number of planes must be > 1")
		except:
			pass

	def update_demo_turrets(self):
		try:
			new_num = int(self.numturrets_entry.get())
			if new_num > 1:
				self.demo.numTurrets = new_num
			else:
				print("Number of turrets must be > 1")
		except:
			pass


if __name__ == "__main__":
	demo = Demo()
	window=Tk()
	f = GUI(window, demo)
