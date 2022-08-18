import copy, _help

from ntk import Toplevel, PanedWindow, Frame, Label, Entry, Text, SelectBox, Button, gv, Canvas, Scrollbar
from database.table import CashCounter, CashRegister, CashRegisterPaymentHistory, PaymentMethod
from tkinter import DoubleVar
from datetime import datetime
import copy, requests

# gv.error_log(str(f"File: order/snippets/cashcounter.py"))

class OpenCashCounter(Toplevel):
    def __init__(self, *args, **kwargs):
        super(OpenCashCounter, self).__init__(width=672, height=340, title='New cash register', *args, **kwargs)

        # gv.error_log(str(f"self: {self} --> args: {args} --> kwargs: {kwargs}"))

        self.OpeningBalance = DoubleVar()
        self.structure_window()



    def structure_window(self):
        self.paned = PanedWindow(self, pady=10, padx=10)

        self.top_frame = Frame(self.paned, height=262)
        self.bottom_frame = Frame(self.paned, bg='bg-light')
        self.bottom_frame_right = Frame(self.bottom_frame, width=48, sticky='e')

        self.paned.add(self.top_frame)
        self.paned.add(self.bottom_frame)

        cashcounter_list = [c['counterno'] for c in CashCounter().qset.all()]

        self.counter_number_label = Label(
            self.top_frame, text='Counter Number', width=24, bg='#ffffff', case=False, font=('Calibri', 13))
        self.counter_number = SelectBox(
            self.top_frame, column=1, padx=5, boxbg='#ffffff', bg='#DDDDDD', values=cashcounter_list,
            default='Please select cash counter')

        self.opening_balance_label = Label(
            self.top_frame, row=1, text='Opening Balance', width=24, bg='#ffffff', case=False, font=('Calibri', 13))
        self.opening_balance = Entry(
            self.top_frame, row=1, column=1, padx=5, bd=0, font=('Calibri', 14), width=58,
            hlc='#ffffff', hlbg='#ffffff', bg='#DDDDDD', tvar=self.OpeningBalance
        )

        self.note_label = Label(
            self.top_frame, row=2, text='Opening Note', width=24, bg='#ffffff', case=False, font=('Calibri', 13))
        self.note = Text(
            self.top_frame, row=2, column=1, height=7, padx=8, width=224, bd=2, font=('Calibri', 13), bg='#DDDDDD')

        self.submit = Button(
            self.bottom_frame_right, text='Add Opening Balance', width=24, command=lambda: self.open_cash_counter())

    def open_cash_counter(self):
        date_today = datetime.now()
        web_response = None
        create_register = False

        try:
            url = gv.website + "app/checkregister"
            web_response = requests.post(url, data={'userid': gv.user_id, 'counter': self.counter_number.get()})
            web_response = web_response.json()
        except Exception as e:
            gv.error_log(str(e))
            web_response = {
                'data': {
                    "counterstatus": 0
                }
            }

        if web_response:
            data = web_response['data']
            if data.pop('counterstatus', 0) or int(data.pop('status', 1)) == 0:
                register = CashRegister().qset.create(
                    userid=gv.user_id, openclosedate=date_today.strftime('%Y-%m-%d'),
                    counter_no=self.counter_number.get(), opening_balance=self.OpeningBalance.get(),
                    opendate=date_today.strftime('%Y-%m-%d %H:%M:%S'),
                    openingnote=self.note.get(1.0, 'end'), status=1, returning='*'
                )

                register.pop('id')

                try:
                    url = gv.website + "app/cashregistersync"
                    r = requests.post(url, data={'cashinfo': [register]})
                except Exception as error:
                    pass

                self.close(register)
            elif data.pop('status', 0):
                register = CashRegister().qset.create(**data, returning='*')
                self.close(register)
            else:
                _help.messagew(msg1="Counter Register Error", msg2="Unable to register cash counter!", error=True)

    def close(self, register):
        gv.cash_counter = register
        self.destroy()
        gv.shortcut_commands['<Control-p>']['lambda'](None)


