from tkinter import Toplevel
from dev_help.widgets import *
from ntk.objects import gv as gv
import os
from PIL import ImageTk

class AskYesNo:
    def __init__(self, r, rself, *args, **kwargs):
        super(AskYesNo, self).__init__()
        self.master           = master = Toplevel()
        master.geometry("{}x200+{}+{}".format(w(360), int((gv.device_width-w(360))/2), int((gv.device_height-200)/2)))
        master.configure(background="#F5F5F5")
        gv.mayn                = self.master

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)

        self.rself            = rself
        self.rself.title      = args[0][1].get("title")
        self.rself.msg1       = args[0][1].get("msg1")
        self.rself.msg2       = args[0][1].get("msg2")
        self.rself.btext1     = args[0][1].get("btext1")
        self.rself.btext2     = args[0][1].get("btext2")
        self.rself.icon       = args[0][1].get("icon")
        self.rself.result     = args[0][1].get("dresult")
        self.rself.bback1     = args[0][1].get("bback1")
        self.rself.bback2     = args[0][1].get("bback2")

        master.resizable(False, False)
        master.iconbitmap(gv.icon_path)

        im_p            = os.path.join(gv.application_path, "icons", "cus", "neutral-dicision-48.png")
        self.rself.icon_file  = ImageTk.PhotoImage(file=im_p)

        self.rself.ibu  = get_a_label(master, text="", rowspan=2, padx=(15, 0), pady=(4, 10))
        msg1            = get_a_label(master, column=1, columnspan=3, text=ltext("click_yes_to_continue"), pady=6, padx=24, font=("Calibri", 10))
        msg2            = get_a_label(master, row=1, column=1, columnspan=3, text=ltext("are_you_sure_to_proceed"), pady=(6, 24), padx=24, font=("Calibri", 10))

        self.rself.ibu.config(image=self.rself.icon_file, compound="center")

        but1             = get_a_button(master, text="Yes", row=2, column=1, use_ttk=False, padx=0, width=10, ipady=0, ipadx=0)
        but1.config(command=lambda: self.destroy(1))
        but2             = get_a_button(master, text="No", row=2, column=2, use_ttk=False, padx=0, width=10, ipady=0, ipadx=0, bg="#FF0000")
        but2.config(command=lambda: self.destroy(0))

        master.bind("<Return>", lambda e: self.destroy(1))

        if self.rself.title: master.title(self.rself.title)
        if self.rself.msg1: msg1.config(text=self.rself.msg1)
        if self.rself.msg2: msg2.config(text=self.rself.msg2)
        if self.rself.btext1: but.config(text=self.rself.btext1)
        if self.rself.btext2: but.config(text=self.rself.btext2)
        if self.rself.title: master.title(self.rself.title)

        for key, value in master.children.items():
            if key.startswith("!label"):
                value.config(background="#F5F5F5", foreground="#374767", width=40, wraplength=gv.w(256))

            self.rself.ibu.config(width=0)

        gv.rest.master.wait_window(master)

    def destroy(self, b):
        self.rself.result = True if b == 1 else False
        self.master.destroy()
