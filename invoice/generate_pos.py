from tkinter import messagebox, ttk
from threading import Thread
from fpdf import FPDF
import datetime, os

from dev_help.widgets import *
from ntk.objects import gv as gv

from database.table import (
		CustomerInfo, Food, CustomerOrder, OnlineOrder, Bill, BillOnline,
		OrderItem, OnlineOrderItem, Varient, AddOn, QROrder, QRBill, QROrderMenu
	)


class GeneratePosInvoice:
	def __init__(self, *args, **kwargs):
		super(GeneratePosInvoice, self).__init__(*args)
		self.realself = kwargs.get("realself")
		self.args = args
		self.kwargs = kwargs
		self.online_order = kwargs.get("online")
		self.qr_order = kwargs.get('qr')

		self.get_dependancy()

	def get_dependancy(this):
		this.create_pos_order_invoice()

	def get_space(s, l=0, d=" ", ml=44):
		spacing = ""
		if l < ml:
			for i in range(int((ml - l)/2)):
				spacing = spacing + "{}".format(d)
		return spacing

	def create_pos_order_invoice(this):
		self 			= this.realself
		saleinvoice 	= this.kwargs.get("invoice_id")
		due 			= this.kwargs.get("due")
		self.orders 	= []

		if type(saleinvoice) != list:
			saleinvoice = [saleinvoice]

		alltotal, \
		subtotal, \
		vat, \
		discount, \
		sd, \
		grand_total, \
		paid_amount, \
		change_due = {
						'total': 0,
						'billed': 0,
						'vat': 0,
						'discount': 0,
						'scharge': 0,
						'cpaid': 0
					}, 0, 0, 0, 0, 0, 0, 0

		order, \
		bill, \
		customer = None, None, None

		if this.online_order:
			ordCls, blCls, ordItms = OnlineOrder, BillOnline, OnlineOrderItem

		elif this.qr_order:
			ordCls, blCls, ordItms = QROrder, QRBill, QROrderMenu

		else:
			ordCls, blCls, ordItms = CustomerOrder, Bill, OrderItem

		for sinv in saleinvoice:
			if this.qr_order:
				order = ordCls().qset.filter(
										invoice=sinv
									).first()
				order_id_reg = 'orderd'
			else:
				order = ordCls().qset.filter(
										saleinvoice=sinv
									).first()
				order_id_reg = 'id'

			if order:
				bill = blCls().qset.filter(
											order_id=order[order_id_reg]
										).first()

			if order and bill:
				customer = CustomerInfo().qset.filter(
												id=order['customer_id']
											).first()

				if customer:
					self.orders.append({
										'order': order,
										'bill': bill,
										'customer': customer,
									})

		# if not order or not bill or not customer: return

		if not self.orders: return

		allsinv = ','.join(str(o['order'].get('saleinvoice', o['order'].get('invoice'))) for o in self.orders)

		if due:
			abs_path = os.path.join(
								gv.invoice_path,
								"{}{}_due_invoice.pdf".format(
									# order['saleinvoice']
									allsinv,
									"On" if this.online_order else ""
								)
							)

		else:
			abs_path = os.path.join(
								gv.invoice_path,
								"{}{}_pos_invoice.pdf".format(
									# order['saleinvoice'],
									allsinv,
									"On" if this.online_order else ""
								)
							)

		inv_file 		= FPDF()
		inv_file.add_page()
		inv_file.set_xy(0, 0)

		# inv_file.add_font("roboto", "", os.path.join(gv.install_path, 'Amiri Italic 400.ttf'), uni=True)
		inv_file.add_font('roboto',"", "FreeSerif.ttf", uni = True)

		inv_file.set_font('roboto', "", 11.0)
		inv_file.set_fill_color(69, 194, 3)
		inv_file.set_draw_color(225, 230, 239)

		def cell(le, d=" ", ml=0, ln=2, w=0, h=4, bd=0, al="c", s_a="c"):
			sp = this.get_space(
							len(le),
							d,
							ml
						)

			if s_a.lower() == "c":
				inv_file.cell(
							ln=ln,
							w=w,
							h=h,
							border=bd,
							align=al.upper(),
							txt="{}{}{}".format(
								sp,
								le,
								sp
							)
						)

			elif s_a.lower() == "l":
				inv_file.cell(
							ln=ln,
							w=w,
							h=h,
							border=bd,
							align=al.upper(),
							txt="{}{}{}".format(
								sp,
								sp,
								le
							)
						)

			elif s_a.lower() == "r":
				inv_file.cell(
							ln=ln,
							w=w,
							h=h,
							border=bd,
							align=al.upper(),
							txt="{}{}{}".format(
								le,
								sp,
								sp
							)
						)

		def multi_cell(le, w=0, h=0):
			inv_file.multi_cell(
							w=w,
							h=h,
							txt=le
						)

		inv_file.image(
					os.path.join(
								gv.file_dir, gv.st['logo']
							),
							x=20,
							w=40,
							h=11,
							type='PNG',
							link="{}".format(
								gv.website
							)
						)

		multi_cell(le="\n\n")

		cell(
			'{}'.format(
				gv.st['address']
			),
			ln=2,
			w=56,
			h=6,
			al="C",
			s_a="C",
			ml=18
		)

		cell(
			"{}".format(
				gv.st['phone']
			),
			ln=2,
			w=56,
			h=5,
			al="C",
			s_a="C",
			ml=18
		)

		multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			"{}".format(""),
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			s_a="R",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		if len(self.orders) == 1:
			inv_file.set_font('arial', "B", 9.0)

			customer = self.orders[0]['customer']

			cell(
				"{}".format(
					customer['customer_name'] if customer else ""
				),
				ln=2,
				w=56,
				h=6,
				al="C",
				s_a="C",
				ml=18
			)

		inv_file.set_font('roboto', "", 7.0)

		cell(
			"{}".format(
				"Date: %s" %datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
			),
			ln=2,
			w=56,
			h=5,
			al="C",
			s_a="C",
			ml=18
		)

		cell(
			'',
			ln=2,
			d="_",
			w=56,
			h=0,
			bd="B",
			al="L"
		)

		multi_cell(le="\n\n")

		cell(
			ltext("q"),
			w=6,
			ln=0,
			h=8,
			al="L",
			s_a="R",
			ml=3
		)

		cell(
			ltext("item"),
			w=22,
			ln=0,
			h=8,
			al="L",
			s_a="R",
			ml=9
		)

		cell(
			ltext("size"),
			w=10,
			ln=0,
			h=8,
			al="L",
			s_a="R",
			ml=4
		)

		cell(
			ltext("price"),
			w=10,
			ln=0,
			h=8,
			al="L",
			s_a="R",
			ml=4
		)

		cell(
			ltext("total"),
			w=13,
			ln=2,
			h=8,
			al="R",
			s_a="L",
			ml=4
		)

		multi_cell(le="\n\n")

		# if this.online_order:
		# 	menu_order = OnlineOrderItem().qset.filter(
		# 											order_id=order['id']
		# 										).all()
		#
		# else:
		# 	menu_order = OrderItem().qset.filter(
		# 										order_id=order['id']
		# 									).all()

		for itr in self.orders:
			order, bill, customer = itr['order'], itr['bill'], itr['customer']

			menu_order = ordItms().qset.filter(
												order_id=order[order_id_reg]
											).all()

			alltotal['total'] += float(order['totalamount'] or 0)
			alltotal['billed'] += float(bill['bill_amount'] or 0)
			alltotal['vat'] += float(bill['VAT'] or 0)
			alltotal['discount'] += float(bill['discount'] or 0)
			alltotal['scharge'] += float(bill['service_charge'] or 0)
			alltotal['cpaid'] += float(order.get('customerpaid', order.get('paidamount', 0)))

			if menu_order:
				for menu in menu_order:
					item_food  	= Food().qset.filter(
									id=menu['menu_id'], ProductsIsActive=1, sep='AND'
								).first()

					variant 	= Varient().qset.filter(
													id=menu['varientid']
												).first()

					cell(
						str(int(menu['menuqty'])),
						ln=0,
						w=6,
						h=5,
						al="L",
						s_a="R",
						ml=3
					)

					cell(
						(item_food['ProductName'][0:13] + \
						 (".." if len(item_food['ProductName']) > 14 else "")) if \
						 item_food else "",
						 ln=0,
						 w=21,
						 h=5,
						 al="L",
						 s_a="R",
						 ml=5
					)

					cell(
						(variant['variantName'][0:7] + \
						 ('..' if len(variant['variantName']) > 7 else '')) if \
						 variant else "",
						 ln=0,
						 w=10,
						 h=5,
						 al="L",
						 s_a="R",
						 ml=5
					)

					cell(
						str(int(variant['price']) if variant else ""),
						ln=0,
						w=10,
						h=5,
						al="R",
						s_a="L",
						ml=4
					)

					cell(
						str(int(int(menu['menuqty'])*float(variant['price'] if \
						variant else 0))),
						ln=2,
						w=13,
						h=5,
						al="R",
						s_a="L",
						ml=4
					)

					multi_cell(le="\n\n")

					subtotal 	= subtotal + (int(menu['menuqty'])*\
									float(variant['price'] if variant else 0))

					if menu['add_on_id'] != "" and menu['add_on_id']:
						for i, v in enumerate(list(menu['add_on_id'].split(","))):
							try:
								ao_id = int(v)
								ao_qt = list(menu['addonsqty'].split(","))[i]

								addon = AddOn().qset.filter(
														id=ao_id
													).first()

								if addon:
									cell(
										str(addon['add_on_name'])[0:11] + \
										 (".." if len(str(addon['add_on_name'])) > 12 else ""),
										ln=0,
										w=24,
										h=5,
										al="L",
										s_a="R",
										ml=5
									)

									cell(
										str(int(ao_qt)) + ("p" if int(ao_qt) == 1 else "ps"),
										ln=0,
										w=10,
										h=5,
										al="L",
										s_a="R",
										ml=5
									)

									cell(
										str(int(addon['price'])),
										ln=0,
										w=13,
										h=5,
										al="R",
										s_a="L",
										ml=4
									)

									cell(
										str(int(int(ao_qt)*float(addon['price']))),
										ln=2,
										w=13,
										h=5,
										al="R",
										s_a="L",
										ml=4
									)

									multi_cell(le="\n\n")

									subtotal = subtotal + (\
														int(ao_qt)*\
														float(addon['price'])
													)

							except: pass

		cdue = alltotal['total']-float(order.get('customerpaid', order.get('paidamount', 0)))
		cdue = cdue if cdue>=0 else 0

		inv_file.set_font('arial', "B", 9.0)

		cell(
			'',
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		cell(
			"{}".format(
				ltext("subtotal")
			),
			ln=0,
			w=42,
			h=5,
			al="L",
			s_a="R",
			ml=16
		)

		cell(
			"{:.2f}".format(subtotal),
			ln=2,
			w=18,
			h=5,
			al="R",
			s_a="L",
			ml=4
		)

		multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			'',
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		cell(
			"{}".format(
				ltext("vat") + "(%)"
			),
			ln=0,
			w=42,
			h=5,
			al="L",
			s_a="R",
			ml=16
		)

		cell(
			"{:.2f}".format(alltotal['vat']),
			ln=2,
			w=18,
			h=5,
			al="R",
			s_a="L",
			ml=4
		)

		multi_cell(le="\n\n")

		cell(
			"{}".format(
				ltext("discount") + ('(%)' if gv.st['discount_type'] else '')
			),
			ln=0,
			w=42,
			h=5,
			al="L",
			s_a="R",
			ml=16
		)

		cell(
			"{:.2f}".format(alltotal['discount']),
			ln=2,
			w=18,
			h=5,
			al="R",
			s_a="L",
			ml=4
		)

		multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			'',
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		cell(
			"{}".format(
				ltext("service_charge")
			),
			ln=0,
			w=42,
			h=5,
			al="L",
			s_a="R",
			ml=16
		)

		cell(
			"{:.2f}".format(alltotal['scharge']),
			ln=2,
			w=18,
			h=5,
			al="R",
			s_a="L",
			ml=4
		)

		multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			'',
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			"{}".format(
				ltext("grand_total")
			),
			ln=0,
			w=42,
			h=5,
			al="L",
			s_a="R",
			ml=16
		)

		cell(
			"{:.2f}".format(alltotal['billed']),
			ln=2,
			w=18,
			h=5,
			al="R",
			s_a="L",
			ml=4
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			'',
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		if due:
			cell(
				"{}".format(
					ltext("total_due")
				),
				ln=0,
				w=42,
				h=5,
				al="L",
				s_a="R",
				ml=16
			)

			cell(
				"{:.2f}".format(alltotal['billed']),
				ln=2,
				w=18,
				h=5,
				al="R",
				s_a="L",
				ml=4
			)

			multi_cell(le="\n\n")

		else:
			cell(
				"{}".format(
					ltext("customer_paid_amount")
				),
				ln=0,
				w=42,
				h=5,
				al="L",
				s_a="R",
				ml=16
			)

			cell(
				"{:.2f}".format(alltotal['cpaid']),
				ln=2,
				w=18,
				h=5,
				al="R",
				s_a="L",
				ml=4
			)

			multi_cell(le="\n\n")

			cell(
				"{}".format(
					ltext("change_due")
				),
				ln=0,
				w=42,
				h=5,
				al="L",
				s_a="R",
				ml=16
			)

			cell(
				"{:.2f}".format(cdue),
				ln=2,
				w=18,
				h=5,
				al="R",
				s_a="L",
				ml=10
			)

			multi_cell(le="\n\n")

		inv_file.set_font('arial', "B", 9.0)

		cell(
			'',
			ln=2,
			d="`",
			w=56,
			h=3,
			al="L",
			ml=56
		)

		inv_file.set_font('roboto', "", 7.0)

		multi_cell(le="\n\n")

		cell(
			"Receipt:{}|Order:{} User:{}".format(
				allsinv.split(',',1)[0],
				allsinv,
				gv.user_firstname + gv.user_lastname
			),
			ln=2,
			w=56,
			h=5,
			s_a="C",
			ml=0
		)

		multi_cell(le="\n\n")

		cell(
			gv.st['powerbytxt'],
			ln=0,
			w=56,
			h=5,
			s_a="C",
			ml=0
		)

		multi_cell(le="\n\n")

		inv_file.output(abs_path, 'F')
