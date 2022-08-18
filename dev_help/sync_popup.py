from dev_help.widgets import *
from ntk.objects import gv as gv
from tkinter import Toplevel
import os
from PIL import ImageTk

class SyncPopUp:
    def __init__(self, *args, **kwargs):
        super(SyncPopUp, self).__init__()
        self.master = master = Toplevel()

        master.geometry("360x140+{}+{}".format(int((gv.device_width-360)/2), int((gv.device_height-220)/2)))
        master.configure(background="#F5F5F5")
        master.title("Synchronization running")
        master.resizable(False, False)
        master.iconbitmap(gv.icon_path)

        im_p            = os.path.join(gv.application_path, "icons", "cus", "active-search-3-24.png")
        self.icon_file  = ImageTk.PhotoImage(file=im_p)

        self.ibu    = get_a_label(master, text="", rowspan=2, padx=(15, 0), pady=(4, 10))
        self.srtr   = get_a_label(master, column=1, columnspan=2, text="", pady=6, padx=24, font=("Calibri", 10))
        self.pwrc   = get_a_label(master, row=1, column=1, columnspan=2, text="", pady=(6, 24), padx=24, font=("Calibri", 10))

        self.ibu.config(image=self.icon_file, compound="center")

        self.srtr.config(text="Some or all records will be modify")
        self.pwrc.config(text="Please wait while all record checked")

        self.okb    = get_a_button(master, text="OK", row=3, column=2, use_ttk=False, padx=(72, 24), width=10, ipady=0, ipadx=0)
        self.okb.config(state="disable", command=lambda: self.destroy())

        for key, value in master.children.items():
            if key.startswith("!label"):
                value.config(background="#F5F5F5", foreground="#374767", width=40)

            self.ibu.config(width=0)

    def destroy(self):
        self.master.destroy()
