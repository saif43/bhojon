from ntk import Toplevel, Frame, Canvas, gv, PanedWindow, Scrollbar, SelectBox
from database.table import OrderItem, SubOrder, Food, AddOn, Varient
from dev_help.widgets import canvas_mouse_el, destroy_child
import json, _help, copy, os
from database.table import SubOrder, Bill, CustomerOrder
from pprint import pprint
from order.snippets.split_payment import OrderSplitPayment
from tkinter import PhotoImage

# gv.error_log(str(f"File: order/snippets/split.py"))

class SplitOrder:
    def __init__(self, order_kw, *args, **kwargs):
        super(SplitOrder, self).__init__(*args, **kwargs)

        # gv.error_log(str(f"self: {self} --> order_kw: {order_kw} --> args: {args} --> kwargs: {kwargs}"))

        if gv.split_order_window:
            gv.split_order_window.destroy()

        gv.split_order_window = self.master = Toplevel(width=972, height=480, title="Split Order")

        order = order_kw['order']
        self.order_menus = order_kw['order_menus']
        self.max_split = order_kw['max_split']

        self.sub_cart = {}
        self.menu_foods = {}
        self.menu_variants = {}
        self.sub_order_canvas = {}
        self.menu_assigned = {}

        self.chk_item = 0
        for x in self.order_menus:
            self.chk_item +=1
        
        self.split_session_order = SubOrder().qset.filter(order_id=order['id']).all()

        for id_x, sub_order in enumerate(self.split_session_order):
            try:
                order_menu_id = json.loads(sub_order['order_menu_id'])

                for menu_id, menu_info in order_menu_id.items():
                    menu_variant = '%s_%s' % (menu_id, menu_info['variant'])

                    if menu_variant in self.menu_assigned:
                        self.menu_assigned[menu_variant] += menu_info['quantity']
                    else:
                        self.menu_assigned[menu_variant] = menu_info['quantity']

                self.split_session_order[id_x]['order_menu_id'] = order_menu_id
            except: pass

        self.current_sub_order_canvas = None
        self.split_number_selector = None
        self.min_strict_sub_order = 0

        self.order = order

        self.paned = PanedWindow(self.master, orient='horizontal')
        self.left_frame = Canvas(self.paned, width=200, mousescroll=False, highlightbackground="#FFFFFF")
        self.left_frame_scroll = Scrollbar(self.paned, self.left_frame)
        self.right_frame = PanedWindow(self.paned)

        self.select_frame = Frame(self.right_frame)
        self.suborder_frame = Frame(self.right_frame)

        self.main_canvas = Canvas(self.suborder_frame, width=708, height=396, scrollregion=[0, 0, 676, 960])
        self.main_canvas_scroll = Scrollbar(self.suborder_frame, self.main_canvas)
        self.main_canvas_scroll_x = Scrollbar(
            self.suborder_frame, self.main_canvas,
            row=1, column=0, orient='horizontal', sticky='we'
        )

        self.right_frame.add(self.select_frame)
        self.right_frame.add(self.suborder_frame)

        self.paned.add(self.left_frame)
        self.paned.add(self.left_frame_scroll)
        self.paned.add(self.right_frame)

        self.load_foods()

        if self.split_session_order:
            self.load_sub_orders(self.split_session_order)

        self.structure_split_window()

    def load_sub_orders(self, sub_orders):

        # gv.error_log(str(f"self: {self} --> func: load_sub_orders | sub_orders: {sub_orders}"))

        self.split_session_order = []
        for sub_order in sub_orders:
            if type(sub_order['order_menu_id']) != dict:
                sub_order['order_menu_id'] = json.loads(sub_order['order_menu_id'])

            self.split_session_order.append(sub_order)

    def select_sub_order(self, e):
        canvas = e.widget

        # gv.error_log(str(f"self: {self} --> func: select_sub_order | sub_orders: {e}"))

        for key, value in self.sub_order_canvas.items():
            value_canvas = value['canvas']

            if value_canvas != canvas:
                value_canvas.config(bd=0, highlightbackground="#F1F1F1") #bg='#F1F1F1',
            else:
                value['key'] = key
                self.current_sub_order_canvas = value
                value_canvas.config(bd=2, highlightbackground="#37A000") #bg='#37A000',

    def add_item_to_sub_order(self, index, menu_id, variant_id, menu_item):

        # gv.error_log(str(f"self: {self} --> func: add_item_to_sub_order | index: {index} | menu_id: {menu_id} | variant_id{variant_id} | menu_item: {menu_item}"))

        counter = self.current_sub_order_canvas['counter']
        # gv.error_log(str(f"func: add_item_to_sub_order --> counter: {counter}"))
        if self.split_session_order[counter]['status'] in ['False', False, 0]:
            return

        item = globals()['sof_price_%s' % index]
        quantity = float(self.left_frame.itemcget(item, 'text'))

        # gv.error_log(str(f"func: add_item_to_sub_order --> quantity: {quantity} | left_frame: {self.left_frame}"))

        if self.current_sub_order_canvas and quantity > 0.0:
            this_order = self.split_session_order[counter]

            if type(this_order['order_menu_id']) != dict:
                this_order['order_menu_id'] = json.loads(this_order['order_menu_id'])

            previous_menu_item = this_order['order_menu_id']

            # gv.error_log(str(f"func: add_item_to_sub_order --> is_customqty: {menu_item['is_customqty']}"))

            if int(menu_item['is_customqty']):
                add_quantity = quantity
                left_quantity = 0.0
            else:
                add_quantity = 1
                left_quantity = quantity - 1.0

                assign_key = "%s_%s" % (menu_id, variant_id)
                self.menu_assigned[assign_key] = self.menu_assigned.get(assign_key, 0) + 1

            if previous_menu_item.get(str(menu_id), False):
                previous_menu_item[str(menu_id)]['quantity'] += add_quantity
            else:
                previous_menu_item[str(menu_id)] = {
                    'variant': variant_id,
                    'quantity': add_quantity
                }

            self.current_sub_order_canvas['result'] = previous_menu_item

            self.left_frame.itemconfig(item, text=f'{left_quantity:.2f}')

            # gv.error_log(str(f"func: add_item_to_sub_order --> is_customqty: {left_quantity}")) 
            self.single_sub_order_canvas(
                        self.sub_order_canvas['so_canvas_%s' % counter]['canvas'], this_order, counter)
        else:
            return

    def remove_item_from_sub_order(self, event, counter, menu):

        # gv.error_log(str(f"self: {self} --> func: remove_item_from_sub_order | index: {counter} | menu_id: {menu}"))

        session_sub_order = self.split_session_order[counter]

        variant_id = session_sub_order['order_menu_id'][str(menu)]['variant']
        menu_quantiy = session_sub_order['order_menu_id'][str(menu)]['quantity']
        session_sub_order['order_menu_id'].pop(str(menu))

        self.current_sub_order_canvas['result'] = session_sub_order['order_menu_id']
        self.menu_assigned["%s_%s" % (menu, variant_id)] -= menu_quantiy

        self.initial_sub_cart()
        self.load_foods()

    def load_foods(self):
        self.left_frame.delete('all')

        item_row = 1

        # gv.error_log(str(f"=============== func: load_foods ====================")) 
        for index, menu in enumerate(self.order_menus):

            # gv.error_log(str(f"index: {index} | menu: {menu}"))
 
            menu_id = menu['menu_id']
            variant_id = menu['varientid']

            food = Food().qset.filter(id=menu_id).first()
            variant = Varient().qset.filter(id=variant_id).first()

            self.menu_foods[menu_id] = food
            self.menu_variants[variant_id] = variant

            item_row_32 = item_row * 32

            globals()['sof_rect_%s' % index] = self.left_frame.create_rectangle(
                5, item_row_32 - 15, 198, item_row_32 + 15, fill="#FAFAFA", outline="#FFFFFF")

            globals()['sof_item_%s' % index] = self.left_frame.create_text(
                10, item_row_32, text=food['ProductName'][:24],
                font=('Calibri', 11, 'bold'), anchor='w', fill="#374767")

            globals()['sof_price_%s' % index] = self.left_frame.create_text(
                196, item_row_32, text=menu['menuqty'] - self.menu_assigned.get("%s_%s" % (menu_id, variant_id), 0),
                font=('Calibri', 11, 'bold'), anchor='e', fill="#374767")

            canvas_mouse_el(self.left_frame, globals()['sof_rect_%s' % index])
            canvas_mouse_el(self.left_frame, globals()['sof_item_%s' % index])
            canvas_mouse_el(self.left_frame, globals()['sof_price_%s' % index])

            self.left_frame.tag_bind(
                globals()['sof_rect_%s' % index], '<Button-1>',
                lambda e, ind=index, m_id=menu_id, v_id=variant_id,
                       menu_item=food: self.add_item_to_sub_order(ind, m_id, v_id, menu_item))

            self.left_frame.tag_bind(
                globals()['sof_item_%s' % index], '<Button-1>',
                lambda e, ind=index, m_id=menu_id, v_id=variant_id,
                       menu_item=food: self.add_item_to_sub_order(ind, m_id, v_id, menu_item))

            self.left_frame.tag_bind(
                globals()['sof_price_%s' % index], '<Button-1>',
                lambda e, ind=index, m_id=menu_id, v_id=variant_id,
                       menu_item=food: self.add_item_to_sub_order(ind, m_id, v_id, menu_item))

            self.left_frame.create_line(5, item_row_32 + 16, 198, item_row_32 + 16, fill='#374767')

            item_row += 1

        self.left_frame.config(scrollregion=[0, 0, 200, item_row * 32], height=item_row * 32)

    def order_sub_cart(self):
        sub_cart_demo = {
            'order_id': self.order['id'],
            'customer_id': self.order['customer_id'],
            'vat': 0,
            'discount': 0,
            's_charge': 0,
            'total_price': 0,
            'status': True,
            'order_menu_id': {},
            'adons_id': "",
            'adons_qty': '',
        }

        split_number_selected = self.split_number_selector.get()
        sub_cart = self.split_session_order
        exists_sub_order = len(sub_cart)

        # gv.error_log(str(f"exists_sub_order: {exists_sub_order} --> func: remove_item_from_sub_order | split_number_selected: {split_number_selected} | sub_cart: {sub_cart}"))

        # try:
        split_number = int(
            split_number_selected if split_number_selected != 'Select number of split' else exists_sub_order)

        if split_number > exists_sub_order:
            add_more = split_number - exists_sub_order
            for i in range(add_more):
                self.split_session_order.append(copy.deepcopy(sub_cart_demo))
        else:
            return

        for child in self.main_canvas.winfo_children():
            child.destroy()

        self.main_canvas.delete('all')

        self.initial_sub_cart()

        # except Exception as e:
        #     print(e)

    def initial_sub_cart(self):
        row_number = 0
        column_number = 0
        x_position, y_position = 0, 0

        for counter, sub_order in enumerate(self.split_session_order):
            x_position = (column_number * 356)
            y_position = (row_number * 306)

            canvas_number = 'so_canvas_%s' % counter
            globals()[
                '%s_fill' %canvas_number] = '#F1F1F1' if sub_order['status'] not in ['False', False, 0] else "#28A745"

            sub_order_canvas = Canvas(
                self.main_canvas, width=346, height=300,
                bg=globals()['%s_fill' %canvas_number])

            sub_order_canvas.bind('<Button-1>', lambda e: self.select_sub_order(e))

            self.main_canvas.create_window(
                x_position + 2, y_position + 2,
                window=sub_order_canvas, height=300, anchor='nw')

            total, vat, service_charge, grand_total = self.single_sub_order_canvas(
                                                                    sub_order_canvas, sub_order, counter)

            self.sub_order_canvas[canvas_number] = {
                'canvas': sub_order_canvas,
                'result': {},
                'counter': counter
            }

            column_number += 1

            if counter % 2 != 0:
                row_number += 1
                column_number = 0

        self.main_canvas.config(scrollregion=[0, 0, 710, y_position + 396])

    def single_sub_order_canvas(self, sub_order_canvas, sub_order_items, counter):
        sub_order_canvas.delete('all')

        total_price, vat, service_charge, grand_total = 0, 0, 0, 0

        sub_order_items_order_menu_id = sub_order_items['order_menu_id']

        item_row = 2
        canvas_number = 'so_canvas_%s' % counter
        fill_color = globals()['%s_fill' %canvas_number]

        item_props_ = [
            [0, 87, 'Item'], [87, 161, 'Variant Name'], [161, 229, 'Unit Price'],
            [229, 266, 'Qnty'], [266, 348, 'Total Price']
        ]

        for index, prop in enumerate(item_props_):
            sub_order_canvas.create_rectangle(
                prop[0], 0, prop[1], 42,
                fill=fill_color, outline='#DCDBD9')

            sub_order_canvas.create_text(
                prop[0] + ((prop[1] - prop[0]) / 2), 21,
                text=prop[2], width=prop[1]-(prop[0] + 3), font=('Calibri', 11, 'bold'))

        for menu_id, menu_info in sub_order_items_order_menu_id.items():

            food = Food().qset.filter(id=menu_id).first()
            variant = Varient().qset.filter(id=menu_info['variant']).first()

            sub_item_total = variant['price'] * menu_info['quantity']
            total_price += sub_item_total
            current_vat = (sub_item_total / 100) * gv.st['vat']
            vat += current_vat
            grand_total += (sub_item_total + current_vat)

            food_props_ = [
                [0, 87, food['ProductName'][:13]],
                [87, 161, variant['variantName'][:10]],
                [161, 229, variant['price']],
                [229, 266, menu_info['quantity']],
                [266, 332, sub_item_total]
            ]

            rect_y1 = (((item_row - 1) * 32) + 10)
            rect_y2 = ((item_row * 32) + 10)
            text_y = ((item_row * 32) - 6)

            for index, prop in enumerate(food_props_):
                sub_order_canvas.create_rectangle(
                    prop[0], rect_y1, prop[1],
                    rect_y2, fill=fill_color, outline='#DCDBD9')

                sub_order_canvas.create_text(
                    prop[0] + ((prop[1] - prop[0]) / 2), text_y,
                    text=prop[2], width=85, font=('Calibri', 10, 'bold'))

            if sub_order_items['status'] not in ['False', False, 0]:
                dmin_img_p = os.path.join(gv.fi_path, "cus", 'x-mark-24.png')
                image_name = 'split_del_icon_{}_{}_{}'.format(counter, menu_id, variant['id'])

                globals()[image_name] = PhotoImage(file=dmin_img_p).subsample(2, 2)

                globals()["%s_%s_del_rect" %(canvas_number, menu_id)] = sub_order_canvas.create_rectangle(
                    332, rect_y1, 348, rect_y2, fill='red', outline='#DCDBD9')

                globals()["%s_%s_del_img" %(canvas_number, menu_id)] = sub_order_canvas.create_image(
                    339, text_y, image=globals()[image_name])

                canvas_mouse_el(sub_order_canvas, globals()["%s_%s_del_rect" %(canvas_number, menu_id)])
                canvas_mouse_el(sub_order_canvas, globals()["%s_%s_del_img" % (canvas_number, menu_id)])

                sub_order_canvas.tag_bind(
                    globals()["%s_%s_del_rect" %(canvas_number, menu_id)], "<Button-1>",
                    lambda e, element=counter, menu=menu_id: \
                        self.remove_item_from_sub_order(e, element, menu)
                )

                sub_order_canvas.tag_bind(
                    globals()["%s_%s_del_img" % (canvas_number, menu_id)], "<Button-1>",
                    lambda e, element=counter, menu=menu_id: \
                        self.remove_item_from_sub_order(e, element, menu)
                )

            item_row += 1

        sub_order_footer_item = [
            ['Total', f'{total_price:.2f}'],
            ['Vat', f'{vat:.2f}'],
            ['Service Charge', f'{service_charge:.2f}'],
            ['Grand Total', f'{grand_total:.2f}']
        ]

        for ix, item in enumerate(sub_order_footer_item):
            sub_order_canvas.create_rectangle(
                0, (((item_row - 1) * 32) + 10), 196,
                ((item_row * 32) + 10), fill=fill_color, outline='#DCDBD9')

            sub_order_canvas.create_text(
                14, ((item_row * 32) - 6),
                text=item[0], width=346, font=('Calibri', 10, 'bold'), anchor='w')

            sub_order_canvas.create_rectangle(
                196, (((item_row - 1) * 32) + 10), 346,
                ((item_row * 32) + 10), fill=fill_color, outline='#DCDBD9')

            sub_order_canvas.create_text(
                336, ((item_row * 32) - 6),
                text=item[1], width=346, font=('Calibri', 10, 'bold'), anchor='e')

            item_row += 1

        if sub_order_items['status'] not in ['False', False, 0]:
            globals()['%s_payrect' % (counter)] = sub_order_canvas.create_rectangle(
                156, (((item_row - 1) * 32) + 18), 338,
                ((item_row * 32) + 24), fill='#37A000', outline='#DCDBD9')

            globals()['%s_paytext' % (counter)] = sub_order_canvas.create_text(
                247, (item_row * 32) + 5, fill="#FFFFFF",
                text="Pay now & Print invoice", width=186, font=('Calibri', 11, 'bold'), anchor='c')

            canvas_mouse_el(sub_order_canvas, globals()['%s_payrect' % (counter)])
            canvas_mouse_el(sub_order_canvas, globals()['%s_paytext' % (counter)])

            sub_order_canvas.tag_bind(
                        globals()['%s_payrect' % (counter)], "<Button-1>", lambda e, element=counter: \
                            self.pay_now_and_print_invoice(e, element)
                    )
            sub_order_canvas.tag_bind(
                        globals()['%s_paytext' % (counter)], "<Button-1>", lambda e, element=counter: \
                            self.pay_now_and_print_invoice(e, element)
                    )

            item_row += 1

        if (item_row * 32) < 300:
            sub_order_canvas.config(height=300, scrollregion=[0, 0, 346, 300])
        else:
            sub_order_canvas.config(height=item_row * 32, scrollregion=[0, 0, 346, item_row * 32])

        # gv.split_order_session['orders'][self.order['id']]['sub_orders'][counter] = \
        #                                                         self.split_session_order['sub_orders'][counter]
        #
        # gv.split_order_session['orders'][self.order['id']]['menu_assigned'] = self.menu_assigned

        sub_order_current = self.split_session_order[counter]
        sub_order_current['order_menu_id'] = json.dumps(sub_order_current['order_menu_id'])

        sub_order_current['total_price'] = total_price
        sub_order_current['vat'] = vat

        if 'id' in sub_order_current:
            SubOrder().qset.update(**sub_order_current, where="id")
        else:
            sub_order_created = SubOrder().qset.create(**sub_order_current)
            self.split_session_order[counter]['id'] = sub_order_created['id']

        sub_order_current['order_menu_id'] = json.loads(sub_order_current['order_menu_id'])

        self.load_foods()

        return total_price, vat, service_charge, grand_total
        # except Exception as e: print(e)

        # return total_price, vat, service_charge, grand_total

    def structure_split_window(self):
        max_split = self.max_split

        self.min_strict_sub_order = 0
        for counter, sub_order in enumerate(self.split_session_order):
            try:
                order_menu_id = sub_order['order_menu_id']
                if type(order_menu_id) != dict:
                    order_menu_id = json.loads(order_menu_id)

                    self.split_session_order[counter]['order_menu_id'] = order_menu_id

                for menu_id, menu_info in order_menu_id.items():
                    self.min_strict_sub_order += menu_info['quantity']
            except: pass

        min_split = 2 + self.min_strict_sub_order

        if self.split_number_selector:
            self.split_number_selector.destroy()

        if max_split > 1:
            self.split_number_selector = SelectBox(
                self.select_frame, width=56, height=24,
                values=['Select number of split', *[i for i in range(min_split, int(max_split + 1))]],
                selectcommand=lambda: self.order_sub_cart()
            )

        self.initial_sub_cart()

    def check_split(self):
        itemd = 0.0
        is_split = True
        for x in range(self.chk_item):
            item = globals()['sof_price_%s' % x]
            quantity = float(self.left_frame.itemcget(item, 'text'))
            # gv.error_log(str(f"********************************* {quantity} *********************************"))
            if quantity != 0.0:
                itemd += quantity
                is_split = False
        return is_split, itemd
                   
    def pay_now_and_print_invoice(self, event, counter):
        # gv.error_log(str(f"Total ********************************* COUTER {counter} *********************************"))
        

        # gv.error_log(str(f"********************************* {self.check_split()} *********************************"))
        is_split, item = self.check_split()
        if is_split:
            split_object = self.split_session_order[counter]

            # order_object = self.order
            order_object = CustomerOrder().qset.filter(id=self.order['id']).first()

            if not split_object['order_menu_id']:
                _help.messagew(msg1="Split Order", msg2="Please select at least one item!", error=True)
                return

            # order_object['customerpaid'] += split_object['total_price']
            customer_order = CustomerOrder().qset.update(**order_object, where='id', returning='*')

            split_object['status'] = False

            # gv.error_log(str(f"Sub Order ID:  {split_object['id']} Status: {split_object['status']}"))

            split_object['order_menu_id'] = json.dumps(split_object['order_menu_id'])
            sub_order_updated = SubOrder().qset.update(**split_object, where='id', returning='*')

            sub_order_updated['order_menu_id'] = json.loads(sub_order_updated['order_menu_id'])
            self.split_session_order[counter] = sub_order_updated

            self.initial_sub_cart()

            dd = OrderSplitPayment(customer_order, sub_order_updated)
            # gv.error_log(str(f"Call Oeder Split Payment: {dd}"))

        else:
            _help.messagew(msg1="Split Order", msg2=f"You have {item} items left, split this first", error=True)
            return