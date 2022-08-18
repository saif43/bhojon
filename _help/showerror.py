from tkinter import Toplevel
from dev_help.widgets import *
from ntk.objects import gv as gv
from ntk import Toplevel, Label, Button
import os
from PIL import ImageTk


class ShowError:
    def __init__(self, r, rself, *args, **kwargs):
        super(ShowError, self).__init__()
        self.rself = rself
        self.rself.title = args[0][1].get("title")

        self.master = master = Toplevel(
            width=w(360), height=200, bg='#FAFAFA', title=self.rself.title or "Error",
            x=int((gv.device_width-w(360))/2), y=int((gv.device_height-200)/2))

        # master.geometry("{}x200+{}+{}".format(w(360), int((gv.device_width-w(360))/2), int((gv.device_height-200)/2)))
        # master.configure(background="#F5F5F5")

        gv.mse = self.master

        # master.grid_rowconfigure(0, weight=1)
        # master.grid_rowconfigure(1, weight=1)
        # master.grid_rowconfigure(2, weight=1)

        # print(args)

        self.rself.msg1 = args[0][1].get("msg1")
        self.rself.msg2 = args[0][1].get("msg2")
        self.rself.btext = args[0][1].get("btext")
        self.rself.icon = args[0][1].get("icon")
        self.rself.result = args[0][1].get("dresult")

        master.resizable(False, False)
        master.iconbitmap(gv.icon_path)

        im_p = os.path.join(gv.application_path, "icons", "cus", "error-7-48 (2).png")
        self.rself.icon_file = ImageTk.PhotoImage(file=im_p)

        self.rself.ibu = Label(
            master, text="", rowspan=2, padx=(15, 0), pady=(4, 10), bg='#FAFAFA', fg="#374767")
        msg1 = Label(
            master, column=1, columnspan=2, bg='#F5F5F5', fg="#374767", case='capital',
            text=self.rself.msg1 if self.rself.msg1 else gv.ltext("trying_to_do_your_task"),
            pady=6, padx=24, font=("Calibri", 12), width=30, length=gv.w(196))
        msg2 = Label(
            master, row=1, column=1, columnspan=2, bg='#F5F5F5', fg="#374767", case='capital',
            text=self.rself.msg2 if self.rself.msg2 else gv.ltext("something_wrong"),
            pady=(6, 24), padx=24, font=("Calibri", 10), width=40, length=gv.w(256))

        self.rself.ibu.config(image=self.rself.icon_file, compound="center")

        but = Button(
            master, text="OK", row=2, column=2, padx=(72, 24), width=10, ipady=0, ipadx=0)
        but.config(command=lambda: self.destroy())

        gv.rest.master.bind("<Return>", lambda e: self.destroy())

        if self.rself.title: master.title(self.rself.title)
        # if self.rself.msg1: msg1.config(text=self.rself.msg1)
        # if self.rself.msg2: msg2.config(text=self.rself.msg2)
        if self.rself.btext: but.config(text=self.rself.btext)
        if self.rself.title: master.title(self.rself.title)

        # for key, value in master.children.items():
        #     if key.startswith("!label"):
        #         value.config(width=40, wraplength=gv.w(256))

            # self.rself.ibu.config(width=0)

        gv.rest.master.wait_window(master)

    def destroy(self):
        self.rself.result = "OK"
        self.master.destroy()
