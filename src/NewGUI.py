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
		self.field_height = self.field_width = 500
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
		self.demo.model.text.delete('1.0', END)
		self.demo.model.text.print("clicked at %d %d \n" % ( int(event.x), int(event.y)), 1)
		KB = self.demo.get_KB_from_click(int(event.x), int(event.y))
		self.demo.model.text.print_KB(KB)

	def add_mouse_listener(self):
		self.app_canvas.bind("<Button-1>", self.mouse_callback)

	def build_canvas(self):
		#instantiate 
		self.app_canvas = Canvas(self, width=self.field_width,height=self.field_height)
		self.text_canvas = Canvas(self, width=500,height=500)
		self.button_canvas = Canvas(self, width=50,height=500)
		self.text_button_canvas = Canvas(self, width=50,height=40)
		
		#give demo class pointers to the GUI
		self.demo.canvas = self.app_canvas
		self.demo.model.setText(TextCanvas(self.text_canvas))
		

	def add_buttons(self):
		## TODO, make labels and entryfields in seperate canvases

		## create canvasses for each of the entry fields
		self.numplanes_entry_canvas = Canvas(self.button_canvas)
		self.numplanes_entry_canvas.pack(side=TOP)
		self.numturrets_entry_canvas = Canvas(self.button_canvas)
		self.numturrets_entry_canvas.pack(side=TOP)
		self.turret_range_canvas = Canvas(self.button_canvas)
		self.turret_range_canvas.pack(side=TOP)
		self.turret_confidence_canvas = Canvas(self.button_canvas)
		self.turret_confidence_canvas.pack(side=TOP)
		self.numepochs_entry_canvas = Canvas(self.button_canvas)
		self.numepochs_entry_canvas.pack(side=TOP)
		self.failprob_entry_canvas = Canvas(self.button_canvas)
		self.failprob_entry_canvas.pack(side=TOP)
		self.sim_speed_entry_canvas = Canvas(self.button_canvas)
		self.sim_speed_entry_canvas.pack(side=TOP)
		self.protocol_entry_canvas = Canvas(self.button_canvas)
		self.protocol_entry_canvas.pack(side=TOP)

		## create text for in the labels
		self.numPlanes_text = StringVar()
		self.numPlanes_text.set(  "Number of planes:\t\t")
		self.numTurrets_text = StringVar()
		self.numTurrets_text.set( "Number of turrets:\t\t")
		self.turret_range_text = StringVar()
		self.turret_range_text.set( "Turret range:\t\t\t")
		self.turret_conf_text = StringVar()
		self.turret_conf_text.set( "Turret confidence threshold:\t")
		self.numEpochs_text = StringVar()
		self.numEpochs_text.set("Number of epochs:\t\t")
		self.failprob_text = StringVar()
		self.failprob_text.set(   "Failure probability:\t\t")
		self.speed_text = StringVar()
		self.speed_text.set("Simulation speed (iter/second)\t")
		self.protocol_text = StringVar()
		self.protocol_text.set("Communication protocol:\t\t\t\t")


		## create labels
		self.numplanes_label = Label(self.numplanes_entry_canvas, textvariable=self.numPlanes_text)
		self.numplanes_label.pack(side=LEFT)
		self.numturrets_label = Label(self.numturrets_entry_canvas, textvariable=self.numTurrets_text)
		self.numturrets_label.pack(side=LEFT)
		self.turret_range_label = Label(self.turret_range_canvas, textvariable=self.turret_range_text)
		self.turret_range_label.pack(side=LEFT)
		self.turret_confidence_label = Label(self.turret_confidence_canvas, textvariable=self.turret_conf_text)
		self.turret_confidence_label.pack(side=LEFT)
		self.numepochs_label = Label(self.numepochs_entry_canvas, textvariable=self.numEpochs_text)
		self.numepochs_label.pack(side=LEFT)
		self.failprob_label = Label(self.failprob_entry_canvas, textvariable=self.failprob_text)
		self.failprob_label.pack(side=LEFT)
		self.speed_label = Label(self.sim_speed_entry_canvas, textvariable=self.speed_text)
		self.speed_label.pack(side=LEFT)
		self.protocol_label = Label(self.protocol_entry_canvas, textvariable=self.protocol_text)
		self.protocol_label.pack(side=LEFT)

		## create entry fields
		self.numplanes_entry = Entry(self.numplanes_entry_canvas)
		self.numplanes_entry.pack(side=LEFT)
		self.numturrets_entry = Entry(self.numturrets_entry_canvas)
		self.numturrets_entry.pack(side=LEFT)
		self.turret_range_entry = Entry(self.turret_range_canvas)
		self.turret_range_entry.pack(side=LEFT)
		self.turret_conf_entry = Entry(self.turret_confidence_canvas)
		self.turret_conf_entry.pack(side=LEFT)
		self.numepochs_entry = Entry(self.numepochs_entry_canvas)
		self.numepochs_entry.pack(side=LEFT)
		self.failprob_entry = Entry(self.failprob_entry_canvas)
		self.failprob_entry.pack(side=LEFT)
		self.sim_speed_entry = Entry(self.sim_speed_entry_canvas)
		self.sim_speed_entry.pack(side=LEFT)

		## set default values in the fields
		self.numplanes_entry.insert(0, 1)
		self.numturrets_entry.insert(0, 3)
		self.turret_range_entry.insert(0, self.demo.turret_range)
		self.turret_conf_entry.insert(0, self.demo.model.turret_enemy_threshold)
		self.numepochs_entry.insert(0, 20)
		self.failprob_entry.insert(0, 0.1)
		self.sim_speed_entry.insert(0, 10)
		
		## create buttons for updating with callback function
		self.update_planes = Button(self.numplanes_entry_canvas, text = "Update", command = self.update_demo_planes)
		self.update_planes.pack(side=LEFT)
		self.update_turrets = Button(self.numturrets_entry_canvas, text = "Update", command = self.update_demo_turrets)
		self.update_turrets.pack(side=LEFT)
		self.update_turret_range = Button(self.turret_range_canvas, text = "Update", command = self.update_turret_range)
		self.update_turret_range.pack(side=LEFT)
		self.update_turret_confidence = Button(self.turret_confidence_canvas, text = "Update", command = self.update_turret_confidence)
		self.update_turret_confidence.pack(side=LEFT)
		self.update_epochs = Button(self.numepochs_entry_canvas, text = "Update", command = self.update_demo_max_epoch_counter)
		self.update_epochs.pack(side=LEFT)
		self.update_failprob = Button(self.failprob_entry_canvas, text = "Update", command = self.update_demo_failprob)
		self.update_failprob.pack(side=LEFT)
		self.update_speed = Button(self.sim_speed_entry_canvas, text = "Update", command = self.update_simulation_speed)
		self.update_speed.pack(side=LEFT)

		## create radio button for switching between modes
		self.mode_val = StringVar()
		self.mode1 = Radiobutton(self.protocol_entry_canvas, text="A1", variable=self.mode_val, value="A1", indicatoron=0, command = self.update_protocol).pack(side=LEFT)
		self.mode2 = Radiobutton(self.protocol_entry_canvas, text="TCP", variable=self.mode_val, value="TCP", indicatoron=0, command = self.update_protocol).pack(side=LEFT)
		self.mode_val.set("A1")

		## create speed control canvas + buttons
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

		##  create text panel buttons
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

	def update_protocol(self):
		self.demo.model.set_protocol(self.mode_val.get())

	def update_demo_max_epoch_counter(self):
		try:
			new_num = int(self.numepochs_entry.get())
			if new_num > 1:
				self.demo.model.numepochs = new_num
			else:
				print("Maximum number of messages must be > 1")
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

	def update_turret_range(self):
		try: 
			new_num = int(self.turret_range_entry.get())
			if new_num > 0:
				self.demo.turret_range = new_num
			else:
				print("Turret range must be > 0")
		except:
			pass

	def update_turret_confidence(self):
		try: 
			new_num = int(self.turret_conf_entry.get())
			if new_num > 0:
				self.demo.model.turret_enemy_threshold = new_num
			else:
				print("Turret confidence must be > 0")
		except:
			pass

	def update_demo_failprob(self):
		try:
			new_num = float(self.failprob_entry.get())
			if new_num > 0.0 and new_num <= 1.0:
				self.demo.model.failprob = new_num
			else:
				print("Failprob has to be within [0.0, 1.0]")
		except:
			pass

	def update_simulation_speed(self):
		try:
			new_num = float(self.sim_speed_entry.get())
			new_num = 1.0/new_num
			if new_num > 0:
				self.demo.sim_speed = new_num
			else:
				print("Speed must be larger than 0")
		except:
			pass


if __name__ == "__main__":
	demo = Demo()
	window=Tk()
	f = GUI(window, demo)
