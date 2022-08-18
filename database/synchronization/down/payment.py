from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, PaymentMethod


class Payment:
    def __init__(self, rself, *arg, **kwargs):
        super(Payment, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_payment_list(rself)

    def sync_down_payment_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'payment'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/paymentlist"
                r = requests.post(url, data=data)
                paymentlist = r.json().get("data").get("paymentinfo")
            except:
                paymentlist = None

            if paymentlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from payment method")
                    PaymentMethod().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from payment method")

                pcidl = [str(r['id']) for r in PaymentMethod().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(paymentlist):
                    c['id'] = c.pop('payment_method_id')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for payment method {} {}/{}".format(c['payment_method'], ix+1, len(paymentlist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for payment method {} {}/{}".format(c['payment_method'], ix+1, len(paymentlist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for payment method {} {}/{}".format(c['payment_method'], ix+1, len(paymentlist)))
                            cr_list.append(c)

                if cr_list:
                    PaymentMethod().qset.create_all(cr_list)
                if up_list:
                    PaymentMethod().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'payment'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
