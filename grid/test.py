#some GUI drawing basics

from tkinter import *
from PIL import ImageTk, Image
import math


class MouseMover():
  
  def __init__(self):
    self.item = 0; self.previous = (0, 0)
    self.x = 0; self.y =0;
  
  def select(self, event):
    widget = event.widget                       # Get handle to canvas 
    # Convert screen coordinates to canvas coordinates
    xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
    self.item = widget.find_closest(xc, yc)[0]        # ID for closest
    self.x = xc
    self.y = yc
    canvas.x = xc
    canvas.y = yc
    drawState(canvas)
    
    
  
  def drag(self, event):
    widget = event.widget
    xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
    canvas.move(self.item, xc-self.previous[0], yc-self.previous[1])
    self.previous = (xc, yc)

def getClosestTile(n):
	print ("n",n)
	n = math.floor(n)
	return n

def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1)


def loadTextures(canvas,cellwidth,cellheight):
	canvas.flak = Image.open("flak.jpg")
	canvas.flak = ImageTk.PhotoImage(canvas.flak.resize((cellwidth, cellheight), Image.ANTIALIAS))
	canvas.land = Image.open("land.jpg")
	canvas.land = ImageTk.PhotoImage(canvas.land.resize((cellwidth, cellheight), Image.ANTIALIAS))

def drawState(self):
	w=self.winfo_width()
	h=self.winfo_height()

	cellwidth = w//10
	cellheight=h//10
	if self.init == 1:
		self.init = 0
		loadTextures(canvas,cellwidth,cellheight)
		for row in range(10):
			for col in range(10):
				canvas.create_image(col*cellwidth,row*cellheight,image=canvas.land,anchor=NW)
	else:
		row = getClosestTile(self.y/cellheight)
		col = getClosestTile(self.x/cellwidth)	
		# print("row",row,'col',col)
		canvas.create_image(col*cellwidth,row*cellheight,image=canvas.flak,anchor=NW)
		create_circle((col+0.5)*cellwidth,(row+0.5)*cellheight, cellheight, canvas)
		

def buttonhandler(event):
	if event.widget==thebutton:
		canvas.init = 1
		drawState(canvas)
    # if event.widget==select:
	else:
	    canvas.delete('all')
window=Tk()

canvas = Canvas(window, width=500,height=500)
canvas.grid(row=0,column=0,columnspan=2)
# Get an instance of the MouseMover object
mm = MouseMover()

# Bind mouse events to methods (could also be in the constructor)
canvas.bind("<Button-1>", mm.select)
canvas.bind("<B1-Motion>", mm.drag)
thebutton=Button(window,text="Draw")
thebutton.grid(row=1,column=10)
select=Button(window, text="Select")
select.grid(row=1,column =2)
thebutton2=Button(window,text="Erase")
thebutton2.grid(row=1,column=1)
window.update_idletasks()
canvas.x = mm.x
canvas.y = mm.y
thebutton.bind('<Button-1>',buttonhandler)
thebutton2.bind('<Button-1>',buttonhandler)
select.bind('<Button-1>',buttonhandler)
#drawState(canvas)
window.mainloop()
    
