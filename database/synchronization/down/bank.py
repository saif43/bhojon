from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import Bank as tbBank, SyncResult


class Bank:
    def __init__(self, rself, *arg, **kwargs):
        super(Bank, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_bank_list(rself)

    def sync_down_bank_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'bank'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/banklist"
                r = requests.post(url, data=data)
                banklist = r.json().get("data").get("bankinfo")
            except:
                banklist = None

            if banklist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from bank")
                    tbBank().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from bank")

                pcidl = [str(r['id']) for r in tbBank().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(banklist):
                    c['id'] = c.pop('bankid')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for bank {} {}/{}".format(c['bank_name'], ix+1, len(banklist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for bank {} {}/{}".format(c['bank_name'], ix+1, len(banklist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for bank {} {}/{}".format(c['bank_name'], ix+1, len(banklist)))
                            cr_list.append(c)

                if cr_list:
                    tbBank().qset.create_all(cr_list)
                if up_list:
                    tbBank().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'bank'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
