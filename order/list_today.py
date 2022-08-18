from dev_help.widgets import *
from ntk.objects import gv as gv
from invoice.view import ViewInvoice
from invoice.view_pos import ViewPosInvoice
from order.snippets.sub_orders import SubOrderWindow
# from dev_help.tooltip import ToolTip
import datetime, os, order
from PIL import Image, ImageTk

from database.table import CustomerInfo, CustomerType, Employee, CustomerOrder, Tables, SubOrder
from ntk import Frame, Canvas, Scrollbar, PanedWindow, Label, Entry

# gv.error_log(str(f"File: order/list_today.py"))

class TodayOrderList:
	def __init__(self, realself, *args, **kwargs):
		super(TodayOrderList, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> args: {args} --> kwargs: {kwargs}"))

		self.realself = realself
		gv.today_ord = self

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.tor_li_head_holder = Frame(self.new_order_paned, width=gv.device_width - 80, height=44, pady=0)
		self.tor_li_head = Frame(self.tor_li_head_holder, width=gv.device_width - 80, height=44, pady=0, sticky="e")

		self.tor_li_content = PanedWindow(
			self.new_order_paned, row=1, width=gv.device_width - 42, height=gv.device_height - 120, pady=5)

		self.new_order_paned.add(self.tor_li_head_holder)
		self.new_order_paned.add(self.tor_li_content)

		self.tor_li_header_frame = Canvas(self.tor_li_content, width=gv.device_width - 42, height=44, mousescroll=False)
		self.tor_li_canv_holder = PanedWindow(
			self.tor_li_content, width=gv.device_width - 42, height=gv.device_height - 288, row=1, pady=10, orient='horizontal')

		self.tor_footer_frame_holder = Frame(self.tor_li_content, row=2, width=gv.device_width - 80)
		self.tor_footer_frame = Frame(self.tor_footer_frame_holder, row=2, pady=0, sticky="e")

		self.tor_li_content.add(self.tor_li_header_frame)
		self.tor_li_content.add(self.tor_li_canv_holder)
		self.tor_li_content.add(self.tor_footer_frame_holder)

		self.tor_li_canvas = Canvas(
			self.tor_li_canv_holder, width=gv.device_width - 42, height=44, scrollregion=[0, 0, 1160, 0],
			row=1, highlightbackground="#FAFAFA")

		self.scroll_tor_li = Scrollbar(self.tor_li_canv_holder, self.tor_li_canvas, row=1)

		self.tor_li_canv_holder.add(self.tor_li_canvas)
		self.tor_li_canv_holder.add(self.scroll_tor_li)

		this.get_today_order_list_head(self, self.tor_li_head)

	def get_self(this, self):
		return self

	def today_order_popup_callback(
			this, self, event=None, data=None, update=False, view=False, pos_view=False, split=False):
		if data and update:
			destroy_child(self.realself.resturant_frame)
			order.update_order(self.realself, self.realself.resturant_frame, data)

		elif data and view:
			if self.view_order_window:
				self.view_order_window.master.destroy()

			this.viewordertoplevel = Toplevel(self.realself.master)
			self.view_order_window = ViewInvoice(self, this.viewordertoplevel, data['saleinvoice'])

		elif data and pos_view:
			if self.pos_view_order_window:
				self.pos_view_order_window.master.destroy()

			this.vieworderinvoicelevel = Toplevel(self.realself.master)
			self.pos_view_order_window = ViewPosInvoice(
				self, this.vieworderinvoicelevel, data['saleinvoice'], pos_invoice=True)

		elif data and split:
			SubOrderWindow(order=data)

	def get_today_order_list_head(this, self, master):
		self.tlhs_l = Label(master, text="Search", case=None, sticky="e", font=("Calibri", 10, "bold"), pady=0)
		self.tlh_sd = Entry(master, column=1, sticky="w", pady=0)

		self.tlh_sd.bind(
			"<KeyRelease>", lambda e, funct=self.tor_footer_frame,
							   canv=self.tor_li_canvas, target=this.get_today_order_list_content,
							   entry=self.tlh_sd: gv.order_list_search(self, e, funct, canv, target, entry, today=1))

		self.tlhs_l.config(background="#FFFFFF")

		gv.gto_li_cont = this.get_today_order_list_content

		orders = CustomerOrder().qset.filter(order_date=datetime.datetime.now().strftime('%Y-%m-%d')).all()
		gv.paginator(self, self.tor_footer_frame, orders, self.tor_li_canvas, this.get_today_order_list_content)

	def get_today_order_list_content(this, self, master, orders=None, all=None):
		master.delete("all")
		i_n 						= 1
		fobs 						= []
		this.today_ord_can 			= master
		this.tolh_frame 			= self.tor_li_header_frame
		vfile_path 					= os.path.join(gv.fi_path, "cus", "details-large-view-24.png")
		vpfile_path 				= os.path.join(gv.fi_path, "cus", "view-details-24.png")
		efile_path 					= os.path.join(gv.fi_path, "cus", "edit-3-24.png")
		ord_status 					= ['', 'Pending', 'Processing', 'Ready', 'Complete', 'Cancel']

		queryset = SubOrder().qset.filter(search='order_id').all()
		sub_orders = set([q['order_id'] for q in queryset])

		x_v = [
			[gv.w(0), gv.w(55)], [gv.w(55), gv.w(155)], [gv.w(155), gv.w(255)], [gv.w(255), gv.w(425)],
			[gv.w(425), gv.w(625)], [gv.w(625), gv.w(765)], [gv.w(765), gv.w(900)], [gv.w(900), gv.w(1000)],
			[gv.w(1000), gv.w(1105)], [gv.w(1105), gv.w(1205)], [gv.w(1205), gv.w(1324)]]

		hll = [
			ltext("sl"), ltext("invoice_id"), ltext("online_id"), ltext("customer_name"), ltext("customer_type"),
			ltext("waiter"), ltext("table"), ltext("order_date"), ltext("amount"), ltext("status"), ltext("action")]
		for i in x_v:
			this.tolh_frame.create_rectangle(
				i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.tolh_frame.create_text(
				x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(orders) == 0:
			this.today_ord_can.create_text(
				gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_order_found")),
				width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.today_ord_can.config(
				height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(
				Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize(
					(gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.today_ord_can.create_image(
				gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(orders) > 0:
			for order in orders:
				try:
					customer = CustomerInfo().qset.filter(id=order['customer_id']).first()
					customer_type = CustomerType().qset.filter(id=order['customer_type']).first()
					waiter = Employee().qset.filter(id=order['waiter_id']).first()
					table = Tables().qset.filter(id=order['table_no']).first()

					txl = [
						all.index(order)+1,
						order['saleinvoice'],
						order['order_id_online'] if order['order_id_online'] else "",
						customer['customer_name'] if customer else "",
						customer_type['customer_type'] if customer_type else "",
						waiter['first_name'] + " " + waiter['last_name'] if waiter['last_name'] else "",
						table['tablename'] if table else "",
						order['order_date'],
						order['totalamount'],
						ord_status[order['order_status']]
					]

					rtbi = []
					for ix, i in enumerate(x_v):
						tbi = this.today_ord_can.create_rectangle(
							i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
						rtbi.append(tbi)

						this.today_ord_can.tag_bind(
							tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(
								this.today_ord_can, rtbi, fill))
						this.today_ord_can.tag_bind(
							tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(
								this.today_ord_can, rtbi, fill))

						if ix<10:
							this.today_ord_can.create_text(
								i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24,
								font=("Calibri", 10), anchor="w", fill="#374767")

					globals()["toview_image_{}".format(i_n)] = PhotoImage(file=vfile_path).subsample(2, 2)
					globals()["toposview_image_{}".format(i_n)] = PhotoImage(file=vpfile_path).subsample(2, 2)
					globals()["toedit_image_{}".format(i_n)] = PhotoImage(file=efile_path).subsample(2, 2)

					for i in [
						[8, 14, 30, globals()["toedit_image_{}".format(i_n)], 'toedit_'],
						[34, 40, 56, globals()["toview_image_{}".format(i_n)], 'toview_'],
						[60, 64, 80, globals()["toposview_image_{}".format(i_n)], 'toposview_']]:
						globals()["{}btrec_{}".format(i[4], i_n)] = this.today_ord_can.create_rectangle(
							x_v[10][0]+i[0], ((i_n-1)*34)+8, x_v[10][0]+i[2],
							((i_n-1)*34)+28, fill="#37A000", outline="#FFFFFF")
						globals()["{}btim_{}".format(i[4], i_n)] = this.today_ord_can.create_image(
							x_v[10][0]+i[1], ((i_n-1)*34)+17, image=i[3], anchor="w")

					for i in ['toedit_btrec_', 'toedit_btim_']:
						this.today_ord_can.tag_bind(
							globals()["{}{}".format(i, i_n)], "<Button-1>",
							lambda event=None, self=self, data=order, update=True: this.today_order_popup_callback(
								self, event, data, update=update))

					for i in ['toview_btrec_', 'toview_btim_']:
						this.today_ord_can.tag_bind(
							globals()["{}{}".format(i, i_n)], "<Button-1>",
							lambda event=None, self=self, data=order, view=True: this.today_order_popup_callback(
								self, event, data, view=view))

					for i in ['toposview_btrec_', 'toposview_btim_']:
						this.today_ord_can.tag_bind(
							globals()["{}{}".format(i, i_n)], "<Button-1>",
							lambda event=None, self=self, data=order, pos_view=True: this.today_order_popup_callback(
								self, event, data, pos_view=pos_view))

					if order['id'] in sub_orders:
						globals()["tosplitrectview_{}".format(i_n)] = this.today_ord_can.create_rectangle(
							x_v[10][0] + 84, ((i_n - 1) * 34) + 8, x_v[10][0] + 115,
							((i_n - 1) * 34) + 28, fill="#37A000", outline="#FFFFFF")
						globals()["tosplitview_{}".format(i_n)] = this.today_ord_can.create_text(
							x_v[10][0] + 88, ((i_n - 1) * 34) + 17, text='Split', anchor="w", fill='#FFF')

						for i in ['tosplitrectview_', 'tosplitview_']:
							this.today_ord_can.tag_bind(
								globals()["{}{}".format(i, i_n)], "<Button-1>",
								lambda event=None, self=self, data=order, pos_view=True: this.today_order_popup_callback(
									self, event, data, split=True))

						canvas_mouse_el(this.today_ord_can, globals()["tosplitrectview_{}".format(i_n)])
						canvas_mouse_el(this.today_ord_can, globals()["tosplitview_{}".format(i_n)])

					canvas_mouse_el(this.today_ord_can, globals()["toedit_btim_{}".format(i_n)])
					canvas_mouse_el(this.today_ord_can, globals()["toview_btim_{}".format(i_n)])
					canvas_mouse_el(this.today_ord_can, globals()["toposview_btim_{}".format(i_n)])

					dh = gv.device_height - 268
					mh = i_n * 34

					if int(mh) >= int(dh):
						this.today_ord_can.config(scrollregion=[0, 0, 1150, mh])
					else:
						this.today_ord_can.config(scrollregion=[0, 0, 1150, dh])

					i_n = i_n + 1

				except:
					pass

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
