from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, OnlineOrder as tbOnlineOrder, OnlineOrderItem, BillOnline, BillCardPaymentOnline


class OnlineOrder:
    def __init__(self, rself, *arg, **kwargs):
        super(OnlineOrder, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_online_order_list(rself)

    def sync_down_online_order_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'onlineorder'}, where='table_name')

        oocr_li, ooicr_li, ooup_li, bocr_li, boup_li = [], [], [], [], []
        oo_cls, bo_cls = tbOnlineOrder().columns(), BillOnline().columns()

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/allonlineorder"
                r = requests.post(url, data=data)
                oorders = r.json().get("data").get("orderinfo")
            except:
                oorders = None

            if oorders:
                if gv.deep_sync:
                    tbOnlineOrder().qset.delete_all()
                    BillOnline().qset.delete_all()

                OnlineOrderItem().qset.delete_all()

                poil = [r['id'] for r in tbOnlineOrder().qset.filter(search='id').all()]
                noil = [int(o.get("orderd")) for o in oorders]

                for iters, so in enumerate(oorders):
                    if gv.lds_lab:
                        gv.lds_lab.config(text="Downloading online order: {} out of {}".format(iters + 1, len(oorders)))

                    so_b = so.get("billinfo")
                    so_m = so.get("menu", [])

                    so["id"] = so.pop("orderd")
                    so["saleinvoice"] = so.pop("invoice")
                    so["isthirdparty"] = so.pop("thirdparty")
                    so["tokenno"] = so.pop("token")
                    so["customerpaid"] = so.pop("paidamount")

                    so_b["id"] = so_b.pop("bill_id")
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
                        ooicr_li.append(so_sm)

                    cso = dict((k, v) for k, v in so.items() if k in oo_cls)
                    csob = dict((k, v) for k, v in so_b.items() if k in bo_cls)

                    if noil[iters] in poil and not gv.deep_sync:
                        ooup_li.append(cso)
                        boup_li.append(csob)
                    else:
                        oocr_li.append(cso)
                        bocr_li.append(csob)

                if ooup_li:
                    tbOnlineOrder().qset.update_all(ooup_li, where='id')
                if boup_li:
                    BillOnline().qset.update_all(boup_li, where='id')
                if oocr_li:
                    tbOnlineOrder().qset.create_all(oocr_li)
                if bocr_li:
                    BillOnline().qset.create_all(bocr_li)
                if ooicr_li:
                    OnlineOrderItem().qset.create_all(ooicr_li)

            SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'onlineorder'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
