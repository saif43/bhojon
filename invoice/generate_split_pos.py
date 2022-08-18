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


class GenerateSplitPosInvoice:
	def __init__(self, *args, **kwargs):
		super(GenerateSplitPosInvoice, self).__init__(*args)
		self.args = args
		self.kwargs = kwargs

		print(args, kwargs)

		self.get_dependancy()

	def get_dependancy(this):
		this.create_pos_order_invoice()

	def get_space(s, l=0, d=" ", ml=44):
		spacing = ""
		if l < ml:
			for i in range(int((ml - l)/2)):
				spacing = spacing + "{}".format(d)
		return spacing

	def create_pos_order_invoice(self):
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

		order = self.kwargs.get('order')
		bill = self.kwargs.get('bill')
		sub_order = self.kwargs.get('sub_order')

		# {'id': 27, 'saleinvoice': '0027', 'marge_order_id': 'None', 'customer_id': 1, 'customer_type': 1,
		#  'isthirdparty': 0, 'waiter_id': 174, 'kitchen': 0, 'order_date': '2021-06-03', 'order_time': '10:35:53',
		#  'table_no': 50, 'tokenno': '1', 'totalamount': 2300, 'customerpaid': 1380, 'customer_note': '0',
		#  'order_status': 1, 'order_id_online': 10931, 'sync_status': 0, 'anyreason': 'None', 'cookingtime': '00:00'}

		# {'id': 25, 'customer_id': 1, 'order_id': 27, 'total_amount': 2000, 'discount': 0, 'service_charge': 0,
		#  'VAT': 300, 'bill_amount': 2300, 'bill_date': '2021-06-03', 'bill_time': '10:35:53', 'bill_status': 1,
		#  'payment_method_id': 4, 'create_by': 2, 'create_date': '2021-06-03', 'update_by': None,
		#  'update_date': '2021-06-06'}

		# {'id': 22, 'order_id': 27, 'customer_id': 1, 'vat': 180.0, 'discount': 0, 's_charge': 0, 'total_price': 1200.0,
		#  'status': 'False', 'order_menu_id': {'19': {'variant': 18, 'quantity': 1}}, 'adons_id': '', 'adons_qty': ''}

		customer = None

		if order and bill:
			customer = CustomerInfo().qset.filter(
											id=order['customer_id']
										).first()

		allsinv = 'Split{}_{}'.format(sub_order['id'], order['saleinvoice'])

		abs_path = os.path.join(
							gv.invoice_path,
							"{}_pos_invoice.pdf".format(
								# order['saleinvoice'],
								allsinv
							)
						)

		inv_file = FPDF()
		inv_file.add_page()
		inv_file.set_xy(0, 0)

		# inv_file.add_font("roboto", "", os.path.join(gv.install_path,'Amiri Italic 400.ttf'), uni=True)
		inv_file.add_font('roboto',"", "FreeSerif.ttf", uni = True)

		inv_file.set_font('roboto', "", 11.0)
		inv_file.set_fill_color(69, 194, 3)
		inv_file.set_draw_color(225, 230, 239)

		def cell(le, d=" ", ml=0, ln=2, w=0, h=4, bd=0, al="c", s_a="c"):
			sp = self.get_space(
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

		inv_file.set_font('arial', "B", 9.0)

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
				"Date: %s" % datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
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

		menu_order = sub_order['order_menu_id']

		alltotal['total'] += float(order['totalamount'] or 0)
		alltotal['billed'] += float(bill['bill_amount'] or 0)
		alltotal['vat'] += float(bill['VAT'] or 0)
		alltotal['discount'] += float(bill['discount'] or 0)
		alltotal['scharge'] += float(bill['service_charge'] or 0)
		alltotal['cpaid'] += float(order.get('customerpaid', order.get('paidamount', 0)))

		print(menu_order)

		if menu_order:
			for menu_id, menu_info in menu_order.items():
				item_food  	= Food().qset.filter(
								id=menu_id, ProductsIsActive=1, sep='AND'
							).first()

				variant 	= Varient().qset.filter(
												id=menu_info['variant']
											).first()

				cell(
					str(int(menu_info['quantity'])),
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
					str(int(int(menu_info['quantity'])*float(variant['price'] if \
					variant else 0))),
					ln=2,
					w=13,
					h=5,
					al="R",
					s_a="L",
					ml=4
				)

				multi_cell(le="\n\n")

				subtotal 	= subtotal + (int(menu_info['quantity'])*\
								float(variant['price'] if variant else 0))

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
			"{:.2f}".format(sub_order['vat']),
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
			"{:.2f}".format(sub_order['discount']),
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
			"{:.2f}".format(sub_order['s_charge']),
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
			"{:.2f}".format(
				(sub_order['total_price'] + sub_order['vat'] + sub_order['s_charge']) - sub_order['discount']),
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

		unique_id = "%s_%s" % (order['saleinvoice'], sub_order['id'])

		cell(
			"Receipt:{}|Order:{} User:{}".format(
				unique_id, unique_id, gv.user_firstname + gv.user_lastname),
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
