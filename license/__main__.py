from tkinter import ttk
from threading import Thread

from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv
from PIL import Image, ImageTk

from license.check_license import CheckLicense

import os

class License:
    def __init__(self, realself, master, *args, **kwargs):
        super(License, self).__init__(*args, **kwargs)
        realself.master.title("Activate software - bdtask")
        self.realself 							= realself
        self.master 							= master
        self.PurchaseKey                        = StringVar()
        self.ProductKey                         = StringVar()
        self.DatabaseName                       = StringVar()
        self.WebAddress                         = StringVar()

        self.DatabaseName.set("restora")

        self.license_depend_thread = Thread(target = lambda: self.get_dependency_master(), daemon = True)
        self.license_depend_thread.start()

    def get_dependency_master(self):
        def set_license():
            CheckLicense(self)

        self.lse_w_paned 		    = get_a_panedwindow(self.master, padx=0, pady=0, row=1, style="Custom.TFrame")

        sl 	= Thread(target=set_license, daemon=True)
        sl.start()
