from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import Bank as tbBank

class Bank:
	def __init__(self, realself, *args, **kwargs):
		super(Bank, self).__init__(*args, **kwargs)
		self.realself 					= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.bnk_head 				= get_a_frame(self.bnk_paned, width=1160, height=200, pady=0, sticky="e", style="Custom.TFrame")
		self.bnk_content 			= get_a_frame(self.bnk_paned, row=1, width=1160, height=430, pady=(0, 20), style="Custom.TFrame")
		self.bnk_header_frame 		= get_a_canvas(self.bnk_content, width=1324, height=34, scrollregion=[0,0,1160,0])
		self.bnk_footer_frame 		= get_a_frame(self.bnk_content, pady=10, row=2, sticky="e", style="Custom.TFrame")
		self.bnk_canvas 			= get_a_canvas(self.bnk_content, width=1324, height=34, scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.bnk_scroll 			= get_a_scrollbar(self.bnk_content, self.bnk_canvas, row = 1)

		this.get_bnk_head(self, self.bnk_head)

	def bnk_popup_callback(this, self, event=None, data=None, delete=None):
		return

	def get_bnk_head(this, self, master):
		self.bnk_head_search_label 		= get_a_label(master, text=ltext("search"), sticky="e", font=("Calibri", 10, "bold"))
		self.bnk_head_search_entry 		= get_a_entry(master, column=1, sticky="w")

		self.bnk_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.bnk_footer_frame, canv=self.bnk_canvas, target=this.get_bnk_content, entry=self.bnk_head_search_entry, table=tbBank: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.bnk_head_search_label.config(background="#FFFFFF")

		banks = tbBank().qset.filter().all()
		gv.paginator(self, self.bnk_footer_frame, banks, self.bnk_canvas, this.get_bnk_content)

	def get_bnk_content(this, self, master, banks=None, all=None):
		master.delete("all")
		self.bnk_table_created 			= False
		this.bnk_canvas 				= master
		this.cth_frame 					= self.bnk_header_frame
		i_n 							= 1

		if banks is None:
			banks = gv.get_queryset_from_table(table="tbl_bank", search=False, active=False)

		x_v = [[gv.w(0), gv.w(85)], [gv.w(85), gv.w(1324)]]

		hll = [ltext("sl"), ltext("bank_name")]
		for i in x_v:
			this.cth_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.cth_frame.create_text(x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(banks) == 0:
			# this.bnk_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.bnk_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.bnk_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.bnk_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(banks) > 0:
			for bank in banks:
				txl = [ all.index(bank)+1, bank['bank_name'] ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.bnk_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.bnk_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.bnk_canvas, rtbi, fill))
					this.bnk_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.bnk_canvas, rtbi, fill))

					this.bnk_canvas.create_text(i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.bnk_canvas.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*34
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.bnk_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
