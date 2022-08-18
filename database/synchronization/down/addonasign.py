from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import AddOnAsign, SyncResult


class AddonAsign:
    def __init__(self, rself, *arg, **kwargs):
        super(AddonAsign, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_addon_asign_list(rself)

    def sync_down_addon_asign_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'addonasign'}, where='table_name')

        try:
            data = {"android": 123}
            try:
                url = gv.website + "app/addonsassignlist"
                r = requests.post(url, data=data)
                addonasignlist = r.json().get("data").get("addonsinfo")
            except:
                addonasignlist = None

            if addonasignlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from asigned addon")
                    AddOnAsign().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from asigned addon")

                pcidl = [str(r['id']) for r in AddOnAsign().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(addonasignlist):
                    c['id'] = c.pop('row_id')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for asigned addon {}/{}".format(ix+1, len(addonasignlist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for asigned addon {}/{}".format(ix+1, len(addonasignlist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for asigned addon {}/{}".format(ix+1, len(addonasignlist)))
                            cr_list.append(c)

                if cr_list:
                    AddOnAsign().qset.create_all(cr_list)
                if up_list:
                    AddOnAsign().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'addonasign'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
