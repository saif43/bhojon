from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, Varient as tbVarient


class Varient:
    def __init__(self, rself, *arg, **kwargs):
        super(Varient, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_varient_list(rself)

    def sync_down_varient_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'varient'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/varientlist"
                r = requests.post(url, data=data)
                varientlist = r.json().get("data").get("foodvarientinfo")
            except:
                varientlist = None

            if varientlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from food varient")
                    tbVarient().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from food varient")

                pcidl = [str(r['id']) for r in tbVarient().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(varientlist):
                    c['id'] = c.pop('variantid')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for food varient {} {}/{}".format(c['variantName'], ix+1, len(varientlist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for food varient {} {}/{}".format(c['variantName'], ix+1, len(varientlist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for food varient {} {}/{}".format(c['variantName'], ix+1, len(varientlist)))
                            cr_list.append(c)

                if cr_list:
                    tbVarient().qset.create_all(cr_list)
                if up_list:
                    tbVarient().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'varient'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
