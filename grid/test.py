#some GUI drawing basics

from tkinter import *

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
    
    
  
  def drag(self, event):
    widget = event.widget
    xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
    canvas.move(self.item, xc-self.previous[0], yc-self.previous[1])
    self.previous = (xc, yc)



def checkerboard(self):
	w=self.winfo_width()
	h=self.winfo_height()

	cellwidth = w//10
	cellheight=h//10
	if self.init:
		for row in range(10):
			for col in range(10):
				fillcolor='white'
				self.create_rectangle(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight,fill=fillcolor)

		self.init = 0
	else:
		row = self.y
		col = self.x
		print(self.x,self.y)
		fillcolor='red'
	self.create_rectangle(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight,fill=fillcolor)


def buttonhandler(event):
    if event.widget==thebutton:
		canvas.init = 1
		checkerboard(canvas)
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
#checkerboard(canvas)
window.mainloop()
    
