from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import AddOn

# gv.error_log(str(f"File: food/list_addon.py"))

class AddOnList:
	def __init__(self, realself, *args, **kwargs):
		super(AddOnList, self).__init__(*args, **kwargs)
		self.realself 				= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self 						= this.realself

		self.addon_list_head 			= get_a_frame(self.addon_list_panedwindow, width=1160, height=200, pady=0, sticky="e", style="Custom.TFrame")
		self.addon_list_content 		= get_a_frame(self.addon_list_panedwindow, row=1, width=1160, height=430, pady=(0, 20), style="Custom.TFrame")
		self.addon_list_header_frame 	= get_a_canvas(self.addon_list_content, width=1324, height=34, scrollregion=[0,0,1160,0])
		self.addon_list_footer_frame 	= get_a_frame(self.addon_list_content, pady=0, row=2, sticky="e", style="Custom.TFrame")
		self.addon_list_canvas 			= get_a_canvas(self.addon_list_content, width=1324, height=34, scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.scrollcart 				= get_a_scrollbar(self.addon_list_content, self.addon_list_canvas, row = 1, column = 1)

		this.get_addon_head(self, self.addon_list_head)

	def get_addon_head(this, self, master):
		self.addon_table_created = False

		self.addon_list_head_search_label 		= get_a_label(master, text=ltext("search_addon"), sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.addon_list_head_search_entry 		= get_a_entry(master, column=1, sticky="w", pady=(0, 10))

		self.addon_list_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.addon_list_footer_frame, canv=self.addon_list_canvas, target=this.get_addon_content, entry=self.addon_list_head_search_entry, table=AddOn: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.addon_list_head_search_label.config(background="#FFFFFF")

		addons = AddOn().qset.all()
		gv.paginator(self, self.addon_list_footer_frame, addons, self.addon_list_canvas, this.get_addon_content)

	def get_addon_content(this, self, master, addons=None, all=None):
		master.delete("all")
		i_n 					= 1
		this.addon_canvas 		= master
		this.alh_frame 			= self.addon_list_header_frame

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(720)], [gv.w(720), gv.w(1020)], [gv.w(1020), gv.w(1324)]]

		hll = [ltext("sl"), ltext("addon_name"), ltext("price"), ltext("status")]
		for i in x_v:
			this.alh_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.alh_frame.create_text(x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.h(10), "bold"), anchor="w", fill="#374767")

		if len(addons) == 0:
			# this.addon_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.addon_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.addon_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.addon_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(addons) > 0:
			for addon in addons:
				txl = [ all.index(addon)+1, addon['add_on_name'], addon['price'], "Active" if int(addon['is_active']) == 1 else "Inactive" ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.addon_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.addon_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.addon_canvas, rtbi, fill))
					this.addon_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.addon_canvas, rtbi, fill))

					this.addon_canvas.create_text(i[0]+gv.w(12), ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.addon_canvas.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*34
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.addon_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
