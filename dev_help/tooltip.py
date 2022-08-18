from tkinter import *
from tkinter.ttk import  *
from dev_help.widgets import  *

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.configure(background="#37A000", bd=1)

        label = get_a_label(self.tw, text=self.text, pady=0, padx=0, width=len(self.text) if len(self.text) < 28 else 28, font=("Calibri", 9, "bold"))
        label.config(text=self.text, background="#000000", foreground="#ffffff", wraplength=self.wraplength)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
