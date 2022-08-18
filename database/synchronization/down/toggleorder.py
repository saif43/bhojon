from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, CustomerOrder, OrderItem, Bill, BillCardPayment


class ToggleOrder:
    def __init__(self, rself, *arg, **kwargs):
        super(ToggleOrder, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_online_order_list(rself)

    def sync_down_online_order_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'synced_order'}, where='table_name')

        ooicr_li, ooup_li, boup_li = [], [], []
        oo_cls, bo_cls = CustomerOrder().columns(), Bill().columns()

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/allofflineorder"
                r = requests.post(url, data=data)
                oorders = r.json().get("data").get("orderinfo")
            except:
                oorders = None

            if oorders:
                pors = CustomerOrder().qset.all()
                poil = [r['id'] for r in pors]
                noil = [r['order_id_online'] for r in pors]

                for iters, so in enumerate(oorders):
                    if so['orderd'] in noil:
                        if gv.lds_lab:
                            gv.lds_lab.config(text="Downloading synced order: {} out of {}".format(iters + 1, len(oorders)))

                        so_b = so.get("billinfo")
                        so_m = so.get("menu", [])

                        so["id"] = poil[noil.index(so['orderd'])]
                        so["saleinvoice"] = so.pop("invoice")
                        so["isthirdparty"] = so.pop("thirdparty")
                        so["tokenno"] = so.pop("token")
                        so["customerpaid"] = so.pop("paidamount")
                        so["cookingtime"] = so.pop("cooked_time")
                        so["sync_status"] = 1
                        so["anyreason"] = so.pop('reason')

                        bill = Bill().qset.filter(order_id=poil[noil.index(so['orderd'])]).first()
                        so_b["id"] = bill['id']
                        so_b["subtotal"] = so_b.pop("total_amount")
                        so_b["servicecharge"] = so_b.pop("service_charge")
                        so_b["vat"] = so_b.pop("VAT")
                        so_b["totalamount"] = so_b.pop("bill_amount")
                        so_b["order_date"] = so_b.pop("bill_date")
                        so_b["order_time"] = so_b.pop("bill_time")
                        so_b["billstatus"] = so_b.pop("bill_status")
                        so_b["paymentmethod"] = so_b.pop("payment_method_id")
                        so_b["createby"] = so_b.pop("create_by")
                        so_b["order_date"] = so_b.pop("create_date")
                        so_b["updateby"] = so_b.pop("update_by")
                        so_b["updatedate"] = so_b.pop("update_date")

                        for so_sm in so_m:
                            so_sm['id'] = so_sm.pop('row_id')
                            so_sm['variantid'] = so_sm.pop('varientid')
                            ooicr_li.append(so_sm)

                        cso = dict((k, v) for k, v in so.items() if k in oo_cls)
                        csob = dict((k, v) for k, v in so_b.items() if k in bo_cls)

                        ooup_li.append(cso)
                        bo_up.append(csob)

                if ooup_li:
                    CustomerOrder().qset.update_all(ooup_li, where='id')
                    for o in ooup_li:
                        OrderItem().qset.delete(order_id=o['id'])
                if boup_li:
                    Bill().qset.update_all(bo_up, where='id')
                if ooicr_li:
                    OrderItem().qset.create_all(ooicr_li)

            SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'synced_order'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
