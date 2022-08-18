
from dev_help.widgets import *
from ntk.objects import gv as gv
# from tkinter import ttk
# import os
# from threading import Thread
from __restora__.global_ import setting

from database.table import Food, Varient

# gv.error_log(str(f"File: order/snippets/addtocart.py"))

class AddToCart:
	def __init__(self, realself, data=None, action=False, *args, **kwargs):
		super(AddToCart, self).__init__(*args)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> data: {data} --> action: {action} --> args: {args} --> kwargs: {kwargs}"))

		self.realself = realself
		self.data = data
		gv.add_to_cart = self

		realself.service_charge.bind(
								'<KeyRelease>', lambda event, self=realself: \
								gv.add_to_cart.count_grand_total(
															realself, event
														)
													)

		realself.discount.bind(
							'<KeyRelease>', lambda event, self=realself: \
							gv.add_to_cart.count_grand_total(
														realself, event
													)
												)

		setting()

		# print(self.data)

		if self.data:
			self.add_to_cart(self.realself, self.data)
		elif action and kwargs.get("id_"):
			self.cart_item_action(
							self.realself,
							kwargs.get("event"),
							kwargs.get("id_"),
							kwargs.get("increase"),
							kwargs.get("decrease"),
							kwargs.get("delete"),
							kwargs.get("vid_") # Change
						)

	def count_grand_total(this, self, event=None):

		# gv.error_log(str(f"Func: count_grand_total() --> {this} --> {self}"))

		if self.service_charge.get() == "":
			self.ServiceChargeVar.set(0)

		if self.discount.get() == "":
			self.DiscountVar.set(0)

		granted_cd = {}

		for k, v in gv.cart_data.items():
			if v.get("quantity") > 0:
				granted_cd[k] = v

		gv.cart_data = granted_cd

		total, foo, men = 0.0, None, None
		for key, value in gv.cart_data.items():
			if value:
				tot = value.get("total")
				total = total + float(tot)

			if len(value.get("addons")) > 0:
				for sk, sao in value.get("addons").items():
					atot = sao.get("total")
					total = total + float(atot)

		if gv.st:
			vt = gv.st['vat']
			if vt and (vt != 0 and vt != ""):
				vt = (total/100) * vt
				self.VatVar.set(float(f'{vt:.2f}'))
				self.VatText.set(str(self.VatVar.get()))
			else:
				self.VatVar.set(0)
				self.VatText.set('0')
		else:
			self.VatVar.set(0)
			self.VatText.set('0')

		try:
			scv = float(self.ServiceChargeVar.get())
			if gv.st and gv.st['service_chargeType']:
				service_charge = (total/100) * scv
			else:
				service_charge = scv
		except:
			service_charge = 0

		try:
			dv = float(self.DiscountVar.get())
			if gv.st and gv.st['discount_type']:
				discount = (total/100) * dv
			else:
				discount = dv
		except:
			discount = 0

		grand_total = (total + self.VatVar.get() + service_charge) - discount

		self.SubtotalVar.set(float(f'{total:.2f}'))
		self.GrandTotalVar.set(float(f'{grand_total:.2f}'))
		self.GrandTotalText.set(str(self.GrandTotalVar.get()))

		return grand_total

	def cart_item_action(this, self, event=None, id_=None, increase=False, decrease=False, delete=False, vid_=None): # parameter added vid_

		# gv.error_log(str(f"Func: cart_item_action() --> {this} --> {self} --> id_{id_} --> {increase} {decrease} {delete}"))

		if id_:
			def update_cart(quantity, total):
				# gv.error_log(str(f"Func: update_cart()"))
				if quantity > 0 and total > 0:
					gv.cart_data["item_{}_{}".format(id_, vid_)]["quantity"] = quantity
					gv.cart_data["item_{}_{}".format(id_, vid_)]["total"] = total

			def delete_item():
				# gv.error_log(str(f"Func: delete_item()"))
				if "item_{}_{}".format(id_, vid_) in gv.cart_data.keys():
					gv.cart_data.pop("item_{}_{}".format(id_, vid_))

			def increase_item():
				# gv.error_log(str(f"Func: increase_item() item_{id_}_{vid_}"))
				add = True
				if "item_{}_{}".format(id_, vid_) in gv.cart_data.keys():
					item = gv.cart_data["item_{}_{}".format(id_, vid_)]

					if gv.st['stock_validation']:
						vnt = Varient().qset.filter(variantid=id_).first()
						if vnt:
							mnu = Food().qset.filter(
									id=vnt['menuid'], ProductsIsActive=1, sep='AND'
								).first()

						else:
							mnu = None

						if mnu:
							add = gv.check_stock(mnu)
						else:
							add = False

					if add:
						new_qnty = item.get("quantity") + 1.

						new_total = float(item.get("total")) + float(item.get("price"))

						update_cart(new_qnty, new_total)

			def decrease_item():
				# gv.error_log(str(f"Func: decrease_item()"))
				if "item_{}_{}".format(id_, vid_) in gv.cart_data.keys():
					item = gv.cart_data["item_{}_{}".format(id_, vid_)]

					new_qnty = int(item.get("quantity")) - 1

					new_total = float(item.get("total")) - float(item.get("price"))

					if int(new_qnty) < 1:
						delete_item()
						return

					else:
						update_cart(new_qnty, new_total)

			if delete:
				delete_item()
			elif increase:
				increase_item()
			elif decrease:
				decrease_item()

			gv.get_order_cart(gv.order_sys_realself)
			this.count_grand_total(self)

	def add_to_cart(this, self, data=None, *args, **kwargs):

		# gv.error_log(str(f"Func: add_to_cart() --> {this} --> {self} --> data: {data} --> {args} {kwargs}"))

		variant = data['variant']
		menu = data['menu']
		prev_item = gv.cart_data.get("item_{}_{}".format(
												menu['id'], variant['id']
											)
										)
		# gv.error_log(str(f"Variable: variant --> {variant}"))
		# gv.error_log(str(f"Variable: menu --> {menu}"))
		# gv.error_log(str(f"Variable: prev_item --> {prev_item}"))

		if prev_item:
			new_quantity = data["quantity"] + prev_item['quantity']
			new_total = new_quantity * variant["price"]

			new_add_ons = {}

			if len(prev_item["addons"]) > 0:
				for i, v in prev_item["addons"].items():
					new_add_ons[i] = v

				for i, v in data["addons"].items():
					new_add_ons[i] = v

			else:
				new_add_ons = data["addons"]
		else:
			new_quantity = data["quantity"]
			new_total = new_quantity * variant['price']
			new_add_ons = data['addons']

		item = {
			"variant_id": variant["id"],
			"menu_id": menu["id"],
			"title": menu["ProductName"],
			"size": variant["variantName"],
			"price": variant["price"],
			"quantity": new_quantity,
			"total": new_total,
			"addons": new_add_ons
		}

		gv.cart_data["item_{}_{}".format(menu['id'], variant['id'])] = item

		# gv.error_log(str(f"Variable: gv.cart_data --> {gv.cart_data}"))


		gv.get_order_cart(gv.order_sys_realself)

		this.count_grand_total(self)
