from tkinter import messagebox, ttk
from threading import Thread
from fpdf import FPDF
import datetime, os

from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv

from database.table import (
	CustomerInfo,
	Food,
	CustomerOrder,
	OnlineOrder,
	Bill,
	BillOnline,
	OrderItem,
	OnlineOrderItem,
	Varient,
	AddOn,
	QROrder,
	QRBill,
	QROrderMenu
)


class GenerateInvoice:
	def __init__(self, *args, **kwargs):
		super(GenerateInvoice, self).__init__(*args)
		self.realself = kwargs.get("realself")
		self.args = args
		self.kwargs = kwargs
		self.online_order = kwargs.get("online")
		self.qr_order = kwargs.get("qr")

		self.get_dependancy()

	def get_dependancy(this):
		this.create_order_invoice()

	def get_space(s, l=0, d=" ", ml=44):
		spacing = ""
		if l < ml:
			for i in range(int((ml - l)/2)):
				spacing = spacing + "{}".format(d)
		return spacing

	def create_order_invoice(this):
		subtotal, discount, service_charge, vat, grand_total, cust_paid_am, change_due = 0, 0, 0, 0, 0, 0, 0
		order, bill, customer, HeadName = None, None, None, None

		self = this.realself
		saleinvoice = this.kwargs.get("saleinvoice")

		if this.online_order:
			order = OnlineOrder().qset.filter(saleinvoice=saleinvoice).first()
			if order:
				bill = BillOnline().qset.filter(order_id=order['id']).first()

		elif this.qr_order:
			order = QROrder().qset.filter(invoice=saleinvoice).first()
			if order:
				bill = QRBill().qset.filter(order_id=order['orderd']).first()

		else:
			order = CustomerOrder().qset.filter(saleinvoice=saleinvoice).first()
			if order:
				bill = Bill().qset.filter(order_id=order['id']).first()

		if order:
			customer = CustomerInfo().qset.filter(id=order['customer_id']).first()

		if customer:
			HeadName = customer['customer_no'] + "-" + customer['customer_name']

		if not order or not bill or not customer: return

		abs_path = os.path.join(
			gv.invoice_path, "{}{}_invoice.pdf".format(saleinvoice, "On" if this.online_order else ""))

		app_name, store_address, store_email = gv.st['storename'], gv.st['address'], gv.st['email']

		inv_file = FPDF()
		inv_file.add_page()
		inv_file.set_xy(0, 0)
		# inv_file.add_font("roboto", "", r'.fonts\Amiri Italic 400.ttf', uni=True)
		# inv_file.add_font("roboto", "B",r'.fonts\'FreeSerifBold.ttf', uni=True)
		# inv_file.add_font("roboto", "", os.path.join(gv.install_path,'Amiri Italic 400.ttf'), uni=True)
		# inv_file.add_font("roboto", "B",os.path.join(gv.install_path, 'FreeSerifBold.ttf'), uni=True)

		inv_file.add_font('roboto',"", "FreeSerif.ttf", uni = True)
		inv_file.add_font("roboto", "B", 'FreeSerifBold.ttf', uni=True)

		inv_file.set_font('roboto', "", 11.0)
		inv_file.set_fill_color(249, 249, 249)
		inv_file.set_draw_color(228, 229, 231)
		inv_file.set_text_color(55, 71, 103)
		inv_file.set_subject(gv.st['title'] + ' Order Detail Invoice')
		inv_file.set_display_mode("default", "continuous") #fullwidth, real, default, single, two, default
		inv_file.set_creator(gv.st['storename'])
		inv_file.set_author(gv.st['storename'])

		def cell(le, d=" ", ml=0, ln=0, w=0, h=6, bd=0, al="l", s_a="r"):
			al 	= al.upper()
			s_a = s_a.lower()
			sp 	= this.get_space(len(le), d, ml)

			if s_a == "c":
				inv_file.cell(ln=ln, w=w, h=h, border=bd, align=al, fill=0, txt="{}{}{}".format(sp, le, sp))
			elif s_a == "l":
				inv_file.cell(ln=ln, w=w, h=h, border=bd, align=al, fill=0, txt="{}{}{}".format(sp, sp, le))
			elif s_a == "r":
				inv_file.cell(ln=ln, w=w, h=h, border=bd, align=al, fill=0, txt="{}{}{}".format(le, sp, sp))

		def multi_cell(le, w=0, h=0, al="J"):
			inv_file.multi_cell(w=w, h=h, txt=le, align=al)

		try:
			inv_file.image(os.path.join(gv.file_dir, gv.st['logo']), x=9, y=4, w=48, h=12, link="%s" %gv.website)
		except Exception as e: gv.error_log(str(e))

		inv_file.set_xy(148, 4)

		ostatus = ['', 'Pending', 'Processing', 'Ready', 'Complete', 'Cancel']

		inv_file.set_font('roboto', "B", 13.0)
		cell(ltext("invoice"), h=9, w=24, al='l', ln=2)
		inv_file.set_font('roboto', "", 8.0)

		cell("{}: {}".format(ltext("invoice_no"), saleinvoice), w=24, ln=2)
		cell("{}: {}".format(ltext("order_status"), ostatus[order['order_status']]), w=24, ln=2)
		cell("{}: {}".format(ltext("billing_date"), order['order_date']), w=24, ln=2)

		inv_file.image(os.path.join(gv.depend_image_path, "billing-from.png"), x=9, y=24, w=24, h=6)

		inv_file.set_xy(9, 32)
		inv_file.set_font('roboto', "B", 11.0)
		cell(gv.st['title'], w=24, ln=2)
		inv_file.set_font('roboto', "", 8.0)
		cell(gv.st['address'], w=24, ln=2)
		cell(ltext('mobile') + ': ' + (gv.st['phone'] or ''), w=24, ln=2)
		cell(ltext('email_address') + ': ' + (gv.st['email'] or ''), w=24)

		inv_file.image(os.path.join(gv.depend_image_path, "billing-to.png"), x=148, y=36, w=24, h=6)

		inv_file.set_xy(148, 45)
		inv_file.set_font('roboto', "B", 11.0)
		cell(customer['customer_name'], w=24, ln=2)
		inv_file.set_font('roboto', "", 8.0)
		cell(ltext('address') + ': ' + (customer['customer_address'] or ''), w=24, ln=2)
		cell(ltext('mobile') + ': ' + (customer['customer_phone'] or ''), w=24, ln=2)

		inv_file.dashed_line(10, 66, 206, 66, 1, 1)

		x_v = [12, 60, 90, 116, 132, 174]
		w_s = [64, 30, 30, 24, 48]
		aw_s = [94, 30, 24, 48]
		fw_s = [148, 48]

		h_l = [ltext("item"), ltext("size"), ltext("unit_price"), ltext("quantity"), ltext("total_price")]

		inv_file.set_xy(10, 76)
		inv_file.set_font('roboto', "B", 9.0)
		for ix, x in enumerate(h_l):
			cell(x, w=w_s[ix], bd=1)
		inv_file.ln()

		if this.online_order:
			menu_order = OnlineOrderItem().qset.filter(order_id=order['id']).all()
		elif this.qr_order:
			menu_order = QROrderMenu().qset.filter(order_id=order['orderd']).all()
		else:
			menu_order = OrderItem().qset.filter(order_id=order['id']).all()

		i = 12

		inv_file.set_font('roboto', "", 8.0)

		if menu_order:
			for menu in menu_order:
				item_food = Food().qset.filter(id=menu['menu_id'], ProductsIsActive=1, sep='AND').first()
				variant = Varient().qset.filter(id=menu['varientid']).first()

				v_l = [
					[(item_food['ProductName'][0:46] + (
						".." if len(item_food['ProductName']) > 47 else "")) if item_food else "", 'l', 'r'],
					[variant.get('variantName', ''), 'l', 'r'],
					[variant.get('price', 0), 'c', 'c'],
					[menu['menuqty'], 'c', 'c'],
					[float(variant.get('price') or 0)*int(menu['menuqty'] or 0), 'r', 'l']
				]

				inv_file.set_xy(10, i*7)
				for ix, x in enumerate(w_s):
					cell(str(v_l[ix][0]), w=x, al=v_l[ix][1], s_a=v_l[ix][2], bd=1, h=7)

				maid = menu['add_on_id']
				maqt = menu['addonsqty']

				i += 1

				if maid != '' and maqt != '':
					add_ids, add_qts = maid.split(','), maqt.split(',')

					for e, aid in enumerate(add_ids):
						addon = AddOn().qset.filter(id=aid).first()

						if addon:
							av_l = [
								[addon['add_on_name'], 'l', 'r'],
								[addon['price'], 'c', 'c'],
								[add_qts[e], 'c', 'c'],
								[float(addon['price'] or 0)*int(add_qts[e] or 0), 'r', 'l']
							]

							inv_file.set_xy(10, i*7)
							for ix, x in enumerate(aw_s):
								cell(str(av_l[ix][0]), w=x, al=av_l[ix][1], s_a=av_l[ix][2], bd=1, h=7)

							i += 1

		tot_am = float(bill['bill_amount'] or 0)
		paid_am = float(order.get('customerpaid', order.get('paidamount', 0)))
		diff = tot_am-paid_am

		fv_l = [
			[ltext('subtotal'), bill['total_amount'], 'B'],
			[ltext('discount'), bill['discount'], 'B'],
			[ltext('service_charge'), bill['service_charge'], 'B'],
			[ltext('vat'), bill['VAT'], 'B'],
			[ltext('grand_total'), tot_am, 'B'],
			[ltext('total_due'), diff if diff > 0 else 0, ''],
			[ltext('change_due'), (+diff) if diff < 0 else 0, '']
		]

		for f in fv_l:
			inv_file.set_xy(10, i*7)
			inv_file.set_font('roboto', f[2], 9.0)

			cell(str(f[0]), w=fw_s[0], al='r', s_a='l', bd=1, h=7)
			cell("{:.2f}".format(f[1]), w=fw_s[1], al='r', s_a='l', bd=1, h=7)

			i += 1

		fpath = os.path.join(gv.user_image_path, "sign", "%s_sign.png" % gv.user_id)
		if os.access(fpath, os.F_OK):
			inv_file.image(fpath, x=144, y=(i+6)*7, w=32, h=14)

		inv_file.output(abs_path, 'F')
