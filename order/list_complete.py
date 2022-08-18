from dev_help.widgets import *
from ntk.objects import gv as gv
from invoice.view import ViewInvoice
from invoice.view_pos import ViewPosInvoice
import os
from PIL import Image, ImageTk

from database.table import CustomerInfo, CustomerType, Employee, Tables, CustomerOrder
from ntk import Frame, Canvas, Scrollbar, PanedWindow, Label, Entry

# gv.error_log(str(f"File: order/list_complete.py"))

class CompleteOrderList:
	def __init__(self, realself, *args, **kwargs):
		super(CompleteOrderList, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> args: {args} --> kwargs: {kwargs}"))

		self.realself = realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.cord_l_head_holder = Frame(self.order_list_paned, width=gv.device_width - 80, height=34, pady=0)
		self.cord_l_head = Frame(self.cord_l_head_holder, width=gv.device_width - 80, height=34, pady=0, sticky="e")

		self.cord_l_content = PanedWindow(
			self.order_list_paned, row=1, width=gv.device_width - 42, height=gv.device_height - 120, pady=5)

		self.order_list_paned.add(self.cord_l_head_holder)
		self.order_list_paned.add(self.cord_l_content)

		self.cord_l_header_frame = Canvas(self.cord_l_content, width=gv.device_width - 42, height=34, mousescroll=False)
		self.cord_l_canv_holder = PanedWindow(
			self.cord_l_content, width=gv.device_width - 42,
			height=gv.device_height - 268, row=1, pady=10, orient='horizontal')

		self.cord_l_footer_frame_holder = Frame(self.cord_l_content, row=2, width=gv.device_width - 80)
		self.cord_l_footer_frame = Frame(self.cord_l_footer_frame_holder, row=2, pady=0, sticky="e")

		self.cord_l_content.add(self.cord_l_header_frame)
		self.cord_l_content.add(self.cord_l_canv_holder)
		self.cord_l_content.add(self.cord_l_footer_frame_holder)

		self.cord_l_canvas = Canvas(
			self.cord_l_canv_holder, width=gv.device_width - 42, height=34, scrollregion=[0, 0, 1160, 0],
			row=1, highlightbackground="#FAFAFA")

		self.scroll_order_list = Scrollbar(self.cord_l_canv_holder, self.cord_l_canvas, row=1)

		self.cord_l_canv_holder.add(self.cord_l_canvas)
		self.cord_l_canv_holder.add(self.scroll_order_list)

		this.get_complete_order_list_head(self, self.cord_l_head)

	def get_self(this, self):
		return self

	def complete_order_popup_callback(this, self, event=None, data=None, pos=False):
		if pos and data:
			if self.vieworderinvoicelevel: self.vieworderinvoicelevel.destroy()

			self.vieworderinvoicelevel 			= Toplevel(self.realself.master)
			self.view_order_invoice_window 		= ViewPosInvoice(
				self, self.vieworderinvoicelevel, data['saleinvoice'], pos_invoice=True)
		elif data:
			if self.viewordertoplevel: self.viewordertoplevel.destroy()

			self.viewordertoplevel 				= Toplevel(self.realself.master)
			self.view_order_detail_window 		= ViewInvoice(self, self.viewordertoplevel, data['saleinvoice'])

	def get_complete_order_list_head(this, self, master):
		self.complete_order_table_created = False

		self.cord_l_head_search_label 		= Label(
			master, text=ltext("search"), case=None, sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.cord_l_head_search_entry 		= Entry(
			master, column=1, sticky="w", pady=(0, 10))

		self.cord_l_head_search_entry.bind(
			"<KeyRelease>",
			lambda e, funct=self.cord_l_footer_frame, canv=self.cord_l_canvas,\
				   target=this.get_complete_order_list_content, entry=self.cord_l_head_search_entry: gv.order_list_search(
				self, e, funct, canv, target, entry, status=4))

		self.cord_l_head_search_label.config(background="#FFFFFF")

		orders = CustomerOrder().qset.filter(order_status=4).all()
		gv.paginator(self, self.cord_l_footer_frame, orders, self.cord_l_canvas, this.get_complete_order_list_content)

	def get_complete_order_list_content(this, self, master, orders=None, all=None):
		master.delete("all")
		i_n 							= 1
		this.comp_ord_can 				= master
		this.colh_frame 				= self.cord_l_header_frame
		dfile_path 						= os.path.join(gv.fi_path, "cus", "details-large-view-24.png")
		lfile_path 						= os.path.join(gv.fi_path, "cus", "view-details-24.png")

		x_v = [
			[gv.w(0), gv.w(55)], [gv.w(55), gv.w(175)],
			[gv.w(175), gv.w(295)], [gv.w(295), gv.w(475)], [gv.w(475), gv.w(635)],
			[gv.w(635), gv.w(800)], [gv.w(800), gv.w(960)], [gv.w(960), gv.w(1095)],
			[gv.w(1095), gv.w(1195)], [gv.w(1195), gv.w(1324)]]

		hll = [
			ltext("sl"), ltext("invoice_id"), ltext('online_id'),
			ltext("customer_name"), ltext("customer_type"), ltext("waiter"),
			ltext("table"), ltext("order_date"), ltext("amount"), ltext("action")]

		for i in x_v:
			this.colh_frame.create_rectangle(
				i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.colh_frame.create_text(
				x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(orders) == 0:
			this.comp_ord_can.create_text(
				gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_order_found")),
				width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.comp_ord_can.config(
				height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(
				Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.comp_ord_can.create_image(
				gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(orders) > 0:
			for order in orders:
				customer 		= CustomerInfo().qset.filter(id=order['customer_id']).first()
				customer_type 	= CustomerType().qset.filter(id=order['customer_type']).first()
				waiter 			= Employee().qset.filter(id=order['waiter_id']).first()
				table 			= Tables().qset.filter(id=order['table_no']).first()

				txl = [
					all.index(order)+1,
					order['saleinvoice'],
					order['order_id_online'] if order['order_id_online'] else "",
					customer['customer_name'] if customer else "",
					customer_type['customer_type'] if customer_type else "",
					waiter['first_name'] + " " + waiter['last_name'] if waiter['last_name'] else "",
					table['tablename'] if table else "",
					order['order_date'],
					order['totalamount']
				]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.comp_ord_can.create_rectangle(
						i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.comp_ord_can.tag_bind(
						tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.comp_ord_can, rtbi, fill))
					this.comp_ord_can.tag_bind(
						tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(
							this.comp_ord_can, rtbi, fill))

					if ix<9:
						this.comp_ord_can.create_text(
							i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24,
							font=("Calibri", 10), anchor="w", fill="#374767")

				globals()["cmodetail_image_{}".format(i_n)] 	= PhotoImage(file=dfile_path).subsample(2, 2)
				globals()["cmoposview_image_{}".format(i_n)] 	= PhotoImage(file=lfile_path).subsample(2, 2)

				for i in [
					[43, 50, 68, globals()["cmodetail_image_{}".format(i_n)], 'cmordt_'],
					[74, 80, 98, globals()["cmoposview_image_{}".format(i_n)], 'cmorpv_']]:
					globals()["{}btrec_{}".format(i[4], i_n)] = this.comp_ord_can.create_rectangle(
						x_v[9][0]+i[0], ((i_n-1)*34)+8, x_v[9][0]+i[2], ((i_n-1)*34)+28, fill="#37A000", outline="#FFFFFF")
					globals()["{}btim_{}".format(i[4], i_n)] = this.comp_ord_can.create_image(
						x_v[9][0]+i[1], ((i_n-1)*34)+17, image=i[3], anchor="w")

				for i in ['cmordt_btrec_', 'cmordt_btim_']:
					this.comp_ord_can.tag_bind(
						globals()["{}{}".format(i, i_n)], "<Button-1>",
						lambda event=None, self=self, data=order: this.complete_order_popup_callback(self, event, data))

				for i in ['cmorpv_btrec_', 'cmorpv_btim_']:
					this.comp_ord_can.tag_bind(
						globals()["{}{}".format(i, i_n)], "<Button-1>",
						lambda event=None, self=self, data=order: this.complete_order_popup_callback(
							self, event, data, pos=True))

				dh = gv.device_height - 268
				mh = i_n * 34

				if int(mh) >= int(dh):
					this.comp_ord_can.config(scrollregion=[0, 0, 1150, mh])
				else:
					this.comp_ord_can.config(scrollregion=[0, 0, 1150, dh])

				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
