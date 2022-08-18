from tkinter import *
from tkinter import messagebox, ttk
from ntk.objects import gv
import calendar, time, os, datetime

class DatePicker:
    def __init__(self, toplevel, rootx, rooty, insert_to, format_str=None, *args, **kwargs):
        super().__init__()
        self.master = toplevel
        self.str_format = format_str or '%02d-%s-%s'
        self.insert_to = insert_to

        self.master.title("Date Picker")
        self.master.iconbitmap(gv.icon_path)
        self.master.resizable(0, 0)
        self.master.geometry("+{}+{}".format(rootx, rooty))
        self.master.overrideredirect(1)

        self.style = ttk.Style()
        self.style.configure("TButton", background="#e4e5e7", foreground = "#374767")

        self.init_frames()
        self.init_needed_vars()
        self.init_month_year_labels()
        self.init_buttons()
        self.space_between_widgets()
        self.fill_days()
        self.make_calendar()

    def init_frames(self):
        self.frame1 = Frame(self.master)
        self.frame1.pack()

        self.frame_days = Frame(self.master)
        self.frame_days.pack()

    def init_needed_vars(self):
        self.month_names = tuple(calendar.month_name)
        self.day_names = tuple(calendar.day_abbr)
        self.year = time.strftime("%Y")
        self.month = time.strftime("%B")

    def init_month_year_labels(self):
        self.year_str_var = StringVar()
        self.month_str_var = StringVar()

        self.year_str_var.set(self.year)
        self.year_lbl = Label(self.frame1, textvariable=self.year_str_var,
                                 width=3)
        self.year_lbl.grid(row=0, column=5)

        self.month_str_var.set(self.month)
        self.month_lbl = Label(self.frame1, textvariable=self.month_str_var,
                                  width=8)
        self.month_lbl.grid(row=0, column=1)

    def init_buttons(self):
        self.left_yr = Button(self.frame1, text="←", width=5,
                                  command=self.prev_year)
        self.left_yr.grid(row=0, column=4)

        self.right_yr = Button(self.frame1, text="→", width=5,
                                   command=self.next_year)
        self.right_yr.grid(row=0, column=6)

        self.left_mon = Button(self.frame1, text="←", width=5,
                                   command=self.prev_month)
        self.left_mon.grid(row=0, column=0)

        self.right_mon = Button(self.frame1, text="→", width=5,
                                    command=self.next_month)
        self.right_mon.grid(row=0, column=2)

    def space_between_widgets(self):
        self.frame1.grid_columnconfigure(3, minsize=40)

    def prev_year(self):
        self.prev_yr = int(self.year_str_var.get()) - 1
        self.year_str_var.set(self.prev_yr)

        self.make_calendar()

    def next_year(self):
        self.next_yr = int(self.year_str_var.get()) + 1
        self.year_str_var.set(self.next_yr)

        self.make_calendar()

    def prev_month(self):
        index_current_month = self.month_names.index(self.month_str_var.get())
        index_prev_month = index_current_month - 1
        if index_prev_month == 0:
            self.month_str_var.set(self.month_names[12])
        else:
            self.month_str_var.set(self.month_names[index_current_month - 1])

        self.make_calendar()

    def next_month(self):
        index_current_month = self.month_names.index(self.month_str_var.get())

        try:
            self.month_str_var.set(self.month_names[index_current_month + 1])
        except IndexError: self.month_str_var.set(self.month_names[1])

        self.make_calendar()

    def fill_days(self):
        col = 0
        for day in self.day_names:
            self.lbl_day = Label(self.frame_days, text=day)
            self.lbl_day.grid(row=0, column=col)
            col += 1

    def make_calendar(self):
        try:
            for dates in self.m_cal:
                for date in dates:
                    if date == 0:
                        continue

                    self.delete_buttons(date)

        except AttributeError: pass

        year = int(self.year_str_var.get())
        month = self.month_names.index(self.month_str_var.get())
        self.m_cal = calendar.monthcalendar(year, month)

        for dates in self.m_cal:
            row = self.m_cal.index(dates) + 1
            for date in dates:
                col = dates.index(date)

                if date == 0:
                    continue

                self.make_button(str(date), str(row), str(col))

    def make_button(self, date, row, column):
        exec(
            "self.btn_" + date + " = ttk.Button(self.frame_days, text=" + date
            + ", width=5)\n"
            "self.btn_" + date + ".grid(row=" + row + " , column=" + column
            + ")\n"
            "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
        )

    def delete_buttons(self, date):
        exec(
            "self.btn_" + str(date) + ".destroy()"
        )

    def get_date(self, clicked=None):
        clicked_button = clicked.widget
        year = self.year_str_var.get()
        month = self.month_names.index(self.month_str_var.get())
        date = clicked_button['text']

        self.full_date = self.str_format % (date, month, year)
        try:
            self.master.withdraw()
            self.insert_to.config(state="normal")
            self.insert_to.delete(0, END)
            self.insert_to.insert(0, self.full_date)
            self.insert_to.config(state="readonly")
        except AttributeError as ae: messagebox.showerror("Date picker exception", ae)

    def destroy(self):
        try:
            self.master.withdraw()
        except Exception as e: messagebox.showerror("Date picker exception", e)
