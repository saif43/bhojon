
import os, datetime, requests, _help
import sys
from tkinter import messagebox

from dev_help.tooltip import ToolTip
from dev_help.widgets import *
from ntk.objects import gv as gv
from dev_help.calculator import Calculator
from order.snippets.listacoritem import FoodItemData
from order.snippets.addtocart import AddToCart
from order.snippets.place import PlaceOrder
from PIL import Image, ImageTk

from ntk import SelectBox, Button


from database.table import (
            CustomerInfo,
            CustomerType,
            Employee,
            FoodCategory,
            Food,
            Tables,
            Varient,
            FoodAvailablity,
            AddOn,
            AddOnAsign,
            ThirdPartyCustomer
    )


def get_order_cart(self):
    self.cart_canvas.delete('all')
    self.cart_canvas.config(cursor='arrow')
    self.ci_row = 1
    self.w = w = self.cart_canvas.winfo_width() / 524

    self.xy = [ 
        [w*2, w*216],
        [w*216, w*272],
        [w*272, w*324],
        [w*324, w*410],
        [w*410, w*482],
        [w*482, w*524]
    ]

    self.ct_x = [w*6, w*244, w*320, w*368, w*476]

    ht_l = [
        ltext('item'), ltext('varient'),
        ltext('price'), ltext('quantity'), ltext('total')
    ]

    for i in self.xy:
        self.cart_canvas.create_rectangle(
                (i[0]), (self.ci_row * 32 - 16),
                (i[1]), (self.ci_row * 32 + 16), outline='#e4e5e7'
            )

    for e, i in enumerate(ht_l):
        d = self.xy[e][1]-self.xy[e][0]
        self.cart_canvas.create_text(
                self.xy[e][0]+(d/2), self.ci_row*32,
                text=('{}'.format(ht_l[e])), font=('Calibri', 10, 'bold'),
                anchor='center', fill='#374767', width=d 
            )

    self.ci_row += 1

    if len(gv.cart_data) > 0:
        mmin_img_p = os.path.join(gv.fi_path, "cus", 'minus-7-24.png')
        pmin_img_p = os.path.join(gv.fi_path, "cus", 'plus-24.png')
        dmin_img_p = os.path.join(gv.fi_path, "cus", 'delete-2-24.png')

        for i_key, i_data in gv.cart_data.items():
            if i_data.get('quantity') > 0:

                globals()['d_icon_{}'.format(self.ci_row)] = PhotoImage(file=mmin_img_p).subsample(2, 2)

                globals()['i_icon_{}'.format(self.ci_row)] = PhotoImage(file=pmin_img_p).subsample(2, 2)

                globals()['del_icon_{}'.format(self.ci_row)] = PhotoImage(file=dmin_img_p).subsample(2, 2)

                text = (
                    i_data.get('title')[0:56] +
                    ('...' if len(i_data.get('title')) > 56 else '')
                ).capitalize()

                w = self.w

                ct_t = [
                    [text, 'w'],
                    [
                        i_data.get('size')[0:7] +
                        ('..' if len(i_data.get('size')) > 7 else ''),
                        'center'
                    ],
                    [int(i_data.get('price')), 'e'],
                    [i_data.get('quantity'), 'center'],
                    [int(i_data.get('total')), 'e']
                ]

                for i in self.xy:
                    self.cart_canvas.create_rectangle(
                                        (i[0]), (self.ci_row * 32 - 16),
                                        (i[1]), (self.ci_row * 32 + 16),
                                        outline='#e4e5e7'
                                    )

                for e, i in enumerate(self.ct_x):
                    self.cart_canvas.create_text(
                                        i, (self.ci_row * 32),
                                        text=('{}'.format(ct_t[e][0])),
                                        font=('Calibri', 10, 'bold'),
                                        anchor=ct_t[e][1], fill='#374767',
                                        width=(self.ct_x[(e + 1 - e)])
                                    )

                bt_l = [
                    [
                        'cdi', (w*328), (w*344), (w*336),
                        globals()['d_icon_%s'%self.ci_row], 'cdim', 1, 0, 0
                    ],
                    [
                        'cii', (w*392), (w*408), (w*400),
                        globals()['i_icon_%s'%self.ci_row], 'ciim', 0, 1, 0
                    ],
                    [
                        'cci', (w*488), (w*504), (w*496),
                        globals()['del_icon_%s'%self.ci_row], 'ccim', 0, 0, 1
                    ]
                ]

                for bt in bt_l:
                    gv.gl['{}_{}'.format(bt[0], self.ci_row)] = self.cart_canvas.create_rectangle(
                                    bt[1], self.ci_row*32-10, bt[2],
                                    self.ci_row*32+10, outline='#37A000',
                                    fill="#F0F0F0"
                                )

                    gv.gl['{}_{}'.format(bt[5], self.ci_row)] = self.cart_canvas.create_image(
                                    bt[3], self.ci_row*32,
                                    image=bt[4], anchor='c'
                                )

                    canvas_mouse_el(
                                self.cart_canvas,
                                gv.gl['{}_{}'.format(bt[0],
                                self.ci_row)]
                            )

                    canvas_mouse_el(
                                self.cart_canvas,
                                gv.gl['{}_{}'.format(bt[5],
                                self.ci_row)]
                            )

                    for act in [bt[0], bt[5]]:
                        self.cart_canvas.tag_bind(
                                gv.gl['{}_{}'.format(act, self.ci_row)],
                                '<Button-1>', lambda event, \
                                id_=i_data.get('menu_id'), \
                                vid_=i_data.get('variant_id'), \
                                dec=bt[6], inc=bt[7], delt=bt[8]: \
                                AddToCart(
                                    self, action=True, id_=id_, \
                                    decrease=dec, increase=inc, delete=delt, vid_ = vid_   # Change
                                )
                            )

                self.ci_row = self.ci_row + 1

                if len(i_data.get('addons')) > 0:
                    for ao_key, ao_data in i_data.get('addons').items():
                        if ao_data.get('qnty') > 0:
                            ct_t = [
                                [ao_data.get('title'), 'w'],
                                ['', 'center'],
                                [int(ao_data.get('price')), 'e'],
                                [int(ao_data.get('qnty')), 'center'],
                                [int(ao_data.get('total')), 'e']
                            ]

                            for i in self.xy:
                                self.cart_canvas.create_rectangle(
                                            (i[0]), (self.ci_row * 32 - 16),
                                            (i[1]), (self.ci_row * 32 + 16),
                                            outline='#e4e5e7'
                                        )

                            for e, i in enumerate(self.ct_x):
                                self.cart_canvas.create_text(
                                            i, (self.ci_row * 32),
                                            text=('{}'.format(ct_t[e][0])),
                                            font=('Calibri', 9, 'bold'),
                                            anchor=ct_t[e][1], fill='#374767',
                                            width=(self.ct_x[(e + 1 - e)])
                                        )

                            self.ci_row = self.ci_row + 1

                y2 = gv.h(472)
                if (self.ci_row+2)*32 >= y2:
                    y2 = (self.ci_row+2)*32

                self.cart_canvas.config(scrollregion=[0, 0, gv.w(488), y2])

                if self.update:
                    self.update_order_button.focus_set()
                else:
                    self.place_order_button.focus_set()



    else:
        self.cart_canvas.delete('all')

        self.cart_canvas.config(scrollregion=[0,0,0,gv.w(472)])

        self.cempty = ImageTk.PhotoImage(
                                Image.open(
                                    os.path.join(
                                        gv.fi_path, 'cus', 'empty_op.png'
                                    )
                                ).resize(
                                    (gv.h(96),gv.h(96)),
                                    Image.ANTIALIAS
                                )
                            )

        self.cart_canvas.create_image(
                                gv.w(488)/2, gv.h(472)/2,
                                image=self.cempty, anchor='center'
                            )


