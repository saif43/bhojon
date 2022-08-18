from tkinter import messagebox, ttk
from tkinter import Canvas
from threading import Thread
import datetime, os, subprocess, win32gui, sys, time
from PIL import ImageGrab
from tkdocviewer import *

from dev_help.widgets import *
from ntk import gv, PanedWindow, Frame, Button, Toplevel, Canvas

from invoice import PrintInvoice, GenerateInvoice

from database.table import CustomerInfo, Food, OnlineOrder, BillOnline, CustomerOrder, Bill, QROrder, QRBill


class ViewInvoice:
	def __init__(self, realself, master, invid, *args, **kwargs):
		super(ViewInvoice, self).__init__(*args)
		master.destroy()
		self.master = Toplevel(width=780, height=610, bg='#F1F1F1', title='Order Detail Invoice')
		self.realself = realself
		self.invoice_id = invid
		self.online_order = kwargs.get("online")
		self.qr_order = kwargs.get("qr")

		if self.online_order:
			self.order = OnlineOrder().qset.filter(saleinvoice=self.invoice_id).first()
			if self.order:
				self.bill = BillOnline().qset.filter(order_id=self.order['id']).first()

		elif self.qr_order:
			self.order = QROrder().qset.filter(invoice=self.invoice_id).first()
			if self.order:
				self.bill = QRBill().qset.filter(order_id=self.order['orderd']).first()

		else:
			self.order = CustomerOrder().qset.filter(saleinvoice=self.invoice_id).first()
			if self.order:
				self.bill = Bill().qset.filter(order_id=self.order['id']).first()

		if not self.order:
			return

		if invid:
			self.show_sys = "invoice"

		self.get_dependancy()

	def get_dependancy(self):
		self.master_paned = PanedWindow(self.master, pady=5, padx=5)
		self.content = Frame(self.master_paned, width=gv.wpc*1200, row=1)
		self.content_canvas = Canvas(
			self.content, width=gv.wpc*218, height=gv.hpc*80, row=1, pady=0, mousescroll=False)
		self.ath_sign = Canvas(
			self.content, width=gv.wpc*188, height=gv.hpc*80, row=2, bg="#F1F3F6", mousescroll=False)

		self.master_paned.add(self.content)

		self.inv_file = os.path.join(
			gv.invoice_path, "{}{}_invoice.pdf".format(self.invoice_id, "On" if self.online_order else ""))

		GenerateInvoice(
			realself=self.realself, saleinvoice=self.invoice_id, online=self.online_order, qr=self.qr_order)

		self.dv = DocViewer(
			self.content, width=790, height=510, highlightbackground='#FFFFFF',
			highlightcolor="#FFFFFF", highlightthickness=0, relief="flat", borderwidth=0)
		self.dv.grid(row=0, columnspan=4)
		self.dv._x_scrollbar.config(width=5)
		self.dv._y_scrollbar.config(width=5)

		self.pimg = PhotoImage(file=os.path.join(gv.fi_path, "cus", "printer-5-24.png"))
		self.print_but = Button(
			self.content, row=1, padx=(56, 10), ipady=5, column=1, text="",
			bg="#53D4FA", image=self.pimg, compound="center", width=56, height=38)

		self.rimg = PhotoImage(file=os.path.join(gv.fi_path, "cus", "refresh-24.png"))
		self.reload_but = Button(
			self.content, row=1, column=2, padx=(10, 56), ipady=5, text="",
			bg="#F0F0F0", image=self.rimg, compound="center", width=56, height=38)

		def print_invoice():
			PrintInvoice(print_file=self.inv_file)
			self.master.destroy()

		self.print_but.config(command=lambda: print_invoice())
		self.reload_but.config(command=lambda: self.reload())

		self.content_canvas.create_window(94, 48, window=self.ath_sign, height=80, width=188, anchor="center")

		pref = os.path.join(gv.user_image_path, "sign", "%s_sign.png" %gv.user_id)
		if os.access(pref, os.F_OK):
			self.presigned = PhotoImage(file=pref)
			self.ath_sign.create_image(0, 40, image=self.presigned, anchor="w")
		else: self.presigned = False

		self.resignrec = self.content_canvas.create_rectangle(188, 60, 218, 80, fill="#45C203", outline="#FFFFFF")
		self.resignimg = PhotoImage(file=os.path.join(gv.fi_path, "cus", "brush-24.png")).subsample(1, 2)
		self.resignbut = self.content_canvas.create_image(203, 70, image=self.resignimg)

		canvas_mouse_el(self.content_canvas, self.resignrec)
		canvas_mouse_el(self.content_canvas, self.resignbut)

		self.content_canvas.tag_bind(self.resignrec, "<Button-1>", lambda e: self.ath_sign.delete("all"))
		self.content_canvas.tag_bind(self.resignbut, "<Button-1>", lambda e: self.ath_sign.delete("all"))

		self.ath_sign.bind("<B1-Motion>", lambda e: self.sign(e))
		self.ath_sign.bind("<ButtonRelease-1>", lambda e: self.save_sign())

		self.inv_file_r = self.inv_file.replace('\\', '\\\\').replace('/', '\\\\')
		self.dv.display_file(self.inv_file_r)

	def reload(self):
		GenerateInvoice(
			realself=self.realself, saleinvoice=self.invoice_id, online=self.online_order, qr=self.qr_order)
		self.dv.display_file(self.inv_file_r)

	def sign(self, e):
		x1, y1 = (e.x-2), (e.y-2)
		x2, y2 = (e.x+1), (e.y+1)
		self.ath_sign.create_oval(x1, y1, x2, y2, fill="#374767")

	def save_sign(self):
		HWND = self.ath_sign.winfo_id()
		rect = win32gui.GetWindowRect(HWND)
		im = ImageGrab.grab(rect).save(os.path.join(gv.user_image_path, "sign", "%s_sign.png" %gv.user_id))

		self.reload()
