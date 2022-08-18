from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, CustomerInfo


class Customer:
    def __init__(self, rself, *arg, **kwargs):
        super(Customer, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_customer_list(rself)

    def sync_down_customer_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'customer'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/customerlist"
                r = requests.post(url, data=data)
                customerlist = r.json().get("data").get("customerinfo")
            except:
                customerlist = None

            if customerlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from customer")
                    CustomerInfo().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from customer")

                pcidl = [str(r['id']) for r in CustomerInfo().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(customerlist):
                    c['id'] = c.pop('customer_id')
                    c['customer_no'] = c.pop('cuntomer_no')
                    c['customer_name'] = c.pop('customer_name').replace("'", "")
                    c['customer_phone'] = c.pop('customer_phone').replace("'", "")
                    c['customer_email'] = c.pop('customer_email').replace("'", "")

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for customer {} {}/{}".format(c['customer_name'], ix+1, len(customerlist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for customer {} {}/{}".format(c['customer_name'], ix+1, len(customerlist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for customer {} {}/{}".format(c['customer_name'], ix+1, len(customerlist)))
                            cr_list.append(c)

                if cr_list:
                    CustomerInfo().qset.create_all(cr_list)
                if up_list:
                    CustomerInfo().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'customer'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
