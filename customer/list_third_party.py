from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import ThirdPartyCustomer

class ThirdPartyCustomerList:
	def __init__(self, realself, *args, **kwargs):
		super(ThirdPartyCustomerList, self).__init__(*args, **kwargs)
		self.realself 				= realself
		gv.add_tpc 			= self

		self.get_dependency_master()

	def get_dependency_master(this):
		self 					= this.realself

		self.tpc_list_head 		= get_a_frame(self.tpc_li_paned, width=1160, height=200, pady=0, sticky="e", style="Custom.TFrame")
		self.tpc_list_content 	= get_a_frame(self.tpc_li_paned, row=1, width=820, height=430, pady=(0, 0), style="Custom.TFrame")
		self.tpc_list_header 	= get_a_canvas(self.tpc_list_content, width=1324, height=34, pady=(0, 0), scrollregion=[0,0,1160,0])
		self.tpc_list_footer 	= get_a_frame(self.tpc_list_content, pady=0, row=2, sticky="e", style="Custom.TFrame")
		self.tpc_list_canv 		= get_a_canvas(self.tpc_list_content, width=1324, height=34, pady=(0, 0), scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.scrollcart 		= get_a_scrollbar(self.tpc_list_content, self.tpc_list_canv, row = 1)

		this.get_tpc_head(self, self.tpc_list_head)

	def get_tpc_head(this, self, master):
		self.tpc_table_created = False

		self.tpc_li_hsl 		= get_a_label(master, text=ltext("search_company"), sticky="e", font=("Calibri", 10, "bold"))
		self.tpc_li_hse 		= get_a_entry(master, column=1, sticky="w")
		self.tpc_li_hse.bind("<KeyRelease>", lambda e, funct=self.tpc_list_footer, canv=self.tpc_list_canv, target=this.get_tpc_content, entry=self.tpc_li_hse, table=ThirdPartyCustomer: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.tpc_li_hsl.config(background="#FFFFFF")

		tpcs = ThirdPartyCustomer().qset.all()
		gv.paginator(self, self.tpc_list_footer, tpcs, self.tpc_list_canv, this.get_tpc_content)

	def get_tpc_content(this, self, master, tpcs=None, all=None):
		master.delete("all")
		i_n 					= 1
		this.tpc_canvas 		= master
		this.tplh_frame 		= self.tpc_list_header

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(350)], [gv.w(350), gv.w(620)], [gv.w(620), gv.w(1324)]]

		hll = [ltext("sl"), ltext("company_name"), ltext("commission"), ltext("address")]
		for i in x_v:
			this.tplh_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.tplh_frame.create_text(x[0]+gv.w(8), 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(tpcs) == 0:
			# this.tpc_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", gv.w(10), "bold"), fill="#374767")

			this.tpc_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.tpc_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.tpc_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(tpcs) > 0:
			for tpc in tpcs:
				txl = [ all.index(tpc)+1, tpc['company_name'], tpc['commision'], tpc['address'] ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.tpc_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.tpc_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.tpc_canvas, rtbi, fill))
					this.tpc_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.tpc_canvas, rtbi, fill))

					this.tpc_canvas.create_text(i[0]+gv.w(12), ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.tpc_canvas.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*34
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.tpc_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
