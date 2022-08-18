
from ntk.objects import gv
import _help, requests, datetime

from database.table import CashCounter, SyncResult


class ResCounter:
    def __init__(self, rself, *arg, **kwargs):
        super(ResCounter, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_counter_list(rself)

    def sync_down_counter_list(this, self):
        SyncResult().qset.update(
            last_checked=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=0, table_name='counter', where='table_name'
        )

        try:
            data = {"android": 123}
            try:
                url = gv.website + "app/cashcounter"
                r = requests.post(url, data=data)
                cash_counters = r.json().get("data").get("counterinfo")
            except Exception as e:
                gv.error_log(str(e))
                cash_counters = None

            if cash_counters:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from cash counter")
                    CashCounter().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from cash counter")

                pcidl = [str(r['id']) for r in CashCounter().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(cash_counters):
                    c['id'] = c.pop('countedid')

                    if gv.deep_sync:
                        gv.rstatus_l.config(
                            text="Adding record for cash counter {} {}/{}".format(c['counterno'],
                                                                                  ix+1, len(cash_counters)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(
                                text="Updating record for cash counter {} {}/{}".format(c['counterno'],
                                                                                        ix+1, len(cash_counters)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(
                                text="Adding record for cash counter {} {}/{}".format(c['counterno'],
                                                                                      ix+1, len(cash_counters)))
                            cr_list.append(c)

                if cr_list:
                    CashCounter().qset.create_all(cr_list)
                if up_list:
                    CashCounter().qset.update_all(up_list, where='id')

                SyncResult().qset.update(
                    last_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=1, table_name='counter', where='table_name')

        except Exception as e:
            gv.error_log(str(e))
