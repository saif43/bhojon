import os, requests, datetime, urllib, sqlite3, json, _help
from tkinter import messagebox
from ntk.objects import gv as gv

from database.table import (
    SyncResult, CustomerInfo, Food, CustomerOrder, Bill,
    OrderItem, BillCardPayment, Varient, MultiPay, SubOrder
)


class Order:
    def __init__(self, *args, **kwargs):
        super(Order, self).__init__()

        self.master = kwargs.get("master")
        self.realself = kwargs.get("realself")

        print('Update orders')

        self.sync_up_order()

    def sync_up_order(self):
        data = None
        snc_ord_l = []
        mdata = {}
        orderinfo = []

        SyncResult().qset.update(**{
            'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 0, 'table_name': 'order'}, where='table_name')

        try:
            orders = CustomerOrder().qset.filter(sync_status=0).all()

            if len(orders) > 0:
                for iters, order in enumerate(orders):
                    if gv.sds_lab:
                        t = "Uploading offline order: {} out of {}".format(iters, len(orders))
                        gv.sds_lab.config(text=t)

                    addata = []
                    CartData = []
                    data = {}

                    customer = cust = CustomerInfo().qset.filter(id=order['customer_id'], is_active=1, sep='AND').first()
                    bill = Bill().qset.filter(order_id=order['id']).first()
                    menu_orders = OrderItem().qset.filter(order_id=order['id']).all()

                    if bill and menu_orders:
                        billcd = BillCardPayment().qset.filter(bill_id=bill['id']).first()

                        for menu_order in menu_orders:
                            food = Food().qset.filter(id=menu_order['menu_id'], ProductsIsActive=1, sep='AND').first()
                            variant = Varient().qset.filter(id=menu_order['varientid']).first()

                            if food and variant:
                                idata = {
                                    "order_id": "",
                                    "menu_id": str(food['id']),
                                    "menuqty": str(int(menu_order['menuqty'])),
                                    "add_on_id": str(menu_order['add_on_id']),
                                    "addonsqty": str(menu_order['addonsqty']),
                                    "varientid": str(variant['id']),
                                    "food_status": "0"
                                }

                                CartData.append(idata)

                        data = {
                            "order_id": str(order['order_id_online']) if str(order['order_id_online']) != "0" else "",
                            "saleinvoice": "",
                            "nofification": "",
                            "orderacceptreject": "",
                            "menu": "MenuData",
                            "shipping_type": "",
                            "delivarydate": "",
                            "ismultipay": 0,
                            'marge_order_id': order['marge_order_id'],
                            "Pay_type": []
                        }

                        mpayes = MultiPay().qset.filter(order_id=order['id'], marge_order_id=order['marge_order_id']).all()

                        if mpayes:
                            data['ismultipay'] = 1

                            ptypes = []

                            for mpay in mpayes:
                                ptype = {
                                    'order_id': order['order_id_online'],
                                    'margeorderid': data['marge_order_id'],
                                    'payment_type_id': mpay['payment_type_id'],
                                    'amount': mpay['amount'],
                                    'cardpinfo': []
                                }

                                pcard = BillCardPayment().qset.filter(multipay_id=mpay['id']).first()

                                if pcard:
                                    ptype['cardpinfo'].append({
                                        "card_no": "%s" %pcard['card_no'],
                                        "terminal_name": "%s" %pcard['terminal_name'],
                                        "Bank": "%s" %pcard['bank_name']
                                    })

                                ptypes.append(ptype)

                            data['Pay_type'] = ptypes

                        for i in [
                            'customer_id', 'isthirdparty', 'waiter_id', 'kitchen', 'order_date',
                            'order_time', 'cookedtime', 'table_no', 'tokenno', 'totalamount', 'customerpaid',
                            'customer_note', 'anyreason', 'order_status', 'marge_order_id']:
                            data[i] = order.get(i, "")

                        for i in [
                            "total_amount", "discount", "service_charge", "VAT", "bill_amount", "bill_date",
                            "bill_time", "bill_status", "payment_method_id", "create_by", "create_date",
                            "update_by", "update_date"]:
                            data[i] = bill.get(i, "")

                        for i in ["card_no", "terminal_name", "bank_name"]:
                            data[i] = billcd.get(i, "") if billcd else ""

                        if cust:
                            for i in [
                                'id', 'cuntomer_no', 'customer_name', 'customer_email', 'customer_phone',
                                'password', 'customer_token', 'customer_address', 'customer_picture',
                                'favorite_delivery_address', 'is_active']:
                                data[i] = str(cust.get(i, ""))

                            data['customer_id'] = data.pop('id')

                        data['menu'] = CartData
                        data['issplit'] = 0
                        data['cutomertype'] = order.get('customer_type', '')

                        splitpay_status = 0

                        sub_orders = SubOrder().qset.filter(order_id=order['id']).all()

                        if sub_orders:
                            data['issplit'] = 1
                            splitinfo = []

                            for sub_order in sub_orders:
                                splitmenu = []

                                if sub_order['status'] == 'False':
                                    splitpay_status = 1

                                for menu_id, menu_info in json.loads(sub_order['order_menu_id']).items():
                                    splitmenu.append({
                                        "menuid": menu_id,
                                        "qty": menu_info['quantity'],
                                        "isadons": 0
                                    })

                                splitinfo.append({
                                    "splitid": sub_order['id'],
                                    "customerid": order['customer_id'],
                                    "vat": sub_order['vat'],
                                    "servicecharge": sub_order['s_charge'],
                                    "discount": sub_order['discount'],
                                    "total": sub_order['total_price'],
                                    "status": sub_order['status'],
                                    "splitmenu": splitmenu
                                })

                            data['splitinfo'] = splitinfo
                            data['splitpay_status'] = splitpay_status

                        orderinfo.append(data)

                mdata['orderinfo'] = orderinfo

                if len(orderinfo) > 0:
                    finald = {"orderinfo": json.dumps(mdata)}

                    try:
                        url = gv.website + "app/ordersync"
                        response = requests.post(url, data=finald)
                        print(response.content.decode())
                        res_data = response.json().get("data").get("orderinfo")

                    except:
                        res_data = None

                    if res_data:
                        for i, rd_o in enumerate(res_data):
                            oid_onl = rd_o.get("ordering") if rd_o.get("ordering") != "" else 0
                            # bid_onl = rd_o.get("billid") if rd_o.get("billid") != "" else 0
                            CustomerOrder().qset.update(**{
                                'order_id_online': oid_onl, 'sync_status': 1, 'id': orders[i]['id']}, where='id')

            SyncResult().qset.update(**{
                'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 1, 'table_name': 'order'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
