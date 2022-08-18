from dev_help.widgets import *
from PIL import Image, ImageTk
from ntk.objects import gv as gv
import os, time
from PIL import Image, ImageTk

from database.table import FoodCategory

# gv.error_log(str(f"File: food/list_category.py"))

class CategoryList:
	def __init__(self, realself, *args, **kwargs):
		super(CategoryList, self).__init__(*args, **kwargs)
		self.realself 					= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self 						= this.realself

		self.f_cat_l_head 			= get_a_frame(self.food_category_list_panedwindow, width=1160, height=200, pady=0, sticky="e", style="Custom.TFrame")
		self.f_cat_l_content 		= get_a_frame(self.food_category_list_panedwindow, row=1, width=1160, pady=(0, 20), height=430, style="Custom.TFrame")
		self.f_cat_l_header_frame 	= get_a_canvas(self.f_cat_l_content, width=1324, height=46, scrollregion=[0,0,1160,0])
		self.f_cat_l_footer_frame 	= get_a_frame(self.f_cat_l_content, pady=0, row=2, sticky="e", style="Custom.TFrame")
		self.f_cat_l_canvas 		= get_a_canvas(self.f_cat_l_content, width=1324, height=46, scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.scrollcart 			= get_a_scrollbar(self.f_cat_l_content, self.f_cat_l_canvas, row = 1)

		this.get_food_category_head(self, self.f_cat_l_head)

	def food_category_popup_callback(this, self, event=None, data=None, delete=None):
		return

	def get_food_category_head(this, self, master):
		self.food_category_table_created = False

		self.category_list_head_search_label 		= get_a_label(master, text=ltext("search_category"), sticky="e", font=("Calibri", 10, "bold"))
		self.category_list_head_search_entry 		= get_a_entry(master, column=1, sticky="w")

		self.category_list_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.f_cat_l_footer_frame, canv=self.f_cat_l_canvas, target=this.get_food_category_content, entry=self.category_list_head_search_entry, table=FoodCategory: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.category_list_head_search_label.config(background="#FFFFFF")

		foodcats = FoodCategory().qset.all()
		gv.paginator(self, self.f_cat_l_footer_frame, foodcats, self.f_cat_l_canvas, this.get_food_category_content)

	def get_food_category_content(this, self, master, foodcats=None, all=None):
		master.delete("all")
		this.master_category 	= master
		this.clh_frame 			= self.f_cat_l_header_frame
		i_n 					= 1

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(170)], [gv.w(170), gv.w(620)], [gv.w(620), gv.w(1070)], [gv.w(1070),  gv.w(1324)]]

		hll = [ltext("sl"), ltext("image"), ltext("category_name"), ltext("parent_menu"), ltext("status")]
		for i in x_v:
			this.clh_frame.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.clh_frame.create_text(x[0]+8, 23, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(foodcats) == 0:
			# this.master_category.create_text(gv.w(1324)/2, 23, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.master_category.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.master_category.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.master_category.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(foodcats) > 0:
			for foodcat in foodcats:
				globals()["foodcat_item_image_{}".format(foodcat['id'])] = False
				if foodcat['CategoryImage']:
					try:
						path = os.path.join(gv.file_dir, foodcat['CategoryImage'])
						img = Image.open(path)
						img.thumbnail((38, 44), Image.ANTIALIAS)
						globals()["foodcat_item_image_{}".format(foodcat['id'])] = ImageTk.PhotoImage(img)
					except Exception as e: gv.error_log(str(e))

				obj = FoodCategory().qset.filter(id=foodcat['parentid'], CategoryIsActive=1).first()

				txl = [ all.index(foodcat)+1, 'img', foodcat['Name'], obj['Name'] if obj else "", "Active" if foodcat['CategoryIsActive'] == 1 else "Inactive" ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.master_category.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.master_category.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.master_category, rtbi, fill))
					this.master_category.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.master_category, rtbi, fill))

					if txl[ix] == 'img' and globals()["foodcat_item_image_{}".format(foodcat['id'])]:
						this.master_category.create_image(i[0]+gv.w(57), ((i_n-1)*46)+23, image=globals()["foodcat_item_image_{}".format(foodcat['id'])])
					else:
						this.master_category.create_text(i[0]+gv.w(12), ((i_n-1)*46)+23, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.master_category.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*46
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.master_category.config(height=can_h, scrollregion=[0, 0, 1150, i_n*46])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
