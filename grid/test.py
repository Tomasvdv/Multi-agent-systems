#some GUI drawing basics

from tkinter import *
from PIL import ImageTk, Image
import math
import random
import numpy as np

class MouseMover():
  
	def __init__(self):
		self.item = 0; self.previous = (0, 0)
		self.x = 0; self.y =0;
		self.turretCounter = 0;
		self.selectedTurrets = []

	def selectTurret(self, event):
		widget = event.widget                       # Get handle to canvas 
		# Convert screen coordinates to canvas coordinates

		xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
		self.item = widget.find_closest(xc, yc)[0]        # ID for closest
		self.x = xc
		self.y = yc
		canvas.x = xc
		canvas.y = yc
		# turret = getTurret(self,getClosestTile(self.x/canvas.model.cellwidth),getClosestTile(self.y/canvas.model.cellheight))
		# print(turret)
		# self.selectedTurrets.append(turret) 
		# self.turretCounter += 1 

		# if self.turretCounter > 1:
		# 	turret =self.selectedTurrets[self.turretCounter]
		# 	print("turret",turret)
		# 	# x1 = self.selectedTurrets[self.turretCounter-1]["col"]
			# x2 = self.selectedTurrets[self.turretCounter]["col"]
			# y = self.selectedTurrets[self.turretCounter-1]["row"]
			# y2 = self.selectedTurrets[self.turretCounter]["row"]
			# canvas.create_line(x1, y1, x2, y2)  	 



	def drag(self, event):
		widget = event.widget
		xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
		canvas.move(self.item, xc-self.previous[0], yc-self.previous[1])
		self.previous = (xc, yc)

class Model():
	def __init__(self):
		self.planes = {}
		self.planesCounter = 0
		self.defenceCounter = 0
		self.lines = [] 



def getClosestTile(n):
	n = math.floor(n)
	return n

def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1)

def planeInRange(self):
	for dic in self.model.defences:
		if self.model.plane.get("row") <= dic.get("row")+2 and 	dic.get("row") -2 <= self.model.plane.get("row") and self.model.plane.get("col") <= dic.get("col")+2 and dic.get("col")-2 <= self.model.plane.get("col") :
			dic["plane in range"] = 1  
			print ("plane detected!")

def getTurret(self,row,col):
	# print ("(row,col)", row,col)
	for idx in canvas.model.defences:
		# print ("idx",idx)
		if idx["row"] == row and idx["col"] == col:
			# print ("Found")
			return idx

def loadTextures(canvas,cellwidth,cellheight):
	canvas.flak = Image.open("flak.jpg")
	canvas.flak = ImageTk.PhotoImage(canvas.flak.resize((cellwidth, cellheight), Image.ANTIALIAS))
	canvas.land = Image.open("land.jpg")
	canvas.land = ImageTk.PhotoImage(canvas.land.resize((cellwidth, cellheight), Image.ANTIALIAS))
	canvas.airplane = Image.open("plane.jpg")
	canvas.airplane = ImageTk.PhotoImage(canvas.airplane.resize((cellwidth,cellheight), Image.ANTIALIAS))

def initializePlane(self):

	row = random.randint(1,3)
	col = random.randint(1,3)
	cellwidth = canvas.model.cellwidth
	cellheight = canvas.model.cellheight
	canvas.model.plane={
	"name": "plane1",
	"row": row,
	"col": col,
	"direction": random.randint(0,4),
	"health": 100
	}

	canvas.create_image(col*cellwidth,row*cellheight,image=canvas.airplane,anchor=NW)
	# print("Plane initialized at:",row,col)
	planeInRange(self)
