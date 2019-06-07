from tkinter import *
from PIL import ImageTk, Image
import math
import random
import numpy as np
from mouse_mover import mouseMover
from plane import Plane
from turret import Turret
from sim_model import Model
from model import Kripke_model
from text import Text
import time

TURRET_RANGE = 3
SPEED = 1 #0.5
NUMBER_TURRETS = 3

class Demo():

	def __init__(self):

		self.init = 1
		self.turretCounter = 0
		self.planeCounter = 0;
		# self.lines = []
		self.model = Model()
		self.kripke = Kripke_model()

	def buttonhandler(self,event):
		self.drawState()

	def getClosestTile(n):
		n = math.floor(n)
		return n

	def create_circle(self,x, y, r, canvas): #center coordinates, radius
	    x0 = x - r
	    y0 = y - r
	    x1 = x + r
	    y1 = y + r
	    return canvas.create_oval(x0, y0, x1, y1)

	def loadTextures(self,cellwidth,cellheight):
		self.canvas.flak = Image.open("flak.jpg")
		self.canvas.flak = ImageTk.PhotoImage(self.canvas.flak.resize((cellwidth, cellheight), Image.ANTIALIAS))
		self.canvas.land = Image.open("land.jpg")
		self.canvas.land = ImageTk.PhotoImage(self.canvas.land.resize((cellwidth, cellheight), Image.ANTIALIAS))
		self.canvas.airplane = Image.open("plane.jpg")
		self.canvas.airplane = ImageTk.PhotoImage(self.canvas.airplane.resize((cellwidth,cellheight), Image.ANTIALIAS))
		self.canvas.friendly = Image.open("friendly.jpg")
		self.canvas.friendly = ImageTk.PhotoImage(self.canvas.friendly.resize((cellwidth,cellheight), Image.ANTIALIAS))
	
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
		if friendly > 0.25:
			self.model.add_plane(name, col, row, dx, dy, False)
			self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.airplane,anchor=NW)
		else:
			self.model.add_plane(name, col, row, dx, dy, True)
			self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.friendly,anchor=NW)
		self.planeCounter += 1
		print(name + " added")
		
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
			for idx in range (NUMBER_TURRETS):
				row = random.randint(0,9)
				col = random.randint(0,9)
				name = "Turret_" + str(self.turretCounter)
				self.model.add_turret(name,col,row)
				self.model.turrets[idx].turret_range = TURRET_RANGE
				self.canvas.create_image(col*cellwidth,row*cellheight,image= self.canvas.flak,anchor=NW)
				self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, self.model.turrets[idx].turret_range*cellheight, self.canvas)
				self.turretCounter += 1
				turret = self.model.turrets[idx]
				turret.kripke_knowledge[turret.name] = ['friendly', 'not_friendly']

			#init and draw planes
			self.initializePlane()								
		else:
			self.drawStep()
		# self.construct_kripke()


	def drawStep(self):
		flag = 0
		self.model.run_epoch(self.text)
		self.canvas.delete("all")

		if len(self.model.planes) == 0:
			self.initializePlane()
			for turret in self.model.turrets: #Previous plane crashed / was shot down. Create new KB
				turret.kripke_knowledge[turret.name] = ['friendly', 'not_friendly']

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

		self.drawPlanes(flag)
		
		#draw turrets
		for turret in self.model.turrets:
			(col, row) = turret.pos
			self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.flak,anchor=NW)
			self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, turret.turret_range*cellheight, self.canvas)
		self.draw_shots(cellwidth)
		# for turret in self.model.turrets:
		# 	print("\n")
		# 	print(turret.kripke_knowledge)
		# 	print("\n")

	def drawPlanes(self,flag):
		cellwidth = self.canvas.cellwidth	
		cellheight= self.canvas.cellheight
		if flag == 1:
			self.initializePlane()
		else:
			for plane in self.model.planes:
				col = plane.pos[0]
				row = plane.pos[1]
				print("row,col",row,col)
				if not plane.isfriendly:
					self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.airplane,anchor=NW)
				else:
					self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.friendly,anchor=NW)		

	def draw_shots(self, cellwidth):
		for turret in self.model.turrets:
			for plane in self.model.planes:
				if np.linalg.norm(turret.pos - plane.pos) <= turret.turret_range and not plane.isfriendly:
					print("SHOOT!")
					x1 = (turret.pos[0] + 0.5)*cellwidth
					y1 = (turret.pos[1] + 0.5)*cellwidth
					x2 = (plane.pos[0] + 0.5)*cellwidth
					y2 = (plane.pos[1] + 0.5)*cellwidth
					print(x1, x2, y1, y2)
					self.canvas.create_line(x1,y1,x2,y2,fill='blue',width = 5, dash=(4,4))
	
	def construct_kripke(self):
		all_knowlegde = []
		turret_names = []
		knowledge = []
		for turret in self.model.turrets:
			print(turret.kripke_knowledge)
			for key, val in turret.kripke_knowledge.items():
				if not val in all_knowlegde:
					all_knowlegde.append(val)
				if len(val) < 2:
					tup = (val[0], val[0])
				else:
					tup = tuple(val)
				knowledge.append(tup)
			turret_names.append(turret.name)
		print('knowledge: ', knowledge)
		print('turret names: ', turret_names)
		self.kripke.put_data_in_model(knowledge= knowledge, agent_names= turret_names)
		self.kripke.show_model()

demo = Demo()
window=Tk()
top = Toplevel()
mm = mouseMover()
demo.canvas = Canvas(window, width=500,height=500)
demo.text = Text(top)
demo.canvas.grid(row=0,column=0,columnspan=2)
demo.canvas.draw=Button(window,text="Draw")
demo.canvas.draw.grid(row=1,column=3)
demo.canvas.bind("<Button-1>", mm.select)
demo.canvas.draw.bind('<Button-1>',demo.buttonhandler)

demo.canvas.update()
demo.drawState()
running = True

while running:
	demo.drawState()
	time.sleep(SPEED)
	window.update_idletasks()
	window.update()
	demo.text.text_window.update_idletasks()
	demo.text.text_window.update()