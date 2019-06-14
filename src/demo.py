'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Constructs a demo. Handles the information that is shown in the GUI. 
					This information includes: location of planes and turrets, shooting range
					of the turrets.
'''

from tkinter import *
from PIL import ImageTk, Image
import math
import random
import numpy as np
from mouse_mover import mouseMover
from plane import Plane
from turret import Turret
from sim_model import Model
from text import TextCanvas
import time
from PIL import Image
from PIL import ImageTk
from statistics import Statistics

TURRET_RANGE = 3
NUMBER_TURRETS = 3

class Demo():

	def __init__(self):
		self.sim_speed = 0
		self.init = 1
		self.turretCounter = 0
		self.planeCounter = 0
		self.numPlanes = 1
		self.numTurrets = 3
		self.nummessages = 20
		# self.lines = []
		self.model = Model()
		self.statistics = Statistics()
		# self.demospeed = SPEED
		self.paused = True
		self.step = False
		self.running = True
		self.show_statistics = False
		self.get_kb = False
		self.show_messages = False
	# Function to make the play buttion function 
	def play_handler(self):
		print("RUN SIMULATION")
		self.paused = False
		self.step = False
		self.running = True

	#Function to retrieve the knowledge base of a specific turret selected on screen
	def get_KB_from_click(self, x_click, y_click):
		if self.get_kb:
			cellwidth = self.canvas.cellwidth
			cellheight = self.canvas.cellheight
			for t in self.model.turrets:
				(x, y) = t.pos
				if x * cellwidth < x_click and (x+1) * cellwidth > x_click and \
				   y * cellheight < y_click and (y+1) * cellheight > y_click:
					return t.knowledge
		return []

	def turret_kb_handler(self):
		self.show_statistics = False
		self.statistics.text.remove()
		self.get_kb = True

	def messages_handler(self):
		print("MESSAGE ")
		self.get_kb = False
		self.show_statistics = False
		self.statistics.text.remove()
		self.show_messages= True
		self.message_manager.print()

	#Function to pause the simulation with the pause button
	def pause_handler(self):
		print("PAUSED HANDLER")
		self.paused = True
	
	#Function to run the simulation step by step
	def step_handler(self):
		print("STEP HANDLER")
		self.step = True
		self.drawState()
	
	def statisics_handler(self):
		self.show_statistics = True
		self.statistics.text.remove()
		self.get_kb = False
		self.show_messages = False
		self.statistics.showStatistics()

    #Function to round fload n to the closest integer number
	def getClosestTile(n):
		n = math.floor(n)
		return n

	def create_circle(self,x, y, r, canvas): #center coordinates, radius
	    x0 = x - r
	    y0 = y - r
	    x1 = x + r
	    y1 = y + r
	    return canvas.create_oval(x0, y0, x1, y1)
	#Function to load all the images needed for the simulation
	def loadTextures(self,cellwidth,cellheight):
		self.canvas.flak = Image.open("flak.jpg")
		self.canvas.flak = ImageTk.PhotoImage(self.canvas.flak.resize((cellwidth, cellheight), Image.ANTIALIAS))
		self.canvas.land = Image.open("land.jpg")
		self.canvas.land = ImageTk.PhotoImage(self.canvas.land.resize((cellwidth, cellheight), Image.ANTIALIAS))
		self.canvas.airplane = Image.open("plane.jpg")
		self.canvas.airplane = ImageTk.PhotoImage(self.canvas.airplane.resize((cellwidth,cellheight), Image.ANTIALIAS))
		self.canvas.friendly = Image.open("friendly.jpg")
		self.canvas.friendly = ImageTk.PhotoImage(self.canvas.friendly.resize((cellwidth,cellheight), Image.ANTIALIAS))
	
	#Function to initialize a plane with a random starting direction. It can be either a friendly or an enemy plane
	def initializePlane(self):
		friendly = random.random()
		dx = 0
		dy = 0
		row = random.randint(1,9)
		if random.random() >= 0.5:
			col = 9
			dy = -1
		else:
			col = 0
			dy = 1
		if col == 0:
			dx = 1
		else:
			dx = -1

		if random.random() < 0.25:
			dx = 0
		elif random.random() < 0.25:
			dy = 0
		#leaves 50% chance that the plane will go diagonal

		cellwidth = self.canvas.cellwidth
		cellheight = self.canvas.cellheight
		name = "Plane_" + str(self.planeCounter)
		# 75% change of being an enemy plane
		if friendly > 0.25:
			self.model.add_plane(name, col, row, dx, dy, False)
			self.statistics.enemy_planes_generated += 1
			self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.airplane,anchor=NW)
		else:
			self.model.add_plane(name, col, row, dx, dy, True)
			self.statistics.friendly_planes_generated += 1 
			self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.friendly,anchor=NW)
		self.planeCounter += 1
		print(name + " added")
		self.message_manager.set_tracked(name)

	#Function to initialize the simulation	
	def drawState(self):
		w=self.canvas.winfo_width()
		h=self.canvas.winfo_height()

		cellwidth = w//10	
		cellheight=h//10
		self.canvas.cellheight = cellheight
		self.canvas.cellwidth = cellwidth
		
		if self.init ==1:
			self.previousX = -1
			self.previousY = -1
			self.init = 0
			counter = 0
			self.loadTextures(cellwidth,cellheight)
			
		
			#draw background
			for row in range(10):
				for col in range(10):
					self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.land,anchor=NW)
			

			#init and draw turrets
			for idx in range(self.numTurrets):
				row = random.randint(0,9)
				col = random.randint(0,9)
				name = "Turret_" + str(self.turretCounter)
				self.model.add_turret(name,col,row)
				self.model.turrets[idx].turret_range = TURRET_RANGE
				self.canvas.create_image(col*cellwidth,row*cellheight,image= self.canvas.flak,anchor=NW)
				self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, self.model.turrets[idx].turret_range*cellheight, self.canvas)
				self.turretCounter += 1
				turret = self.model.turrets[idx]

			#init and draw planes
			for _ in range(self.numPlanes):
				self.initializePlane()								
		else:
			self.drawStep()

	#Function to update the number of turrets according to the ammount defined at the user interface. It either adds or deletes turrets and their connextions based on the ammount specified by the user.
	def update_turrets(self, add_amount):
		w=self.canvas.winfo_width()
		h=self.canvas.winfo_height()
		cellwidth = w//10	
		cellheight=h//10

		# Add turrets
		if add_amount > 0:
			for idx in range(add_amount):
				row = random.randint(0,9)
				col = random.randint(0,9)
				name = "Turret_" + str(self.turretCounter)
				self.model.add_turret(name,col,row)
				self.model.turrets[idx].turret_range = TURRET_RANGE
				self.canvas.create_image(col*cellwidth,row*cellheight,image= self.canvas.flak,anchor=NW)
				self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, self.model.turrets[idx].turret_range*cellheight, self.canvas)
				self.turretCounter += 1
				turret = self.model.turrets[idx]

				# Add and draw turret connections
				for turret1, turret2 in self.model.connections:
					(x1, y1) = turret1.pos
					(x2, y2) = turret2.pos
					x1 = (x1 + 0.5) * cellwidth
					x2 = (x2 + 0.5) * cellwidth
					y1 = (y1 + 0.5) * cellheight
					y2 = (y2 + 0.5) * cellheight
					self.canvas.create_line(x1,y1,x2,y2,fill='red',width = 5)
		
		# Delete turrets and connections
		if add_amount < 0:
			for idx in range(abs(add_amount), -1, -1): #In reverse order, since turrets are removed. Otherwise we get a list index overflow
				new_connections = []
				# print("TURRET: ", len(self.model.turrets), idx)
				turret = self.model.turrets[idx]
				
				for idx, (tur1, tur2) in enumerate(self.model.connections):
					if not (tur1 == turret or tur2 == turret):
						new_connections.append((tur1, tur2))
				self.model.turrets.remove(turret)
				self.model.connections = new_connections

   #Function to draw each step of the simulation.
	def drawStep(self):
		flag = 0
		self.statistics.text.remove()
		self.message_manager.remove()
		counter = self.statistics.friendly_planes_shot
		self.model.run_epoch(self.nummessages,self.message_manager,self.statistics)
		
		if self.statistics.friendly_planes_shot > counter:
			print("friendly plane shot ")
			self.messages_handler()
			self.pause_handler()

		self.canvas.delete("all")
		
		if self.show_statistics:
			self.statistics.showStatistics()

		if self.show_messages == True:
			self.message_manager.print()


		# print("HERE: ", self.numTurrets, len(self.model.turrets), self.numTurrets - len(self.model.turrets))
		self.update_turrets(self.numTurrets - len(self.model.turrets))

		while len(self.model.planes) < self.numPlanes:
			self.initializePlane()
			# Empty the knowledge base of the turrets, new plane is added
			for turret in self.model.turrets:
				turret.knowledge = set([])

		cellheight = self.canvas.cellheight
		cellwidth = self.canvas.cellwidth

		#draw background
		for row in range(10):
			for col in range(10):
				self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.land,anchor=NW)


		for turret1, turret2 in self.model.connections:
			(x1, y1) = turret1.pos
			(x2, y2) = turret2.pos

			x1 = (x1 + 0.5) * cellwidth
			x2 = (x2 + 0.5) * cellwidth
			y1 = (y1 + 0.5) * cellheight
			y2 = (y2 + 0.5) * cellheight

			self.canvas.create_line(x1,y1,x2,y2,fill='red',width = 5)

		self.drawPlanes()
		
		#draw turrets
		for turret in self.model.turrets:
			(col, row) = turret.pos
			self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.flak,anchor=NW)
			self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, turret.turret_range*cellheight, self.canvas)
		self.draw_shots(cellwidth)

	#Function to draw each plane on the canvas after each step.
	def drawPlanes(self):
		cellwidth  = self.canvas.cellwidth	
		cellheight = self.canvas.cellheight

		for plane in self.model.planes:
			col = plane.pos[0]
			row = plane.pos[1]
			
			if not plane.isfriendly:
				self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.airplane,anchor=NW)
			else:
				self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.friendly,anchor=NW)

	#Function which draws the blue dotted lines to indicate a turret is shooting at the connected plane.
	def draw_shots(self, cellwidth):
		for turret in self.model.turrets:
			for plane in self.model.planes:
				if np.linalg.norm(turret.pos - plane.pos) <= turret.turret_range and not plane.isfriendly:
					x1 = (turret.pos[0] + 0.5)*cellwidth
					y1 = (turret.pos[1] + 0.5)*cellwidth
					x2 = (plane.pos[0] + 0.5)*cellwidth
					y2 = (plane.pos[1] + 0.5)*cellwidth
					print(x1, x2, y1, y2)
					self.canvas.create_line(x1,y1,x2,y2,fill='blue',width = 5, dash=(4,4))

#This is used for testing the demo.py file
if __name__ == '__main__':
	demo = Demo()
	window=Tk()
	top = Toplevel()
	mm = mouseMover()
	demo.canvas = Canvas(window, width=500,height=500)
	demo.text = Text(top)

	width = 40
	height = 40

	play_img = Image.open("../img/play.png")
	play_img = play_img.resize((width,height), Image.ANTIALIAS)
	play_img =  ImageTk.PhotoImage(play_img)

	pause_img = Image.open("../img/pause.png")
	pause_img = pause_img.resize((width,height), Image.ANTIALIAS)
	pause_img =  ImageTk.PhotoImage(pause_img)

	ff_img = Image.open("../img/ff.png")
	ff_img = ff_img.resize((width,height), Image.ANTIALIAS)
	ff_img =  ImageTk.PhotoImage(ff_img)

	demo.canvas.grid(row=0,column=0,columnspan=2)
	#demo.canvas.draw1=Button(window,text="Run simulation", command=demo.button_handler, image)
	demo.canvas.draw1=Button(window, command=demo.button_handler, image=play_img)
	demo.canvas.draw1.grid(row=1,column=2)
	demo.canvas.draw2=Button(window, command=demo.pause_handler, image=pause_img)
	demo.canvas.draw2.grid(row=1,column=3)
	demo.canvas.draw3=Button(window, command=demo.step_handler, image=ff_img)
	demo.canvas.draw3.grid(row=1,column=4)

	demo.canvas.update()
	demo.drawState()

