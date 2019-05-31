from tkinter import *
from PIL import ImageTk, Image
import math
import random
import numpy as np
from mouse_mover import mouseMover

class Demo():

	def __init__(self):

		self.init = 1
		self.defenceCounter = 0
		self.lines = []
		

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

	def planeInRange(self):
		for dic in self.defences:
			if self.plane.get("row") <= dic.get("row")+2 and 	dic.get("row") -2 <= self.plane.get("row") and self.plane.get("col") <= dic.get("col")+2 and dic.get("col")-2 <= self.plane.get("col") :
				dic["plane in range"] = 1  
				print ("plane detected!")

	def loadTextures(self,cellwidth,cellheight):
		self.canvas.flak = Image.open("flak.jpg")
		self.canvas.flak = ImageTk.PhotoImage(self.canvas.flak.resize((cellwidth, cellheight), Image.ANTIALIAS))
		self.canvas.land = Image.open("land.jpg")
		self.canvas.land = ImageTk.PhotoImage(self.canvas.land.resize((cellwidth, cellheight), Image.ANTIALIAS))
		self.canvas.airplane = Image.open("plane.jpg")
		self.canvas.airplane = ImageTk.PhotoImage(self.canvas.airplane.resize((cellwidth,cellheight), Image.ANTIALIAS))

	def initializePlane(self):

		row = random.randint(1,3)
		col = random.randint(1,3)
		cellwidth = self.canvas.cellwidth
		cellheight = self.canvas.cellheight
		self.plane={
		"name": "plane1",
		"row": row,
		"col": col,
		"direction": random.randint(0,4),
		"health": 100
		}

		self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.airplane,anchor=NW)
		# print("Plane initialized at:",row,col)
		self.planeInRange()
		
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
			
		
			for row in range(10):
				for col in range(10):
					self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.land,anchor=NW)
			

			for idx in range (3):
				row = random.randint(0,9)
				col = random.randint(0,9)
				print ("turret at(row,col",row,col)
				self.canvas.create_image(col*cellwidth,row*cellheight,image= self.canvas.flak,anchor=NW)
				self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, 2*cellheight, self.canvas)

				defence =	{
				"name": self.defenceCounter,
				"row": row,
				"col": col,
				"plane in range" : 0,
				"health": 100
				}

			
				if idx ==0:
					self.defences = [defence]
					self.defenceCounter+=1
					self.previousX = col
					self.previousY = row
					# print ("first update",row,col)

				else:
					# print("line created at",self.previousX*cellwidth, self.previousY*cellheight, col*cellwidth, row*cellheight)
					self.canvas.create_line((self.previousX+0.5)*cellwidth, (self.previousY + 0.5)* cellheight, (col+0.5)*cellwidth, (row+0.5)*cellheight,fill='red',width = 5)
					line = {"x1": (self.previousX+0.5)*cellwidth, "y1":(self.previousY + 0.5)* cellheight, "x2": (col+0.5) * cellwidth, "y2" : (row+0.5)*cellheight }
					self.lines.append(line)
					self.previousX = col
					self.previousY = row
					# print ("previous set to",row,col) 
					self.defences.append(defence)
					self.defenceCounter+=1
			
			self.initializePlane()								
		else:
			self.drawStep()

	def drawStep(self):
		self.canvas.delete("all")
		cellheight = self.canvas.cellheight
		cellwidth = self.canvas.cellwidth

		for row in range(10):
			for col in range(10):
				self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.land,anchor=NW)
		# print("Done drawing grass")
		self.drawPlanes()
		# print("plane update")
		for row in range(10):
			for col in range(10):			
				for defence in self.defences:
					if defence["row"] == row and defence["col"] == col:
						self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.flak,anchor=NW)
						self.create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, 2*cellheight, self.canvas)
		for line in self.lines:
			x1 = line["x1"]
			x2 = line["x2"]
			y1 = line["y1"]
			y2 = line["y2"]
			self.canvas.create_line(x1,y1,x2,y2,fill='red',width = 5)
			# print ("Done with drawing step")

	def drawPlanes(self):
		plane = self.plane
		row = plane.get("row")
		col = plane.get("col")
		speed = 1
		if plane.get("direction") == 1:
			row = row + speed
		if plane.get("direction") == 2:
			row = row - speed
		if plane.get("direction") == 3:
			col = col + speed
		else:
			col = col - speed
			
		self.plane["row"] = row
		self.plane["col"] = col
		cellwidth = self.canvas.cellwidth	
		cellheight= self.canvas.cellheight
		
		self.canvas.create_image(col*cellwidth,row*cellheight,image=self.canvas.airplane,anchor=NW)
		
		if row > 10 or row < 0 or col > 10 or col < 0	:
			self.initializePlane()
		self.planeInRange()	

demo = Demo()
window=Tk()
mm = mouseMover()
demo.canvas = Canvas(window, width=500,height=500)
demo.canvas.grid(row=0,column=0,columnspan=2)
demo.canvas.draw=Button(window,text="Draw")
demo.canvas.draw.grid(row=1,column=3)
demo.canvas.bind("<Button-1>", mm.select)
demo.canvas.draw.bind('<Button-1>',demo.buttonhandler)
window.mainloop()
