from threading import Thread
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv

from setting.application import ApplicationSetting as AS

class ApplicationSetting:
	def __init__(self, realself, master, *args, **kwargs):
		super(ApplicationSetting, self).__init__(*args, **kwargs)
		realself.master.title("{} - {}".format(ltext("application_setting"), gv.st['storename']))
		self.master 							= master
		self.realself 							= realself

		self.app_setting_depend_thread 	= Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.app_setting_depend_thread.start()

	def get_dependency_master(self):
		def application_setting_popup():
			AS(self)

		self.application_setting_paned 		= get_a_panedwindow(self.master, pady=5, padx=5, style="Custom.TFrame")
		self.setting_frame 					= get_a_frame(self.application_setting_paned, width=1160, height=580, padx=int(gv.device_width/15), pady=(24, 0), style="Custom.TFrame")
		self.spacer_canv 					= get_a_canvas(self.application_setting_paned, row=2, width=gv.device_width-15, columnspan=10, highlightbackground='#FFFFFF')

		application_setting_popup()
