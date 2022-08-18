from tkinter import *
from tkinter import ttk
from ntk.objects import gv as gv
from PIL import ImageTk
import calendar, time, os, datetime

class TimePicker:
    def __init__(self, rootx, rooty, insert_to, format_str=None, toplevel=None, *args, **kwargs):
        super().__init__()
        self.master = gv.timepicker = Toplevel(gv.rest.resturant_frame)
        # self.master.overrideredirect(1)
        self.master.geometry("+{}+{}".format(rootx-56, rooty))
        self.master.iconbitmap(gv.icon_path)
        self.master.resizable(0, 0)
        self.master.title("Time Picker")
        self.master.configure(background="#FFFFFF", bd=4)

        self.insert_to      = insert_to

        self.Hour           = DoubleVar()
        self.Minute         = DoubleVar()
        self.PickedTime     = StringVar()

        dec_img_p           = os.path.join(gv.depend_image_path, "minus-16-_1_ - Copy.png")
        inc_img_p           = os.path.join(gv.depend_image_path, "icons8-plus-math-16.png")

        self.chotime_l      = Label(self.master, text="Choose time", font=("Calibri", 12))
        self.chotime_l.grid(columnspan=4, padx=4, pady=(2, 8), ipady=1)

        self.pickedtime_l   = ttk.Label(self.master, text="Time", font=("Calibri", 12))
        self.pickedtime_l.grid(row=1, padx=4, pady=8)

        self.pickedtime_d   = Entry(self.master, text="", textvariable=self.PickedTime, bg="#FFFFFF", readonlybackground="#FFFFFF", bd=0, justify="c", font=("Calibri", 12))
        self.pickedtime_d.grid(row=1, column=1, columnspan=3, padx=4, pady=8)
        self.pickedtime_d.config(state="readonly")

        def released(e, w, m=True):
            try:
                if e.char.isdigit():
                    if m:
                        self.Minute.set(int(w.get()))
                    else:
                        self.Hour.set(int(w.get()))

                else: w.delete(len(w.get())-1, len(w.get()))

                self.set_picked_time()

            except: w.insert(0, "0")

        def hour_change(inc=True):
            if inc:
                self.Hour.set(int(self.Hour.get()+1) if self.Hour.get() < 23 else 0)
            else: self.Hour.set(int(self.Hour.get()-1) if self.Hour.get() > 0 else 0)

            self.set_picked_time()

        def minute_change(inc=True):
            if inc:
                self.Minute.set(int(self.Minute.get()+1) if self.Minute.get() < 59 else 0)
            else: self.Minute.set(int(self.Minute.get()-1) if self.Minute.get() > 0 else 0)

            self.set_picked_time()

        self.hour_l         = ttk.Label(self.master, text="Hour", font=("Calibri", 12))
        self.hour_l.grid(row=2, padx=4, pady=8)

        globals()["dec_img_hour"] 	= ImageTk.PhotoImage(file=dec_img_p)
        globals()["inc_img_hour"] 	= ImageTk.PhotoImage(file=inc_img_p)

        self.hour_ddb       = Button(self.master, text="", width=16, bg="#FFFFFF", activebackground="#FFFFFF", bd=0, cursor="hand2", relief=FLAT, font=("Calibri", 12))
        self.hour_ddb.grid(row=2, column=1, padx=(4, 2), pady=8)
        self.hour_ddb.config(command=lambda: hour_change(inc=False), image=globals()["dec_img_hour"], compound="center")

        self.hour_d         = ttk.Entry(self.master, textvariable=self.Hour, font=("Calibri", 12))
        self.hour_d.grid(row=2, column=2, padx=2, pady=8)
        self.hour_d.bind("<KeyRelease>", lambda e: released(e, w=self.hour_d, m=False))

        self.hour_dib       = Button(self.master, text="", width=16, bg="#FFFFFF", activebackground="#FFFFFF", bd=0, cursor="hand2", relief=FLAT, font=("Calibri", 12))
        self.hour_dib.grid(row=2, column=3, padx=(2, 4), pady=8)
        self.hour_dib.config(command=lambda: hour_change(), image=globals()["inc_img_hour"], compound="center")

        self.minute_l       = ttk.Label(self.master, text="Minute", font=("Calibri", 12))
        self.minute_l.grid(row=3, padx=4, pady=8)

        globals()["dec_img_min"] 	= ImageTk.PhotoImage(file=dec_img_p)
        globals()["inc_img_min"] 	= ImageTk.PhotoImage(file=inc_img_p)

        self.minute_dib     = Button(self.master, text="", width=16, bg="#FFFFFF", activebackground="#FFFFFF", bd=0, cursor="hand2", relief=FLAT, font=("Calibri", 12))
        self.minute_dib.grid(row=3, column=1, padx=(4, 2), pady=8)
        self.minute_dib.config(command=lambda: minute_change(inc=False), image=globals()["dec_img_min"], compound="center")

        self.minute_d       = ttk.Entry(self.master, textvariable=self.Minute, font=("Calibri", 12))
        self.minute_d.grid(row=3, column=2, padx=2, pady=8)
        self.minute_d.bind("<KeyRelease>", lambda e: released(e, w=self.minute_d))

        self.minute_ddb     = Button(self.master, text="", width=16, bg="#FFFFFF", activebackground="#FFFFFF", bd=0, cursor="hand2", relief=FLAT, font=("Calibri", 12))
        self.minute_ddb.grid(row=3, column=3, padx=(2, 4), pady=8)
        self.minute_ddb.config(command=lambda: minute_change(), image=globals()["inc_img_min"], compound="center")

        self.done_button    = Button(self.master, text="Done", width=8, bg="#37A000", fg="#FFFFFF", bd=0, cursor="hand2", relief=FLAT, font=("Calibri", 11))
        self.done_button.grid(row=4, column=2, columnspan=2, padx=(4, 2), pady=(18, 12))
        self.done_button.config(command=lambda: self.select_time_done())

        for key, value in self.master.children.items():
            if key.startswith("!label"):
                value.config(foreground="#374767", background="#FFFFFF", width=8, font=("Calibri", 11, "bold"))

            if key.startswith("!entry"):
                value.config(width=7)

        self.chotime_l.config(width=24, anchor="c", background="#ECE8DA")

        try:
            h, m = str(self.insert_to.get()).split(":")
            self.Hour.set(int(h))
            self.Minute.set(int(m))
            self.PickedTime.set("{}:{}".format(h, m))
        except: pass

        def donothing():
            pass

        def destory_tpk():
            if gv.timepicker:gv.timepicker.destroy()
            gv.rest.master.bind("<Button-1>", lambda e: donothing())

        gv.rest.master.bind("<Button-1>", lambda e: destory_tpk())

    def set_picked_time(self):
        h = str(int(self.Hour.get()))
        m = str(int(self.Minute.get()))
        self.PickedTime.set("{}:{}".format(("0" if len(h)<2 else "") + h, ("0" if len(m)<2 else "") + m))

    def insert_time(self):
        self.insert_to.config(state="normal")
        self.insert_to.delete(0, END)
        self.insert_to.insert(0, self.PickedTime.get())
        self.insert_to.config(state="readonly")

    def select_time_done(self):
        self.insert_time()
        self.destroy()

    def destroy(self):
        self.master.destroy()
