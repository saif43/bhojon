from dev_help.widgets import *
from ntk.objects import gv
from ntk import Toplevel, PanedWindow, Frame, Label

# gv.error_log(str(f"File: order/snippets/cancel_reason.py"))

class CancelReason:
    def __init__(self, order_id, *args, **kwargs):
        super(CancelReason, self).__init__(*args, **kwargs)
        self.order_id                = order_id
        gv.cancel_reason_data 		 = ""

        # gv.error_log(str(f"self: {self} --> order_id: {order_id} --> args: {args} --> kwargs: {kwargs}"))

        if not order_id: return

        gv.cancel_reason_master = self.master = master = Toplevel(
                                                            gv.rest.master, bg="#FAFAFA",
                                                            title=ltext("cancel_reason"),
                                                            width=580, height=260,
                                                            x=int((gv.device_width-580)/2),
                                                            y=int((gv.device_height-260)/2)
                                                        )

        self.modal_paned = PanedWindow(self.master, sticky='wne', padx=0, pady=0)
        self.modal_frame = Frame(self.modal_paned, padx=0, pady=0)

        self.modal_paned.add(self.modal_frame)

        self.can_rea_oidl = Label(
                                    self.modal_frame, padx=(56, 10),
                                    pady=(24, 10), text=ltext("order_id")
                                )

        self.can_rea_oidd = Label(
                                    self.modal_frame, column=1,
                                    pady=(24, 10),
                                    text="{}".format(self.order_id)
                                )

        self.can_rea_dtl = Label(
                                    self.modal_frame, row=1,
                                    padx=(56, 10),
                                    text=ltext("cancel_reason")
                                )

        self.can_rea_dtd = get_a_text(
                                    self.modal_frame, width=36,
                                    height=4, row=1, column=1,
                                    font=("Calibri", 12), relief="groove"
                                )

        self.can_rea_dtd.config(
                            bd=2,
                            highlightbackground="#37A000",
                            highlightcolor="#37A000"
                        )

        self.canreasdata = StringVar()

        self.submitcanreason = get_a_button(
                                        self.modal_frame, text=ltext("submit"),
                                        width=15, row=2, column=1, pady=24,
                                        padx=(172, 10), ipadx=0, ipady=2,
                                        use_ttk=False,
                                        font=("Calibri", 10, "bold")
                                    )

        self.submitcanreason.config(
                                command=lambda: self.submit()
                            )

        for key, value in self.modal_frame.children.items():
            if key.startswith("!label"):
                value.config(
                        background="#FFFFFF",
                        foreground="#374767",
                        font=("Calibri", 12)
                    )

        gv.rest.master.wait_window(master)

    def submit(self):
        gv.cancel_reason_data       = self.can_rea_dtd.get(1.0, "end")
        self.master.destroy()
