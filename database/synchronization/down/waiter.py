from ntk.objects import gv as gv
import _help, requests, datetime, string

from database.table import SyncResult, Employee, User


class Waiter:
    def __init__(self, rself, *arg, **kwargs):
        super(Waiter, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_waiter_list(rself)

    def sync_down_waiter_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'waiter'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/waiterlist"
                r = requests.post(url, data=data)
                waiterlist = r.json().get("data").get("waiterinfo")
                userlist = r.json().get("data").get("userinfo")
            except:
                waiterlist = None
                userlist = None

            if waiterlist and userlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from waiter and user")
                    Employee().qset.delete_all()
                    User().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from waiter and user")

                pwidl = [str(r['id']) for r in Employee().qset.filter(search='id').all()]
                puidl = [str(r['id']) for r in User().qset.filter(search='id').all()]
                wcr_list, wup_list, ucr_list, uup_list = [], [], [], []

                for ix, c in enumerate(waiterlist):
                    c['id'] = c.pop('emp_his_id')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for waiter {} {}/{}".format(c['first_name'], ix+1, len(waiterlist)))
                        wcr_list.append(c)
                    else:
                        if c['id'] in pwidl:
                            gv.rstatus_l.config(text="Updating record for waiter {} {}/{}".format(c['first_name'], ix+1, len(waiterlist)))
                            wup_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for waiter {} {}/{}".format(c['first_name'], ix+1, len(waiterlist)))
                            wcr_list.append(c)

                chwds = string.digits + string.ascii_letters

                for ix, c in enumerate(userlist):
                    fpass = ""

                    if c.get("password"):
                        for s in c.get("password"):
                            fpass = fpass + str(chwds.index(s))

                    c['password'] = fpass

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for user {} {}/{}".format(c['firstname'], ix+1, len(userlist)))
                        ucr_list.append(c)
                    else:
                        if c['id'] in puidl:
                            gv.rstatus_l.config(text="Updating record for user {} {}/{}".format(c['firstname'], ix+1, len(userlist)))
                            uup_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for user {} {}/{}".format(c['firstname'], ix+1, len(userlist)))
                            ucr_list.append(c)

                if wcr_list:
                    Employee().qset.create_all(wcr_list)
                if wup_list:
                    Employee().qset.update_all(wup_list)
                if ucr_list:
                    User().qset.create_all(ucr_list)
                if uup_list:
                    User().qset.update_all(uup_list)

            SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'waiter'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
