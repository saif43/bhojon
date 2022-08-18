from tkinter import Toplevel, PhotoImage
from dev_help.widgets import *
from ntk.objects import gv as gv
import os


class ShowInfo:
    def __init__(self, r, rself, *args, **kwargs):
        super(ShowInfo, self).__init__()
        self.master           = master = Toplevel()
        master.geometry("{}x200+{}+{}".format(w(360), int((gv.device_width-w(360))/2), int((gv.device_height-200)/2)))
        master.configure(background="#F5F5F5")
        gv.msi                = self.master

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)

        self.rself            = rself
        self.rself.title      = args[0][1].get("title")
        self.rself.msg1       = args[0][1].get("msg1")
        self.rself.msg2       = args[0][1].get("msg2")
        self.rself.btext      = args[0][1].get("btext")
        self.rself.icon       = args[0][1].get("icon")
        self.rself.result     = args[0][1].get("dresult")

        master.resizable(False, False)
        master.iconbitmap(gv.icon_path)

        self.rself.icon_file  = PhotoImage(file=os.path.join(gv.application_path, "icons", "cus", "info-5-48 (1).png"))

        self.rself.ibu  = get_a_label(master, text="", rowspan=2, padx=(15, 0), pady=(4, 10))
        msg1            = get_a_label(master, column=1, columnspan=2, text=ltext("task_result_apear_here"), pady=6, padx=24, font=("Calibri", 10))
        msg2            = get_a_label(master, row=1, column=1, columnspan=2, text=ltext("more_info_in_help"), pady=(6, 24), padx=24, font=("Calibri", 10))

        self.rself.ibu.config(image=self.rself.icon_file, compound="center")

        but             = get_a_button(master, text="OK", row=2, column=2, use_ttk=False, padx=(72, 24), width=10, ipady=0, ipadx=0)
        but.config(command=lambda: self.destroy())

        gv.rest.master.bind("<Return>", lambda e: self.destroy())

        if self.rself.title: master.title(self.rself.title)
        if self.rself.msg1: msg1.config(text=self.rself.msg1)
        if self.rself.msg2: msg2.config(text=self.rself.msg2)
        if self.rself.btext: but.config(text=self.rself.btext)
        if self.rself.title: master.title(self.rself.title)

        for key, value in master.children.items():
            if key.startswith("!label"):
                value.config(background="#F5F5F5", foreground="#374767", width=40, wraplength=gv.w(256))

            self.rself.ibu.config(width=0)

        gv.rest.master.wait_window(master)

    def destroy(self):
        self.rself.result = "OK"
        self.master.destroy()
