import socket, time, _help, os
from threading import Thread
from ntk.objects import gv as gv
from tkinter import *
from PIL import Image, ImageTk
from dev_help.tooltip import ToolTip
from database.table import OnlineOrder


class SyncLoop:
	def __init__(self, user_call=False, *args, **kwargs):
		super(SyncLoop, self).__init__()
		self.user_call 				= user_call
		self.togger_opened			= False
		self.s_sdbt 				= False

		self.short_delay_thread 	= Thread(target=self.short_delay_sync, daemon=True)
		self.short_delay_thread.start()

		self.long_delay_thread 		= Thread(target=self.long_delay_sync, daemon=True)
		self.long_delay_thread.start()

	def sync_det_but(self):
		if not self.s_sdbt:
			gv.s_sdbt = Button(gv.rest.master, text="", bg="#FFFFFF", activebackground="#FFFFFF", fg="#000000", relief="groove", bd=0, cursor="hand2")
			gv.s_sdbt.place(x=gv.device_width - 300, y=10)
			gv.s_sdbt.config(command=lambda: self.sync_det_but_toggler())
			ToolTip(gv.s_sdbt, "Toggle Detail")
			self.s_sdbt = True
			self.sdbs_th.start()

	def sync_det_but_spinner(self):
		while self.s_sdbt:
			i = 360
			while i>1:
				time.sleep(0.01)
				img = Image.open(os.path.join(gv.fi_path, 'cus', 'circle-dashed-4-24.png'))
				imr = img.rotate(i)
				self.sync_det_but_spinner_img = ImageTk.PhotoImage(imr)
				gv.s_sdbt.config(image=self.sync_det_but_spinner_img, compound="center")
				i -= 2
			time.sleep(0.01)

		if not self.s_sdbt:
			gv.s_sdbt.destroy()

	def sync_det_but_toggler(self):
		if self.togger_opened:
			for w in [gv.sds_lab, gv.lds_lab, gv.sodu_lab]:
				try:
					if w:
						w.place(x=-9999, y=-9999)
				except: pass

			self.togger_opened = False
		else:
			for w in [gv.sds_lab, gv.lds_lab, gv.sodu_lab]:
				try:
					if w:
						w.place(x=gv.device_width - 556, y=7)
				except: pass

			self.togger_opened = True

	def short_delay_sync(self):
		tots_del = (int(int(gv.st['sync_short_delay'].split(":")[0])*60 + int(gv.st['sync_short_delay'].split(":")[1]))*60) - 16

		sync_short_st = StringVar()
		sync_short_st.set("Order synchronization in 15 seconds")

		def dss_sf():
			self.do_short_sync=False
			self.sdsi = -1
			self.short_sync_lab.destroy()
			self.short_sync_sc_bt.destroy()

		while True:
			if not gv.user_is_authenticated or gv.sync_loop_stop: break

			if gv.user_is_authenticated and len(gv.cart_data) == 0 and len(gv.sync_list) == 0:
				self.do_short_sync = True
				self.sdsi = 15

				self.short_sync_lab = Label(gv.rest.master, textvariable=sync_short_st, bg="#FFFFFF", activebackground="#FFFFFF", fg="#374767", font=("Calibri", 10, "bold"))
				self.short_sync_sc_bt = Button(gv.rest.master, text="Skip for Now", bg="#3A95E4", activebackground="#FFFFFF", fg="#FFFFFF", font=("Calibri", 10, "bold"), relief="groove", bd=0, cursor="hand2")
				self.short_sync_sc_bt.config(command=lambda: dss_sf())

				self.short_sync_lab.place(x=gv.device_width - 596, y=10)
				self.short_sync_sc_bt.place(x=gv.device_width - 356, y=10)

				while self.sdsi>=0:
					sync_short_st.set("Order synchronization in {} second".format(self.sdsi, "" if self.sdsi<2 else "s"))
					time.sleep(1)
					self.sdsi -= 1

				if self.do_short_sync:
					self.short_sync_lab.destroy()
					self.short_sync_sc_bt.destroy()

					self.sdbs_th = Thread(target=self.sync_det_but_spinner, daemon=True)
					self.sync_det_but()

					try:
						socket.create_connection(("www.google.com", 80))

						gv.sync_pop = None
						gv.deep_sync = False
						try:
							gv.rstatus_l = gv.sds_lab = Label(gv.rest.master, text="Uploading offline order", bg="#FFFFFF", activebackground="#FFFFFF", fg="#374767", font=("Calibri", 10, "bold"))

							gv.sync_class_l[17](self)
							gv.sds_lab.config(text="Offline order uploaded")
							gv.sds_lab.destroy()
						except Exception as e: gv.error_log(str(e))

						try:
							gv.rstatus_l = gv.lds_lab = Label(gv.rest.master, text="Downloading online order", bg="#FFFFFF", activebackground="#FFFFFF", fg="#374767", font=("Calibri", 10, "bold"))

							gv.sync_class_l[10](self)
							gv.lds_lab.config(text="Online order downloaded")
							gv.lds_lab.destroy()
						except Exception as e: gv.error_log(str(e))

						try:
							gv.rstatus_l = gv.lds_lab = Label(gv.rest.master, text="Downloading new customer", bg="#FFFFFF", activebackground="#FFFFFF", fg="#374767", font=("Calibri", 10, "bold"))

							gv.sync_class_l[6](self)
							gv.lds_lab.config(text="Customer synchronized")
							gv.lds_lab.destroy()
						except Exception as e: gv.error_log(str(e))

						if gv.oo_mas:
							orders = OnlineOrder().qset.all()
							gv.paginator(gv.oo_mas, gv.oo_foot, orders, gv.oo_canv, gv.oo_cont)

						self.s_sdbt = False
						time.sleep(tots_del)

					except Exception as e:
						gv.error_log(str(e))
						self.s_sdbt = False
						time.sleep(tots_del)

				else: time.sleep(tots_del)

			else: time.sleep(tots_del)

	def long_delay_sync(self):
		tot_del 		= (int(int(gv.st['sync_long_delay'].split(":")[0])*60 + int(gv.st['sync_long_delay'].split(":")[1]))*60) - 16
		time.sleep(tot_del)

		sync_long_st = StringVar()
		sync_long_st.set("Changed order update in 15 seconds")

		def dls_sf():
			self.do_long_sync=False
			self.ldsi = -1
			self.long_sync_lab.destroy()
			self.long_sync_sc_bt.destroy()

		while True:
			if not gv.user_is_authenticated or gv.sync_loop_stop: break

			if gv.user_is_authenticated and len(gv.cart_data) == 0 and len(gv.sync_list) == 0:
				self.do_long_sync = True
				self.ldsi = 15

				self.long_sync_lab = Label(gv.rest.master, textvariable=sync_long_st, bg="#FFFFFF", activebackground="#FFFFFF", fg="#374767", font=("Calibri", 10, "bold"))
				self.long_sync_sc_bt = Button(gv.rest.master, text="Skip for Now", bg="#3A95E4", activebackground="#FFFFFF", fg="#FFFFFF", font=("Calibri", 10, "bold"), relief="groove", bd=0, cursor="hand2")
				self.long_sync_sc_bt.config(command=lambda: dls_sf())

				self.long_sync_lab.place(x=gv.device_width - 596, y=10)
				self.long_sync_sc_bt.place(x=gv.device_width - 356, y=10)

				while self.ldsi>=0:
					sync_long_st.set("Changed order update in {} second{}".format(self.ldsi, "" if self.ldsi<2 else "s"))
					time.sleep(1)
					self.ldsi -= 1

				if self.do_long_sync:
					self.long_sync_lab.destroy()
					self.long_sync_sc_bt.destroy()

					self.sdbs_th = Thread(target=self.sync_det_but_spinner, daemon=True)
					self.sync_det_but()

					try:
						socket.create_connection(("www.google.com", 80))

						gv.sync_pop = None
						gv.deep_sync = False
						try:
							gv.rstatus_l = gv.sodu_lab = Label(gv.rest.master, text="Updating changed synced order", bg="#FFFFFF", activebackground="#FFFFFF", fg="#374767", font=("Calibri", 10, "bold"))

							gv.sync_class_l[18](self)
							gv.sodu_lab.config(text="Changed synced order updated")
							gv.sodu_lab.destroy()
						except Exception as e: gv.error_log(str(e))

						self.s_sdbt = False
						time.sleep(tot_del)

					except Exception as e:
						gv.error_log(str(e))
						self.s_sdbt = False
						time.sleep(tot_del)

				else: time.sleep(tot_del)

			else: time.sleep(tot_del)
