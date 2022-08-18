from tkinter import messagebox, ttk
from tkinter import Canvas
from threading import Thread
import datetime, os, time
from invoice import PrintInvoice, GeneratePosInvoice
from tkdocviewer import *

from dev_help.widgets import *
from ntk import gv, PanedWindow, Frame, Button, Toplevel

from invoice import PrintInvoice, GeneratePosInvoice

from database.table import CustomerInfo, Food, CustomerOrder, Bill, OnlineOrder, BillOnline, QROrder, QRBill


class ViewPosInvoice:
	def __init__(self, realself, master, invoice_id, *args, **kwargs):
		super(ViewPosInvoice, self).__init__(*args)
		master.destroy()
		self.master = Toplevel(width=780, height=610, bg='#F1F1F1', title='Order POS Invoice')
		self.realself = realself
		self.invoice_id = invoice_id
		self.pos_invoice = kwargs.get("pos_invoice")
		self.due = kwargs.get("due")
		self.online_order = kwargs.get("online")
		self.qr_order = kwargs.get('qr')
		self.order = None
		self.customer = None

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

		self.customer = CustomerInfo().qset.filter(id=self.order['customer_id']).first()

		if not self.order: return

		self.get_dependancy()

	def get_dependancy(self):
		self.master_paned = PanedWindow(self.master, pady=5, padx=5, width=780, height=610)
		self.content = Frame(self.master_paned, width=gv.wpc*1200, padx=15)
		self.master_paned.add(self.content)

		def print_invoice():
			PrintInvoice(print_file=self.inv_file)
			self.master.destroy()

		self.pimg = PhotoImage(file=os.path.join(gv.fi_path, "cus", "printer-5-24.png"))
		self.print_but = Button(
			self.content, row=1, pady=(20, 0), padx=(300, 10), ipady=5, text="",
			bg="#53D4FA", image=self.pimg, compound="center", width=56, height=38)
		self.print_but.config(command=lambda: print_invoice())

		self.rimg = PhotoImage(file=os.path.join(gv.fi_path, "cus", "refresh-24.png"))
		self.reload_but = Button(
			self.content, row=1, pady=(20, 0), padx=(10, 300), column=1, ipady=5, text="",
			bg="#F0F0F0", image=self.rimg, compound="center", width=56, height=38)
		self.reload_but.config(command=lambda: self.reload())

		self.inv_file = os.path.join(
			gv.invoice_path, "{}{}_pos_invoice.pdf".format(self.invoice_id, "On" if self.online_order else ""))
		GeneratePosInvoice(
			realself=self.realself, invoice_id=self.invoice_id, online=self.online_order, qr=self.qr_order)

		self.dv = DocViewer(
			self.content, width=755, height=500, highlightbackground='#FFFFFF',
			highlightcolor="#FFFFFF", highlightthickness=0, relief="flat", borderwidth=0)
		self.dv.grid(row=0, columnspan=2)
		self.dv._x_scrollbar.config(width=0)
		self.dv._y_scrollbar.config(width=5)

		self.dv.display_file(self.inv_file)

	def reload(self):
		GeneratePosInvoice(
			realself=self.realself, invoice_id=self.invoice_id, online=self.online_order, qr=self.qr_order)
		self.dv.display_file(self.inv_file)
