from dev_help.widgets import *
from ntk.objects import gv as gv
from invoice.view import ViewInvoice
from invoice.view_pos import ViewPosInvoice
import os
from PIL import Image, ImageTk

from database.table import CustomerInfo, Employee, CustomerOrder, Tables
from ntk import Frame, Canvas, Scrollbar, PanedWindow, Label, Entry

# gv.error_log(str(f"File: order/list.py"))

class OrderList:
	def __init__(self, realself, *args, **kwargs):
		super(OrderList, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> args: {args} --> kwargs: {kwargs}"))

		self.realself 					= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.order_list_head_holder = Frame(self.order_list_paned, width=gv.device_width - 80, height=34, pady=0)
		self.order_list_head = Frame(self.order_list_head_holder, width=gv.device_width - 80, height=34, pady=0, sticky="e")

		self.order_list_content = PanedWindow(
			self.order_list_paned, row=1, width=gv.device_width - 42, height=gv.device_height - 120, pady=5)

		self.order_list_paned.add(self.order_list_head_holder)
		self.order_list_paned.add(self.order_list_content)

		self.order_list_header_frame = Canvas(
			self.order_list_content, width=gv.device_width - 42, height=34, mousescroll=False)
		self.order_list_canv_holder = PanedWindow(
			self.order_list_content, width=gv.device_width - 42,
			height=gv.device_height - 268, row=1, pady=10, orient='horizontal')

		self.order_list_footer_frame_holder = Frame(self.order_list_content, row=2, width=gv.device_width - 80)
		self.order_list_footer_frame = Frame(self.order_list_footer_frame_holder, row=2, pady=0, sticky="e")

		self.order_list_content.add(self.order_list_header_frame)
		self.order_list_content.add(self.order_list_canv_holder)
		self.order_list_content.add(self.order_list_footer_frame_holder)

		self.order_list_canvas = Canvas(
			self.order_list_canv_holder, width=gv.device_width - 42,
			height=gv.device_height - 268, scrollregion=[0, 0, 1160, 0],
			row=1, highlightbackground="#FAFAFA")

		self.scroll_order_list = Scrollbar(self.order_list_canv_holder, self.order_list_canvas, row=1)

		self.order_list_canv_holder.add(self.order_list_canvas)
		self.order_list_canv_holder.add(self.scroll_order_list)

		this.get_order_list_head(self, self.order_list_head)

	def get_self(this, self):
		return self

	def order_list_popup_callback(this, self, event=None, view=False, view_invoice=False, data=None):
		if view:
			if self.viewordertoplevel: self.viewordertoplevel.destroy()

			self.viewordertoplevel 			= Toplevel(self.realself.master)
			self.view_order_detail_window 	= ViewInvoice(
				self, self.viewordertoplevel, data['saleinvoice'])

		elif view_invoice:
			if self.vieworderinvoicelevel: self.vieworderinvoicelevel.destroy()

			self.vieworderinvoicelevel 		= Toplevel(self.realself.master)
			self.view_order_invoice_window 	= ViewPosInvoice(
				self, self.vieworderinvoicelevel, data['saleinvoice'], pos_invoice=True)

	def get_order_list_head(this, self, master):
		self.order_table_created = False

		self.olhs_l 	= Label(
			master, text=ltext("search"), case=None, sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.olhs_e 	= Entry(master, column=1, sticky="w", pady=(0, 10))

		self.olhs_e.bind(
			"<KeyRelease>",
			lambda e, funct=self.order_list_footer_frame, canv=self.order_list_canvas,\
				   target=this.get_order_list_content, entry=self.olhs_e: gv.order_list_search(
				self, e, funct, canv, target, entry))

		self.olhs_l.config(background="#FFFFFF")

		orders = CustomerOrder().qset.filter().all()
		gv.paginator(self, self.order_list_footer_frame, orders, self.order_list_canvas, this.get_order_list_content)

	def get_order_list_content(this, self, master, orders=None, all=None):
		master.delete("all")
		i_n 						= 1
		this.master_canvas 			= master
		this.olh_frame 				= self.order_list_header_frame
		dfile_path 					= os.path.join(gv.fi_path, "cus", "details-large-view-24.png")
		lfile_path 					= os.path.join(gv.fi_path, "cus", "view-details-24.png")
		ord_status 					= ['', 'Pending', 'Processing', 'Ready', 'Complete', 'Cancel']

		x_v = [
			[gv.w(0), gv.w(55)], [gv.w(55), gv.w(175)], [gv.w(175), gv.w(295)],
			[gv.w(295), gv.w(475)], [gv.w(475), gv.w(635)], [gv.w(635), gv.w(800)],
			[gv.w(800), gv.w(960)], [gv.w(960), gv.w(1095)], [gv.w(1095), gv.w(1195)], [gv.w(1195), gv.w(1324)]]

		hll = [
			ltext("sl"), ltext("invoice_id"), ltext('online_id'), ltext("customer_name"),
			ltext("waiter"), ltext("table"), ltext("status"), ltext("order_date"), ltext("amount"), ltext("action")]

		for i in x_v:
			this.olh_frame.create_rectangle(
				i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.olh_frame.create_text(
				x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(orders) == 0:
			this.master_canvas.create_text(
				gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_order_found")),
				width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.master_canvas.config(
				height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(
				Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.master_canvas.create_image(
				gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(orders) > 0:
			for order in orders:
				customer 	= CustomerInfo().qset.filter(id=order['customer_id']).first()
				waiter 		= Employee().qset.filter(id=order['waiter_id']).first()
				table 		= Tables().qset.filter(id=order['table_no']).first()

				txl = [
					all.index(order)+1,
					order['saleinvoice'],
					order['order_id_online'] if order['order_id_online'] else "",
					customer['customer_name'] if customer else "",
					waiter['first_name'] + " " + waiter['last_name'] if waiter['last_name'] else "",
					table['tablename'] if table else "",
					ord_status[order['order_status']],
					order['order_date'],
					order['totalamount'],
				]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.master_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.master_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.master_canvas, rtbi, fill))
					this.master_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.master_canvas, rtbi, fill))

					if ix<9:
						this.master_canvas.create_text(i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				globals()["oview_image_{}".format(i_n)] 	= PhotoImage(file=dfile_path).subsample(2, 2)
				globals()["oposview_image_{}".format(i_n)] 	= PhotoImage(file=lfile_path).subsample(2, 2)

				for i in [
					[43, 50, 68, globals()["oview_image_{}".format(i_n)], 'ororv_'],
					[74, 80, 98, globals()["oposview_image_{}".format(i_n)], 'ororpv_']]:
					globals()["{}btrec_{}".format(
						i[4], i_n)] = this.master_canvas.create_rectangle(
						x_v[9][0]+i[0], ((i_n-1)*34)+8, x_v[9][0]+i[2], ((i_n-1)*34)+28, fill="#37A000", outline="#FFFFFF")
					globals()["{}btim_{}".format(
						i[4], i_n)] = this.master_canvas.create_image(x_v[9][0]+i[1], ((i_n-1)*34)+17, image=i[3], anchor="w")

				for i in ['ororv_btrec_', 'ororv_btim_']:
					this.master_canvas.tag_bind(
						globals()["{}{}".format(i, i_n)], "<Button-1>",
						lambda event=None, data=order, view=True, self=self: this.order_list_popup_callback(
							self, event, data=data, view=view))

				for i in ['ororpv_btrec_', 'ororpv_btim_']:
					this.master_canvas.tag_bind(
						globals()["{}{}".format(i, i_n)], "<Button-1>",
						lambda event=None, data=order, view_invoice=True, self=self: this.order_list_popup_callback(
							self, event, data=data, view_invoice=view_invoice))

				for i in ['ororv_btrec_', 'ororpv_btrec_', 'ororv_btim_', 'ororpv_btim_']:
					canvas_mouse_el(this.master_canvas, globals()["{}{}".format(i, i_n)])

				dh = gv.device_height - 268
				mh = i_n * 34

				if int(mh) >= int(dh):
					this.master_canvas.config(scrollregion=[0, 0, 1150, mh])
				else:
					this.master_canvas.config(scrollregion=[0, 0, 1150, dh])

				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
