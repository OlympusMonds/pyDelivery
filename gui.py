from Tkinter import Tk, BOTH
from ttk import Frame, Button, Style
from functools import partial

class MainGUI(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.initUI()
		
		self.communicators = {}
		self.buttons = {}


	def initUI(self):
		self.parent.title("PyDelivery")
		self.style = Style()
		self.style.theme_use("default")

		self.pack(fill=BOTH, expand=1)

		quitButton = Button(self, text="Quit", command=self.quit)
		quitButton.place(x=50, y=50)


	def delete_communicator(self, name):
		del self.communicators[name]
		self.buttons[name].destroy()
		del self.buttons[name]


	def add_communicator(self, comm):
		if comm.name not in self.communicators.keys():
			self.communicators[comm.name] = comm
			commButton = Button(self, text=comm.name, command=partial(self.delete_communicator, comm.name))
			commButton.place(x=50, y=len(self.communicators.keys())*50+50)
			self.buttons[comm.name] = commButton
		else:
			pass
