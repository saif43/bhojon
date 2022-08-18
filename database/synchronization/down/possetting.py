from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import PosSetting as tbPosSetting, SyncResult


class PosSetting:
    def __init__(self, rself, *arg, **kwargs):
        super(PosSetting, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_bank_list(rself)

    def sync_down_bank_list(this, self):
        SyncResult().qset.update(
            last_checked=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=0, table_name='pos_setting', where='table_name'
        )

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/posetting"
                r = requests.post(url, data=data)
                settlist = r.json().get("data").get("posetting")
            except:
                settlist = None

            if settlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from pos setting")
                    tbPosSetting().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from pos setting")

                pcidl = [str(r['id']) for r in tbPosSetting().qset.filter(search='id').all()]
                cr_list = []

                for ix, c in enumerate(settlist):
                    gv.rstatus_l.config(text="Adding record for pos setting {}/{}".format(ix+1, len(settlist)))
                    cr_list.append(c)

                if cr_list:
                    tbPosSetting().qset.create_all(cr_list)

                SyncResult().qset.update(
                    last_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=1, table_name='pos_setting', where='table_name'
                )

        except Exception as e:
            gv.error_log(str(e))
