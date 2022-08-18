from dev_help.widgets import *
from tkinter import PhotoImage
from tkinter import messagebox
import os, string
from threading import Thread
from ntk.objects import gv
from ntk import Text as ocText, PanedWindow, Frame, Button


class Calculator:
	def __init__(self, toplevel, realself, *args, **kwargs):
		super(Calculator, self).__init__(*args, **kwargs)
		self.master = master = gui = toplevel
		master.title("Calculator")
		master.geometry("300x380+{}+{}".format(int((gv.device_width-300)/2), int((gv.device_height-380)/2)))
		master.resizable(0, 0)
		master.configure(background="#F1F3F6")
		self.master.iconbitmap(gv.icon_path)
		self.realself 			= realself

		master.protocol("WM_DELETE_WINDOW", self.quite_ins)

		self.calculator_thread 	= Thread(target=self.get_calculator, daemon=True)
		self.calculator_thread.start()

	def get_calculator(self):
		master 	= self.master
		self.expression = ""

		self.calc_paned = PanedWindow(master, pady=5, padx=5, bg="#FFFFFF")
		self.calc_frame = Frame(self.calc_paned, pady=0, padx=0, bg="#FFFFFF")

		file_path = os.path.join(gv.fi_path, "cus", "power-32 (1).png")
		globals()["but_exit_img"]	= PhotoImage(file=file_path).subsample(1, 1)

		file_path = os.path.join(gv.fi_path, "cus", "delete-3-24.png")
		globals()["but_bdel_img"]	= PhotoImage(file=file_path).subsample(1, 1)

		self.equation = ocText(
				self.calc_frame,
				bg="#37a000",
				fg="fg-light",
				columnspan=4,
				width=28,
				height=2,
				padx=0,
				pady=4,
				font=("Calibri", 15)
			)

		self.equation.bind("<KeyRelease>", lambda e: self.keyreleased())

		globals()["but_clear"] = Button(
				self.calc_frame,
				text="C",
				row=1,
				column=0,
				pady=4,
				padx=4,
				ipady=10,
				ipadx=4,
				font=("Calibri", 13, "bold"),
				bg="#E7F7DE",
				fg="#5E5858",
				width=5,
				command=lambda: self.clear(),
				abg="#F1F3F6",
				height=1
			)

		globals()["but_bdel"] = Button(
				self.calc_frame,
				text="",
				row=1,
				column=1,
				pady=4,
				padx=4,
				ipady=12,
				ipadx=24,
				image=globals()["but_bdel_img"],
				compound="center",
				bg="#E7F7DE",
				fg="#5E5858",
				width=15,
				command=lambda: self.backspace(),
				abg="#F1F3F6",
				height=26
			)

		globals()["but_exit"] = Button(
				self.calc_frame,
				text="",
				row=1,
				column=3,
				pady=4,
				padx=4,
				ipady=7,
				ipadx=24,
				image=globals()["but_exit_img"],
				compound="center",
				bg="#E7F7DE",
				fg="#5E5858",
				width=15,
				command=lambda: self.quite_ins(),
				abg="#F1F3F6",
				height=36
			)

		globals()["but_equal"] = Button(
				self.calc_frame,
				text="=",
				row=5,
				column=3,
				pady=4,
				padx=4,
				ipady=10,
				ipadx=4,
				font=("Calibri", 13, "bold"),
				width=5,
				command=lambda: self.equalpress(),
				abg="#45C203",
				height=1
			)

		rc_l = [
			[2, 0], [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2],
			[3, 3], [4, 0], [4, 1], [4, 2], [4, 3], [5, 0], [5, 1], [5, 2]]
		btx_l = ["7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "*", "0", ".", "/"]

		for e, i in enumerate(rc_l):
			globals()["but_{}".format(e)] = Button(
					self.calc_frame,
					text=btx_l[e],
					row=i[0],
					column=i[1],
					pady=4,
					padx=4,
					ipady=10,
					ipadx=4,
					width=5,
					font=("Calibri", 13, "bold"),
					bg="#E7F7DE",
					fg="#5E5858",
					abg="#F1F3F6",
					command=lambda t=btx_l[e]: self.press(t),
					height=1
				)

	def keyreleased(self):
		self.expression = self.equation.get_text().replace('\n', '')
		self.equation.set_text(self.expression)

	def backspace(self):
		pt 	= self.equation.get_text()
		if len(pt) > 0:
			nt = pt[0:len(pt)-2]
			self.equation.set_text(nt)
			self.expression = nt

	def press(self, num):
		self.expression = self.expression + str(num)
		self.equation.set_text(self.expression)

	def equalpress(self):
		try:
			self.expression = "".join(s for s in self.expression if s in list(string.digits)+['.','+','-','*','/'])
			self.expression = self.expression.replace("\n", "").replace('\t', '').replace('\s', '')
			total = str(eval(self.expression))
			self.equation.set_text(total)
			self.expression = total
		except:
			self.equation.set_text(" Invalid ")
			self.expression = ""

	def clear(self):
		self.expression = ""
		self.equation.set_text("")

	def quite_ins(self):
		self.realself.calculator_toplevel = None
		self.master.destroy()
