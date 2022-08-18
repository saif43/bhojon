from tkinter import *
from dev_help.widgets import *
from ntk.objects import gv as gv

from database.table import CustomerInfo, CustomerType, Employee, FoodCategory, Food, Tables, CustomerOrder, Varient

import _help
from datetime import datetime as dtime


def order_list_search(
		self, event=None, funct=None, canv=None, target=None, entry=None,
		table=CustomerOrder, today=False, status=False, *args, **kwargs):
	try:
		if entry:
			entry_d = entry.get()
		else:
			entry_d = None

		objects = []
		fobjects = []

		if entry_d and entry_d != "":
			l_entry_d = "%" + entry_d + "%"

			cols = table().columns()
			kwd = dict((c, l_entry_d) for c in cols)

			cols = ['saleinvoice', 'order_date', 'order_time', 'totalamount', 'customer_note']

			ccols = ['customer_no', 'customer_name', 'customer_email', 'customer_phone', 'customer_address']
			csid = CustomerInfo().qset.filter(search='id', **dict((c, l_entry_d) for c in ccols)).first()
			if csid:
				kwd['customer_id'] = customer['id']

			cust_type = CustomerType().qset.filter(search='id', **dict((c, l_entry_d) for c in ['customer_type'])).first()
			if cust_type:
				kwd['customertype'] = cust_type['id']

			wcols = ['first_name', 'middle_name', 'last_name', 'email']
			waiter = Employee().qset.filter(search='id', **dict((c, l_entry_d) for c in wcols)).first()
			if waiter:
				kwd['waiter_id'] = waiter['id']

			tables = Tables().qset.filter(search='id', **dict((c, l_entry_d) for c in ['tablename'])).first()
			if tables:
				kwd['table_no'] = table['id']

			fts = " {} ".format('OR').join("{} LIKE('{}')".format(k,v) for k,v in kwd.items())

			if today:
				fts = '(' + fts + ')' + " AND order_date='{}'".format(dtime.now().strftime("%Y-%m-%d"))
			elif status:
				fts = '(' + fts + ')' + " AND order_status='{}'".format(status)

			q = "* FROM {} WHERE {}".format(table().table, fts)

			objects 	= table().qset.filter(q=q).all()

		elif entry_d == "":
			if today:
				objects = table().qset.filter(order_date=dtime.now().strftime("%Y-%m-%d")).all()
			elif status:
				objects = table().qset.filter(order_status=status).all()
			else:
				objects = table().qset.all()

		gv.paginator(self, funct, objects, canv, target)

	except Exception as e:
		gv.error_log(str(e))


def update_posfood_canvas(event, entry=None, select=None, *args, **kwargs):
	# try:
	if entry:
		entry_d = entry.get()
	else:
		entry_d = None
	if select:
		combo_d = select.get()
	else:
		combo_d = None

	if entry:
		l_entry_d = "%" + entry_d + "%"

	objects = []
	if_obj = []

	if combo_d and entry_d and combo_d != "" and entry_d != "":
		cat_obj = FoodCategory().qset.filter(Name=combo_d, CategoryIsActive=1, sep="AND").first()

		if cat_obj:
			if_obj = Food().qset.filter(
				CategoryID=cat_obj['id'], ProductName=l_entry_d, ProductsIsActive=1, sep='AND', like=1).all()

	elif combo_d and combo_d != "":
		cat_obj = FoodCategory().qset.filter(Name=combo_d, CategoryIsActive=1, sep="AND").first()
		if_obj = Food().qset.filter(CategoryID=cat_obj['id'], ProductsIsActive=1, sep='AND').all()

	elif entry_d and entry_d != "":
		if_obj = Food().qset.filter(ProductName=l_entry_d, ProductsIsActive=1, like=1, sep='AND').all()

	else:
		if_obj = Food().qset.filter(ProductsIsActive=1).all()

	# for obj in if_obj:
	# 	variants = Varient().qset.filter(menuid=obj['id']).all()
	#
	# 	if len(variants) > 0:
	# 		for ob in variants:
	# 			objects.append(ob)

	gv.food_item_frame(
		None, gv.pos_invoice, gv.pos_invoice.food_canvas, gv.pos_invoice.f_cart_table, products=if_obj)

	# except Exception as e:
	# 	pass


def update_combo_by_query(
		event, table, column, combo, active=False, active_field="is_active", active_field_data=1, fill=False, j=' '):
	cls = column.split(', ')
	try:
		query = "%" + combo.get() + "%"
		kw = {active_field: active_field_data} if active else {}

		if query != "%%":
			for c in cls:
				kw[c] = query

		cursd = [('%s'%j).join(r[c] for c in cls) for r in table().qset.filter(**kw, like=1).all()]

		combo.config(values=cursd)

		if fill and cursd:
			combo.set(cursd[0])
	except Exception as e:
		gv.error_log(str(e))

	return cursd


def update_canvas_search(self, event, funct, canv, target, entry, table, *args, **kwargs):
	try:
		objects = []
		query = "%" + entry.get() + "%"
		cols = table().columns()
		objects = table().qset.filter(like=1, **{**dict((c,query) for c in cols), **kwargs}).all()

		gv.paginator(self, funct, objects, canv, target)
	except Exception as e: gv.error_log(str(e))


def choice_dropdown(
		self, frame, width=30, font=('Calibri', 10), row=0, column=0, padx=(10, 10),
		pady=(10, 10), dic={'Pizza','Fries'}, default="Choose combo..", entry=True,
		sticky='w', readonly=False, current=False, rest=True):
	if rest:
		font = (font[0], gv.h(font[1])-1, font[2] if len(font)>2 else 'normal')
	try:
		choices = dic

		def load_all_food_again():
			self.search_combo.set("")
			self.search_field.delete(0, END)
			variants = Varient().qset.all()
			gv.food_item_frame(None, gv.pos_invoice, gv.pos_invoice.food_canvas, gv.pos_invoice.f_cart_table, variants=variants)

		if entry:
			self.search = get_a_entry(frame, pady=5, textvariable=self.Search, width=width, font=font, row=row)
			self.cobmocheck = get_a_combobox(frame, pady=5, values=choices, width=width - 6, height=24, row=row, column=column+1, padx=padx, sticky=sticky)
			self.search_button = get_a_button(frame, pady=5, width=5, text = "ALL", row=row, column=column+2, ipady=0, ipadx=14, use_ttk=False)
			self.search_button.config(command = lambda: load_all_food_again())

			return self.search, self.cobmocheck

		self.cobmocheck = get_a_combobox(frame, values=choices, width=width - 6, height=24, row=row, column=column+1, padx=padx, pady=pady, sticky=sticky)
		if readonly: self.cobmocheck.config(state="readonly")
		if current and dic: self.cobmocheck.current(0)

		return self.cobmocheck
	except Exception as e:
		gv.error_log(str(e))


gv.update_canvas_search = update_canvas_search
gv.update_combo_by_query = update_combo_by_query
gv.update_posfood_canvas = update_posfood_canvas
gv.order_list_search = order_list_search
gv.choice_dropdown = choice_dropdown
