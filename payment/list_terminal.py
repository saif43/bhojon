from dev_help.widgets import *
from ntk.objects import gv as gv
import os, time
from PIL import Image, ImageTk

from database.table import CardTerminal as tbCardTerminal

class CardTerminal:
	def __init__(self, realself, *args, **kwargs):
		super(CardTerminal, self).__init__(*args, **kwargs)
		self.realself 					= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.ct_head 				= get_a_frame(self.ct_paned, width=1160, height=200, sticky="e", pady=0, style="Custom.TFrame")
		self.ct_content 			= get_a_frame(self.ct_paned, row=1, width=1160, height=430, pady=(0, 20), style="Custom.TFrame")
		self.ct_header_frame 		= get_a_canvas(self.ct_content, width=1324, height=34, scrollregion=[0,0,1160,0])
		self.ct_footer_frame 		= get_a_frame(self.ct_content, pady=10, row=2, sticky="e", style="Custom.TFrame")
		self.ct_canvas 				= get_a_canvas(self.ct_content, width=1324, height=34, scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.ct_scroll 				= get_a_scrollbar(self.ct_content, self.ct_canvas, row = 1)

		this.get_ct_head(self, self.ct_head)

	def ct_popup_callback(this, self, event=None, data=None, delete=None):
		return

	def get_ct_head(this, self, master):
		self.ct_head_search_label 		= get_a_label(master, text=ltext("search"), sticky="e", font=("Calibri", 10, "bold"))
		self.ct_head_search_entry 		= get_a_entry(master, column=1, sticky="w")

		self.ct_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.ct_footer_frame, canv=self.ct_canvas, target=this.get_ct_content, entry=self.ct_head_search_entry, table=tbCardTerminal: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.ct_head_search_label.config(background="#FFFFFF")

		terminals = tbCardTerminal().qset.filter().all()
		gv.paginator(self, self.ct_footer_frame, terminals, self.ct_canvas, this.get_ct_content)

	def get_ct_content(this, self, master, terminals=None, all=None):
		master.delete("all")
		self.ct_table_created 	= False
		this.ct_canvas 			= master
		this.cth_frame 					= self.ct_header_frame
		i_n 							= 1

		if terminals is None:
			terminals = gv.get_queryset_from_table(table="tbl_card_terminal", search=False, active=False)

		x_v = [[gv.w(0), gv.w(85)], [gv.w(85), gv.w(1324)]]

		hll = [ltext("sl"), ltext("card_terminal_name")]
		for i in x_v:
			this.cth_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.cth_frame.create_text(x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(terminals) == 0:
			# this.ct_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.ct_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.ct_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.ct_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(terminals) > 0:
			for terminal in terminals:
				txl = [ all.index(terminal)+1, terminal['terminal_name'] ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.ct_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.ct_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.ct_canvas, rtbi, fill))
					this.ct_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.ct_canvas, rtbi, fill))

					this.ct_canvas.create_text(i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.ct_canvas.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*34
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.ct_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
