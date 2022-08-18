from dev_help.widgets import *
from ntk.objects import gv
from ntk import SelectBox, Frame, PanedWindow, Canvas, Toplevel, Button
from order.snippets.addtocart import AddToCart
import os
# from PIL import ImageTk
from database.table import Food, AddOn, AddOnAsign, Varient

# gv.error_log(str(f"File: order/snippets/listacoritem.py"))

class FoodItemData:
	def __init__(self, realself, product=None, variants=None, *args, **kwargs):
		super(FoodItemData, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> product: {product} --> variants: {variants} --> args: {args} --> kwargs: {kwargs}"))

		self.realself = realself

		realself.food_item_data_toplevel = self.master = Toplevel(
			width=800, height=356, bg='#FAFAFA',
			title=ltext("select_food_and_addon")
		)

		self.menu = product
		self.variants = variants

		gv.food_item_data = self

		self.result = {
			'total_quantity': 0.0 if gv.st['stock_validation'] else 1.0
		}

		self.passable_data = {}
		self.passable_addon = {}

		self.modal_painedwindow = PanedWindow(self.master, sticky='wne', padx=0, pady=0)

		self.modal_frame = Frame(self.modal_painedwindow, padx=0, pady=0)

		self.modal_painedwindow.add(self.modal_frame)

		self.item_canvas = Canvas(
								self.modal_frame, width=798, height=100,
								scrollregion=[0, 0, 798, 0], mousescroll=False, highlightcolor='bg-white'
							)

		self.itmao_canv = Canvas(
								self.modal_frame, row=1, width=798,
								height=100, scrollregion=[0, 0, 798, 0], highlightcolor='bg-white'
							)

		itmt_l = [
			[ltext("item_info"), 100],
			[ltext("quantity"), 300],
			[ltext("size"), 425],
			[ltext("price"), 550],
			[ltext("total"), 675]
		]

		for itm in itmt_l:
			self.item_canvas.create_text(
								itm[1], 24, text=itm[0],
								font=('Calibri', h(10), 'bold'),
								anchor='center'
							)

		self.CartTableQuantity = DoubleVar()
		self.CartTableQuantity.set(self.result['total_quantity'])

		add_ons = None
		i_n = 1

		add_ons = AddOnAsign().qset.filter(menu_id=self.menu['id']).all()

		def update_price_and_total():
			self.item_canvas.itemconfig(
				item_props_result['variant_price'], text=str(self.variant['price'])
			)

			self.item_canvas.itemconfig(
				item_props_result['variant_total'],
				text=str(self.variant['price'] * self.result['total_quantity'])
			)

		def dynamic_quantity():
			quantity = self.CartTableQuantity.get()
			add = gv.check_stock(self.menu, quantity)

			if add:
				self.result['total_quantity'] = quantity
				self.CartTableQuantity.set(quantity)

				update_price_and_total()

		def inc_dec_call(inc=True):
			pqt = self.result['total_quantity']

			if inc:
				quantity = float(pqt)+1.
			else:
				if pqt > 1:
					quantity = float(pqt)-1.

			add = gv.check_stock(self.menu, quantity)
			if add:
				self.result['total_quantity'] = quantity
				self.CartTableQuantity.set(quantity)

				update_price_and_total()

		def change_variance():
			variance = Varient().qset.filter(variantName=item_props_result['item_variant'].get()).first()

			if variance:
				self.variant = variance

				update_price_and_total()

		min_img_p = os.path.join(gv.fi_path, 'cus', "minus-7-24.png")
		globals()["itm_dec_but"] = PhotoImage(file=min_img_p).subsample(2, 2)

		min_img_p = os.path.join(
							gv.fi_path, 'cus', "plus-24.png"
						)

		globals()["itm_inc_but"] = PhotoImage(file=min_img_p).subsample(2, 2)

		item_props_result = {
			'variant_price': None,
			'variant_total': None,
			'item_name': None,
			'item_quantity': None,
			'item_variant': None,
			'quantity_dec': None,
			'quantity_inc': None
		}

		self.variant = self.variants[0]

		item_props_list = [
			[self.menu['ProductName'], 100, 'text', 'item_name'],
			[globals()["itm_dec_but"], 248, 'dec', 'quantity_dec'],
			[self.result['total_quantity'], 300, 'quantity', 'item_quantity'],
			[globals()["itm_inc_but"], 348, 'inc', 'quantity_inc'],
			[self.variant['variantName'], 425, 'variants', 'item_variant'],
			[self.variant['price'], 550, 'price', 'variant_price'],
			[self.variant['price'], 675, 'total', 'variant_total']
		]

		for ix, item in enumerate(item_props_list):
			if item[2] == 'dec':
				item_props_result[item[3]] = self.item_canvas.create_image(
											item[1], 60,
											image=globals()["itm_dec_but"]
										)

				self.item_canvas.tag_bind(
										item_props_result[item[3]], '<Button-1>',
										lambda e: inc_dec_call(inc=False)
									)

				canvas_mouse_el(self.item_canvas, item_props_result[item[3]])

			elif item[2] == 'inc':
				item_props_result[item[3]] = self.item_canvas.create_image(
									item[1], 60, image=globals()["itm_inc_but"]
								)

				self.item_canvas.tag_bind(
									item_props_result[item[3]], '<Button-1>',
									lambda e: inc_dec_call()
								)

				canvas_mouse_el(self.item_canvas, item_props_result[item[3]])

			elif item[2] == 'quantity':
				item_props_result[item[3]] = get_a_entry(
									self.item_canvas,
									textvariable=self.CartTableQuantity,
									use_ttk=0
								)

				self.item_canvas.create_window(
									item[1], 60, window=item_props_result[item[3]],
									anchor='center', width=72, height=24
								)

				item_props_result[item[3]].bind("<KeyRelease>", lambda e: dynamic_quantity())

			elif item[2] == 'variants':
				variants_names = [variant['variantName'] for variant in self.variants]
				item_props_result[item[3]] = SelectBox(
									self.item_canvas, default=variants_names[0],
									selectcommand=lambda: change_variance(),
									values=variants_names, width=10
								)

				self.item_canvas.create_window(
									item[1], 60, window=item_props_result[item[3]].frame_master,
									anchor='center', width=108, height=24
								)

			else:
				item_props_result[item[3]] = self.item_canvas.create_text(
									item[1], 60, text=item[0],
									font=('Calibri', h(9), 'bold'),
									fill='#374767', anchor='center',
									width=172
								)

		add_ons_list = []

		if add_ons:
			for add_on in add_ons:
				obj = AddOn().qset.filter(id=add_on['add_on_id']).first()
				if obj:
					add_ons_list.append(obj)

		if add_ons_list:
			def count_addon_again(event=None, item=None, add_on=None, mado=None):
				if int(globals()["addOnQnty_{}".format(item)].get()) < 0:
					globals()["addOnQnty_{}".format(item)].set(0)

				def start_addon_count():
					try:
						qnty = globals()["addOnQnty_{}".format(item)].get()
					except: qnty = 0

					total = float(mado['price'] or 0)*qnty

					globals()["addon_{}".format(add_on['id'])] = {
						"add_on_id" : mado['id'] if mado else None,
						"title" : (mado['add_on_name'] if mado else "").capitalize(),
						"price" : mado['price'],
						"qnty" : qnty,
						"total" : total
					}

					self.itmao_canv.itemconfig(
										globals()['aotot_%s'%item],
										text=str(total)
									)

					self.passable_addon["{}".format(add_on['id'])] = \
					 globals()["addon_{}".format(add_on['id'])]

				if event:
					if event.char.isdigit():
						start_addon_count()
					else:
						globals()["add_on_qnty_{}".format(item)].delete(
								len(globals()["add_on_qnty_{}".format(item)]\
								.get())-1, len(globals()["add_on_qnty_{}"\
								.format(item)].get())
							)
				else:
					start_addon_count()

			def aon_inc_dec_call(itm, add_on, mado, inc=True):
				pqt = globals()["addOnQnty_{}".format(itm)].get()
				if pqt == "": pqt = "0"

				if inc:
					globals()["addOnQnty_{}".format(itm)].set(int(pqt)+1)
				else: globals()["addOnQnty_{}".format(itm)].set(int(pqt)-1)

				count_addon_again(
						event=None, item=itm,
						add_on=add_on, mado=mado
					)

			itmaohl = [
				[96, ltext("addon_name")],
				[297, ltext("addon_qnty")],
				[547, ltext("addon_price")],
				[672, ltext("total")]
			]

			for aoh in itmaohl:
				self.itmao_canv.create_text(
						aoh[0], i_n*12, text=aoh[1],
						font=('Calibri', h(9), 'bold')
					)

			i_n = i_n + 1

			for obj in add_ons_list:
				if i_n == 4:
					self.item_addon_scrollbar = get_a_scrollbar(
										self.modal_frame,
										self.itmao_canv,
										row=1, column=1
									)

					self.itmao_canv.bind(
							"<MouseWheel>", lambda e, \
							canv=self.itmao_canv: mousewheel_scroll(canv, e)
						)

				if i_n <= 4:
					self.itmao_canv.config(height=(i_n+1)*24)

				# obj = AddOn().qset.filter(id=add_on['add_on_id']).first()

				# if obj:
				globals()["addOnQnty_{}".format(i_n)] = IntVar()

				itmt_l = [
					[
						"{}".format(obj['add_on_name'] if obj else ""),
						96,
						'text'
					],
					[globals()["itm_dec_but"], 245, 'dec'],
					[
						globals()["addOnQnty_{}".format(i_n)].get(),
						297,
						'qnty'
					],
					[globals()["itm_inc_but"], 345, 'inc'],
					[obj['price'], 547, 'text'],
					[0, 672, 'total']
				]

				for itm in itmt_l:
					if itm[2] == 'dec':
						globals()["aon_qt_dec_{}".format(i_n)] = self.itmao_canv.create_image(
											itm[1], i_n*32,
											image=globals()["itm_dec_but"]
										)

						self.itmao_canv.tag_bind(
									globals()["aon_qt_dec_{}".format(i_n)],
									'<Button-1>', lambda e, itm=i_n,
									add_on=add_on, mado=obj: \
									aon_inc_dec_call(
										itm, add_on,
										mado, inc=False
									)
								)

						canvas_mouse_el(
								self.itmao_canv,
								globals()["aon_qt_dec_{}".format(i_n)]
							)

					elif itm[2] == 'inc':
						globals()["aon_qt_inc_{}".format(i_n)] = self.itmao_canv.create_image(
											itm[1], i_n*32,
											image=globals()["itm_inc_but"]
										)

						self.itmao_canv.tag_bind(
									globals()["aon_qt_inc_{}".format(i_n)],
									'<Button-1>', lambda e, itm=i_n,
									add_on=add_on, mado=obj: \
									aon_inc_dec_call(
										itm, add_on, mado
									)
								)

						canvas_mouse_el(
								self.itmao_canv,
								globals()["aon_qt_inc_{}".format(i_n)]
							)

					elif itm[2] == 'qnty':
						globals()["add_on_qnty_{}".format(i_n)] = get_a_entry(
							self.itmao_canv,
							textvariable=globals()[
								"addOnQnty_{}".format(i_n)
							],
							use_ttk=0
						)

						self.itmao_canv.create_window(
							itm[1], i_n*32,
							window=globals()[
								"add_on_qnty_{}".format(i_n)
							],
							anchor='center',
							width=72, height=24
						)

						globals()["add_on_qnty_{}".format(i_n)].bind(
							"<KeyRelease>", lambda e, itm=i_n,
												   add_on=add_on, mado=obj: \
								count_addon_again(
									e, itm, add_on, mado
								)
						)

					elif itm[2] == 'total':
						globals()['aotot_%s'%i_n] = self.itmao_canv.create_text(
								itm[1], i_n*32, text=itm[0],
								font=('Calibri', h(9), 'bold'),
								fill='#374767', anchor='center'
							)

					else:
						self.itmao_canv.create_text(
								itm[1], i_n*32, text=itm[0],
								font=('Calibri', h(9), 'bold'),
								fill='#374767', anchor='center',
								width=172
							)

				self.itmao_canv.config(
									scrollregion=[0, 0, 798, (i_n+1)*32]
								)

				i_n = i_n + 1
		# else:
			# self.master.config(height=60)
			# self.itmao_canv.config(height=0)

		self.get_cart_item_data = Button(
						self.modal_frame, text="Add To Cart", ipady=1,
						row=2, column=0, pady=16, ipadx=0, height=1,
						font=("Calibri", w(12), "bold")
					)

		self.get_cart_item_data.config(
									command=lambda: self.add_to_cart()
								)

	def add_to_cart(self):
		data = {
			'menu': self.menu,
			'variant': self.variant,
			'quantity': self.result['total_quantity'],
			'addons': self.passable_addon
		}

		AddToCart(self.realself, data)

		self.master.destroy()
