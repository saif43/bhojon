from dev_help.widgets import *
from PIL import Image, ImageTk
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import FoodCategory, Food
from ntk import Frame, Canvas, Scrollbar, PanedWindow, Label, Entry

# gv.error_log(str(f"File: food/list.py"))

class FoodList:
	def __init__(self, realself, *args, **kwargs):
		super(FoodList, self).__init__(*args, **kwargs)
		self.realself = realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.food_list_head_holder = Frame(self.food_list_paned, width=gv.device_width - 80, height=34, pady=0)
		self.food_list_head = Frame(self.food_list_head_holder, width=gv.device_width - 80, height=34, pady=0, sticky="e")

		self.food_list_content = PanedWindow(
			self.food_list_paned, row=1, width=gv.device_width - 42, height=gv.device_height - 120, pady=5)

		self.food_list_paned.add(self.food_list_head_holder)
		self.food_list_paned.add(self.food_list_content)

		self.food_list_header_frame = Canvas(self.food_list_content, width=gv.device_width - 42, height=34, mousescroll=False)
		self.food_list_canv_holder = PanedWindow(
			self.food_list_content, width=gv.device_width - 42,
			height=gv.device_height - 268, row=1, pady=10, orient='horizontal')

		self.food_list_footer_frame_holder = Frame(self.food_list_content, row=2, width=gv.device_width - 80)
		self.food_list_footer_frame = Frame(self.food_list_footer_frame_holder, row=2, pady=0, sticky="e")

		self.food_list_content.add(self.food_list_header_frame)
		self.food_list_content.add(self.food_list_canv_holder)
		self.food_list_content.add(self.food_list_footer_frame_holder)

		self.food_list_canvas = Canvas(
			self.food_list_canv_holder, width=gv.device_width - 42,
			height=gv.device_height - 268, scrollregion=[0, 0, 1160, 0],
			row=1, highlightbackground="#FAFAFA")

		self.scroll_order_list = Scrollbar(self.food_list_canv_holder, self.food_list_canvas, row=1)

		self.food_list_canv_holder.add(self.food_list_canvas)
		self.food_list_canv_holder.add(self.scroll_order_list)

		this.get_food_head(self, self.food_list_head)

	def food_popup_callback(this, self, event=None, data=None, delete=None):
		return

	def get_food_head(this, self, master):
		self.food_table_created = False

		self.food_list_head_search_label 		= Label(
			master, text=ltext("search_food"), case=None, sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.food_list_head_search_entry 		= Entry(master, column=1, sticky="w", pady=(0, 10))

		self.food_list_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.food_list_footer_frame, canv=self.food_list_canvas, target=this.get_food_content, entry=self.food_list_head_search_entry, table=Food: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.food_list_head_search_label.config(background="#FFFFFF")

		foods = Food().qset.all()
		gv.paginator(self, self.food_list_footer_frame, foods, self.food_list_canvas, this.get_food_content)

	def get_food_content(this, self, master, foods=None, all=None):
		master.delete("all")
		i_n 				= 1
		this.food_canvas 	= master
		this.flh_frame 		= self.food_list_header_frame

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(170)], [gv.w(170), gv.w(420)], [gv.w(420), gv.w(670)], [gv.w(670), gv.w(984)], [gv.w(984), gv.w(1124)], [gv.w(1124), gv.w(1324)]]

		hll = [ltext("sl"), ltext("image"), ltext("category_name"), ltext("food_name"), ltext("component"), ltext("vat"), ltext("status")]
		for i in x_v:
			this.flh_frame.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.flh_frame.create_text(x[0]+8, 23, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(foods) == 0:
			# this.food_canvas.create_text(gv.w(1324)/2, 23, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.food_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.food_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.food_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(foods) > 0:
			for food in foods:
				globals()["food_item_image_{}".format(food['id'])] = False
				if food['ProductImage']:
					try:
						path = os.path.join(gv.file_dir, food['ProductImage'])
						img = Image.open(path)
						img.thumbnail((38, 44), Image.ANTIALIAS)
						globals()["food_item_image_{}".format(food['id'])] = ImageTk.PhotoImage(img)
					except Exception as e: gv.error_log(str(e))

				cat = FoodCategory().qset.filter(id=food['CategoryID'], CategoryIsActive=1, sep='AND').first()

				txl = [
					all.index(food)+1, 'img', cat['Name'] if cat else "",
					food['ProductName'][0:62] + ("..." if len(str(food['ProductName'])) > 62 else ""),
					food['component'][0:62] + ("..." if len(str(food['component'])) > 62 else ""),
					food['productvat'] if food['productvat'] != "" else 0,
					"Active" if food['ProductsIsActive'] == 1 else "Inactive"
				]

				for i in x_v:
					this.food_canvas.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F7", fill="#FAFAFA" if i_n%2 == 0 else "#FFFFFF")

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.food_canvas.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.food_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.food_canvas, rtbi, fill))
					this.food_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.food_canvas, rtbi, fill))

					if txl[ix] == 'img' and globals()["food_item_image_{}".format(food['id'])]:
						this.food_canvas.create_image(i[0]+gv.w(57), ((i_n-1)*46)+23, image=globals()["food_item_image_{}".format(food['id'])])
					else:
						this.food_canvas.create_text(i[0]+gv.w(12), ((i_n-1)*46)+23, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				# pr_h = this.food_canvas.bbox("all")[3]
				# dh = (gv.device_height/100)*72
				# mh = i_n*46
				# if int(mh) < int(dh):
				# 	can_h = mh
				# else:pr_h
				# this.food_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*46])

				dh = gv.device_height - 268
				mh = i_n * 34

				if int(mh) >= int(dh):
					this.food_canvas.config(scrollregion=[0, 0, 1150, mh])
				else:
					this.food_canvas.config(scrollregion=[0, 0, 1150, dh])

				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
