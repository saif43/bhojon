from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import Food, AddOnAsign, AddOn

# gv.error_log(str(f"File: food/list_assign.py"))

class AddOnAsignList:
	def __init__(self, realself, *args, **kwargs):
		super(AddOnAsignList, self).__init__(*args, **kwargs)
		self.realself 				= realself
		gv.add_addon_asign 			= self

		self.get_dependency_master()

	def get_dependency_master(this):
		self 								= this.realself

		self.addon_asign_list_head 			= get_a_frame(self.addon_asign_list_panedwindow, width=1160, height=200, pady=0, sticky="e", style="Custom.TFrame")
		self.addon_asign_list_content 		= get_a_frame(self.addon_asign_list_panedwindow, row=1, width=1160, pady=(0, 20), height=430, style="Custom.TFrame")
		self.addon_asign_list_header_frame 	= get_a_canvas(self.addon_asign_list_content, width=1324, height=34, scrollregion=[0,0,1160,0])
		self.addon_asign_list_footer_frame 	= get_a_frame(self.addon_asign_list_content, pady=0, row=2, sticky="e", style="Custom.TFrame")
		self.addon_asign_canvas 			= get_a_canvas(self.addon_asign_list_content, width=1324, height=34, scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.scrollcart 					= get_a_scrollbar(self.addon_asign_list_content, self.addon_asign_canvas, row = 1)

		this.get_addon_asign_head(self, self.addon_asign_list_head)

	def get_addon_asign_head(this, self, master):
		def search():
			ed = self.addon_asign_head_search_entry.get()
			addons = AddOn().qset.filter(add_on_name=ed, search='id').all()

			kw = {}
			if ed != "":
				kw = dict(('add_on_id', v['id']) for v in addons)

			gv.update_canvas_search(self, None, self.addon_asign_list_footer_frame, self.addon_asign_canvas, this.get_addon_asign_content, self.addon_asign_head_search_entry, AddOnAsign, **kw)

		self.addon_asign_head_search_label 		= get_a_label(master, text=ltext("search_addon"), sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.addon_asign_head_search_entry 		= get_a_entry(master, column=1, sticky="w", pady=(0, 10))

		self.addon_asign_head_search_entry.bind("<KeyRelease>", lambda event: search())

		self.addon_asign_head_search_label.config(background="#FFFFFF")

		addonasigns = AddOnAsign().qset.all()
		gv.paginator(self, self.addon_asign_list_footer_frame, addonasigns, self.addon_asign_canvas, this.get_addon_asign_content)

	def get_addon_asign_content(this, self, master, addonasigns=None, all=None):
		master.delete("all")
		i_n 					= 1
		this.addon_asign_canvas = master
		this.aalh_frame 		= self.addon_asign_list_header_frame

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(725)], [gv.w(725), gv.w(1324)]]

		hll = [ltext("sl"), ltext("addon_name"), ltext("food_name")]
		for i in x_v:
			this.aalh_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.aalh_frame.create_text(x[0]+gv.w(8), 17, text="{}".format(hll[it]), font=("Calibri", gv.h(10), "bold"), anchor="w", fill="#374767")

		if len(addonasigns) == 0:
			# this.addon_asign_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.addon_asign_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.addon_asign_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.addon_asign_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(addonasigns) > 0:
			for obj in addonasigns:
				addon_obj 	= AddOn().qset.filter(id=obj['add_on_id']).first()
				food 		= Food().qset.filter(id=obj['menu_id'], ProductsIsActive=1, sep='AND').first()

				txl 		= [ all.index(obj)+1, addon_obj['add_on_name'] if addon_obj else "", food['ProductName'] if food else "" ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.addon_asign_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.addon_asign_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.addon_asign_canvas, rtbi, fill))
					this.addon_asign_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.addon_asign_canvas, rtbi, fill))

					this.addon_asign_canvas.create_text(i[0]+gv.w(12), ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.addon_asign_canvas.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*34
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.addon_asign_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
