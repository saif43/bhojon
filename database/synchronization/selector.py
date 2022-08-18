
from dev_help.widgets import *
from threading import Thread
from ntk.objects import gv as gv
import os, _help, order, time
from PIL import Image, ImageTk
from ntk import Frame, PanedWindow, Canvas, Scrollbar, Toplevel

from database.table import SyncResult


class SyncSelector:
    def __init__(self, rself, *args, **kwargs):
        super(SyncSelector, self).__init__()

        self.res_width = 895 if 895 < gv.device_width else gv.device_width
        self.res_height = 480 if 480 < gv.device_height else gv.device_height

        self.master = Toplevel(
            width=self.res_width, height=self.res_height, title=ltext("select_synchronizable_table"))

        self.master.protocol("WM_DELETE_WINDOW", self.destroy)

        gv.swin = True
        self.args = args
        self.kwargs = kwargs
        self.rself = rself

        self.modal_frame = PanedWindow(self.master, width=self.res_width, height=self.res_height)
        self.header_canv = Canvas(
            self.modal_frame, padx=0, width=self.res_width, height=32,
            mousescroll=False, scrollregion=[0, 0, self.res_width, 0])
        self.modal_canv = Canvas(
            self.modal_frame, row=1, padx=5, width=self.res_width, height=self.res_height-100,
            mousescroll=True, scrollregion=[0, 0, self.res_width, 0])
        self.table_list_scroll = Scrollbar(self.modal_frame, self.modal_canv, orient='horizontal', column=0)
        self.footer_frame_holder = Frame(self.modal_frame, row=2, height=32, width=self.res_width)
        self.footer_frame = Frame(self.footer_frame_holder, row=2, sticky="e")

        self.modal_frame.add(self.header_canv)
        self.modal_frame.add(self.modal_canv)
        self.modal_frame.add(self.table_list_scroll)
        self.modal_frame.add(self.footer_frame_holder)

        self.synchronization_selector()

    def synchronization_selector(self):
        unchecked_mark = os.path.join(gv.fi_path, "cus", "check-mark-3-20.png")
        checked_mark = os.path.join(gv.fi_path, "cus", "check-mark-3-24 (1).png")

        i_n = 1
        x_v = [[0, 55], [55, 340], [340, 490], [490, 640], [640, 770], [770, 895]]

        self.sabi = PhotoImage(file=checked_mark).subsample(1, 2)

        hll = [ltext("sn"), ltext("item"), ltext("last_update"), ltext("last_check"), ltext("status"), '']

        for it, x in enumerate(x_v):
            self.header_canv.create_text(
                x[0]+12, 24, text="{}".format(hll[it]),
                font=("Calibri", gv.w(10), "bold"), anchor="w", fill="#374767"
            )

        self.sab = get_a_button(
            self.modal_frame, text=ltext("all"), image=self.sabi,
            compound="right", column=1, width=20, padx=6, ipady=0,
            ipadx=12, bg="#FFFFFF", fg="#282828", relief="flat", use_ttk=False
        )

        self.header_canv.create_window(
            x_v[len(x_v)-1][0]+64, 24, window=self.sab,
            width=124, height=24, anchor="center"
        )

        self.sab.config(
            activeforeground="#000000", activebackground="#FFFFFF",
            command=lambda: self.toggle_select(all=True)
        )

        gv.rstatus_l = get_a_label(self.footer_frame, text="")
        gv.rstatus_l.config(background="#FFFFFF", foreground="#374767", font=("Calibri", 10, "bold"))

        self.deep_sync_button = get_a_button(
            self.footer_frame, column=1, text=ltext("start_deep_sync"),
            use_ttk=False, ipady=5, bg="#E0A800", width=14
        )
        gv.sync_but = self.sync_button = get_a_button(
            self.footer_frame, column=2, text=ltext("start_sync"),
            use_ttk=False, bg="#218838", ipady=5, width=14
        )

        def start(deep=False):
            gv.deep_sync = deep
            self.ssbs_th = Thread(target=self.sync_det_but_spinner, daemon=True)
            self.ss_th = Thread(target=self.start_sync, daemon=True)
            self.ss_th.start()

        self.deep_sync_button.config(
            activebackground="#37A000", disabledforeground="#FFFFFF",
            command=lambda: start(True)
        )
        self.sync_button.config(activebackground="#37A000", disabledforeground="#FFFFFF", command=lambda: start())

        for en, tbl in enumerate(gv.tablelist):
            rtbi = []
            for i in x_v:
                tbi = self.modal_canv.create_rectangle(
                    i[0], (i_n-1)*28, i[1], i_n*28,
                    fill="#FFFFFF" if i_n%2 == 0 else "#FAFAFA", outline="#F1F3F6"
                )
                rtbi.append(tbi)

                self.modal_canv.tag_bind(
                    tbi, "<Enter>",
                    lambda e, rtbi=rtbi, fill="#F5F5F5": self.entered(self.modal_canv, rtbi, fill)
                )
                self.modal_canv.tag_bind(
                    tbi, "<Leave>",
                    lambda e, rtbi=rtbi, fill="#FFFFFF" if i_n%2 == 0 else "#F9F9F9": self.entered(
                        self.modal_canv, rtbi, fill
                    )
                )

            globals()["sr_{}".format(en)] = self.modal_canv.create_rectangle(
                770, (i_n-1)*28, 895, i_n*28,
                fill="#FFFFFF" if i_n%2 == 0 else "#F9F9F9", outline="#F1F3F6"
            )

            self.modal_canv.create_text(
                20, (i_n*28)-14, text="{}".format(i_n),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )
            self.modal_canv.create_text(
                75, (i_n*28)-14, text="{}".format(gv.tbltextlist[en]),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )

            globals()["sr_{}".format(en)] = self.modal_canv.create_rectangle(
                770, (i_n-1)*28, 895, i_n*28,
                fill="#FFFFFF" if i_n%2 == 0 else "#FAFAFA", outline="#F1F3F6"
            )

            self.modal_canv.create_text(
                20, (i_n*28)-14, text="{}".format(i_n),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )
            self.modal_canv.create_text(
                75, (i_n*28)-14, text="{}".format(gv.tbltextlist[en]),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )

            tsr = SyncResult().qset.filter(table_name=tbl).first()

            if tsr:
                tsr_l = [tsr['last_update'], tsr['last_checked'], "Success" if tsr['status']==1 else "Error"]
            else:
                tsr_l = ["None", "None", "None"]

            self.modal_canv.create_text(
                360, (i_n*28)-14, text="{}".format(tsr_l[0]),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )
            self.modal_canv.create_text(
                510, (i_n*28)-14, text="{}".format(tsr_l[1]),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )
            self.modal_canv.create_text(
                660, (i_n*28)-14, text="{}".format(tsr_l[2]),
                font=("Calibri", 8, "bold"), fill="#374767", anchor="w"
            )

            globals()["ucm_{}".format(en)] = PhotoImage(file=unchecked_mark).subsample(1, 2)
            globals()["cm_{}".format(en)] = PhotoImage(file=checked_mark).subsample(1, 2)

            globals()["sm_but_{}".format(en)] = self.modal_canv.create_image(
                820, (i_n*28)-14, image=globals()["ucm_{}".format(en)], anchor="w"
            )

            self.modal_canv.tag_bind(
                globals()["sm_but_{}".format(en)], "<Button-1>",
                lambda e, enn=en: self.toggle_select(enn)
            )
            self.modal_canv.tag_bind(
                globals()["sr_{}".format(en)], "<Button-1>",
                lambda e, enn=en: self.toggle_select(enn)
            )

            canvas_mouse_el(self.modal_canv, globals()["sr_{}".format(en)])
            canvas_mouse_el(self.modal_canv, globals()["sm_but_{}".format(en)])

            i_n = i_n + 1
            self.modal_canv.config(scrollregion=[0, 0, self.res_width, (i_n+1)*26])

    def toggle_select(self, enn=None, all=False):
        if all:
            if gv.tablelist == gv.sync_list:
                gv.sync_list = []
                for i in range(len(gv.tablelist)):
                    self.modal_canv.itemconfigure(
                        globals()["sm_but_{}".format(i)], image=globals()["ucm_{}".format(i)]
                    )

            else:
                gv.sync_list = gv.tablelist
                for i in range(len(gv.tablelist)):
                    self.modal_canv.itemconfigure(
                        globals()["sm_but_{}".format(i)], image=globals()["cm_{}".format(i)]
                    )

        else:
            if gv.tablelist[enn] in gv.sync_list:
                self.modal_canv.itemconfigure(
                    globals()["sm_but_{}".format(enn)], image=globals()["ucm_{}".format(enn)]
                )
                ind = gv.sync_list.index(gv.tablelist[enn])
                gv.sync_list.pop(ind)
            else:
                self.modal_canv.itemconfigure(
                    globals()["sm_but_{}".format(enn)], image=globals()["cm_{}".format(enn)]
                )
                gv.sync_list.append(gv.tablelist[enn])

    def sync_det_but_spinner(self):
        if gv.deep_sync: gv.sync_but = self.deep_sync_button

        while True:
            i = 360
            try:
                while i>1:
                    try:
                        time.sleep(0.01)
                        img = Image.open(os.path.join(gv.fi_path, 'cus', 'circle-dashed-4-24.png'))
                        imr = img.rotate(i)
                        self.sync_det_but_spinner_img = ImageTk.PhotoImage(imr)
                        gv.sync_but.config(
                            image=self.sync_det_but_spinner_img, compound="left",
                            width=144 if gv.deep_sync else 120, text=gv.sync_but_t
                        )
                        i -= 2
                    except: raise
                time.sleep(0.01)
            except: break

    def start_sync(self):
        if not gv.user_is_authenticated:
            _help.messagew(
                root=gv.rest.master, msg1=ltext("authentication_error"),
                msg2=ltext("please_login_to_do_synchronization"), error=True
            )
            return

        tbl_l = [r['table_name'] for r in SyncResult().qset.filter(search='table_name').all()]
        for table in gv.tablelist:
            if not table in tbl_l:
                SyncResult().qset.create(**{'table_name':table})

        if len(gv.sync_list) == 0:
            _help.messagew(
                root=gv.rest.master, msg1=ltext("trying_to_start_synchronization"),
                msg2=ltext("please_select_table_to_start_synchronization"), error=True
            )
        else:
            # try:
            gv.sync_pop = None

            def change_status(t, s=True):
                gv.rstatus_l.config(
                    text="{} {}".format(gv.tbltextlist[gv.tablelist.index(t)],
                                        "updating..." if s else "updated")
                )

            self.ssbs_th.start()

            self.deep_sync_button.config(state="disabled")
            self.sync_button.config(state="disabled")

            for ix, tbl in enumerate(gv.tablelist):
                if tbl in gv.sync_list:
                    gv.sync_but_t = " {} {}/{}".format(
                        "Deep sync" if gv.deep_sync else "Sync",
                        gv.sync_list.index(tbl)+1, len(gv.sync_list)
                    )
                    change_status(tbl)
                    gv.sync_class_l[ix](self)
                    change_status(tbl, False)
                    time.sleep(1)

            self.destroy()

            destroy_child(gv.menu.realself.resturant_frame)
            gv.menu.refresh()
            order.pos_order(gv.menu.realself, gv.menu.realself.resturant_frame)

            # except Exception as e:
            #     gv.error_log(str(e))
            #     err = _help.messagew(
            #         root=gv.rest.master, msg1=ltext("synchronization_error"),
            #         msg2=ltext("synchronization_exit"), error=True
            #     )
            #     if err.result == "OK":
            #         self.destroy()

    def entered(self, root, rtbi, fill):
        for ti in rtbi:
            root.itemconfig(ti, fill=fill)

    def destroy(self):
        gv.sync_list = []
        gv.swin = False
        self.master.destroy()
