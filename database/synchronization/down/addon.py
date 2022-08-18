from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import AddOn, SyncResult


class Addon:
    def __init__(self, rself, *arg, **kwargs):
        super(Addon, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_addon_list(rself)

    def sync_down_addon_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'addon'}, where='table_name')

        try:
            data = {"android": 123}
            try:
                url = gv.website + "app/addonslist"
                r = requests.post(url, data=data)
                addonslist = r.json().get("data").get("addonsinfo")
            except:
                addonslist = None

            if addonslist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from addon")
                    AddOn().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from addon")

                pcidl = [str(r['id']) for r in AddOn().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(addonslist):
                    c['id'] = c.pop('add_on_id')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for addon {} {}/{}".format(c['add_on_name'], ix+1, len(addonslist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for addon {} {}/{}".format(c['add_on_name'], ix+1, len(addonslist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for addon {} {}/{}".format(c['add_on_name'], ix+1, len(addonslist)))
                            cr_list.append(c)

                if cr_list:
                    AddOn().qset.create_all(cr_list)
                if up_list:
                    AddOn().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'addon'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
