from dev_help.widgets import *
from ntk.objects import gv as gv
from PIL import Image, ImageTk
import os
from PIL import Image, ImageTk

from database.table import Tables

class TableList:
	def __init__(self, realself, *args, **kwargs):
		super(TableList, self).__init__(*args, **kwargs)
		self.realself 					= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self 							= this.realself

		self.table_list_head 			= get_a_frame(self.table_list_panedwindow, width=1160, height=200, pady=0, sticky="e", style="Custom.TFrame")
		self.table_list_content 		= get_a_frame(self.table_list_panedwindow, row=1, width=1160, pady=(0, 20), height=430, style="Custom.TFrame")
		self.table_list_header_frame 	= get_a_canvas(self.table_list_content, width=1324, height=46, scrollregion=[0,0,1160,0])
		self.table_list_footer_frame 	= get_a_frame(self.table_list_content, pady=10, row=2, sticky="e", style="Custom.TFrame")
		self.table_list_canvas 			= get_a_canvas(self.table_list_content, width=1324, height=46, scrollregion=[0,0,1160,0], row=1, highlightbackground="#FAFAFA")
		self.table_scrollbar 			= get_a_scrollbar(self.table_list_content, self.table_list_canvas, row = 1)

		this.get_table_head(self, self.table_list_head)

	def table_popup_callback(this, self, event=None, data=None, delete=None):
		return

	def get_table_head(this, self, master):
		self.table_list_cart_created = False

		self.table_head_search_label 		= get_a_label(master, text=ltext("search"), sticky="e", font=("Calibri", 10, "bold"))
		self.table_head_search_entry 		= get_a_entry(master, column=1, sticky="w")

		self.table_head_search_entry.bind("<KeyRelease>", lambda e, funct=self.table_list_footer_frame, canv=self.table_list_canvas, target=this.get_table_content, entry=self.table_head_search_entry, table=Tables: gv.update_canvas_search(self, e, funct, canv, target, entry, table))

		self.table_head_search_label.config(background="#FFFFFF")

		tables = Tables().qset.filter().all()
		gv.paginator(self, self.table_list_footer_frame, tables, self.table_list_canvas, this.get_table_content)

	def get_table_content(this, self, master, tables=None, all=None):
		master.delete("all")
		this.master_table 			= master
		this.tlh_frame 				= self.table_list_header_frame
		i_n 						= 1

		x_v = [[gv.w(0), gv.w(55)], [gv.w(55), gv.w(924)], [gv.w(924), gv.w(1124)], [gv.w(1124), gv.w(1324)]]

		if not self.table_list_cart_created:
			hll = [ltext("sl"), ltext("table_name"), ltext("capacity"), ltext("icon")]
			for i in x_v:
				this.tlh_frame.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F6", fill="#FAFAFA" if i_n%2==0 else "#FFFFFF")

			for it, x in enumerate(x_v):
				this.tlh_frame.create_text(x[0]+8, 23, text="{}".format(hll[it]), font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767")

			self.table_list_cart_created = True

		if len(tables) == 0:
			# this.master_table.create_text(gv.w(1324)/2, 23, text="{}".format(ltext("no_item_found")), width=200, font=("Calibri", 10, "bold"), fill="#374767")

			this.master_table.create_text(gv.w(1324)/2, (((gv.device_height/100)*72)/2)+84, text="{}".format(ltext("no_item_found")), width=200, anchor='center', font=("Calibri", gv.h(14), "bold"), fill="#374767")

			this.master_table.config(height=(gv.device_height/100)*72, scrollregion=[0, 0, 0, (gv.device_height/100)*72])
			this.fempty  = ImageTk.PhotoImage(Image.open(os.path.join(gv.fi_path, 'cus', 'search_op.png')).resize((gv.h(72),gv.h(72)), Image.ANTIALIAS))
			this.master_table.create_image(gv.w(1324)/2, ((gv.device_height/100)*72)/2, image=this.fempty, anchor='center')

		elif len(tables) > 0:
			for obj in tables:
				globals()["table_icon_{}".format(obj['id'])] = False
				try:
					path = os.path.join(gv.itemmanage_path + '/' + obj['table_icon'])
					img = Image.open(path)
					img.thumbnail((44, 44), Image.ANTIALIAS)
					globals()["table_icon_{}".format(obj['id'])] = ImageTk.PhotoImage(img)
				except Exception as e: gv.error_log(str(e))

				txl = [ all.index(obj)+1, obj['tablename'], obj['person_capicity'], 'img' ]

				for i in x_v:
					this.master_table.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F7", fill="#FAFAFA" if i_n%2 == 0 else "#FFFFFF")

				rtbi = []
				for ix, i in enumerate(x_v):
					tbi = this.master_table.create_rectangle(i[0], (i_n-1)*46, i[1], i_n*46, outline="#F1F3F7", fill="#F9F9F9" if i_n%2==0 else "#FFFFFF")
					rtbi.append(tbi)

					this.master_table.tag_bind(tbi, "<Enter>", lambda e, rtbi=rtbi, fill="#F5F5F5": this.entered(this.master_table, rtbi, fill))
					this.master_table.tag_bind(tbi, "<Leave>", lambda e, rtbi=rtbi, fill="#F9F9F9" if i_n%2 == 0 else "#FFFFFF": this.entered(this.master_table, rtbi, fill))

					if txl[ix] == 'img' and globals()["table_icon_{}".format(obj['id'])]:
						this.master_table.create_image(i[0]+gv.w(57), ((i_n-1)*46)+23, image=globals()["table_icon_{}".format(obj['id'])])
					else:
						this.master_table.create_text(i[0]+gv.w(12), ((i_n-1)*46)+23, text="{}".format(txl[ix]), width=(i[1]-i[0])-24, font=("Calibri", 10), anchor="w", fill="#374767")

				pr_h = this.master_table.bbox("all")[3]
				dh = (gv.device_height/100)*72
				mh = i_n*46
				if int(mh) < int(dh):
					can_h = mh
				else:pr_h
				this.master_table.config(height=can_h, scrollregion=[0, 0, 1150, i_n*46])
				i_n = i_n + 1

	def entered(self, root, rtbi, fill):
		for ti in rtbi:
			root.itemconfig(ti, fill=fill)
