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
		self.selectedTurrets.append = getTurret(self,self.x,self.y) 
		self.turretCounter += 1 

		if turretCounter > 1:
			x1 = self.selectedTurrets[turretCounter-1]["col"]
			x2 = self.selectedTurrets[turretCounter]["col"]
			y = self.selectedTurrets[turretCounter-1]["row"]
			y2 = self.selectedTurrets[turretCounter]["row"]
			canvas.create_line(x1, y1, x2, y2)  	 



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




def getClosestTile(n):
	n = math.floor(n)
	return n

def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1)

def getTurret(self,row,col):
	for idx in canvas.model.defences:
		if idx["row"] == row and idx["col"] == col:
			return idx

def loadTextures(canvas,cellwidth,cellheight):
	canvas.flak = Image.open("flak.jpg")
	canvas.flak = ImageTk.PhotoImage(canvas.flak.resize((cellwidth, cellheight), Image.ANTIALIAS))
	canvas.land = Image.open("land.jpg")
	canvas.land = ImageTk.PhotoImage(canvas.land.resize((cellwidth, cellheight), Image.ANTIALIAS))
	canvas.airplane = Image.open("plane.jpg")
	canvas.airplane = ImageTk.PhotoImage(canvas.airplane.resize((cellwidth,cellheight), Image.ANTIALIAS))

def drawState(self):
	w=self.winfo_width()
	h=self.winfo_height()

	cellwidth = w//10	
	cellheight=h//10
	canvas.model.cellheight = cellheight
	canvas.model.cellwidth = cellwidth
	
	if self.init ==1:
		self.init = 0
		
		loadTextures(canvas,cellwidth,cellheight)
		row = random.randint(0,5)
		col = random.randint(0,5)
		canvas.model.plane={
		"name": "plane1",
		"row": row,
		"col": col,
		"health": 100
		}
		canvas.create_image(col*cellwidth,row*cellheight,image=canvas.airplane,anchor=NW)
		print("Plane initialized at:",row,col)

		for row in range(10):
			for col in range(10):
				canvas.create_image(col*cellwidth,row*cellheight,image=canvas.land,anchor=NW)
		
	else:
		drawPlanes(canvas)

def createDefence(self):
		w=self.winfo_width()
		h=self.winfo_height()

		cellwidth = w//10	
		cellheight=h//10
		row = getClosestTile(self.y/cellheight)
		col = getClosestTile(self.x/cellwidth)	
		print("row,col",row,col)
		canvas.create_image(col*cellwidth,row*cellheight,image=canvas.flak,anchor=NW)
		create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, cellheight, canvas)

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
 
def drawPlanes(self):
	plane = canvas.model.plane
	row = plane.get("row")
	col = plane.get("col")
	speed = 1
	row = row+speed
	canvas.model.plane["row"] = row
	canvas.model.plane["col"] = col
	cellwidth = canvas.model.cellwidth	
	cellheight= canvas.model.cellheight
	print("Plane: (row,col)",row,col)
	
	canvas.create_image(col*cellwidth,row*cellheight,image=canvas.airplane,anchor=NW)
	row = row - speed
	print("Land:(row,col)",row,col)
	canvas.create_image(col*cellwidth,row*cellheight,image=canvas.land,anchor=NW)
				
		

def buttonhandler(event):
	if event.widget==draw:
		drawState(canvas)

	if event.widget==placeTurret:
		createDefence(canvas)

	if event.widget==erase:
	    canvas.delete('all')

	if event.widget==selectTurret:
	    selectTurret(canvas,event)
	
	else:
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
placeTurret=Button(window,text="Place turret")
placeTurret.grid(row=1,column=4)
selectTurret=Button(window, text="Select Turret")
selectTurret.grid(row=1,column =2)
erase=Button(window,text="Erase")
erase.grid(row=1,column=1)

window.update_idletasks()
canvas.x = mm.x
canvas.y = mm.y
draw.bind('<Button-1>',buttonhandler)
erase.bind('<Button-1>',buttonhandler)
selectTurret.bind('<Button-1>',buttonhandler)
placeTurret.bind('<Button-1>',buttonhandler)
#drawState(canvas)
window.mainloop()
    
