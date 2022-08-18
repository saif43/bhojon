from tkinter import Toplevel, Menu
from dev_help.widgets import destroy_child
from ntk.objects import gv
from __restora__.global_ import setting as gl_setting
from database.synchronization.selector import SyncSelector

import user, customer, database, order, food, reservation, setting, payment, webbrowser
gv.order 		= order

# gv.error_log(str(f"File: menu.py"))

class ResturantMenu:


	def __init__(self, realself, master, *args, **kwargs):
		super(ResturantMenu, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> master: {master} --> args: {args} --> kwargs: {kwargs}"))


		self.master 				= master
		self.realself 				= realself
		gv.menu 					= self
		gv.swin 					= False

		menubar 					= Menu(master)

		foodmenu 	= Menu(menubar, tearoff=0, activebackground="#91C9F7", background="#F2F2F2", activeforeground="#000000", font=("Calibri", 10))
		self.add_command(l="Foods...", menu=foodmenu, command=self.win_food)
		self.add_command(l="Food Add-ons...", menu=foodmenu, command=self.win_addones)
		self.add_command(l="Food Category...", menu=foodmenu, command=self.win_food_category)
		self.add_command(l="Tables...", menu=foodmenu, command=self.win_table)
		self.add_command(l="Customer Type...", menu=foodmenu, command=self.win_customer_type)
		self.add_command(l="Payment...", menu=foodmenu, command=self.win_payment_setting)
		self.add_cascade(l="View", menubar=menubar, menu=foodmenu)

		ordermenu 	= Menu(menubar, tearoff=0, activebackground="#91C9F7", background="#F2F2F2", activeforeground="#000000", font=("Calibri", 10))
		self.add_command(l="Order...", menu=ordermenu, command=self.win_order)
		self.add_command(l="POS...", menu=ordermenu, command=self.win_pos_order)
		self.add_cascade(l="Manage Order", menubar=menubar, menu=ordermenu)

		settingmenu = Menu(menubar, tearoff=0, activebackground="#91C9F7", background="#EBEDEF", activeforeground="#000000", font=("", 10))
		self.add_command(l="Application Setting...", menu=settingmenu, command=self.win_app_setting)
		self.add_command(l="Synchronization...", menu=settingmenu, command=self.win_synchronization)
		self.add_cascade(l="Setting", menubar=menubar, menu=settingmenu)

		helpmenu 	= Menu(menubar, tearoff=0, activebackground="#91C9F7", background="#EBEDEF", activeforeground="#000000", font=("", 10))
		self.add_command(l="Development...", menu=helpmenu, command=self.development)
		self.add_cascade(l="Help", menubar=menubar, menu=helpmenu)

		master.config(menu=menubar)

		gv.shortcut_commands = {
			"<Control-p>": {
				'lambda': lambda e: self.win_pos_order(self.realself),
				'name': 'New POS Order'
			},
			"<Control-f>": {
				'lambda': lambda e: self.win_food(self.realself),
				'name': 'Food list'
			},
			"<Control-F>": {
				'lambda': lambda e: self.win_addones(self.realself),
				'name': 'Addons list'
			},
			"<Control-C>": {
				'lambda': lambda e: self.win_food_category(self.realself),
				'name': 'Food category list'
			},
			"<Control-o>": {
				'lambda': lambda e: self.win_order(self.realself),
				'name': 'Order list'
			},
			"<Control-t>": {
				'lambda': lambda e: self.win_table(self.realself),
				'name': 'Table list'
			},
			"<Control-T>": {
				'lambda': lambda e: self.win_customer_type(self.realself),
				'name': 'Customer type list'
			},
			"<Control-P>": {
				'lambda': lambda e: self.win_payment_setting(self.realself),
				'name': 'Payment type list'
			},
			"<Control-S>": {
				'lambda': lambda e: self.win_app_setting(self.realself),
				'name': 'Application setting'
			},
			"<Control-s>": {
				'lambda': lambda e: self.win_synchronization(self.realself),
				'name': 'Synchronization'
			}
		}

		for key, value in gv.shortcut_commands.items():
			master.bind(key, value['lambda'])

		# master.bind("<Control-p>", lambda e: self.win_pos_order(self.realself))
		# master.bind("<Control-f>", lambda e: self.win_food(self.realself))
		# master.bind("<Control-F>", lambda e: self.win_addones(self.realself))
		# master.bind("<Control-C>", lambda e: self.win_food_category(self.realself))
		# master.bind("<Control-o>", lambda e: self.win_order(self.realself))
		# master.bind("<Control-t>", lambda e: self.win_table(self.realself))
		# master.bind("<Control-T>", lambda e: self.win_customer_type(self.realself))
		# master.bind("<Control-P>", lambda e: self.win_payment_setting(self.realself))
		# master.bind("<Control-S>", lambda e: self.win_app_setting(self.realself))
		# master.bind("<Control-s>", lambda e: self.win_synchronization(self.realself))

	def donothing(this, self): pass

	def win_synchronization(this, self):
		if gv.swin:
			return

		SyncSelector(self)

	def win_customer_type(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		customer.customer_type(self, self.resturant_frame)

	def win_payment_setting(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		payment.payment_setting(self, self.resturant_frame)

	def win_app_setting(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		setting.appsetting(self, self.resturant_frame)

	def win_table(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		reservation.table(self, self.resturant_frame)

	def win_food_category(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		food.food_category(self, self.resturant_frame)

	def win_pos_order(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		order.pos_order(self, self.resturant_frame)

	def win_food(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		food.food(self, self.resturant_frame)

	def win_addones(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		food.food_addon(self, self.resturant_frame)

	def win_order(this, self):
		destroy_child(self.resturant_frame)
		this.refresh()
		order.order(self, self.resturant_frame)

	def development(this, self):
		webbrowser.open_new("https://www.bdtask.com/")

	def add_command(this, l="Command", menu=None, ln=36, d=" ", command=None, *args, **kwargs):
		if command and menu:
			spacing = ""
			if len(l) < ln:
				for i in range(int(ln - len(l))):
					spacing = spacing + "{}".format(d)

			if kwargs.get("table"):
				menu.add_command(label="{}{}".format(l, spacing), command=lambda realself=this.realself, table=kwargs.get("table"): command(realself, table))
			else: menu.add_command(label="{}{}".format(l, spacing), command=lambda realself=this.realself: command(realself))

			return menu

	def add_cascade(this, l="Menu", menubar=None, menu=None, ln=12, d=" "):
		if menubar and menu:
			spacing = ""
			if len(l) < ln:
				for i in range(int(ln - len(l))):
					spacing = spacing + "{}".format(d)

			spacing2 = "  "
			menubar.add_cascade(label="{}{}{}".format(spacing2, l, spacing2), menu=menu)

			return menubar

	def refresh(this):
		gv.oo_mas 	= None
		gl_setting()
