
# from tkinter import ttk
# from threading import Thread
# import datetime, os

from dev_help.widgets import *
from ntk.objects import gv as gv

from order.snippets.addtocart import AddToCart

from order.snippets.order import (
		get_order_cart,
		get_controller_count_content,
		get_controller_button_content,
		get_user_staf_table_content,
		get_food_item_frame_content,
		get_search_frame_content,
		get_category_list_content
	)

from database.table import (
		Food,
		Varient,
		AddOn,
		OrderItem
	)

from ntk import PanedWindow, Frame, Canvas, Scrollbar

# gv.error_log(str(f"File: order/update.py"))

class UpdateOrder:
	def __init__(self, realself, order=None, *args, **kwargs):
		super(UpdateOrder, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> order: {order} --> args: {args} --> kwargs: {kwargs}"))

		self.realself = realself
		self.order = order
		self.update = realself.update = True
		gv.pos_order = self
		gv.order_sys = self

		gv.order_sys_realself = self.realself
		gv.food_item_frame = get_food_item_frame_content

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.upcell = PanedWindow(self.update_order_paned, height=gv.h(550), orient='horizontal')
		self.downcell = PanedWindow(self.update_order_paned, height=96, row=1, orient='horizontal')

		self.update_order_paned.add(self.upcell)
		self.update_order_paned.add(self.downcell)

		self.upleftcell = PanedWindow(self.upcell, width=gv.w(860), height=gv.h(550))
		self.uprightcell = PanedWindow(
			self.upcell, width=gv.w(500), column=1,
			height=gv.h(550))

		self.upcell.add(self.upleftcell)
		self.upcell.add(self.uprightcell)

		self.f_search = Frame(self.upleftcell, width=gv.w(860), height=48, bg="bg-white")
		self.upleftdowncell = PanedWindow(
			self.upleftcell, width=gv.w(860), height=gv.h(500), row=1, orient='horizontal')

		self.upleftcell.add(self.f_search)
		self.upleftcell.add(self.upleftdowncell)

		self.f_user_staff_table = Frame(self.uprightcell, width=gv.w(490), height=gv.h(92))
		self.f_cart_table = PanedWindow(self.uprightcell, width=gv.w(490), height=gv.h(450), row=1, orient='horizontal')

		self.uprightcell.add(self.f_user_staff_table)
		self.uprightcell.add(self.f_cart_table)

		self.downleftcell = Frame(self.downcell, width=int(gv.device_width / 2), height=124)
		self.downrightcell = Frame(self.downcell, width=int(gv.device_width / 2), height=124, column=1)

		self.downcell.add(self.downleftcell)
		self.downcell.add(self.downrightcell)

		self.f_cat_item = PanedWindow(self.upleftdowncell, width=gv.w(120), height=0, gridrow=0, orient='horizontal')
		self.f_food_item = Frame(self.upleftdowncell, column=1, width=gv.w(710), height=gv.h(500))

		self.upleftdowncell.add(self.f_cat_item)
		self.upleftdowncell.add(self.f_food_item)

		self.f_controler_count = Frame(
			self.downleftcell,
			width=gv.w(300),
			height=62,
			pady=10,
			bg="#FFFFFF"
		)

		self.f_controler_button = Frame(
			self.downrightcell,
			# width=gv.w(300),
			height=62,
			pady=10,
			bg="#FFFFFF",
			sticky='e'
		)

		self.topand_canvas = Canvas(
			self.f_search,
			width=gv.w(855),
			height=44,
			mousescroll=False
		)

		self.category_canvas = Canvas(
			self.f_cat_item,
			width=gv.w(96),
			height=gv.h(524),
			scrollregion=[0, 0, 0, 0],
			gridrow=0
		)

		self.f_cat_item.add(self.category_canvas)

		self.category_scrollbar = Scrollbar(
			self.f_cat_item,
			scroll_on=self.category_canvas,
			width=5
		)

		self.f_cat_item.add(self.category_scrollbar)

		self.food_canvas = Canvas(
			self.f_food_item,
			width=gv.w(735),
			height=gv.h(500),
			scrollregion=[0, 0, 0, 0],
			# bg="#000000"
		)

		self.food_scrollbar = Scrollbar(
			self.f_food_item,
			scroll_on=self.food_canvas,
			width=5
		)

		self.cart_canvas = Canvas(
			self.f_cart_table,
			width=gv.w(490),
			height=gv.h(450),
			scrollregion=[0, 0, 0, 0],
			row=1
		)

		self.cart_scrollbar = Scrollbar(
			self.f_cart_table,
			scroll_on=self.cart_canvas,
			row=1,
			width=5
		)

		self.f_cart_table.add(self.cart_canvas)
		self.f_cart_table.add(self.cart_scrollbar)

		get_search_frame_content(
							this,
							self,
							self.f_search
						)

		get_user_staf_table_content(
							this,
							self,
							self.f_user_staff_table
						)

		get_controller_button_content(
							this,
							self,
							self.f_controler_button,
							width=30,
							font=('Calibri', 10),
							row=3,
							column=0,
							update=True,
							order=this.order
						)

		get_controller_count_content(
							this,
							self,
							self.f_controler_count,
							width=15,
							font=('Calibri', 10),
							row=3,
							column=0
						)

		get_category_list_content(
							this,
							self,
							self.category_canvas,
							self.f_cat_item
						)

		get_food_item_frame_content(
							this,
							self,
							self.food_canvas,
							self.f_cart_table
						)

		order_menu 	= OrderItem().qset.filter(
										order_id=this.order['id']
									).all()

		if order_menu:
			for order in order_menu:
				menu = Food().qset.filter(
									id=order['menu_id'],
									ProductsIsActive=1,
									sep='AND'
								).first()

				variant = Varient().qset.filter(
									id=order['varientid']
								).first()

				# order_data = {
				# 	"variant_id" : order['varientid'],
				# 	"menu_id" : order['menu_id'],
				# 	"title" : menu['ProductName'],
				# 	"price" : variant['price'],
				# 	"size" : variant['variantName'],
				# 	"qnty" : int(order['menuqty']),
				# 	"total" : float(order['menuqty']) * float(variant['price']),
				# 	"addons" : {}
				# }

				order_data = {
					'menu': menu,
					'variant': variant,
					'quantity': int(order['menuqty']),
					'addons': {}
				}

				if order['add_on_id'] and order['add_on_id'] != "":
					ao_id_list = list(order['add_on_id'].split(", "))
					ao_qty_list = list(order['addonsqty'].split(", "))
					ao_dict = {}

					for i, addon_id in enumerate(ao_id_list):
						add_on = AddOn().qset.filter(id=addon_id).first()

						if add_on:
							addon_data = {
								"add_on_id" : add_on['id'],
								"title" : add_on['add_on_name'],
								"price" : add_on['price'],
								"qnty" : int(ao_qty_list[i]),
								"total" : float(add_on['is_active']) * int(ao_qty_list[i])
							}

							ao_dict["{}".format(add_on['id'])] = addon_data

					order_data["addons"] = ao_dict

				AddToCart(gv.pos_order.realself, order_data)
