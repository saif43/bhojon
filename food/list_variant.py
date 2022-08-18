from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import Image, ImageTk

from database.table import Food, Varient
from ntk import PanedWindow, Frame, Canvas, Scrollbar, Label, Entry

# gv.error_log(str(f"File: food/list_variant.py"))

class VariantList:
	def __init__(self, realself, *args, **kwargs):
		super(VariantList, self).__init__(*args, **kwargs)
		self.realself 				= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.variant_list_head_holder = Frame(self.food_list_paned, width=gv.device_width - 80, height=34, pady=0)
		self.variant_list_head = Frame(
			self.variant_list_head_holder, width=gv.device_width - 80, height=34, pady=0, sticky="e")

		self.variant_list_content = PanedWindow(
			self.food_list_paned, row=1, width=gv.device_width - 42, height=gv.device_height - 120, pady=5)

		self.food_list_paned.add(self.variant_list_head_holder)
		self.food_list_paned.add(self.variant_list_content)

		self.variant_list_header_frame = Canvas(
			self.variant_list_content, width=gv.device_width - 42, height=34, mousescroll=False)
		self.variant_list_canv_holder = PanedWindow(
			self.variant_list_content, width=gv.device_width - 42,
			height=gv.device_height - 268, row=1, pady=10, orient='horizontal')

		self.variant_list_footer_frame_holder = Frame(self.variant_list_content, row=2, width=gv.device_width - 80)
		self.variant_list_footer_frame = Frame(self.variant_list_footer_frame_holder, row=2, pady=10, sticky="e")

		self.variant_list_content.add(self.variant_list_header_frame)
		self.variant_list_content.add(self.variant_list_canv_holder)
		self.variant_list_content.add(self.variant_list_footer_frame_holder)

		self.variant_list_canvas = Canvas(
			self.variant_list_canv_holder, width=gv.device_width - 42,
			height=gv.device_height - 268, scrollregion=[0, 0, 1160, 0],
			row=1, highlightbackground="#FAFAFA")

		self.scroll_order_list = Scrollbar(self.variant_list_canv_holder, self.variant_list_canvas, row=1)

		self.variant_list_canv_holder.add(self.variant_list_canvas)
		self.variant_list_canv_holder.add(self.scroll_order_list)
		
		this.get_variant_head(self, self.variant_list_head)

	def variant_popup_callback(this, self, event=None, data=None, delete=None):
		return

	def get_variant_head(this, self, master):
		self.variant_table_created = False

		self.variant_list_head_search_label 		= Label(master, text=ltext("search_variant"), case=None, sticky="e", font=("Calibri", 10, "bold"), pady=(0, 10))
		self.variant_list_head_search_entry 		= Entry(master, column=1, sticky="w", pady=(0, 10))

		self.variant_list_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.variant_list_footer_frame, canv=self.variant_list_canvas, target=this.get_variant_content, entry=self.variant_list_head_search_entry, table=Varient: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.variant_list_head_search_label.config(background="#FFFFFF")

		variants = Varient().qset.filter().all()
		gv.paginator(self, self.variant_list_footer_frame, variants, self.variant_list_canvas, this.get_variant_content)

	def get_variant_content(this, self, master, variants=None, all=None):
		master.delete("all")
		i_n 					= 1
		this.variant_canvas 	= master
		this.vlh_frame 			= self.variant_list_header_frame

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(690)], [gv.w(690), gv.w(1324)]]

		hll = [ltext("sl"), ltext("variant_name"), ltext("food_name")]
		for i in x_v:
			this.vlh_frame.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

		for it, x in enumerate(x_v):
			this.vlh_frame.create_text(x[0]+8, 17, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

		if len(variants) == 0:
			# this.variant_canvas.create_text(gv.w(1324)/2, 17, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.variant_canvas.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.variant_canvas.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.variant_canvas.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(variants) > 0:
			for variant in variants:
				for i in x_v:
					this.variant_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

				food = Food().qset.filter(id=variant['menuid'], ProductsIsActive=1, sep="AND").first()

				txl = [ all.index(variant)+1, variant['variantName'], food['ProductName'] if food else "" ]

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.variant_canvas.create_rectangle(i[0], (i_n-1)*34, i[1], i_n*34, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.variant_canvas.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.variant_canvas, rtbi, fill))
					this.variant_canvas.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.variant_canvas, rtbi, fill))

					this.variant_canvas.create_text(i[0]+12, ((i_n-1)*34)+17, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				# pr_h = this.variant_canvas.bbox("all")[3]
				# dh = (gv.device_height/100)*72
				# mh = i_n*34
				# if int(mh) < int(dh):
				# 	can_h = mh
				# else:pr_h
				# this.variant_canvas.config(height=can_h, scrollregion=[0, 0, 1150, i_n*34])

				dh = gv.device_height - 268
				mh = i_n * 34

				if int(mh) >= int(dh):
					this.variant_canvas.config(scrollregion=[0, 0, 1150, mh])
				else:
					this.variant_canvas.config(scrollregion=[0, 0, 1150, dh])

				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
