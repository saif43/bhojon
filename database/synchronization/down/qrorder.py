from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, QROrder as tbQROrder, QROrderMenu, QRBill


class QROrder:
    def __init__(self, rself, *arg, **kwargs):
        super(QROrder, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_qr_order_list(rself)

    def sync_down_qr_order_list(this, self):
        SyncResult().qset.update(**{
                            'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'status': 0, 'table_name': 'qr_order'
                        }, where='table_name')

        qr_cr_li, qr_icr_li, qr_up_li, qr_b_cr_li, qr_b_up_li = [], [], [], [], []
        qr_o_cls, qr_b_cls = tbQROrder().columns(), QRBill().columns()

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/allqrorder"
                r = requests.post(url, data=data)
                qr_orders = r.json().get("data").get("orderinfo")
            except:
                qr_orders = None

            if qr_orders:
                if gv.deep_sync:
                    tbQROrder().qset.delete_all()
                    QRBill().qset.delete_all()

                QROrderMenu().qset.delete_all()

                prev_qr_ids = [r['id'] for r in tbQROrder().qset.filter(search='id').all()]
                new_qr_ids = [int(o.get("orderd")) for o in qr_orders]

                for en_i, so in enumerate(qr_orders):
                    if gv.lds_lab:
                        gv.lds_lab.config(
                            text="Downloading qr order: {} out of {}".format(en_i + 1, len(qr_orders)))

                    so_customer = so.pop("customerinfo", {})
                    so_bill = so.pop("billinfo", {})
                    so_menu = so.pop("menu", [])

                    qr_o_ = dict((k, v) for k, v in so.items() if k in qr_o_cls)
                    qr_b_ = dict((k, v) for k, v in so_bill.items() if k in qr_b_cls)

                    if new_qr_ids[en_i] in prev_qr_ids and not gv.deep_sync:
                        qr_up_li.append(qr_o_)
                        qr_b_up_li.append(qr_b_)
                    else:
                        qr_cr_li.append(qr_o_)
                        qr_b_cr_li.append(qr_b_)

                    qr_icr_li = qr_icr_li + so_menu

                if qr_up_li:
                    tbQROrder().qset.update_all(qr_up_li, where='id')

                if qr_b_up_li:
                    QRBill().qset.update_all(qr_b_up_li, where='id')

                if qr_cr_li:
                    tbQROrder().qset.create_all(qr_cr_li)

                if qr_b_cr_li:
                    QRBill().qset.create_all(qr_b_cr_li)

                if qr_icr_li:
                    QROrderMenu().qset.create_all(qr_icr_li)

            SyncResult().qset.update(**{
                                'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'status': 1, 'table_name': 'qr_order'
                            }, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