def get_controller_count_content(this, self, frame, width, font, row, column):
    self.SubtotalVar = DoubleVar()
    self.VatVar = DoubleVar()
    self.ServiceChargeVar = DoubleVar()
    self.DiscountVar = DoubleVar()
    self.GrandTotalVar = DoubleVar()
    self.VatText = StringVar()
    self.GrandTotalText = StringVar()

    self.ServiceChargeVar.set(gv.st['service_charge'])
    self.VatText.set('0')
    self.GrandTotalText.set('0')

    try:
        if self.__class__.__name__ == "EditOrder":
            disc = self.bill['discount']
            serv = self.bill['service_charge']
            self.DiscountVar.set(disc)
            self.ServiceChargeVar.set(serv)
        else:
            self.DiscountVar.set(0)
            self.ServiceChargeVar.set(0)
    except Exception as e:
        exception_message = str(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        gv.error_log(str('Raised error due to ' + (f"An Exception Occured. \n Exception Type: {str(exception_type)}. Arguments: [{exception_message}]. File Name: {filename}, Line no: {exception_traceback.tb_lineno}")))




    self.vat_label = get_a_label(
                                        frame, text=(ltext('vat')) + '%',
                                        row=3, padx=(5, 15),
                                        pady=0, ignore_ttk=True
                                    )

    self.vat = get_a_entry(
                                        frame, textvariable=self.VatText,
                                        width=16, row=3, column=1, pady=0,
                                        padx=(5, 5), use_ttk=False
                                    )

    self.service_charge_label = get_a_label(
                                        frame, text=(ltext('service_charge')) +
                                        (' %' if gv.st['service_chargeType'] else ''),
                                        row=3, padx=(5, 15), pady=0,
                                        column=3, ignore_ttk=True
                                    )

    self.service_charge = get_a_entry(
                                        frame, textvariable=(self.ServiceChargeVar),
                                        width=16, row=3, column=4, columnspan=2,
                                        pady=0, padx=(5, 5), use_ttk=False
                                    )

    self.discount_label = get_a_label(
                                        frame, text=(ltext('discount')) +
                                        (' %' if gv.st['discount_type'] else ''),
                                        row=4, padx=(5, 15),
                                        pady=0, ignore_ttk=True
                                    )

    self.discount = get_a_entry(
                                        frame, textvariable=(self.DiscountVar),
                                        width=16, row=4, column=1,
                                        columnspan=2, pady=0,
                                        padx=(5, 5), use_ttk=False
                                    )

    self.grand_total_label = get_a_label(
                                        frame, text=(ltext('grand_total')),
                                        row=4, column=3, padx=(5, 15),
                                        pady=0, ignore_ttk=True
                                    )

    self.grand_total = get_a_entry(
                                        frame, textvariable=self.GrandTotalText,
                                        width=20, row=4, column=4,
                                        pady=0, padx=(5, 5), use_ttk=False
                                    )

    ToolTip(self.vat, ltext('vat_auto_counted'))
    ToolTip(self.service_charge, ltext('service_charge_amount'))
    ToolTip(self.discount, ltext('discount_amount'))
    ToolTip(self.grand_total, ltext('grand_total_auto_counted'))

    for key, value in frame.children.items():
        if key.startswith('!label'):
            value.config(
                background='#FFFFFF', width=w(14),
                fg='#374767', font=('Calibri', 10, 'bold')
            )

    for item in (self.vat, self.grand_total):
        item.config(readonlybackground='#FFFFFF', state='readonly')

    for item in (self.service_charge, self.discount, self.vat, self.grand_total):
        item.config(justify='center', font=('Calibri', w(13), 'bold'), bd=0)


def get_controller_button_content(this, self, frame, width, \
                                font, row, column, \
                                update=False, order=None):

    def place_order_button_callback(quick=False):
        if update and order:
            PlaceOrder(this, self, update=update, order=order)
        else:
            if quick:
                PlaceOrder(this, self, quick_order=True)
            else: PlaceOrder(this, self)

    if this.update:
        self.update_order_button = Button(
                                frame, text=(ltext('update_order')),
                                pady=(12, 12), padx=(8, 12),
                                ipady=15
                            )

        self.update_order_button.config(
                                command=place_order_button_callback
                            )

    else:
        def cancel_order_button_callback():
            clear(this, self)

        def calculator_button_callback():
            if self.calculator_toplevel: return

            self.calculator_toplevel = Toplevel(frame)

            self.calculator_window = Calculator(
                                            self.calculator_toplevel,
                                            realself=self
                                        )

        icon_obj = Image.open(
                                            os.path.join(
                                                gv.fi_path, "cus", 'calculator-8-48.png'
                                            )
                                        )

        icon_obj.thumbnail((48, 48), Image.ANTIALIAS)
        self.calculator_icon = ImageTk.PhotoImage(image=icon_obj)

        self.place_order_button = Button(
                                            frame, text=(ltext('place_order')),
                                            row=row, column=(column + 4),
                                            pady=0, padx=(12, 8),
                                            ipadx=0, ipady=4, width=12, height=1,
                                            font=('Calibri', 14), bd=2
                                        )

        self.quick_order_button = Button(
                                            frame, text=(ltext('quick_order')),
                                            row=row, column=(column + 3),
                                            pady=0, padx=(12, 12),
                                            ipadx=0, ipady=4, width=12, height=1,
                                            font=('Calibri', 14),
                                            bg='#3A95E4', bd=2
                                        )

        self.cancel_order_button = Button(
                                            frame, text=(ltext('cancel_order')),
                                            row=row, column=(column + 2),
                                            pady=0, padx=(12, 12),
                                            ipadx=0, ipady=4, width=12, height=1,
                                            font=('Calibri', 14), bg='red', bd=2
                                        )

        self.calculator_button = get_a_button(
                                            frame, width=0, row=row,
                                            relief=FLAT, column=(column + 1),
                                            pady=0, padx=(7, 0), ipadx=0,
                                            ipady=0, use_ttk=False,
                                            bg='#FFFFFF'
                                        )

        self.calculator_button.config(
                                text='', image=(self.calculator_icon),
                                compound='center', activebackground='#FFFFFF',
                                command=calculator_button_callback
                            )

        self.quick_order_button.config(
                                command=lambda : \
                                place_order_button_callback(quick=True)
                                # messagebox.showinfo('Your Order placed successfully')

                            )

        self.place_order_button.config(command=place_order_button_callback)
        self.cancel_order_button.config(command=cancel_order_button_callback)


def get_user_staf_table_content(this, self, frame):
    globals()['staffs_choices'] = [
                        r['first_name'] for r in \
                        Employee().qset.filter(search='first_name').all()
                    ]

    globals()['table_choices'] = [
                        r['tablename'] for r in \
                        Tables().qset.filter(search='tablename').all()
                    ]

    globals()['cust_choices'] = [
                        r['customer_name'] for r in \
                        CustomerInfo().qset.filter(search='customer_name').all()
                    ]

    globals()['custtyp_choices'] = [
                        r['customer_type'] for r in \
                        CustomerType().qset.filter(search='customer_type').all()
                    ]

    globals()['customer'] = CustomerInfo().qset.filter(id=1).first()

    if globals()['customer']: self.Customer.set(
                                    globals()['customer']['customer_name']
                                )

    globals()['customer_type'] = CustomerType().qset.filter(id=1).first()

    if globals()['customer_type']: self.CustomerType.set(
                                    globals()['customer_type']['customer_type']
                                )

    if globals()['staffs_choices']: self.Waiter.set(
                                    globals()['staffs_choices'][0]
                                )

    if globals()['table_choices']: self.Table.set(
                                    globals()['table_choices'][0]
                                )

    self.CookingTime.set('00:00')

    self.l_tn = None
    self.tn_c = None
    self.l_st_n = None
    self.sn_c = None
    self.un_c = None
    self.ut_c = None
    self.l_dc_n = None
    self.ckt_c = None
    self.dc_c = None
    self.c_c = None
    self.dc_n = None

    def toggle_customer_type(e=None):
        if self.l_tn: self.l_tn.destroy()
        if self.tn_c: self.tn_c.frame_master.destroy()
        if self.l_st_n: self.l_st_n.destroy()
        if self.sn_c: self.sn_c.frame_master.destroy()
        if self.l_dc_n: self.l_dc_n.destroy()
        if self.dc_c: self.dc_c.frame_master.destroy()
        if self.ckt_c: self.ckt_c.destroy()
        if self.dc_n: self.dc_n.destroy()
        if self.c_c: self.dc_c.frame_master.destroy()

        ct_ix = globals()['custtyp_choices'].index(self.CustomerType.get())

        if ct_ix != 1 and ct_ix != 2 and ct_ix != 3:
            self.l_ckt = get_a_label(
                            frame, column=2, text=ltext('time') +
                            ('*' if gv.pst['cooktime'] else ''), padx=4
                        )

            self.ckt_c = get_a_entry(
                            frame, width=16, column=3,
                            padx=0, textvariable=self.CookingTime
                        )

            self.ckt_c.bind('<Button-1>', lambda e: show_clock(e, self.ckt_c))
            self.ckt_c.config(state='readonly')

            self.l_tn = get_a_label(
                            frame, text=ltext('table') +
                            ('*' if gv.pst['tableid'] else ''),
                            row=1, column=2, padx=4
                        )

            self.tn_c = SelectBox(
                            frame, width=16, row=1, column=3,
                            padx=0, values=globals()['table_choices'], pady=10
                        )

            self.tn_c.config(textvariable=self.Table)

            self.l_st_n = get_a_label(
                            frame, text=ltext('waiter') +
                            ('*' if gv.pst['waiter'] else ''),
                            row=1, padx=4
                        )

            self.sn_c = SelectBox(
                            frame, width=16, row=1, column=1,
                            values=globals()['staffs_choices'], padx=0, pady=10
                        )

            self.sn_c.config(textvariable=self.Waiter)

        elif ct_ix == 2:
            comp_chs = [
                    r['company_name'] for r in \
                    ThirdPartyCustomer().qset.filter(search='company_name').all()
                ]

            self.l_dc_n = get_a_label(frame, text=ltext('company') + '*', column=2, padx=4)
            self.dc_c = SelectBox(frame, width=16, column=3, values=comp_chs, padx=0, pady=10)

            self.dc_n = get_a_label(frame, text=ltext('ThirdPartyID'), row=1, column=0, padx=2)
            self.c_c = SelectBox(frame, width=8, row=1, column=1, values=" ", height=10, padx=0, pady=10)




            self.dc_c.config(textvariable=self.DelivaryCompany)

        elif ct_ix == 1 or ct_ix == 3:
            self.l_ckt = get_a_label(
                    frame, column=2, text=ltext('time') +
                    ('*' if gv.pst['cooktime'] else ''), padx=4
                )
        

            self.ckt_c = get_a_entry(
                    frame, width=16, column=3, padx=0,
                    textvariable=self.CookingTime
                )

            self.ckt_c.bind('<Button-1>', lambda e: show_clock(e, self.ckt_c))
            self.ckt_c.config(state='readonly')

            self.l_st_n = get_a_label(
                    frame, text=ltext('waiter') +
                    ('*' if gv.pst['waiter'] else ''),
                    row=1, padx=4
                )

            # self.sn_c = gv.choice_dropdown(self, frame=frame, width=24, row=1, padx=0, dic=(globals()['staffs_choices']), entry=False)

            self.sn_c = SelectBox(
                    frame, width=16, row=1, column=1,
                    values=globals()['staffs_choices'], padx=0, pady=10
                )

            self.sn_c.config(textvariable=(self.Waiter))

        for key, value in frame.children.items():
            if key.startswith('!label'):
                value.config(
                        background='#FFFFFF', foreground='#374767',
                        font=('Calibri', gv.w(10), 'bold')
                    )

    self.l_ut = get_a_label(frame, text=ltext('type') + '*', padx=4)
    # self.ut_c = gv.choice_dropdown(self, frame=frame, width=24, column=0, padx=0, dic=(globals()['custtyp_choices']), entry=False, sticky='w', current=True, readonly=True)

    self.ut_c = SelectBox(
                        frame, width=16, column=1,
                        values=globals()['custtyp_choices'],
                        padx=0, selectcommand=lambda: toggle_customer_type(), pady=10
                    )

    self.ut_c.config(textvariable=(self.CustomerType))
    self.ut_c.bind('<<ComboboxSelected>>', lambda e: toggle_customer_type(e))

    toggle_customer_type()

    for key, value in frame.children.items():
        if key.startswith('!label'):
            value.config(
                        background='#FFFFFF', foreground='#374767',
                        font=('Calibri', gv.w(10), 'bold')
                    )

    if this.order:
        table = Tables().qset.filter(
                                tablename=this.order['table_no']
                            ).first()

        if table: self.Table.set(table['tablename'])

        customer = CustomerInfo().qset.filter(
                                id=this.order['customer_id']
                            ).first()

        if customer: self.Customer.set(customer['customer_name'])

        customer_type = CustomerType().qset.filter(
                                id=this.order['customer_type']
                            ).first()

        if customer_type: self.CustomerType.set(customer_type['customer_type'])

        waiter = Employee().qset.filter(
                                id=this.order['waiter_id']
                            ).first()

        if waiter: self.Waiter.set(waiter['first_name'])

        thirdparty = ThirdPartyCustomer().qset.filter(
                                id=this.order['isthirdparty']
                            ).first()

        if thirdparty: self.DelivaryCompany.set(thirdparty['company_name'])

        self.CookingTime.set(this.order['cookingtime'])


def get_category_list_content(this, self, canvas, frame, categories=None):
    ci = 1

    def upc(sel, e=None):
        self.CatCombo.set(sel)
        gv.update_posfood_canvas(event=e, entry=self.Search, select=self.CatCombo)

    if not categories: categories = [
                        r['Name'] for r in FoodCategory().qset.filter(
                                        search='Name', CategoryIsActive=1
                                    ).all()


                    ]

    if categories:
        categories = ['All'] + categories

        for ix, cat in enumerate(categories):
            globals()['cbr%s'%ix] = canvas.create_rectangle(
                                    w(5), (ci*h(25))-h(12), w(101),
                                    (ci*h(25))+h(12), outline='#D4EAC8',
                                    fill='#37A000'
                                )

            globals()['cb%s'%ix] = canvas.create_text(
                                    w(50), ci*h(25), text='{}'.format(cat),
                                    width=w(88), anchor='center',
                                    font=('Calibri', 11, 'bold'),
                                    fill='#FFFFFF'
                                )

            canvas_mouse_el(canvas, globals()['cbr%s'%ix])
            canvas_mouse_el(canvas, globals()['cb%s'%ix])

            canvas.tag_bind(
                        globals()['cbr%s'%ix], "<Button-1>",
                        lambda e, cat=cat if cat != 'All' else '': upc(sel=cat)
                    )

            canvas.tag_bind(
                        globals()['cb%s'%ix], "<Button-1>",
                        lambda e, cat=cat if cat != 'All' else '': upc(sel=cat)
                    )

            ci = ci + 1

            canvas.config(scrollregion=[0,0,w(102),ci*h(26)])

        if canvas.winfo_height() > ci*h(26):
            canvas.create_rectangle(
                w(5), (ci * h(25)) - h(12),
                w(101), canvas.winfo_height(),
                outline='#FFFFFF', fill='#FF  FFFF'
            )

            canvas.config(scrollregion=[0, 0, w(102), canvas.winfo_height()])


def food_item_data(self, event=None, product=None, search_select=False):
    if search_select:
        product = Food().qset.filter(ProductName=self.search_field.get()).first()

    if not product:
        return

    variants = Varient().qset.filter(menuid=product['id']).all()

    if not variants:
        return

    add_ons = AddOnAsign().qset.filter(menu_id=product['id']).all()

    if add_ons or product['is_customqty'] or len(variants)>1:
        if self.food_item_data_toplevel:
            self.food_item_data_toplevel.destroy()

        self.food_item_data_window = FoodItemData(
                                self, product, variants
                            )

    else:
        variant = variants[0]
        add = check_stock(product)

        if add:
            data = {
                'quantity': 1.,
                'addons': {},
                'menu': product,
                'variant': variant
            }

            AddToCart(self, data)


def get_food_item_frame_content(this, self, canvas, cart_frame, products=None):
    canvas.delete('all')

    self.food_list = []
    row, column = (1, 0)
    self.cart_item_row = 1
    canv_w = gv.device_width / 100 * 81 - 100
    max_col = int(canv_w / 160)
    x_distance = canv_w // max_col

    canvas_button_x1,\
    canvas_button_y1,\
    canvas_button_x2,\
    canvas_button_y2,\
    canvas_button_text_y,\
    canvas_button_image_y,\
    row,\
    column = ( 0, 0, x_distance, 132, 108, 47, 0, 0)

    # if variants is None:
    #     variants = Varient().qset.all()

    if products is None:
        products = Food().qset.filter(ProductsIsActive=1).all()

    if len(products) > 0:
        attf = 0

        for product in products:
            if canvas_button_x2 > int(gv.device_width / 100 * 61) - 126:
                canvas_button_x1,\
                canvas_button_x2,\
                canvas_button_y1,\
                canvas_button_y2 = (
                        0, x_distance, canvas_button_y1 + 132,
                        canvas_button_y2 + 132
                    )

                canvas_button_text_y,\
                canvas_button_image_y = (
                        canvas_button_text_y + 132,
                        canvas_button_image_y + 132
                    )

                row = row + 1
                column = 0

            item_food = product

            if item_food:
                sold = True
                favail = FoodAvailablity().qset.filter(
                            foodid=item_food['id']
                        ).first()

                if favail:
                    sold = False
                    hms = datetime.datetime.now()
                    h, m, s = hms.strftime('%H-%M-%S').split('-')
                    wday = datetime.datetime.today().strftime('%A')

                    if wday in favail['availday']:
                        st, et = favail['availtime'].split('-')
                        sth, stm, sts = st.split(':')
                        eth, etm, ets = et.split(':')

                        sd, ed = (
                                    hms.replace(
                                            hour=(int(sth)),
                                            minute=(int(stm)),
                                            second=(int(sts))),
                                    hms.replace(
                                            hour=(int(eth)),
                                            minute=(int(etm)),
                                            second=(int(ets))
                                    )
                                )

                        if hms > sd and hms < ed:
                            sold = True

                if sold:
                    attf = 1

                    globals()['food_item_image_{}'.format(product['id'])] = None

                    try:
                        if item_food['ProductImage'] != "" and \
                         "application/modules/itemmanage/assets/images" in \
                          item_food['ProductImage']:

                            path = os.path.join(
                                        gv.file_dir, item_food['ProductImage']
                                    )
                        else:
                            path = os.path.join(
                                        gv.file_dir, "application", "modules",
                                        "itemmanage", "assets", "img",
                                        "default.jpg"
                                    )

                        fn_path = path.rsplit('.', 1)[0]
                        ppm_path = fn_path + '.ppm'

                        if not os.access(ppm_path, os.F_OK):
                            try:
                                img = Image.open(path)

                                imgrs = img.resize(
                                                (96, 64), Image.ANTIALIAS
                                            )

                                imgrs.save(ppm_path, 'ppm')

                            except:
                                try:
                                    png_path = fn_path + '.png'

                                    img = Image.open(path)

                                    img.save(png_path, 'png')

                                    imgpng = Image.open(png_path)

                                    imgrs = img.resize(
                                                    (96, 64), Image.ANTIALIAS
                                                )

                                    imgrs.save(ppm_path, 'png')
                                except: pass

                        globals()['food_item_image_{}'.format(product['id'])] \
                         = ImageTk.PhotoImage(file=ppm_path)

                    except Exception as e:
                        gv.error_log(str(e))
                        globals()['food_item_image_{}'.format(product['id'])]  = None

                    globals()['food_img_rect_{}'.format(item_food['id'])] = canvas.create_rectangle(
                                        (canvas_button_x1 + 8),
                                        (canvas_button_y1 + 8),
                                        canvas_button_x2,
                                        (canvas_button_y2 - 47),
                                        outline='#BFBFBF', fill='#FFFFFF'
                                    )

                    globals()['food_txt_rect_{}'.format(item_food['id'])] = canvas.create_rectangle(
                                        (canvas_button_x1 + 8),
                                        (canvas_button_y1 + 86),
                                        canvas_button_x2,
                                        canvas_button_y2,
                                        outline='#BFBFBF', fill='#FAFAFA'
                                    )

                    text = '{}'.format(
                        item_food['ProductName'][0:30] +
                        ('...' if len(item_food['ProductName']) > 30 else ''),
                        # product['variantName'][0:7] +
                        # ('..' if len(product['variantName']) > 7 else '')
                    )

                    globals()['food_text_{}'.format(item_food['id'])] = canvas.create_text(
                        (canvas_button_x1 + 30),
                        canvas_button_text_y,
                        text=('{}'.format(text)), width=112,
                        anchor='w', font=('Calibri', 10, 'bold'), justify=('center'), 
                        fill='#374767'
                    )

                    if globals()['food_item_image_{}'.format(product['id'])]:
                        globals()['food_image_{}'.format(item_food['id'])] = canvas.create_image(
                            (canvas_button_x1 + \
                            int(canvas_button_x2 - canvas_button_x1) / 2 + \
                            3), canvas_button_image_y, \
                            image=globals()['food_item_image_{}'.format(
                                product['id']
                            )]
                        )

                        canvas.tag_bind(globals()['food_image_{}'.format(\
                                    item_food['id'])], '<Button-1>', \
                                    lambda event, product=product: \
                                    food_item_data(self, event, product)
                                )

                        canvas_mouse_el(
                            canvas,
                            globals()['food_image_{}'.format(item_food['id'])]
                        )

                    canvas.tag_bind(
                            globals()['food_img_rect_{}'.format(
                                item_food['id']
                            )],
                            '<Button-1>', lambda event, product=product: \
                            food_item_data(self, event, product)
                        )

                    canvas.tag_bind(
                            globals()['food_txt_rect_{}'.format(
                                item_food['id']
                            )],
                            '<Button-1>', lambda event, product=product: \
                            food_item_data(self, event, product)
                        )

                    canvas.tag_bind(
                            globals()['food_text_{}'.format(
                                item_food['id']
                            )],
                            '<Button-1>', lambda event, product=product: \
                            food_item_data(self, event, product)
                        )

                    canvas_mouse_el(
                        canvas, globals()['food_img_rect_{}'.format(
                            item_food['id']
                        )]
                    )

                    canvas_mouse_el(
                        canvas, globals()['food_txt_rect_{}'.format(
                            item_food['id']
                        )]
                    )

                    canvas_mouse_el(
                        canvas, globals()['food_text_{}'.format(
                            item_food['id']
                        )]
                    )

                    canvas_button_x1,\
                    canvas_button_x2 = (
                            canvas_button_x1 + x_distance,
                            canvas_button_x2 + x_distance
                        )

                    column = column + 1

                    if (row + 1) * 148 + 8 > int(gv.device_height / 100 * 70):
                        canvas.config(
                            scrollregion=[
                                0, 0, 650, (row + 1) * 148 + 8
                            ]
                        )

                    if (row + 1) * 148 + 8 < int(gv.device_height / 100 * 70):
                        canvas.config(
                            scrollregion=[
                                0, 0, 650, int(gv.device_height / 100 * 70)
                            ]
                        )

    if len(products) == 0 or not attf:
        canvas.create_text(
                    gv.w(740)/2, (gv.h(550)/2)+84,
                    # text='{}'.format(
                    #     ltext('no_product_found')
                    # ),
                    width=gv.w(745), anchor='center',
                    font=('Calibri', gv.h(14), 'bold'),
                    fill='#374767'
                )

        canvas.config(scrollregion=[0,0,0,gv.w(550)])

        self.fvempty = ImageTk.PhotoImage(
                                Image.open(
                                    os.path.join(
                                        gv.fi_path, 'cus', 'search_op.png'
                                    )
                                ).resize(
                                    (gv.h(72),gv.h(72)),
                                    Image.ANTIALIAS)
                                )

        canvas.create_image(
                    gv.w(745)/2, gv.h(550)/2,
                    image=self.fvempty, anchor='center'
                )


def search_for_food(this, self, event=None, entry=None, select=None):
    if select:
        if select != '':
            self.CatCombo.set(select)
    gv.update_posfood_canvas(event, self.Search, self.CatCombo)


def get_search_frame_content(this, self, frame):
    self.Search = StringVar()
    self.CatCombo = StringVar()

    img_path = os.path.join(gv.fi_path, 'cus', 'search-9-24.png')
    img = Image.open(img_path)
    img.thumbnail((32, 32), Image.ANTIALIAS)
    img.save(img_path, 'png')
    self.search_icon = ImageTk.PhotoImage(file=img_path)

    vals = []
    # varns = Varient().qset.all()

    foods = Food().qset.filter(ProductsIsActive=1).all()

    # for vrn in varns:
    #     foods = Food().qset.filter(
    #                         id=vrn['menuid'], ProductsIsActive=1,
    #                         search='ProductName', sep='AND'
    #                     ).all()
    #
    #     for fd in foods:
    #         vals.append(
    #             '%s (%s %s%s)' %(
    #                 fd['ProductName'],
    #                 vrn['variantName'],
    #                 gv.st['curr_icon'],
    #                 vrn['price']
    #             )
    #         )

    for fd in foods:
        vals.append(fd['ProductName'])

    self.search_field = SelectBox(
                            frame, default="Search food",
                            selectcommand=lambda : \
                            food_item_data(
                                self, search_select=True),
                                values=vals, onclick='clean'
                            )

    self.search_field.config(bg='#F0F0F0', bd=0)

    # self.search_field.bind('<KeyRelease>', lambda event: self.search_field.show_selection(True))

    self.search_button = get_a_button(
                                frame, padx=0, column=2, pady=0,
                                width=gv.w(20), text='', ipady=2,
                                ipadx=16, use_ttk=False, bg='#FFFFFF'
                            )

    self.search_button.config(
                                image=self.search_icon, compound='center',
                                activebackground='#FFFFFF', command=lambda : \
                                gv.update_posfood_canvas(
                                    event=None, entry=self.Search,
                                    select=self.CatCombo
                                )
                            )

    w = gv.w(846) / 100
    self.topand_canvas.create_window(
                            3, 24, window=self.search_field.frame_master,
                            anchor='w', width=int(w*95), height=gv.h(32)
                        )

    self.topand_canvas.create_window(
                            int(w * 98), 24, window=self.search_button,
                            anchor='c', width=int(w*5), height=gv.h(32)
                        )


def check_stock(menu, quantity=0):
    add = True

    if gv.st['stock_validation']:
        # vnts = Varient().qset.filter(menuid=menu['id']).first()
        add = False

        # for v in vnts:
        it_ = gv.cart_data.get("item_{}".format(menu['id']))
        if it_ and it_ is not None:
            for variant in it_['variants']:
                quantity = quantity + variant["quantity"]

        data = {
            "foodid": str(menu['id']),
            "qty": str(quantity)
        }

        try:
            url = gv.website + "app/checkstock"
            r = requests.post(url, data=data)
            if r.json().get("status_code"):
                add = True

            else:
                _help.messagew(
                    root=gv.rest.master,
                    msg1=ltext("check_stock_before_sell"),
                    msg2=ltext("this_food_set_production_cost_per_unit_not_ready"),
                    error=True
                )

        except Exception as e:
            gv.error_log(str(e))
            add = False
            _help.messagew(
                root=gv.rest.master,
                msg1=ltext("check_stock_before_sell"),
                msg2=ltext("connection_problem"),
                error=True
            )

    return add


def clear(this, self):
    self.cart_canvas.delete('all')
    gv.cart_data = {}
    self.SubtotalVar.set(0)
    self.ServiceChargeVar.set(gv.st['service_charge'])
    self.DiscountVar.set(0)
    self.GrandTotalVar.set(0)
    self.VatText.set('0')
    self.GrandTotalText.set('0')
    self.Search.set('')
    self.Waiter.set('')
    self.Table.set('')
    self.CookingTime.set('00:15')

    
    if gv.st:
        vt = gv.st['vat']

        if vt:
            vt_a = self.SubtotalVar.get() / 100 * vt
            self.VatVar.set(vt_a)
        else: self.VatVar.set(0)

    else:
        self.VatVar.set(0)

    destroy_child(self.f_user_staff_table)

    get_user_staf_table_content(this, self, self.f_user_staff_table)
    get_order_cart(self)


gv.check_stock = check_stock
