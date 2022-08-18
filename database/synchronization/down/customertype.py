from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, CustomerType as cType


class CustomerType:
    def __init__(self, rself, *arg, **kwargs):
        super(CustomerType, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_customer_type_list(rself)

    def sync_down_customer_type_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'customertype'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/customertypelist"
                r = requests.post(url, data=data)
                custtypelist = r.json().get("data").get("customertypeinfo")
            except:
                custtypelist = None

            if custtypelist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from customer type")
                    cType().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from customer type")

                pcidl = [str(r['id']) for r in cType().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(custtypelist):
                    c['id'] = c.pop('customer_type_id')
                    c.pop('ordering')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for customer type {} {}/{}".format(c['customer_type'], ix+1, len(custtypelist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for customer type {} {}/{}".format(c['customer_type'], ix+1, len(custtypelist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for customer type {} {}/{}".format(c['customer_type'], ix+1, len(custtypelist)))
                            cr_list.append(c)

                if cr_list:
                    cType().qset.create_all(cr_list)
                if up_list:
                    cType().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'customertype'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
