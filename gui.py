from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.create_window()
		self.create_menu()

	def create_window(self):
		self.master.title("Air defense system")
		self.pack(fill=BOTH, expand=1)
		quitButton = Button(self, text="Quit system", command=self.client_exit)
		quitButton.place(x=0, y=0)

	def create_menu(self):
		self.master.title("Air defense system")
		self.pack(fill=BOTH, expand=1)
		menu = Menu(self.master)
		self.master.config(menu=menu)
		file = Menu(menu)
		file.add_command(label="Exit", command=self.client_exit)
		menu.add_cascade(label="File", menu=file)
		edit = Menu(menu)
		edit.add_command(label="Undo", command=self.print_something)
		menu.add_cascade(label="Edit", menu=edit)

		import_img = Menu(menu)
		import_img.add_command(label="Show image", command=self.showImage)
		menu.add_cascade(label="Import", menu=import_img)


	def showImage(self):
		load = Image.open("img/aircraft.jpg")
		render = ImageTk.PhotoImage(load)
		img = Label(self, image=render)
		img.image = render
		img.place(x=0, y=0)

	'''
	def showText(self):
		text = Label(self, text="Some text")
		text.pack()
	'''

	def print_something(self):
		print("Action undone")

	def client_exit(self):
		exit()

root = Tk()
root.geometry("400x300")

app = Window(root)
root.mainloop()
