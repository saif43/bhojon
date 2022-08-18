from dev_help.widgets import *
from dev_help.database import *
from tkinter import messagebox, ttk, filedialog
from tkinter import *
from ntk.objects import gv as gv
from dev_help.tooltip import ToolTip
from PIL import Image, ImageTk

import os, time, datetime, _help, order
from threading import Thread

from database.table import Language, Setting

class ApplicationSetting:
	def __init__(self, realself, *args, **kwargs):
		super(ApplicationSetting, self).__init__(*args, **kwargs)
		self.realself 					= realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self 						= this.realself
		this.row 					= 0

		self.appsetting_reset 		= get_a_button(self.setting_frame, text=ltext("reset"), row=11, column=2, padx=(172, 0), bg="#3A95E4", ipady=4, width=16, use_ttk=False)
		self.appsetting_save 		= get_a_button(self.setting_frame, text=ltext("save"), row=11, column=3, padx=(0, 10), ipady=4, width=16, use_ttk=False)

		self.appsetting_reset.config(command=lambda: this.reset())
		self.appsetting_save.config(command=lambda: this.save())

		this.get_basic_meta_content(self, self.setting_frame)
		this.get_application_meta_content(self, self.setting_frame)

		this.reset()

	def get_basic_meta_content(this, self, frame):
		self.bm_app_title_l 		= get_a_label(frame, padx=(56, 16), text=ltext("app_title"))
		self.bm_app_title 			= get_a_entry(frame, column=1, width=36, use_ttk=False, state="readonly")
		self.bm_st_name_l 			= get_a_label(frame, padx=(56, 16), row=1, text=ltext("restaurant_name"))
		self.bm_st_name 			= get_a_entry(frame, row=1, column=1, width=36, use_ttk=False, state="readonly")

		self.bm_app_title.config(bd=0)
		self.bm_st_name.config(bd=0)

		self.cm_ot_l 				= get_a_label(frame, row=2, padx=(56, 16), text=ltext("opening_time"))
		self.cm_ot 					= get_a_entry(frame, row=2, column=1, use_ttk=False, state="readonly")
		self.cm_ct_l 				= get_a_label(frame, row=3, padx=(56, 16), text=ltext("closing_time"))
		self.cm_ct 					= get_a_entry(frame, row=3, column=1, use_ttk=False, state="readonly")
		self.cm_address_l 			= get_a_label(frame, padx=(56, 16), row=4, text=ltext("address"))
		self.cm_address 			= get_a_entry(frame, row=4, column=1, width=36, use_ttk=False, state="readonly")
		self.cm_email_l 			= get_a_label(frame, padx=(56, 16), row=5, text=ltext("email_address"))
		self.cm_email 				= get_a_entry(frame, row=5, column=1, width=36, use_ttk=False, state="readonly")
		self.cm_phone_l 			= get_a_label(frame, padx=(56, 16), row=6, text=ltext("mobile"))
		self.cm_phone 				= get_a_entry(frame, row=6, column=1, use_ttk=False, state="readonly")
		self.apm_c_l 				= get_a_label(frame, padx=(56, 16), text=ltext("currency"), row=7)
		self.apm_c 					= get_a_entry(frame, row=7, column=1, use_ttk=False, state="readonly")

		self.cm_mp_l 				= get_a_label(frame, padx=(56, 16), row=8, text=ltext("max_pagination"))
		self.cm_mp 					= get_a_entry(frame, row=8, column=1)
		self.cm_mr_l 				= get_a_label(frame, padx=(56, 16), row=9, text=ltext("max_rows_per_page"))
		self.cm_mr 					= get_a_entry(frame, row=9, column=1)

		self.cm_ssd_l 				= get_a_label(frame, padx=(56, 16), row=10, text=ltext("order_sync_delay"))
		self.cm_ssd 				= get_a_entry(frame, row=10, column=1, use_ttk=False)
		self.cm_ssd.bind('<Button-1>', lambda e: show_clock(e, self.cm_ssd, u=272, r=24))
		self.cm_ssd.config(state='readonly')

		self.bm_logo_b 				= get_a_button(frame, row=11, column=1, text=ltext("logo"), use_ttk=False, bg="#FFFFFF", fg="#000000", pady=16, padx=0, ipady=8, ipadx=8, width=0)
		self.bm_favicon_b 			= get_a_button(frame, row=11, text=ltext("icon"), use_ttk=False, bg="#FFFFFF", fg="#000000", pady=16, padx=0, ipady=8, ipadx=8, width=0)

		self.bm_favicon_b.config(command=lambda: this.icon_filedialog())

		ToolTip(self.bm_logo_b, ltext("logo_can_be_changed_from_admin_panel"))
		ToolTip(self.bm_favicon_b, ltext("click_to_change_icon"))

	def get_application_meta_content(this, self, frame):
		def key_pressed(e, w):
			try:
				ea = int(w.get())
				if ea == 0:
					w.delete(0, "end")
					w.insert(0, 1)
			except: w.insert(0, 1)

		self.apm_df_l 				= get_a_label(frame, padx=(56, 16), column=2, text=ltext("date_format"))
		self.apm_df 				= get_a_entry(frame, column=3, use_ttk=False, state="readonly")

		self.apm_aa_l 				= get_a_label(frame, padx=(56, 16), text=ltext("application_alignment"), row=1, column=2)
		self.apm_aa 				= get_a_entry(frame, row=1, column=3, use_ttk=False, state="readonly")

		this.cv = ["Amount", "Percent"]
		self.apm_dt_l 				= get_a_label(frame, padx=(56, 16), text=ltext("discount_type"), row=2, column=2)
		self.apm_dt 				= get_a_entry(frame, row=2, column=3, use_ttk=False, state="readonly")

		self.apm_sct_l 				= get_a_label(frame, padx=(56, 16), text=ltext("service_charge_type"), row=3, column=2)
		self.apm_sct 				= get_a_entry(frame, row=3, column=3, use_ttk=False, state="readonly")

		self.apm_vp_l 				= get_a_label(frame, padx=(56, 16), text=ltext("vat_setting"), row=4, column=2)
		self.apm_vp 				= get_a_entry(frame, default=5, row=4, column=3, use_ttk=False, state="readonly")

		self.apm_mpt_l 				= get_a_label(frame, padx=(56, 16), text=ltext("min_delivary_time"), row=5, column=2)
		self.apm_mpt 				= get_a_entry(frame, row=5, column=3, use_ttk=False, state="readonly")

		self.apm_pbt_l 				= get_a_label(frame, padx=(56, 16), pady=(0, 20), text=ltext("powered_by_text"), row=6, column=2)
		self.apm_pbt 				= get_a_text(frame, row=6, column=3, width=36, height=2)

		self.apm_ft_l 				= get_a_label(frame, padx=(56, 16), pady=(0, 20), text=ltext("footer_text"), row=7, column=2)
		self.apm_ft 				= get_a_text(frame, row=7, column=3, width=36, height=2)

		this.langlist 				= Language().columns()[1:]
		self.apm_lg_l 				= get_a_label(frame, padx=(56, 16), row=8, column=2, text=ltext("language"))
		self.apm_lg 				= get_a_combobox(frame, this.langlist, row=8, column=3, readonly=True)
		this.st_val_t = ["Active", "Inactive"]

		self.st_val_l 				= get_a_label(frame, padx=(56, 16), row=9, column=2, text=ltext("stock_validation"))
		self.st_val 				= get_a_combobox(frame, this.st_val_t, row=9, column=3, readonly=True)

		self.apm_lsd_l 				= get_a_label(frame, padx=(56, 16), row=10, column=2, text=ltext("changed_order_update_delay"))
		self.apm_lsd 				= get_a_entry(frame, row=10, column=3, use_ttk=False)
		self.apm_lsd.bind('<Button-1>', lambda e: show_clock(e, self.apm_lsd, u=272, r=24))
		self.apm_lsd.config(state='readonly')

		for key, value in frame.children.items():
			if key.startswith("!label"):
				value.config(background="#FFFFFF", foreground="#374767", font=("Calibri", 10, "bold"), width=24)

			if key.startswith("!entry"):
				value.config(font=('Calibri', 11))
				value.bind("<KeyRelease>", lambda e, w=value: key_pressed(e, w=w))

			if key.startswith("!text"):
				value.config(bg="#F0F0F0", font=("Calibri", 11))

			if key.startswith("!combobox"):
				value.config(width=24, font=('Calibri', 11))

	def reset(this):
		self 				= this.realself
		st 					= gv.setting_table

		if st:
			ed_l = [st['title'], st['storename'], st['opentime'], st['closetime'], st['address'], st['email'], st['phone'], st['powerbytxt'], st['footer_text'], st['vat'], st['currency'], st['min_prepare_time'], st['dateformat'], st['site_align'] if st.get('site_align') else "", this.cv[st['discount_type']], this.cv[st['service_chargeType']], st['language'], "Active" if st['stock_validation'] == 1 else "Inactive", st['sync_short_delay'], st['sync_long_delay']]
		else: ed_l = []

		wg_l = [self.bm_app_title, self.bm_st_name, self.cm_ot, self.cm_ct, self.cm_address, self.cm_email, self.cm_phone, self.apm_pbt, self.apm_ft, self.apm_vp, self.apm_c, self.apm_mpt, self.apm_df, self.apm_aa, self.apm_dt, self.apm_sct, self.apm_lg, self.st_val, self.cm_ssd, self.apm_lsd]

		if len(ed_l) >= len(wg_l):
			for i, entry in enumerate(wg_l):
				if "entry" in str(entry):
					entry.config(state="normal")
					entry.delete(0, "end")
					entry.insert(0, ed_l[i])
					entry.config(bd=0, state="readonly")

				elif "text" in str(entry):
					entry.delete(1.0, "end")
					entry.insert(1.0, ed_l[i])
					entry.config(bd=0, state="disabled")

				elif "combobox" in str(entry):
					entry.set(ed_l[i])

		self.cm_mp.delete(0, "end")
		self.cm_mp.insert(0, st['max_page_per_sheet'])
		self.cm_mr.delete(0, "end")
		self.cm_mr.insert(0, st['row_per_page'])

		self.icon_s_dir = st['favicon'] if st else ""
		self.logo_s_dir = st['logo'] if st else ""

		try:
			img 					= Image.open(os.path.join(gv.file_dir, st['logo'] if st else ""))
			img.thumbnail((128, 128), Image.ANTIALIAS)
			globals()["logo_obj"]	= ImageTk.PhotoImage(img)

			if globals()["logo_obj"]: self.bm_logo_b.config(image=globals()["logo_obj"], compound="top", activebackground="#FFFFFF")
		except Exception as e: gv.error_log(str(e))

		try:
			img 					= Image.open(os.path.join(gv.file_dir, st['favicon'] if st else ""))
			img.thumbnail((48, 48), Image.ANTIALIAS)
			globals()["icon_obj"]	= ImageTk.PhotoImage(img)

			if globals()["icon_obj"]: self.bm_favicon_b.config(image=globals()["icon_obj"], compound="top", activebackground="#FFFFFF")
		except Exception as e: gv.error_log(str(e))

	def save(this):
		self 				= this.realself
		st 					= gv.setting_table

		if st:
			key_l 	= ["id", "favicon", "language", "max_page_per_sheet", "row_per_page", "stock_validation", "sync_short_delay", "sync_long_delay"]
			value_l = [st['id'] if st else 0, self.icon_s_dir, self.apm_lg.get(), self.cm_mp.get(), self.cm_mr.get(), 1 if self.st_val.get() == "Active" else 0, self.cm_ssd.get(), self.apm_lsd.get()]

			Setting().qset.update(**dict((key, value_l[i]) for i, key in enumerate(key_l)))

			asq = _help.messagew(msg1=ltext("changes_saved"), msg2=ltext("continue_edit_or_go_to_home"), btext1=ltext("leave"), btext2=ltext("stay"), question=True)

			if asq.result:
				destroy_child(gv.menu.realself.resturant_frame)
				gv.menu.refresh()
				order.pos_order(gv.menu.realself, gv.menu.realself.resturant_frame)

				gv.icon_path 		= self.icon_s_dir + ".ico"
				gv.rest.master.iconbitmap(gv.icon_path)

	def icon_filedialog(this):
		try:
			self 	 				= this.realself
			img_file 				= filedialog.askopenfilename()

			mf = img_file.rsplit("/")
			ff = mf[len(mf)-1].split(".")[0]

			icon_file 				= ff
			self.icon_s_dir 		= os.path.join(gv.depend_image_dir, icon_file)
			icon_s_path 			= os.path.join(gv.file_dir, self.icon_s_dir)

			img = Image.open(img_file)
			img.thumbnail((32, 32), Image.ANTIALIAS)
			img.save(icon_s_path + ".png", "png")
			img.save(icon_s_path + ".ico", "ico")

			globals()["icon_obj"]		= ImageTk.PhotoImage(file=icon_s_path + ".png")

			if globals()["icon_obj"]: self.bm_favicon_b.config(image=globals()["icon_obj"], compound="top", activebackground="#FFFFFF")

			gv.rest.master.iconbitmap(self.icon_s_dir + '.ico')
		except Exception as e: gv.error_log(str(e))
