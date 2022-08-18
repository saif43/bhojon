
from dev_help.widgets import *
import os, requests, database, _help, hashlib, string, order
from ntk.objects import gv as gv
from __restora__.global_ import user
# from database.synchronization.down.waiter import Waiter
from PIL import Image, ImageTk
from dev_help.ph_entry import PHEntry
from threading import Thread

from database.table import User

from ntk import Frame, Canvas, Button


class LoginForm:
	def __init__(self, realself, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.realself = realself

		self.get_dependency_master()

	def get_dependency_master(this):
		self = this.realself

		self.EmailField.set("admin@example.com")
		self.PasswordData.set("")

		self.login_f = Frame(self.login_modal_paned, padx=0, pady=0)

		self.login_wrap = Canvas(
							self.login_f, width=gv.device_width,
							height=gv.device_height, bg="#0F0E0C",
							highlightbackground="#000000",
							mousescroll=False, padx=0, pady=0
						)

		self.login_canv = Canvas(
							self.login_f, width=gv.w(412),
							height=472, mousescroll=False,
							padx=0, pady=0
						)

		file_path = os.path.join(gv.assets_path, "img", "bg.jpg")
		img_file = Image.open(file_path)
		img_file.thumbnail((gv.device_height, gv.device_height), Image.ANTIALIAS)
		globals()["background_image_0"] = ImageTk.PhotoImage(file=file_path)

		self.login_wrap.create_image(
							gv.device_width/2, gv.device_height/2,
							image=globals()["background_image_0"]
						)

		self.login_wrap.create_window(
							int(self.login_wrap.winfo_width()/2),
							int(gv.device_height/2)-50,
							window=self.login_canv, height=472
						)

		self.ed = PHEntry(
							self.login_f, placeholder="Please enter your email",
							row=1, columnspan=3, textvariable=self.EmailField,
							width=gv.w(36), font=("Calibri", 12), padx=(32, 3)
						)

		self.ed.config(
							bd=0, bg="#F5F5F5", highlightbackground="#85E0FB",
							highlightthickness=1, selectforeground="#374767",
							selectbackground="#37A000"
						)

		self.pd = PHEntry(
							self.login_f, placeholder="Enter your password",
							row=3, columnspan=3, textvariable=self.PasswordData,
							width=gv.w(36), font=("Calibri", 12), padx=(32, 3)
						)

		self.pd.config(show="*")
		self.pd.config(
							bd=0, bg="#F5F5F5", highlightbackground="#85E0FB",
							highlightthickness=1, selectforeground="#374767",
							selectbackground="#37A000"
						)

		self.sb = Button(
							self.login_f, row=4, column=1,
							text=ltext("login"), pady=24, ipady=4,
							width=gv.w(14), font=('Calibri', 10, 'bold')
						)

		w = self.login_canv.winfo_width()

		if gv.st['logo'] and gv.st['logo'] != "":
			try:
				img = Image.open(os.path.join(gv.file_dir, gv.st['logo']))
				img.thumbnail((196, 196), Image.ANTIALIAS)
				self.logo_img = ImageTk.PhotoImage(img)
				self.login_canv.create_image(int(w/2), 56, image=self.logo_img)

			except Exception as e:
				gv.error_log(str(e))

		self.login_canv.create_text(
							int(w/2)-gv.w(166), 130,
							text="{}".format(ltext("email_address")),
							anchor="w", font=('Calibri', gv.h(9), 'bold'), fill='#374767'
						)
		self.login_canv.create_window(int(w/2), 164, window=self.ed, height=32)

		self.login_canv.create_text(
							int(w/2)-gv.w(166), 226,
							text="{}".format(ltext("password")),
							anchor="w", font=('Calibri', gv.h(9), 'bold'), fill='#374767'
						)
		self.login_canv.create_window(int(w/2), 260, window=self.pd, height=32)

		self.login_canv.create_window(
							int(w/2)+gv.w(42), 332,
							window=self.sb, anchor="w", height=30
						)

		def login_call():
			self.sync_tested = False
			this.login()

		self.sb.config(command=lambda: login_call())

		for key, value in self.login_f.children.items():
			if key.startswith("!label"):
				value.config(
						background="#FFFFFF",
						foreground="#374767",
						width=20, font=("Calibri", 11)
					)

		self.login_canv.create_text(
					int(w/2), 404,
					text="{}".format((gv.setting_table['powerbytxt'].split("\n")[0])[0:50]),
					font=("Calibri", gv.h(9), "bold"),
					fill='#374767', anchor='center', width=w
				)

		self.ed.bind("<Return>", lambda e: login_call())
		self.pd.bind("<Return>", lambda e: login_call())

	def login(this):
		self = this.realself
		et = ""

		try:
			user_data = User(init=1).qset.filter(
									email=self.EmailField.get(),
									status=1, sep='AND'
								).first()

			if user_data:
				hpass = hashlib.md5(self.PasswordData.get().encode())
				chwds = string.digits + string.ascii_letters
				fpass = ""
				for s in hpass.hexdigest():
					fpass = fpass + str(chwds.index(s))

				# if fpass == user_data['password']:
				user(user_data)

				this.try_to_open()

			else:
				raise Exception('User not found')

		except Exception as e:
			gv.error_log(str(e))
			et = e

		if not gv.user_is_authenticated and not self.sync_tested:
			this.synchronization(et)

	def synchronization(this, et):
		self = this.realself
		user_data = None
		self.sync_tested = True

		try:
			data = {
				"email": self.EmailField.get(),
				"password": self.PasswordData.get()
			}

			url = gv.website + "app/sign_in"
			r = requests.post(url, data=data)
			us = r.json()
			user_data = us.get("data")

			eml = user_data.get("email")[1]

			if user_data:
				# Waiter(self)

				chwds = string.digits + string.ascii_letters
				fpass = ""

				if user_data.get("password"):
					for s in user_data.get("password"):
						fpass = fpass + str(chwds.index(s))

				user_data['password'] = fpass

				user_data = dict((k, v.replace("\'", '')) for k,v in user_data.items())

				User().qset.create(**user_data)

		except Exception as e:
			gv.error_log(str(e))
			_help.messagew(
				msg1=ltext("login_error"),
				msg2=ltext("something_wrong_please_try_again_later")+\
					 "\n Email or password invalid",
				error=True
			)

		if user_data:
			this.login()

	def try_to_open(this):
		self = this.realself

		if gv.user_is_authenticated:
			def try_sync():
				database.sync_loop()

			thr = Thread(target=try_sync, daemon=True)
			thr.start()

			gv.get_order_cart = order.snippets.order.get_order_cart
			destroy_child(self.realself.resturant_frame)
			order.pos_order(self.realself, self.realself.resturant_frame)