def drawState(self):
	w=self.winfo_width()
	h=self.winfo_height()

	plane = 1
	cellwidth = w//10	
	cellheight=h//10
	canvas.model.cellheight = cellheight
	canvas.model.cellwidth = cellwidth
	
	if self.init ==1:
		self.previousX = -1
		self.previousY = -1
		self.init = 0
		counter = 0
		loadTextures(canvas,cellwidth,cellheight)
		
	
		for row in range(10):
			for col in range(10):
				canvas.create_image(col*cellwidth,row*cellheight,image=canvas.land,anchor=NW)
		

		for idx in range (3):
			row = random.randint(0,9)
			col = random.randint(0,9)
			print ("turret at(row,col",row,col)
			canvas.create_image(col*cellwidth,row*cellheight,image=canvas.flak,anchor=NW)
			create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, 2*cellheight, canvas)

			defence =	{
			"name": canvas.model.defenceCounter,
			"row": row,
			"col": col,
			"plane in range" : 0,
			"health": 100
			}

		
			if idx ==0:
				canvas.model.defences = [defence]
				canvas.model.defenceCounter+=1
				self.previousX = col
				self.previousY = row
				# print ("first update",row,col)

			else:
				# print("line created at",self.previousX*cellwidth, self.previousY*cellheight, col*cellwidth, row*cellheight)
				canvas.create_line((self.previousX+0.5)*cellwidth, (self.previousY + 0.5)* cellheight, (col+0.5)*cellwidth, (row+0.5)*cellheight,fill='red',width = 5)
				line = {"x1": (self.previousX+0.5)*cellwidth, "y1":(self.previousY + 0.5)* cellheight, "x2": (col+0.5) * cellwidth, "y2" : (row+0.5)*cellheight }
				canvas.model.lines.append(line)
				self.previousX = col
				self.previousY = row
				# print ("previous set to",row,col) 
				canvas.model.defences.append(defence)
				canvas.model.defenceCounter+=1
		
		initializePlane(canvas)								
	else:
		drawStep(canvas)

def createDefence(self):
		w=self.winfo_width()
		h=self.winfo_height()

		cellwidth = w//10	
		cellheight=h//10
		row = getClosestTile(self.y/cellheight)
		col = getClosestTile(self.x/cellwidth)	
		canvas.create_image(col*cellwidth,row*cellheight,image=canvas.flak,anchor=NW)
		create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, 2*cellheight, canvas)

		defence =	{
		"name": canvas.model.defenceCounter,
		"row": row,
		"col": col,
		"health": 100
		}

	
		if canvas.model.defenceCounter ==0:
			canvas.model.defences = [defence]
		else:
			canvas.model.defences.append(defence)
		canvas.model.defenceCounter+=1

def drawStep(self):
	canvas.delete("all")
	cellheight = canvas.model.cellheight
	cellwidth = canvas.model.cellwidth

	for row in range(10):
		for col in range(10):
			canvas.create_image(col*cellwidth,row*cellheight,image=canvas.land,anchor=NW)
	# print("Done drawing grass")
	drawPlanes(self)
	# print("plane update")
	for row in range(10):
		for col in range(10):			
			for defence in canvas.model.defences:
				if defence["row"] == row and defence["col"] == col:
					canvas.create_image(col*cellwidth,row*cellheight,image=canvas.flak,anchor=NW)
					create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, 2*cellheight, canvas)
	for line in canvas.model.lines:
		x1 = line["x1"]
		x2 = line["x2"]
		y1 = line["y1"]
		y2 = line["y2"]
		canvas.create_line(x1,y1,x2,y2,fill='red',width = 5)
		# print ("Done with drawing step")

def drawPlanes(self):
	plane = canvas.model.plane
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
		
	canvas.model.plane["row"] = row
	canvas.model.plane["col"] = col
	cellwidth = canvas.model.cellwidth	
	cellheight= canvas.model.cellheight
	
	canvas.create_image(col*cellwidth,row*cellheight,image=canvas.airplane,anchor=NW)
	
	if row > 10 or row < 0 or col > 10 or col < 0	:
		initializePlane(canvas)
	planeInRange(self)		
def buttonhandler(event):
	# if event.widget==draw:
	# 	drawState(canvas)

	# if event.widget==placeTurret:
	# 	createDefence(canvas)

	# if event.widget==erase:
	#     canvas.delete('all')

	# if event.widget==selectTurret:
	#     selectTurret(canvas,event)
	
	# else:
		drawState(canvas)

window=Tk()

canvas = Canvas(window, width=500,height=500)
canvas.grid(row=0,column=0,columnspan=2)
canvas.init = 1
# Get an instance of the MouseMover object
mm = MouseMover()
canvas.model = Model()
# Bind mouse events to methods (could also be in the constructor)
canvas.bind("<Button-1>", mm.selectTurret)
canvas.bind("<B1-Motion>", mm.drag)
draw=Button(window,text="Draw")
draw.grid(row=1,column=3)
# placeTurret=Button(window,text="Place turret")
# placeTurret.grid(row=1,column=4)
# selectTurret=Button(window, text="Select Turret")
# selectTurret.grid(row=1,column =2)
# erase=Button(window,text="Erase")
# erase.grid(row=1,column=1)

window.update_idletasks()
canvas.x = mm.x
canvas.y = mm.y
draw.bind('<Button-1>',buttonhandler)
# erase.bind('<Button-1>',buttonhandler)
# selectTurret.bind('<Button-1>',buttonhandler)
# placeTurret.bind('<Button-1>',buttonhandler)
#drawState(canvas)
window.mainloop()
    
