import tkinter as tk

class PHEntry(tk.Entry):
    def __init__(self, master, placeholder="PLACEHOLDER", color='grey', textvariable=None, width=24, font=('Calibri', 12), row=0, column=0, columnspan=1, rowspan=1, padx=(10, 10), pady=(10, 10), justify="left", sticky='w', default=""):
        super().__init__(master, width=width, font=font, justify=justify)

        self.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=pady, ipady=2, sticky=sticky)
        if textvariable is not None: self.config(textvariable=textvariable)

        self.tv                     = textvariable
        self.placeholder            = placeholder
        self.placeholder_color      = color
        self.default_fg_color       = self['fg']

        self.bind("<FocusIn>", self.foc_in)

        self.put_placeholder()

    def put_placeholder(self):
        if self.tv:
            if self.tv.get() == "":
                self.insert(0, self.placeholder)
        else: self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = "#000000"

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