class CloseCashCounter(Toplevel):
    def __init__(self, *args, **kwargs):
        super(CloseCashCounter, self).__init__(width=700, height=448, title='Close cash register', *args, **kwargs)
        self.ClosingBalance = DoubleVar()
        self.structure_window()

    def structure_window(self):
        register_history = CashRegisterPaymentHistory().qset.filter(register_number=gv.cash_counter['id']).all()
        self.history_map = {}
        for history in register_history:
            if self.history_map.get(history['payment_method'], 0):
                self.history_map[history['payment_method']].append(history)
            else:
                self.history_map[history['payment_method']] = [history]

        self.paned = PanedWindow(self, pady=10, padx=10)

        self.payment_history_paned = PanedWindow(self.paned, height=156, orient='horizontal')
        self.top_canvas = Canvas(self.payment_history_paned, width=648, height=128)
        self.top_canvas_scroll = Scrollbar(self.payment_history_paned, self.top_canvas)
        self.payment_history_paned.add(self.top_canvas)
        self.payment_history_paned.add(self.top_canvas_scroll)

        self.top_frame = Frame(self.paned, height=172)
        self.bottom_frame = Frame(self.paned, bg='bg-light')
        self.bottom_frame_right = Frame(self.bottom_frame, width=48, sticky='e')

        self.paned.add(self.payment_history_paned)
        self.paned.add(self.top_frame)
        self.paned.add(self.bottom_frame)

        self.closing_balance_label = Label(
            self.top_frame, row=1, text='Closing Balance', width=18, bg='#ffffff', case=False, font=('Calibri', 13))
        self.closing_balance = Entry(
            self.top_frame, row=1, column=1, padx=5, bd=0, font=('Calibri', 14), width=48, pady=(10, 0),
            hlc='#ffffff', hlbg='#ffffff', bg='#DDDDDD', tvar=self.ClosingBalance)

        self.note_label = Label(
            self.top_frame, row=2, text='Closing Note', width=18, bg='#ffffff', case=False, font=('Calibri', 13))
        self.note = Text(
            self.top_frame, row=2, column=1, height=4, padx=8, pady=16,
            width=48, bd=2, font=('Calibri', 13), bg='#DDDDDD')

        canvas_item_list = [
            [0, 0, 216, 32, 'S.L'],
            [216, 0, 432, 32, 'Payment Type'],
            [432, 0, 648, 32, 'Total Amount']
        ]

        for item in canvas_item_list:
            self.top_canvas.create_rectangle(item[0], item[1], item[2], item[3], outline='#F1F1F1')
            self.top_canvas.create_text(
                item[0] + 12, item[1] + 16, fill='#374767', font=('Calibri', 13, 'bold'), anchor='w', text=item[4])

        total_sales_amount = 0
        item_number = 1

        if not len(self.history_map)>0:
            self.top_canvas.create_rectangle(0, 32, 648, 64, outline='#F1F1F1', fill='#F0F0F0')
            self.top_canvas.create_text(
                324, 48, fill='#374767', font=('Calibri', 10, 'bold'),
                anchor='center', text='Payment history not available.')
            item_number += 1
        else:
            for key, history in self.history_map.items():
                y1, y2 = item_number*32, (item_number+1)*32
                payment_type = PaymentMethod().qset.filter(id=key).first()

                sales_amount = sum(single['amount'] for single in history)

                canvas_item_list = [
                    [0, y1, 216, y2, item_number, 12, 'w'],
                    [216, y1, 432, y2, payment_type['payment_method'], 228, 'w'],
                    [432, y1, 648, y2, sales_amount, 636, 'e']
                ]

                total_sales_amount += sales_amount

                for item in canvas_item_list:
                    self.top_canvas.create_rectangle(item[0], item[1], item[2], item[3], outline='#F1F1F1')
                    self.top_canvas.create_text(
                        item[5], item[1] + 16, fill='#374767', font=('Calibri', 13), anchor=item[6], text=item[4])

                item_number += 1

        y1, y2, y3 = item_number*32, (item_number+1)*32, (item_number+2)*32

        canvas_item_list = [
            [0, y1, 432, y2, 'Total:'],
            [432, y1, 648, y2, total_sales_amount],
            [0, y2, 432, y3, 'Opening Balance:'],
            [432, y2, 648, y3, gv.cash_counter['opening_balance']]
        ]

        for item in canvas_item_list:
            self.top_canvas.create_rectangle(item[0], item[1], item[2], item[3], outline='#F1F1F1')
            self.top_canvas.create_text(
                item[2] - 12, item[1] + 16, fill='#374767', font=('Calibri', 13), anchor='e', text=item[4])

        self.top_canvas.config(scrollregion=[0, 0, 648, y3])

        self.ClosingBalance.set(total_sales_amount + gv.cash_counter['opening_balance'])

        self.submit = Button(
            self.bottom_frame_right, text='Add Closing Balance', width=24,
            command=lambda: self.close_cash_counter(), bg='bg-success')

    def close_cash_counter(self):
        cash_counter = copy.deepcopy(gv.cash_counter)

        cash_counter['closing_balance'] = self.ClosingBalance.get()
        cash_counter['closedate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cash_counter['closing_note'] = self.note.get(1.0, 'end')
        cash_counter['status'] = 0

        register = CashRegister().qset.update(**cash_counter, returning='*')

        register.pop('id')

        try:
            url = gv.website + "app/cashregistersync"
            r = requests.post(url, data={'cashinfo': [register]})
        except Exception as error:
            pass

        gv.cash_counter = []
        self.destroy()
        gv.shortcut_commands['<Control-p>']['lambda'](None)
