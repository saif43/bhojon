from ntk import Toplevel, Canvas, PanedWindow, gv
from database.table import Bill, SubOrder
from dev_help.widgets import canvas_mouse_el
from tkinter import PhotoImage
from invoice.view_split_pos import ViewSplitPosInvoice
import json, os

# gv.error_log(str(f"File: order/snippets/sub_orders.py"))

class SubOrderWindow:
    def __init__(self, *args, **kwargs):
        super(SubOrderWindow, self).__init__()

        # gv.error_log(str(f"self: {self} args: {args} --> kwargs: {kwargs}"))

        self.order = kwargs.get('order')
        self.bill = Bill().qset.filter(order_id=self.order['id']).first()
        self.sub_orders = SubOrder().qset.filter(order_id=self.order['id']).all()

        if not self.order or not self.bill or not self.sub_orders:
            return

        if gv.sub_order_list_view_window:
            gv.sub_order_list_view_window.destroy()
        gv.sub_order_list_view_window = self.master = Toplevel(
            gv.main_window, title='Sub-Orders', width=790, height=320)

        self.list_paned = PanedWindow(self.master, width=320)

        self.list_canvas = Canvas(self.list_paned, mousescroll=False)

        all_items = [
            [
                [0, 0, 56, 30, 18, 15, 'SL', ('Calibri', 12, 'bold')],
                [56, 0, 528, 30, 74, 15, 'Info', ('Calibri', 12, 'bold')],
                [528, 0, 664, 30, 546, 15, 'Total', ('Calibri', 12, 'bold')],
                [664, 0, 778, 30, 682, 15, 'Action', ('Calibri', 12, 'bold')]
            ]
        ]

        for entry_number, sub_order in enumerate(self.sub_orders):
            if type(sub_order['order_menu_id']) != dict:
                sub_order['order_menu_id'] = json.loads(sub_order['order_menu_id'])

            y_pos = (entry_number+1)*30
            y_plus_pos = (entry_number+2)*30
            y_exact = y_pos+15

            info = 'Vat: {}, Discount: {}, Service charge: {}'.format(
                sub_order['vat'], sub_order['discount'], sub_order['s_charge'])

            all_items.append([
                [0, y_pos, 56, y_plus_pos, 18, y_exact, entry_number+1, ('Calibri', 11)],
                [56, y_pos, 528, y_plus_pos, 74, y_exact, info, ('Calibri', 11)],
                [528, y_pos, 664, y_plus_pos, 546, y_exact, sub_order['total_price'], ('Calibri', 11)]
            ])

        lfile_path = os.path.join(gv.fi_path, "cus", "view-details-24.png")

        for entry_number, item in enumerate(all_items):
            print('entry_number', entry_number)
            for s_item in item:
                self.list_canvas.create_rectangle(
                    s_item[0], s_item[1], s_item[2], s_item[3],
                    fill='#FAFAFA' if entry_number % 2 == 0 else '#DDD', outline='#999')

                self.list_canvas.create_text(
                    s_item[4], s_item[5], text=s_item[6], font=s_item[7], fill='#374767', anchor='w')

            if entry_number > 0:
                globals()["tosplit_pim_%s" % entry_number] = PhotoImage(file=lfile_path).subsample(2, 2)

                self.list_canvas.create_rectangle(
                    664, s_item[1], 778, s_item[3],
                    fill='#FAFAFA' if entry_number % 2 == 0 else '#DDD', outline='#999')

                globals()["tosplit_pirect_%s" % entry_number] = self.list_canvas.create_rectangle(
                    s_item[4] + 132, s_item[1] + 6, s_item[4] + 150, s_item[1] + 24,
                    fill='#37A000', outline='#999')

                globals()["tosplit_pi_%s" % entry_number] = self.list_canvas.create_image(
                    s_item[4] + 140, s_item[5], image=globals()["tosplit_pim_%s" % entry_number], anchor="center")

                canvas_mouse_el(self.list_canvas, globals()["tosplit_pirect_%s" % entry_number])
                canvas_mouse_el(self.list_canvas, globals()["tosplit_pi_%s" % entry_number])

                self.list_canvas.tag_bind(
                    globals()["tosplit_pirect_%s" % entry_number], "<Button-1>",
                    lambda e, order=self.sub_orders[entry_number-1]: \
                        self.view_split_pos(order)
                )

                self.list_canvas.tag_bind(
                    globals()["tosplit_pi_%s" % entry_number], "<Button-1>",
                    lambda e, order=self.sub_orders[entry_number-1]: \
                        self.view_split_pos(order)
                )

        self.list_paned.add(self.list_canvas)

    def view_split_pos(self, order):
        ViewSplitPosInvoice(self, order=self.order, bill=self.bill, sub_order=order)
