from threading import Thread
from fpdf import FPDF
import datetime, os

from dev_help.widgets import *
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
		Tables
	)


class GenerateToken:
	def __init__(self, *args, **kwargs):
		super(GenerateToken, self).__init__(*args)
		self.realself = kwargs.get("realself")
		self.args = args
		self.kwargs = kwargs

		self.get_dependancy()

	def get_dependancy(this):
		this.create_pos_token()

	def get_space(s, l=0, d=" ", ml=44):
		spacing = ""
		if l < ml:
			for i in range(int((ml - l)/2)):
				spacing = spacing + "{}".format(d)
		return spacing

	def create_pos_token(this):
		self = this.realself
		saleinvoice = this.kwargs.get("saleinvoice")

		order = CustomerOrder().qset.filter(
												saleinvoice=saleinvoice
											).first()

		table = Tables().qset.filter(
											id=order['table_no']
										).first()

		abs_path = os.path.join(
									gv.invoice_path, "{}_token.pdf".format(
																	saleinvoice
																)
															)

		inv_file = FPDF()
		inv_file.add_page()
		inv_file.set_xy(0, 0)

		# inv_file.add_font("roboto", "", os.path.join(gv.install_path, 'Amiri Italic 400.ttf'), uni=True)
		inv_file.add_font('roboto',"", "FreeSerif.ttf", uni = True)


		inv_file.set_font('roboto', "", 13.0)
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

		multi_cell(le="\n\n")
		cell('{}: {}'.format(
						ltext("token_no"),
						order['tokenno'] if order else "0"
					),

					ln=2,
					w=56,
					h=8,
					al="C",
					s_a="C",
					ml=40
				)

		multi_cell(le="\n\n")

		cell(
			ltext("q"),
			ln=0,
			w=6,
			h=8,
			al="L",
			s_a="R",
			ml=3
		)

		cell(
			ltext("item"),
			ln=0,
			w=38,
			h=8,
			al="L",
			s_a="R",
			ml=24
		)

		cell(
			ltext("size"),
			ln=2,
			w=24,
			h=8,
			al="L",
			s_a="R",
			ml=5
		)

		multi_cell(le="\n\n")

		menu_order = OrderItem().qset.filter(
										order_id=order['id']
									).all()

		if menu_order:
			for menu in menu_order:
				item_food 	= Food().qset.filter(
							id=menu['menu_id'], ProductsIsActive=1, sep='AND'
						).first()

				variant 	= Varient().qset.filter(
							id=menu['varientid']
						).first()

				cell(
					str(int(menu['menuqty'])),
					ln=0,
					w=6,
					h=6,
					al="L",
					s_a="R",
					ml=3
				)

				cell(
					item_food['ProductName'][0:16] + (".." if len(item_food['ProductName']) > 17 else ""),

					ln=0,
					w=38,
					h=6,
					al="L",
					s_a="R",
					ml=5
				)

				cell(
					variant['variantName'][0:7] + ('..' if len(variant['variantName']) > 7 else ''),

					ln=2,
					w=24,
					h=6,
					al="L",
					s_a="L",
					ml=5
				)

				multi_cell(le="\n\n")

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
									str(addon['add_on_name'])[0:14] + (".." if len(str(addon['add_on_name'])) > 15 else ""),

									ln=0,
									w=44,
									h=6,
									al="L",
									s_a="R",
									ml=27
								)

								cell(
									str(int(ao_qt)),
									ln=2,
									w=24,
									h=6,
									al="L",
									s_a="R",
									ml=5
								)

								multi_cell(le="\n\n")

						except: pass

		multi_cell(le="\n\n")

		cell(
			'',
			ln=2,
			d="-",
			w=56,
			h=0,
			bd="B",
			al="L"
		)

		multi_cell(le="\n\n")

		cell("{}: {} | {}: {}".format(
			ltext("table_no"),
			table['tablename'] if table else "",
			ltext("order_no"),
			order['id']),
			ln=0,
			w=56,
			h=9,
			al="C",
			s_a="C",
			ml=18
		)

		inv_file.output(abs_path, 'F')
