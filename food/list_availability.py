from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import Food, FoodAvailablity
from ntk import PanedWindow, Frame, Canvas, Scrollbar, Label, Entry

# gv.error_log(str(f"File: food/list_availability.py"))

class AvailabilityList:
	def __init__(self, realself, *args, **kwargs):
		super(AvailabilityList, self).__init__(*args, **kwargs)
		self.realself 						= realself
		gv.add_availability 				= self

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.av_l_head_holder = Frame(self.food_list_paned, width=gv.device_width - 80, height=34, pady=0)
		self.av_l_head = Frame(self.av_l_head_holder, width=gv.device_width - 80, height=34, pady=0, sticky="e")

		self.av_l_content = PanedWindow(
			self.food_list_paned, row=1, width=gv.device_width - 42, height=gv.device_height - 120, pady=5)

		self.food_list_paned.add(self.av_l_head_holder)
		self.food_list_paned.add(self.av_l_content)

		self.av_l_header_frame = Canvas(self.av_l_content, width=gv.device_width - 42, height=34, mousescroll=False)
		self.av_l_canv_holder = PanedWindow(
			self.av_l_content, width=gv.device_width - 42, height=gv.device_height - 268, row=1, pady=10, orient='horizontal')

		self.av_l_footer_frame_holder = Frame(self.av_l_content, row=2, width=gv.device_width - 80)
		self.av_l_footer_frame = Frame(self.av_l_footer_frame_holder, row=2, pady=0, sticky="e")

		self.av_l_content.add(self.av_l_header_frame)
		self.av_l_content.add(self.av_l_canv_holder)
		self.av_l_content.add(self.av_l_footer_frame_holder)

		self.av_l_canvas = Canvas(
			self.av_l_canv_holder, width=gv.device_width - 42, height=gv.device_height - 268, scrollregion=[0, 0, 1160, 0],
			row=1, highlightbackground="#FAFAFA")

		self.scroll_order_list = Scrollbar(self.av_l_canv_holder, self.av_l_canvas, row=1)

		self.av_l_canv_holder.add(self.av_l_canvas)
		self.av_l_canv_holder.add(self.scroll_order_list)
		
		this.get_availability_head(self, self.av_l_head)

	def get_availability_head(this, self, master):
		self.availability_table_created = False
		self.av_en 						= StringVar()

		def search(event):
			ed = self.availability_head_search_entry.get()
			foods = Food().qset.filter(ProductName=ed, search='id').all()

			kw = {}
			if ed != '':
				kw = dict(('foodid', v['id']) for v in foods)

			gv.update_canvas_search(self, None, self.av_l_footer_frame, self.av_l_canvas, this.get_availability_content, self.availability_head_search_entry, FoodAvailablity, **kw)

		self.availability_head_search_label 		= Label(master, text=ltext("search_food_name"), case=None, sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.availability_head_search_entry 		= Entry(master, column=1, sticky="w", pady=(0, 10))

		self.availability_head_search_entry.bind("<KeyRelease>", lambda event: search(event))

		self.availability_head_search_label.config(background="#FFFFFF")

		availabilities = FoodAvailablity().qset.all()
		gv.paginator(self, self.av_l_footer_frame, availabilities, self.av_l_canvas, this.get_availability_content)

	def get_availability_content(this, self, master, availabilities=None, all=None):
		master.delete("all")
		i_n 						= 1
		this.availability_canvas 	= master
		this.alh_frame 				= self.av_l_header_frame

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(370)], [gv.w(370), gv.w(685)], [gv.w(685), gv.w(1324)]]

		hll = [ltext("sl"), ltext("food_name"), ltext("available_day"), ltext("available_time")]
		for i in x_v:
			this.alh_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.alh_frame.create_text(x[0]+gv.w(8), 17, text="{}".format(hll[it]), font=("Calibri", gv.h(10), "bold"), anchor="w", fill="#374767")

		if len(availabilities) == 0:
			# this.availability_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.availability_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.availability_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.availability_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(availabilities) > 0:
			for obj in availabilities:
				food = Food().qset.filter(id=obj['foodid'], ProductsIsActive=1, sep="AND").first()

				txl = [ all.index(obj)+1, food['ProductName'] if food else "", obj['availday'], obj['availtime'] ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.availability_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.availability_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.availability_canvas, rtbi, fill))
					this.availability_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.availability_canvas, rtbi, fill))

					this.availability_canvas.create_text(i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				# pr_h = this.availability_canvas.bbox("all")[3]
				# dh = (gv.device_height/100)*72
				# mh = i_n*34
				# if int(mh) < int(dh):
				# 	can_h = mh
				# else:pr_h
				# this.availability_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])

				dh = gv.device_height - 268
				mh = i_n * 34

				if int(mh) >= int(dh):
					this.availability_canvas.config(scrollregion=[0, 0, 1150, mh])
				else:
					this.availability_canvas.config(scrollregion=[0, 0, 1150, dh])

				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
