from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, ThirdPartyCustomer as tbThirdParty


class ThirdParty:
    def __init__(self, rself, *arg, **kwargs):
        super(ThirdParty, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_thirdparty_list(rself)

    def sync_down_thirdparty_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'thirdparty'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/thirdpartylist"
                r = requests.post(url, data=data)
                thirdpartylist = r.json().get("data").get("thirdpartyinfo")
            except:
                thirdpartylist = None

            if thirdpartylist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from thirdparty company")
                    tbThirdParty().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from thirdparty company")

                pcidl = [str(r['id']) for r in tbThirdParty().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(thirdpartylist):
                    c['id'] = c.pop('companyId')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for thirdparty company {} {}/{}".format(c['company_name'], ix+1, len(thirdpartylist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for thirdparty company {} {}/{}".format(c['company_name'], ix+1, len(thirdpartylist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for thirdparty company {} {}/{}".format(c['company_name'], ix+1, len(thirdpartylist)))
                            cr_list.append(c)

                if cr_list:
                    tbThirdParty().qset.create_all(cr_list)
                if up_list:
                    tbThirdParty().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'thirdparty'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
