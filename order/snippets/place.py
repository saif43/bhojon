
import sys
from click import command

from gevent import config
from dev_help.widgets import *
from ntk.objects import gv as gv
from dev_help.notify import Notify
# from tkinter import ttk, Toplevel
import os, json, requests, datetime, time, _help
import order as mod_order, _help

from order.snippets.payment import PosOrderPayment
from invoice import GenerateToken, PrintInvoice

from database.table import (
		CustomerType,
		Employee,
		Food,
		Tables,
		ThirdPartyCustomer,
		AddOn,
		CustomerOrder,
		PaymentMethod,
		CustomerInfo,
		Bill,
		OrderItem
	)


class PlaceOrder:
	def __init__(self, fself, realself, update=False, order=None, *args, **kwargs):
		super(PlaceOrder, self).__init__(*args)
		self.fromself = fself
		self.realself = realself
		self.update = update
		self.order = order
		self.response = False
		self.realself.order_payment_toplevel = None

		self.quick_order = kwargs.get("quick_order")

		if self.update and not self.order: return

		gv.place_order = self

		self.get_dependency(realself)

	def get_dependency(this, self):
		this.waiter, waiter, this.table, table,\
		this.thirdparty, thirdparty = (None, None, None, None, None, None)

		et = ""
		ret_call = False

		if not gv.user_is_authenticated:
			_help.messagew(
					root=gv.rest.master,
					msg1=ltext("trying_to_place_order"),
					msg2=ltext("please_login_to_place_order"),
					error=True
				)

			return

		this.customer = customer = CustomerInfo().qset.filter(id=1).first()

		this.customer_type = customer_type = CustomerType().qset.filter(
								customer_type=self.CustomerType.get()
							).first()

		if not customer:
			et = ltext("please select a customer")
		elif not customer_type:
			et = ltext("please_select_customer_type")
		elif customer_type:
			ct_n = ['', 'WC', 'OC', 'TP', 'TA'][customer_type['id']]

			if ct_n == "":
				et = ltext("please_select_a_valid_customer_type")

			elif ct_n != "TP" and ct_n != "TA" and ct_n != "OC":
				this.waiter = waiter = Employee().qset.filter(
												first_name=self.Waiter.get()
											).first()

				this.table = table = Tables().qset.filter(
												tablename=self.Table.get()
											).first() 

				ctime = self.CookingTime.get()

				if not waiter and gv.pst['waiter']:
					et = ltext("please_select_waiter")

				elif not table and gv.pst['tableid']:
					et = ltext("please_select_table")

			elif ct_n == "TP":
				this.thirdparty = thirdparty = ThirdPartyCustomer().qset.filter(
									company_name=self.DelivaryCompany.get()
								).first()

				if not thirdparty:
					et = ltext("please select delivery company")

			elif ct_n == "TA" or ct_n == "OC":
				this.waiter = waiter = Employee().qset.filter(
									first_name=self.Waiter.get()
								).first()

				ctime = self.CookingTime.get()

				if not waiter and gv.pst['waiter']:
					et = ltext("please select waiter")

		if et != "":
			_help.messagew(
					msg1=ltext("order submission error"),
					msg2=ltext("something wrong") + ": %s" %et,
					error=True
				)

			return

		if len(gv.cart_data) > 0:
			if not this.update:
				this.place_order_to_web(this.realself)
			elif this.update and this.order:
				this.place_order(this.realself)
		else:
			_help.messagew(
					msg1=ltext("order submission error"),
					msg2=ltext("please select item"),
					error=True
				)

	def returned(this, iv):
		if iv == 1:
			GenerateToken(
					realself=this.realself,
					saleinvoice=this.data_n.get("saleinvoice")
				)

			inv_file = os.path.join(
				gv.invoice_path, "{}_token.pdf".format(
					this.data_n.get("saleinvoice")
				)
			)

			PrintInvoice(
					realself=this.realself,
					print_file=inv_file
				)

	def place_order_to_web(this, self):
		addata = []
		CartData = []
		data = {}

		try:
			for key, cd in gv.cart_data.items():
				food = Food().qset.filter(
							id=cd.get('menu_id'), ProductsIsActive=1, sep='AND'
						).first()

				if food:
					idata = {
						"ProductsID": str(food['id']),
						"ProductName": str(food['ProductName']),
						"ProductImage": str(gv.website + food['ProductImage']),
						"count": str(int(cd.get("quantity"))),
						"total": str(int(cd.get("total"))),
						"productvat": str(food['productvat']),
						"OffersRate": str(food['OffersRate']),
						"variantid": str(cd.get("variant_id")),
						"price": str(cd.get("price")),
						"addons": 0
					}

					if cd.get("addons"):
						for ak, ad in cd.get("addons").items():
							addon = AddOn().qset.filter(
													id=ad.get('add_on_id')
												).first()

							if addon:
								ao = {
									"addonsid": str(addon['id']),
									"add_on_name": str(addon['add_on_name']),
									"addonsprice": str(addon['price']),
									"count": str(ad.get("qnty")),
									"total": str(ad.get("total"))
								}
								addata.append(ao)

					if len(addata) > 0:
						idata["addonsinfo"] = addata
						idata["addons"] 	= 1

					CartData.append(idata)

			ctime = self.CookingTime.get()
			if gv.pst['cooktime']:
				ctime = ctime if ctime != '00:00' else '00:15'

			cphone = this.customer['customer_phone']

			data = {
				"customer_id": str(this.customer['id']),
				"full_name": str(this.customer['customer_name']),
				"phone": cphone if len(cphone or '')>4 else "0123456789",
				"cookingtime": ctime,
				"billing_address": "Dhaka",
				"Pay_type": "4",
				"SubtotalTotal": str(self.SubtotalVar.get()),
				"vat": str(self.VatVar.get()),
				"grandtotal": str(self.GrandTotalVar.get()),
				"shippingtype": "",
				"shippingdate": "",
				"service_charge": str(self.ServiceChargeVar.get()),
				"email": str(this.customer['customer_email']),
				"ISshiping": "0",
				"district": "Dhaka",
				"city": "Dhaka",
				"invoice_discount": str(self.DiscountVar.get()),
				"waiter": str(this.waiter['id']) if this.waiter else "",
				"table": str(this.table['id']) if this.table else ""
			}

			data['CartData'] = '{}'.format(str(CartData).replace("\'", "\""))

			url = gv.website + "app/placeorder"
			this.response = requests.post(url, data=data)

			# print(this.response.content.decode())

		except Exception as e:
			gv.error_log(str(e))
			_help.messagew(
				msg1=ltext("order not placed"),
				msg2=ltext("server connection failed saved as unsynchronized"),
				error=True
			)

		this.place_order(self)
		return data

	def place_order(this, self):
		this.NotifyVar = IntVar()
		if not gv.user_is_authenticated:
			_help.messagew(
					msg1=ltext("order not placed"),
					msg2=ltext("please login to place order"),
					error=True
				)

			return

		saleinvoices = [
						r['saleinvoice'] for r in \
							CustomerOrder().qset.filter(
								search='saleinvoice'
						).all()
					]

		if this.response:
			res_data = this.response.json().get("data")
		else:
			res_data = False

		if len(saleinvoices) <= 0:
			saleinvoices = [0000]

		maximum_inv = str(int(max(saleinvoices)) + 1)

		if len(maximum_inv) == 1:
			next_inv = "000" + maximum_inv
		elif len(maximum_inv) == 2:
			next_inv = "00" + maximum_inv
		elif len(maximum_inv) == 3:
			next_inv = "0" + maximum_inv
		else: next_inv = maximum_inv

		now = datetime.datetime.now()

		ct = CustomerType().qset.filter(
										customer_type=self.CustomerType.get()
									).first()

		t_ors = CustomerOrder().qset.filter(
										order_date=now.strftime("%Y-%m-%d")
									).all()

		ocols, bcols = CustomerOrder().columns(), Bill().columns()

		data = {
			"saleinvoice": next_inv,
			"customer_id": this.customer['id'],
			"customer_type": this.customer_type['id'],
			"isthirdparty": this.thirdparty['id'] if this.thirdparty else 0,
			"waiter_id": this.waiter['id'] if this.waiter else "",
			"cookingtime": self.CookingTime.get(),
			"kitchen": 0,
			"order_date": now.strftime("%Y-%m-%d"),
			"order_time": now.strftime("%H:%M:%S"),
			"table_no": this.table['id'] if this.table else 0,
			"tokenno": len(t_ors)+1,
			"subtotal": self.SubtotalVar.get() or 0,
			"discount": self.DiscountVar.get() or 0,
			"vat": self.VatVar.get() or 0,
			"servicecharge": self.ServiceChargeVar.get() or 0,
			"totalamount": self.GrandTotalVar.get() or 0,
			"customerpaid": 0.00,
			"customer_note": 0,
			"order_status": 1,
			"create_by": gv.user_id,
			"update_date": now.strftime("%Y-%m-%d")
		}

		if this.update:
			bill = Bill().qset.filter(order_id=this.order['id']).first()

			data["order_id"] = this.order['id']
			data["saleinvoice"] = this.order['saleinvoice']
			data["bill_id"] = bill['id'] if bill else None
			data["order_status"] = this.order['order_status']
			data["billstatus"] = bill['bill_status'] if bill else None
			data["update_by"] = gv.user_id
			data["update_date"] = now.strftime("%Y-%m-%d")
			data["order_id_online"] = this.order['order_id_online']
			data["sync_status"] = 0

		if this.response:
			if this.response.status_code == 200:
				data["order_id_online"] = res_data.get("Orderid") if res_data else 0
				data["sync_status"] = 1

		if float(data.get("totalamount")) <= float(2):
			return

		odata = dict((k, v) for k, v in data.items() if k in ocols)

		bdata = dict((k, v) for k, v in data.items() if k in bcols)
		bdata['total_amount'] = data["subtotal"]
		bdata['service_charge'] = data["servicecharge"]
		bdata['VAT'] = data["vat"]
		bdata['bill_amount'] = data["totalamount"]
		bdata['bill_date'] = data["order_date"]
		bdata['bill_time'] = data["order_time"]
		bdata['create_date'] = data["order_date"]

		if this.update:
			CustomerOrder().qset.update(**odata, where='saleinvoice')
			bdata['id'] = bill['id']
			Bill().qset.update(**bdata, where='id')
		else:
			CustomerOrder().qset.create(**odata)

		if not this.order:
			this.order = CustomerOrder().qset.filter(
										saleinvoice=odata['saleinvoice']
									).first()

		if not this.update:
			bdata['order_id'] = this.order['id']
			Bill().qset.create(**bdata)

		oicr_li = []
		for i_k, i_v in gv.cart_data.items():
			soi = {
				'order_id': this.order['id'],
				'menu_id': i_v['menu_id'],
				'menuqty': i_v["quantity"],
				'add_on_id': ", ".join(
								str(ao['add_on_id']) for \
								ao in i_v['addons'].values()
							),
				'addonsqty': ", ".join(
								str(ao['qnty']) for \
								ao in i_v['addons'].values()
							),
				'varientid': i_v['variant_id'],
			}

			oicr_li.append(soi)

		OrderItem().qset.delete(where='WHERE order_id = %s' %this.order['id'])
		OrderItem().qset.create_all(oicr_li)

		gv.clear_order(this.fromself, self)
		# if not this.update:
			# orders = CustomerOrder().qset.filter(order_status=1).all()
			#
			# ords = [
			# 	"%s/%s\t%s %s\t%s%s" %(
			# 		o['saleinvoice'],
			# 		o['order_id_online'],
			# 		o['order_date'],
			# 		o['order_time'],
			# 		gv.st['curr_icon'],
			# 		o['totalamount']
			# 	) for o in orders
			# ]

			# this.realself.onord_search.show_selection(values=ords)

			# gv.paginator(
			# 		this.realself, this.realself.ong_ord_footer,
			# 		orders, this.realself.onor_li_canvas, gv.goo_li_cont
			# 	)

			# orders = CustomerOrder().qset.filter(
			# 		order_date=datetime.datetime.now().strftime('%Y-%m-%d')
			# 	).all()
			#
			# gv.paginator(
			# 		this.realself, this.realself.tor_footer_frame,
			# 		orders, this.realself.tor_li_canvas, gv.gto_li_cont
			# 	)

		if this.quick_order:
			order = CustomerOrder().qset.filter(
										saleinvoice=data['saleinvoice']
									).first()

			if order:
				if self.order_payment_toplevel:
					self.order_payment_toplevel.destroy()

				this.qor_pay_win = PosOrderPayment(this, self, [order])
		else:
			if this.update:
				this.data_n = data
				noti = Notify(
						self, text=ltext("order update succesfully"),
						text_2=ltext("do you want to print token no"),
						title=ltext("order update"), var=this.NotifyVar,
						returned=this.returned, button=2,
						button_1_text=ltext("close"),
						button_2_text=ltext("print token"),
						background_1="red"
					)
			

				destroy_child(self.realself.resturant_frame)
				mod_order.pos_order(
							self.realself, self.realself.resturant_frame
						)

			
			else:
				this.data_n = data
				noti = Notify(
						self, text=ltext("order placed succesfully"),
						text_2=ltext("Do you want to print token no"),
						title=ltext("order placed"), var=this.NotifyVar,
						returned=this.returned, button=2,
						button_1_text=ltext("close"),
						button_2_text=ltext("print token"),
						background_1="red"
					
					)

			# try:
			# 	# gv.error_log("========================")
			# 	# self.noti.config(command=self.get_dependancy)
			# # command=this.get_dependancy)
			
			# except Exception as e:
			# 		exception_message = str(e)
			# 		exception_type, exception_object, exception_traceback = sys.exc_info()
			# 		filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
			# 		gv.error_log(str('Raised error due to ' + (
			# 			f"An Exception Occured. \n Exception Type: {str(exception_type)}. Arguments: [{exception_message}]. File Name: {filename}, Line no: {exception_traceback.tb_lineno}")))



		return data

	
			