
from dev_help.widgets import *
from tkinter import *
from ntk.objects import gv as gv
from invoice import PrintInvoice, GenerateSplitPosInvoice
import _help, requests, os, datetime, random, time, string
from threading import Thread

from database.table import (
	CardTerminal, Bank, PaymentMethod, CustomerOrder, SubOrder,
	Bill, BillCardPayment, MultiPay, CashRegisterPaymentHistory
)
from ntk import PanedWindow, Frame, Canvas, Toplevel, SelectBox, Scrollbar, Entry, Button, Toplevel

# gv.error_log(str(f"File: order/snippets/split_payment.py"))

class OrderSplitPayment:
	def __init__(self, order=None, sub_order=None, *args, **kwargs):
		super(OrderSplitPayment, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> order: {order} --> sub_order: {sub_order} --> args: {args} --> kwargs: {kwargs}"))

		self.res_width = 960 if 960 < gv.device_width else gv.device_width
		self.res_height = 620 if 620 < gv.device_height else gv.device_height

		if gv.split_order_payment_top:
			gv.split_order_payment_top.destroy()

		gv.split_order_payment_top = self.master = master = Toplevel(
										width=self.res_width, \
										title="Pay money for sub order", \
										height=self.res_height, \
										resize_x=1, \
										resize_y=1
									)

		self.order = order
		self.sub_order = sub_order
		self.ctl = None
		self.sbnk = None
		self.lfd = None

		# (gv.error_log(strf"++++++++++++++++++++++++++++++++++++ Sub Order: {self.sub_order['id']} ++++++++++++++++++++++++++++++++++++"))
		sub_order2 = SubOrder().qset.update(**{
							'status': True,
							'id': self.sub_order['id']
						}, where='id')

		# gv.error_log(str(f"Sub Order ID:  {self.sub_order['id']} Status: True"))

		self.current_amnt_box = {
							'method': 0,
							'box': 0,
							'cursor': 0
						}

		grand_total = sub_order['total_price'] + sub_order['vat']

		self.amounts = {
					'total': grand_total,
					'due': grand_total,
					'paid': 0.00,
					'change': 0.00
				}

		self.get_dependency_master()

		self.allowed_str = string.digits + '.'

	def get_dependency_master(self):
		self.modal_body = PanedWindow(self.master, orient='horizontal')
		self.modal_body_left = Frame(self.modal_body, width=62)

		self.pay_meths_canv	= Canvas(
								self.modal_body_left, width=620, gridrow=0,
								gridcolumn=0, highlightthickness=0
							)

		self.modal_body_right = Frame(self.modal_body, width=320)

		self.modal_body.add(self.modal_body_left)
		self.modal_body.add(self.modal_body_right)

		self.total_amnt_canv = Canvas(
								self.modal_body_right, mousescroll=False,
								height=162, width=288
							)

		self.button_canv = Canvas(
								self.modal_body_right, mousescroll=False,
								row=1, width=288
							)

		self.op_sb = Button(
						self.modal_body_right,
						text=ltext("Pay Now"), # text=ltext("pay_now_&_print_invoice"),
						row=2, bg='#37A000', pady=10, width=24,
						font=("Calibri", 11, "bold"),
						command=lambda: self.pay_order_amount()
					)

		self.get_order_amnt_detail()
		self.get_money_calculator()

		self.pay_methods = PaymentMethod().qset.filter().all()
		self.pay_methods_tx = [r['payment_method'] for r in self.pay_methods]

		self.banks = {
					r['bank_name']: r for r in Bank().qset.all()
				}

		self.banks_tx = list(self.banks.keys())

		self.terminals = {
					r['terminal_name']: r for r in CardTerminal().qset.all()
				}

		self.terminals_tx = list(self.terminals.keys())

		self.methods = [{
						'ID': 4,
						'Method': 'Cash Payment',
						'Amount': self.amounts['total']
					}]

		self.get_methods_detail()

	def count_changes_amount(self, event=None, number=None):
		meth = self.methods[self.current_amnt_box['method']]

		try:
			if number:
				if number == "C":
					meth['Amount'] = 0.0
					self.current_amnt_box['box'].set("")
				else:
					pcp = self.current_amnt_box['box'].get()
					new_cp = "%s%s" %(pcp, number)
					meth['Amount'] = new_cp
					self.current_amnt_box['box'].set(new_cp)

		except Exception as e: gv.error_log(str(e))

		self.get_methods_detail()

	def count_after_type(self, e=False, itr=False, att=False):
		# print(self.current_amnt_box['cursor'])
		cab = self.current_amnt_box

		f_poss = e.char in self.allowed_str
		# s_poss = e.keysym == 'BackSpace'

		# if f_poss:
			# if e and itr and att:
				# itr[att].set(itr[att].get() + e.char)

				# itr[att].insert(cab['cursor'], e.char)
				# cab['cursor'] += 1

				# if s_poss:
					# itr[att].set(itr[att].get()[:-1])

		if not f_poss:
			itr[att].set(itr[att].get()[:-1])

		self.amounts['paid'] = 0

		for meth in self.methods:
			mbt = meth['amountbox'].get()

			meth['Amount'] = mbt

			self.amounts['paid'] += float(mbt or 0)

		chn = self.amounts['paid'] - self.amounts['total']
		self.amounts['change'] = chn if chn>0 else 0

		self.total_amnt_canv.itemconfig(
							self.amounts['pa_amn'], text= \
							"{}{:.2f}".format(
										gv.st['curr_icon'], \
										self.amounts['paid']
							)
						)

		self.total_amnt_canv.itemconfig(
							self.amounts['ca_amn'], text= \
							"{}{:.2f}".format(
										gv.st['curr_icon'], \
										self.amounts['change']
							)
						)

			# self.get_methods_detail()

	def pay_order_amount(self):
		lofmeths = len(self.methods)

		sosp, somp, mosp, momp = 0, 0, 0, 0
		self.merge_id = ""

		if lofmeths == 0:
			_help.messagew(
					root=gv.rest.master,
					msg1=ltext("payment_not_complete"),
					msg2="Please select at least one payment method",
					error=True
				)

			return

		order = self.order
		bill = Bill().qset.filter(order_id=order['id']).first()
		meth = self.methods[0]

		order_update_kw = {
					'customerpaid': self.order['customerpaid'] + self.amounts['paid'],
					'order_status': 1,
					'saleinvoice': order['saleinvoice'],
					'sync_status': 0
				}

		if self.order['totalamount'] <= (self.order['customerpaid'] + self.amounts['paid']):
			order_update_kw['order_status'] = 4

		order = CustomerOrder().qset.update(**order_update_kw, where='saleinvoice', returning='*')

		bill = Bill().qset.update(**{
							'bill_status': 1,
							'payment_method_id': meth['ID'],
							'id': bill['id']
						}, where='id', returning='*')

		sub_order1 = SubOrder().qset.update(**{
							'status': False,
							'id': self.sub_order['id']
						}, where='id')

		# gv.error_log(str(f"Sub Order ID:  {self.sub_order['id']} Status: False"))

		thr = Thread(target=self.pay_to_web, daemon=True)
		thr.start()

		self.master.destroy()

		allsinv = 'Split{}_{}'.format(self.sub_order['id'], order['saleinvoice'])

		GenerateSplitPosInvoice(order=order, bill=bill, sub_order=self.sub_order)
		inv_file = os.path.join(gv.invoice_path, "%s_pos_invoice.pdf" % allsinv)
		PrintInvoice(print_file=inv_file)

	def pay_to_web(self):
		# order = {ix:r for ix,r in self.select_list.items() if r['sync_status']}.get(0, self.select_list[0])
		order = self.order

		oido = order['order_id_online']
		bill = Bill().qset.filter(order_id=order['id']).first()
		billcard = BillCardPayment().qset.filter(bill_id=bill['id']).first()

		ptypes = []

		issingle = 1 if len(self.methods) == 1 else 0

		for meth in self.methods:
			mpay = 0

			if not issingle:
				obj = {
					'order_id': order['id'],
					'marge_order_id': self.merge_id,
					'payment_type_id': meth['ID'],
					'amount': meth['Amount']
				}

				mpay = MultiPay().qset.create(**obj)

				# mpay = MultiPay().qset.filter(formula='DESC').first()

			ptype = {
				"order_id": "%s" %oido,
				"margeorderid": self.merge_id,
				"payment_type_id": "%s" %meth['ID'],
				"amount": "%s" %meth['Amount'],
				"cardpinfo": []
			}

			if meth['ID'] == 1:
				cnumb = meth['CardDigit']
				tname = self.terminals[meth['Terminal']]['id']
				bname = self.banks[meth['Bank']]['id']

				card = {
					'bill_id': bill['id'],
					'card_no': cnumb,
					'terminal_name': tname,
					'bank_name': bname,
					'multipay_id': mpay['id'] if mpay else ''
				}

				if billcard and issingle:
					card['id'] = billcard['id']
					BillCardPayment().qset.update(**card, where='bill_id')
				else:
					BillCardPayment().qset.create(**card)

				ptype['cardpinfo'].append({
					"card_no": "%s" %cnumb,
					"terminal_name": "%s" %tname,
					"Bank": "%s" %bname
				})

			ptypes.append(ptype)

			counter_payment_history = CashRegisterPaymentHistory().qset.create(
				register_number=gv.cash_counter['id'], payment_method=meth['ID'], amount=meth['Amount'], returning='*')

		if oido:
			try:
				url = gv.website + "app/billpayments"
				r 	= requests.post(url, data={
					'orderid': "%s" %oido,
					'payamount': self.amounts['total'],
					'paymentmethod': "%s" %meth['ID'],
					'cardterminal': "%s" %tname,
					'bankid': "%s" %bname,
					'lastfdigit': "%s" %cnumb,
					'ismultipay': '1' if len(ptypes)>1 else '0',
					'marge_order_id': self.merge_id,
					'Pay_type': ptypes
				})

				gv.sync_class_l[17]()

				status_code = r.status_code

			except: status_code = None

		return status_code

	def method_selected(self, method):
		mmeth = self.pay_methods[self.pay_methods_tx.index(
									self.methods[method]['methodbox'].get()
								)
							]

		self.methods[method]['ID'] = mmeth['id']
		self.methods[method]['Method'] = mmeth['payment_method']

		if mmeth['id'] == 1:
			self.methods[method]['Bank'] = self.banks_tx[0] \
													if self.banks_tx \
													else 'No bank found'

			self.methods[method]['Terminal'] = self.terminals_tx[0] \
													if self.terminals_tx \
													else 'No terminal found'

			self.methods[method]['CardDigit'] = ''

		self.get_methods_detail()

	def method_delete(self, method):
		self.methods.pop(method)

		self.get_methods_detail()

	def method_add(self):
		amn = self.amounts['total'] - self.amounts['paid']

		self.methods.append({
								'ID': 4,
								'Method': 'Cash Payment',
								'Amount': amn if amn>0 else 0
							})

		self.get_methods_detail()

	def get_methods_detail(self):
		self.pay_meths_canv.delete('all')

		mh = self.modal_body_left.winfo_height()

		hovitems = []

		def del_button_hover(lwitm, enter=True):
			if enter:
				self.pay_meths_canv.itemconfig(lwitm, fill='#e6ffff')
				self.pay_meths_canv.config(cursor='hand2')
			else:
				self.pay_meths_canv.itemconfig(lwitm, fill='#FFFFFF')
				self.pay_meths_canv.config(cursor='arrow')

		def hoverd(rs, rect, c_enter='#e6ffff', c_leave='#FFFFFF'):
			for i in rs:
				self.pay_meths_canv.tag_bind(i, '<Enter>', lambda e, \
				 itm=rect: self.pay_meths_canv.itemconfig(itm, fill=c_enter))

				self.pay_meths_canv.tag_bind(i, '<Leave>', lambda e, \
				 itm=rect: self.pay_meths_canv.itemconfig(itm, fill=c_leave))

		self.amounts['paid'] = 0

		row = 1
		cab = self.current_amnt_box

		for ix, method in enumerate(self.methods):
			hovitems.append([])

			globals()["del_pay_meth_{}".format(ix)] = PhotoImage(
												file=os.path.join(
													gv.fi_path, 'cus', 'x-mark.png'
												)
											)

			method['methodbox'] = SelectBox(self.pay_meths_canv, \
			 values=self.pay_methods_tx, default=method['Method'], \
			 selectcommand=lambda id=ix: self.method_selected(id), hlbg="#E4E5E7")

			ma = method['Amount']
			method['amountbox'] = Entry(self.pay_meths_canv, \
			 default="{:.2f}".format(float(ma)) if ma else "", \
			 focusinbg='#F5F5F5', bg='#F5F5F5', hlbg="#E4E5E7")

			method['amountbox'].bind('<FocusIn>', lambda x, \
			 b=method['amountbox'], m=ix: setattr(
							 				self, 'current_amnt_box', {
												'method': m,
												'box': b,
												'cursor': b.index(INSERT)
											}
										)
									)

			method['amountbox'].bind('<KeyRelease>', lambda e, \
			 itr=method, att='amountbox': self.count_after_type(e, itr, att))

			ch = (row+1)*36

			firstch = ch-56

			r1 = self.pay_meths_canv.create_text(
									24, ch-29, anchor='w', width=256, \
									text="Payment Method", font=('Calibri', 11, 'bold')
								)

			r2 = self.pay_meths_canv.create_text(
									324, ch-29, anchor='w', width=256, \
									text="Customer Payment", font=('Calibri', 11, 'bold')
								)

			self.pay_meths_canv.create_window(
									24, ch, anchor='w', width=256, height=32, \
									window=method['methodbox'].frame_master
								)

			self.pay_meths_canv.create_window(
									324, ch, anchor='w', width=256, height=32, \
									window=method['amountbox']
								)

			hovitems[ix] += [r1, r2]

			row += 2

			lastch = ch+36

			if method.get('ID') == 1:
				termbox = SelectBox(self.pay_meths_canv, values=self.terminals_tx, \
				 default=method['Terminal'], hlbg="#E4E5E7", selectcommand=lambda\
				 x=self.methods[ix]: x.update({'Terminal': x['termbox'].get()}))

				bankbox = SelectBox(self.pay_meths_canv, values=self.banks_tx,\
				 default=method['Bank'], hlbg="#E4E5E7", selectcommand=lambda\
				 x=self.methods[ix]: x.update({'Bank': x['bankbox'].get()}))

				lastfour = Entry(self.pay_meths_canv, default=method['CardDigit'],\
				 focusinbg='#F5F5F5', bg='#F5F5F5', hlbg="#E4E5E7")

				lastfour.bind('<KeyRelease>', lambda e, x=self.methods[ix]:\
				 x.update({'CardDigit': x['lastfour'].get()}))

				ch = (row+1)*36

				r1 = self.pay_meths_canv.create_text(24, ch-29, anchor='w', \
				 width=256, text="Card Terminal", font=('Calibri', 11, 'bold'))

				r2 = self.pay_meths_canv.create_text(324, ch-29, anchor='w', \
				 width=256, text="Bank", font=('Calibri', 11, 'bold'))

				r3 = self.pay_meths_canv.create_text(24, ch+43, anchor='w', \
				 width=256, text="Last 4 Digit", font=('Calibri', 11, 'bold'))

				self.pay_meths_canv.create_window(24, ch, anchor='w', \
				 width=256, height=32, window=termbox.frame_master)

				self.pay_meths_canv.create_window(324, ch, anchor='w', \
				 width=256, height=32, window=bankbox.frame_master)

				self.pay_meths_canv.create_window(24, ch+72, anchor='w', \
				 width=256, height=32, window=lastfour)

				hovitems[ix] += [r1, r2, r3]

				method['bankbox'] = bankbox
				method['termbox'] = termbox
				method['lastfour'] = lastfour

				row += 4

				lastch = ch+108

			row += 1

			mh80 = mh-100
			ch32 = ch+36

			self.pay_meths_canv.config(
							height=lastch if lastch<mh80 or mh==1 else mh80, \
							scrollregion=[0,0,620,lastch]
						)

			lower = self.pay_meths_canv.create_rectangle(
							0, firstch, 618, lastch, \
							fill='#FFFFFF', outline='#FFFFFF'
						)

			self.pay_meths_canv.tag_lower(lower)

			self.pay_meths_canv.tag_bind(
							lower, '<Enter>', lambda e, \
							itm=lower: self.pay_meths_canv.itemconfig(
															itm, fill="#e6ffff"
							)
						)

			self.pay_meths_canv.tag_bind(
							lower, '<Leave>', lambda e, itm=lower: \
							self.pay_meths_canv.itemconfig(
													itm, fill="#FFFFFF"
							)
						)

			p1 = self.pay_meths_canv.create_image(
							600, firstch+12, anchor='w', \
							image=globals()["del_pay_meth_{}".format(ix)]
						)

			self.pay_meths_canv.tag_bind(
							p1, '<Enter>', lambda e, itm=lower: \
							del_button_hover(itm)
						)

			self.pay_meths_canv.tag_bind(
							p1, '<Leave>', lambda e, itm=lower: \
							del_button_hover(itm, enter=False)
						)

			self.pay_meths_canv.tag_bind(
							p1, '<Button-1>', lambda e, itm=ix: \
							self.method_delete(itm)
						)

			hoverd(hovitems[ix] + [lower], lower)

			self.amounts['paid'] += float(method['amountbox'].get() or 0)

			if not cab['box']:
				cab['box'] = method['amountbox']

		chn = self.amounts['paid'] - self.amounts['total']
		self.amounts['change'] = chn if chn>0 else 0

		self.total_amnt_canv.itemconfig(
							self.amounts['pa_amn'], text= \
							"{}{:.2f}".format(
										gv.st['curr_icon'], \
										self.amounts['paid']
							)
						)

		self.total_amnt_canv.itemconfig(
							self.amounts['ca_amn'], text= \
							"{}{:.2f}".format(
										gv.st['curr_icon'], \
										self.amounts['change']
							)
						)

		butt = Button(
				self.modal_body_left, text='Add New Payment Method', \
				row=1, bg='#37A000', pady=24, width=24, \
				font=("Calibri", 11, "bold"), command=lambda: self.method_add()
			)

		self.current_amnt_box['box'].focus_set()

	def get_order_amnt_detail(self):
		self.total_amnt_canv.delete('all')

		hitms = ['Total Amount', 'Total Due', 'Payable Amount', 'Change Amount']
		hovitems = [[],[],[],[]]

		def hoverd(rs, c='#FFFFFF'):
			for i in hovitems[rs]:
				self.total_amnt_canv.itemconfig(i, fill=c)
				self.total_amnt_canv.itemconfig(i, fill=c)

		for ix, itm in enumerate(hitms):
			y = (ix+1)*40
			r = self.total_amnt_canv.create_rectangle(
										6, y-40, 160, y, fill='#FFFFFF', \
										outline='#DDDDDD'
						)

			t = self.total_amnt_canv.create_text(
										12, y-20, text=itm, \
										font=('Arial', 13), \
										fill='#374767', anchor='w'
						)

			hovitems[ix].append(r)

			self.total_amnt_canv.tag_bind(
										r, '<Enter>', lambda e, rs=ix, \
										c='#F5F5F5': hoverd(rs, c)
						)

			self.total_amnt_canv.tag_bind(
										r, '<Leave>', lambda e, \
										rs=ix: hoverd(rs)
						)

		bitms = [
			[self.amounts['total'], 'ta_amn'],
			[self.amounts['due'], 'td_amn'],
			[self.amounts['paid'], 'pa_amn'],
			[self.amounts['change'], 'ca_amn']
		]

		for ix, itm in enumerate(bitms):
			y = (ix+1)*40
			r = self.total_amnt_canv.create_rectangle(
										160, y-40, 287, y, fill='#FFFFFF', \
										outline='#DDDDDD'
						)

			self.amounts[itm[1]] = t = self.total_amnt_canv.create_text(
										272, y-20, text="{}{:.2f}".format(
												gv.st['curr_icon'], itm[0]), \
												font=('Arial', 13), \
												fill='#374767', anchor='e',
												width=96
						)

			hovitems[ix].append(r)

			self.total_amnt_canv.tag_bind(
										r, '<Enter>', lambda e, rs=ix, \
										c='#F5F5F5': hoverd(rs, c)
						)

			self.total_amnt_canv.tag_bind(
										r, '<Leave>', lambda e, \
										rs=ix: hoverd(rs)
						)

	def get_money_calculator(self):
		row, column = 0, 1
		butt_list = [
			1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20,
			50, 100, 500, 1000, "0", "00", "C"
		]

		for i in range(18):
			if column%4 == 0:
				row += 1
				column = 1

				self.button_canv.config(height=((row+1)*60)+6)

			x1 = ((column-1)*96)
			y1 = (row*60)
			x2 = column*96
			y2 = (row+1)*60

			globals()["mc_b_r_{}".format(i)] = self.button_canv.create_rectangle( \
										x1 + 6, y1 + 6, x2, y2, \
										fill="#D7ECCC", outline="#37A000"
						)

			globals()["mc_b_t_{}".format(i)] = self.button_canv.create_text( \
										x1 + ((x2-x1)/2), y1 + 30, text= \
										"{}".format(butt_list[i]), \
										font=("Calibri", 13), fill="#374767"
						)

			self.button_canv.tag_bind(
										globals()["mc_b_r_{}".format(i)], \
										"<Button-1>", lambda event, \
										number=butt_list[i]: \
										self.count_changes_amount(
											event, number=number
										)
						)

			self.button_canv.tag_bind(
										globals()["mc_b_t_{}".format(i)], \
										"<Button-1>", lambda event, \
										number=butt_list[i]: \
										self.count_changes_amount(
											event, number=number
										)
						)

			canvas_mouse_el(self.button_canv, globals()["mc_b_r_{}".format(i)])
			canvas_mouse_el(self.button_canv, globals()["mc_b_t_{}".format(i)])

			column += 1

	def count_all_(self):
		pass

	def destroy(self):
		self.master.destroy()
