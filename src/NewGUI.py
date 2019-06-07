from demo import Demo
from text import TextCanvas
import time
from tkinter import *

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

	def add_buttons(self):
		## TODO, make labels and entryfields in seperate canvases
		self.numplanes_entry = Entry(self.button_canvas, text="numplanes")
		self.numplanes_entry.pack(side=LEFT)
		self.updatebutton = Button(self.button_canvas, text = "Update sim", command = self.update_demo_parameters)
		self.updatebutton.pack(side=LEFT)

		self.play_button =Button(self.button_canvas, command=self.demo.button_handler, image=self.load_button_art("../img/play.png"))
		self.play_button.pack()
		self.pause_button=Button(self.button_canvas, command=self.demo.pause_handler, image=self.load_button_art("../img/pause.png"))
		self.pause_button.pack()
		self.ff_button=Button(self.button_canvas, command=self.demo.step_handler, image=self.load_button_art("../img/ff.png"))
		self.ff_button.pack()

	def load_button_art(self, path):
		button_img = Image.open(path)
		button_img = button_img.resize((width,height), Image.ANTIALIAS)
		button_img =  ImageTk.PhotoImage(button_img)

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








# demo = Demo()
# window=Tk()
# top = Toplevel()
# mm = mouseMover()
# demo.canvas = Canvas(window, width=500,height=500)
# demo.text = Text(top)
# demo.canvas.grid(row=0,column=0,columnspan=2)
# # demo.canvas.draw=Button(window,text="Draw")
# # demo.canvas.draw.grid(row=1,column=3)
# # demo.canvas.pack(side=TOP)
# # demo.canvas.bind("<Button-1>", mm.select)
# # demo.canvas.draw.bind('<Button-1>',demo.buttonhandler)

# demo.canvas2 = Canvas(window, width=500,height=50)
# numplanes_entry = Entry(demo.canvas2, text="numplanes")
# numplanes_entry.configure(width = 30)
# updatebutton = Button(demo.canvas2, text = "Update sim", command = update_parameters, anchor = W)
# updatebutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT, anchor = W)
# demo.canvas2.grid(row=0,column=0,columnspan=2)

# demo.canvas.update()
# demo.drawState()
# running = True

# while running:
# 	demo.drawState()
# 	time.sleep(SPEED)
# 	window.update_idletasks()
# 	window.update()
# 	demo.text.text_window.update_idletasks()
# 	demo.text.text_window.update()