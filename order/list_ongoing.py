from dev_help.widgets import *
from ntk.objects import gv as gv
from dev_help.tooltip import ToolTip
from order.snippets.payment import PosOrderPayment
from invoice.view import ViewInvoice
from invoice.view_pos import ViewPosInvoice
# from order.snippets.cancel_reason import CancelReason
import os, order, _help
from PIL import Image, ImageTk
from order.snippets.split import SplitOrder
from ntk import SelectBox, Button, Frame, Canvas, Scrollbar, PanedWindow

from database.table import Employee, CustomerOrder, Tables, Bill, OrderItem, SubOrder, OrderItem

# gv.error_log(str(f"File: order/list_ongoing.py"))

class OngoingOrderList:
	def __init__(self, realself, *args, **kwargs):
		super(OngoingOrderList, self).__init__(*args, **kwargs)
		self.realself = realself
		realself.order_payment_toplevel = None

		gv.ongoing_order = self

		self.viewordertoplevel = None
		self.vieworderinvoicelevel = None
		self.complete_order_toplevel = None

		gv.merge_list = {}

		self.get_dependency_master()

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> args: {args} --> kwargs: {kwargs}"))
		

	def list_ongoing_order(this, self, search_select=False):
		if search_select and self.onord_search.get() != "":
			ords = self.onord_search.get()
			oids = ords.split('\t')[0].split('/')
			orders = CustomerOrder().qset.filter(order_status=1, saleinvoice=oids[0], sep='AND').all()
		else:
			orders = CustomerOrder().qset.filter(order_status=1).all()

		gv.paginator(self, self.ong_ord_footer, orders, self.ong_ord_li_canvas, this.get_ongoing_order_list_content)

	def get_dependency_master(this):
		self = this.realself

		self.ong_ord_li_content = PanedWindow(
								self.new_order_paned, pady=(0, 10),
								width=gv.device_width - 80, height=gv.device_height - 184
							)

		self.ong_ord_footer = Frame(self.new_order_paned, row=1, pady=0, sticky="e")

		self.new_order_paned.add(self.ong_ord_li_content)
		self.new_order_paned.add(self.ong_ord_footer)

		self.ong_ord_header = Frame(self.ong_ord_li_content, pady=0, height=48)
		self.ong_ord_li_canv_holder = PanedWindow(
			self.ong_ord_li_content, row=1, height=gv.device_height - 268, orient='horizontal')

		self.ong_ord_li_content.add(self.ong_ord_header)
		self.ong_ord_li_content.add(self.ong_ord_li_canv_holder)

		self.ong_ord_li_canvas = Canvas(
								self.ong_ord_li_canv_holder, width=gv.device_width - 42, height=gv.device_height - 268,
								scrollregion=[0, 0, 1160, 800], highlightbackground="#FAFAFA"
							)
		self.scroll_ong_ord_li = Scrollbar(self.ong_ord_li_canv_holder, self.ong_ord_li_canvas)

		# self.ong_ord_li_canvas.mousewheel_scrollbar(self.scroll_ong_ord_li)

		self.ong_ord_li_canv_holder.add(self.ong_ord_li_canvas)
		self.ong_ord_li_canv_holder.add(self.scroll_ong_ord_li)

		gv.goo_li_cont = this.get_ongoing_order_list_content

		this.list_ongoing_order(self)

		ords = [
			"%s/%s\t%s %s\t%s%s" %(\
				o['saleinvoice'],\
				o['order_id_online'],\
				o['order_date'],\
				o['order_time'],\
				gv.st['curr_icon'],\
				o['totalamount']\
			) for o in CustomerOrder().qset.filter(order_status=1).all()
		]

		self.onord_search = SelectBox(
								self.ong_ord_header, width=56, padx=20, pady=10, default="Search by order",
								values=ords, selectcommand=lambda: this.list_ongoing_order(self, True), onclick='clean'
							)
		img = PhotoImage(file=os.path.join(gv.fi_path, 'cus', 'recurring-24.png'))
		self.reload_order = Button(
								self.ong_ord_header, text='', image=img, column=1, compound='center',
								ipady=5, height=24, width=48, bg='#FFFFFF', hoverbg='#FFFFFF',
								abg='#FFFFFF', command=lambda: this.list_ongoing_order(self)
							)
		self.onord_merge = Button(
								self.ong_ord_header, text='Merge Payment', column=2, ipady=5, height=1,
								padx=(10, 10), command=lambda: this.merge_payment_callback(self)
							)

	def get_self(this, self):
		return self

	def merge_payment_callback(this, self):
		if gv.merge_list:
			if self.order_payment_toplevel:
				self.order_payment_toplevel.destroy()

			self.complete_order_window = PosOrderPayment(this, self, list(gv.merge_list.values()))

	def ongoing_order_popup_callback(this, self, event=None, order=None, update=False, *args, **kwargs):
		if kwargs.get("complete"):
			if self.order_payment_toplevel:
				self.order_payment_toplevel.destroy()

			self.complete_order_window = PosOrderPayment(this, self, [order])

		elif order and update:
			destroy_child(self.realself.resturant_frame)
			gv.order.update_order(self.realself, self.realself.resturant_frame, order)

		elif order and kwargs.get("split"):
			# split_session_order = SubOrder().qset.filter(order_id=order['id']).all()
			order_menus = OrderItem().qset.filter(order_id=order['id']).all()

			total_quantity = 0.0
			for order_menu in order_menus:
				total_quantity += order_menu['menuqty']

			order_kw = {
				'order': order,
				'max_split': total_quantity,
				'order_menus': order_menus
			}

			if total_quantity > 1.0:
				# gv.error_log(str(f"order_kw: {order_kw}"))
				SplitOrder(order_kw)
			else:
				_help.messagew(msg1="Split Order", msg2="Split not possible with this quantity!", error=True)

		elif kwargs.get("delete"):
			qst = _help.messagew(
				msg1=ltext("order_cancel_query"), msg2=ltext("are_you_sure_to_cancel_order"),
				btext1=ltext("yes"), btext2=ltext("no"), bback1="#FF0000", bback2="#45C203", question=True
			)
			if qst.result == 1:
				# CustomerOrder().qset.delete(where="WHERE saleinvoice = '%s'"%order['saleinvoice'])
				# OrderItem().qset.delete(where="WHERE order_id = '%s'"%order['id'])

				CustomerOrder().qset.update(
					where="saleinvoice", **{'saleinvoice': order['saleinvoice'], 'order_status': 5})

				orders = CustomerOrder().qset.filter(order_status=1).all()

				ords = [
					"%s/%s\t%s %s\t%s%s" %( \
						o['saleinvoice'], o['order_id_online'], o['order_date'], \
						o['order_time'], gv.st['curr_icon'], o['totalamount']) for o in orders]
				self.onord_search.show_selection(values=ords)

				gv.paginator(
					self, self.ong_ord_footer, orders, self.ong_ord_li_canvas, this.get_ongoing_order_list_content)

		elif kwargs.get("invoice"):
			if this.viewordertoplevel: this.viewordertoplevel.destroy()

			this.viewordertoplevel 			= Toplevel(self.realself.master)
			self.view_order_detail_window 	= ViewInvoice(self, this.viewordertoplevel, order['saleinvoice'])

		elif kwargs.get("pos_invoice"):
			if this.vieworderinvoicelevel: this.vieworderinvoicelevel.destroy()

			this.vieworderinvoicelevel 		= Toplevel(self.realself.master)
			self.view_order_invoice_window 	= ViewPosInvoice(self, this.vieworderinvoicelevel, order['saleinvoice'], pos_invoice=True)

	def get_ongoing_order_list_content(this, self, master, orders=None, all=None):
		master.delete("all")
		row = 1
		i_n = 0
		self.ongoing_ord_can = master
		self.onorc_parent = master.winfo_parent()
		tfile_path = os.path.join(gv.fi_path, "cus", "x-mark-24.png")
		dfile_path = os.path.join(gv.fi_path, "cus", "details-large-view-24.png")
		lfile_path = os.path.join(gv.fi_path, "cus", "view-details-24.png")
		efile_path = os.path.join(gv.fi_path, "cus", "edit-3-24.png")

		queryset = SubOrder().qset.filter(search='order_id').all()
		sub_orders = set([q['order_id'] for q in queryset])

		if len(orders) == 0:
			self.ongoing_ord_can.create_text(
				gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_order_found")),
				width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767"
			)

			self.ongoing_ord_can.config(
				height=(gv.device_height/100)*73, scrollregion=[0, 0, 0, (gv.device_height/100)*73])

			this.fempty = ImageTk.PhotoImage(
				Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize(
					(gv.h(72),gv.h(72)), Image.ANTIALIAS))

			self.ongoing_ord_can.create_image(
				gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(orders) > 0:
			checked_mark = os.path.join(gv.fi_path, "cus", "check-mark-3-20.png")
			unchecked_mark = os.path.join(gv.fi_path, "cus", "check-mark-3-24 (1).png")

			for order in orders:
				bill = Bill().qset.filter(order_id=order['id']).first()
				max_item = int((gv.device_width-80)/212)

				if bill:
					if order['id'] in sub_orders:
						has_sub_order = True
					else:
						has_sub_order = False

					if int(i_n*212) >= (max_item*212):
						row = int(i_n/max_item) + 1

						self.ongoing_ord_can.config(scrollregion=[0, 0, 1160, row*132])

					table = Tables().qset.filter(id=order['table_no']).first()
					waiter = Employee().qset.filter(id=order['waiter_id']).first()

					txl = [
						["Table: {}".format(table['tablename']) if table else "", 36, 100],
						["Order: {}".format(order['saleinvoice']), 52, 140],
						["Waiter: {} {}".format(waiter['first_name'], waiter['last_name']) if waiter else "", 76, 140]
					]

					self.ongoing_ord_can.create_rectangle(
						((i_n % max_item)*212) + 20, ((row-1)*132)+20, ((i_n % max_item)+1)*212,
						((row-1)+1)*132, fill="#F5F5F5", outline="#E0E0E0"
					)

					for tx in txl:
						self.ongoing_ord_can.create_text(
							((i_n % max_item)*212) + 28, ((row-1)*132)+tx[1], text=tx[0],
							fill="#9A9A9A", font=("Calibri", 10, "bold"), anchor="w", width=tx[2]
						)

					f, l = ((i_n % max_item) * 212), ((row - 1) * 132)

					if not order['id'] in sub_orders:
						globals()["ongdelb_img_%s" % i_n] = PhotoImage(file=tfile_path).subsample(2, 2)
						globals()["onginvb_img_%s" % i_n] = PhotoImage(file=dfile_path).subsample(2, 2)
						globals()["ongpinvb_img_%s" % i_n] = PhotoImage(file=lfile_path).subsample(2, 2)
						globals()["ongeditb_img_%s" % i_n] = PhotoImage(file=efile_path).subsample(2, 2)
						globals()["cm_%s" % i_n] = PhotoImage(file=checked_mark).subsample(1, 2)
						globals()["ucm_%s" % i_n] = PhotoImage(file=unchecked_mark).subsample(10, 10)

						button_items = [
							[f+28, l+108, f+90, 'Complete', 'ongcomb_', '#37A000', '#FFFFFF', 10],
							[f + 94, l + 108, f + 128, 'Split', 'ongsplitb_', '#37A000', '#FFFFFF', 10],
							[
								f+132, l+108, f+156, globals()["ongdelb_img_{}".format(i_n)],
								'ongdelb_', '#37A000', '#FFFFFF', 10
							],
							[
								f+160, l+108, f+182, globals()["onginvb_img_{}".format(i_n)],
								'onginvb_', '#37A000', '#FFFFFF', 10
							],
							[
								f+186, l+108, f+208, globals()["ongpinvb_img_{}".format(i_n)],
								'ongpinvb_', '#37A000', '#FFFFFF', 10
							],
							[
								f+140, l+36, f+164, globals()["ongeditb_img_{}".format(i_n)],
								'ongeditb_', '#37A000', '#FFFFFF', 10
							],
							[
								f+186, l+36, f+208, globals()["ucm_{}".format(i_n)],
								'mocm_but_', '#FFFFFF', '#37A000', 9
							]
						]

						for i in button_items:
							globals()["{}btrec_{}".format(i[4], i_n)] = self.ongoing_ord_can.create_rectangle(
								i[0], i[1] - i[7], i[2], i[1] + i[7],
								fill=i[5], outline=i[6])
							if i[3] != 'Complete' and i[3] != 'Split':
								globals()["{}btim_{}".format(i[4], i_n)] = self.ongoing_ord_can.create_image(
									i[0] + 12,
									i[1],
									image=i[3],
									anchor="center")
							else:
								globals()["{}btim_{}".format(i[4], i_n)] = self.ongoing_ord_can.create_text(
									i[0] + 7, i[1], text=i[3], width=96,
									font=("Calibri", 9, 'bold'),
									anchor="w", fill="#FFFFFF")

						for i in ['ongsplitb_btrec_', 'ongsplitb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" % (i, i_n)], "<Button-1>", lambda e, o=order: \
									this.ongoing_order_popup_callback(self, e, o, split=True)
							)

						for i in ['ongcomb_btrec_', 'ongcomb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" %(i, i_n)], "<Button-1>", lambda e, o=order: \
									this.ongoing_order_popup_callback(self, e, o, complete=True)
							)

						for i in ['ongdelb_btrec_', 'ongdelb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" %(i, i_n)], "<Button-1>", lambda e, o=order: \
									this.ongoing_order_popup_callback(self, e, o, delete=True)
							)

						for i in ['onginvb_btrec_', 'onginvb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" %(i, i_n)], "<Button-1>", lambda e, o=order: \
								this.ongoing_order_popup_callback(self, e, o, invoice=True)
							)

						for i in ['ongpinvb_btrec_', 'ongpinvb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" %(i, i_n)], "<Button-1>", lambda e, o=order: \
									this.ongoing_order_popup_callback(self, e, o, pos_invoice=True)
							)

						for i in ['ongeditb_btrec_', 'ongeditb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" %(i, i_n)], "<Button-1>", lambda e, o=order: \
									this.ongoing_order_popup_callback(self, e, o, update=True)
							)

						for i in ['mocm_but_btrec_', 'mocm_but_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" %(i, i_n)], "<Button-1>", lambda e, itm=i_n, o=order: \
									this.toggle_merge_select(itm, o)
							)

						ti = [
							0, 0, ltext("cancel_order"), ltext("view_detail"),
							ltext("view_due_invoice"), ltext("update_order"), 0, 0, 0, 0
						]

						ti_key = [
							'ongcomb_btrec_', 'ongcomb_btim_', 'ongdelb_btim_', 'onginvb_btim_',
							'ongpinvb_btim_', 'ongeditb_btim_', 'mocm_but_btrec_', 'mocm_but_btim_',
							'ongsplitb_btrec_', 'ongsplitb_btim_']

						for ix, i in enumerate(ti_key):  #
							if ti[ix]:
								canvas_mouse_el(
									self.ongoing_ord_can, globals()["{}{}".format(i, i_n)], tip=1, text=ti[ix])
							else:
								canvas_mouse_el(self.ongoing_ord_can, globals()["{}{}".format(i, i_n)])

					else:
						i = [f+28, l+108, f+62, 'Split', 'ongsplitb_', '#37A000', '#FFFFFF', 10]

						globals()["{}btrec_{}".format(i[4], i_n)] = self.ongoing_ord_can.create_rectangle(
							i[0], i[1] - i[7], i[2], i[1] + i[7],
							fill=i[5], outline=i[6])

						globals()["{}btim_{}".format(i[4], i_n)] = self.ongoing_ord_can.create_text(
							i[0] + 7, i[1], text=i[3], width=96,
							font=("Calibri", 9, 'bold'),
							anchor="w", fill="#FFFFFF")

						for i in ['ongsplitb_btrec_', 'ongsplitb_btim_']:
							self.ongoing_ord_can.tag_bind(
								globals()["%s%s" % (i, i_n)], "<Button-1>", lambda e, o=order: \
									this.ongoing_order_popup_callback(self, e, o, split=True)
							)

						ti = [0, 0]
						ti_key = ['ongsplitb_btrec_', 'ongsplitb_btim_']

						for ix, i in enumerate(ti_key): #
							if ti[ix]:
								canvas_mouse_el(
									self.ongoing_ord_can, globals()["{}{}".format(i, i_n)], tip=1, text=ti[ix])
							else:
								canvas_mouse_el(self.ongoing_ord_can, globals()["{}{}".format(i, i_n)])

					dh = gv.device_height - 268
					mh = row*136

					if int(mh) >= int(dh):
						self.ongoing_ord_can.config(scrollregion=[0, 0, 1150, mh])
					else:
						self.ongoing_ord_can.config(scrollregion=[0, 0, 1150, dh])

					i_n = i_n + 1

	def toggle_merge_select(self, itm, order):
		if itm in gv.merge_list:
			self.realself.ongoing_ord_can.itemconfigure(globals()["mocm_but_btrec_%s" % itm], fill='#FFFFFF')
			self.realself.ongoing_ord_can.itemconfigure(
				globals()["mocm_but_btim_%s" % itm], image=globals()["ucm_%s" % itm])
			gv.merge_list.pop(itm)
		else:
			self.realself.ongoing_ord_can.itemconfigure(globals()["mocm_but_btrec_%s" % itm], fill='#37A000')
			self.realself.ongoing_ord_can.itemconfigure(
				globals()["mocm_but_btim_%s" % itm], image=globals()["cm_%s" % itm])
			gv.merge_list[itm] = order

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
