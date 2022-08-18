from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import FoodAvailablity, SyncResult


class Availability:
    def __init__(self, rself, *arg, **kwargs):
        super(Availability, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_foodvariable_list(rself)

    def sync_down_foodvariable_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'availability'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/foodvariable"
                r = requests.post(url, data=data)
                foodvariablelist = r.json().get("data").get("foodavailableinfo")
            except:
                foodvariablelist = None

            if foodvariablelist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from food availability")
                    FoodAvailablity().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from food availability")

                pcidl = [str(r['id']) for r in FoodAvailablity().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(foodvariablelist):
                    c['id'] = c.pop('availableID')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for food availability {}/{}".format(ix+1, len(foodvariablelist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for food availability {}/{}".format(ix+1, len(foodvariablelist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for food availability {}/{}".format(ix+1, len(foodvariablelist)))
                            cr_list.append(c)

                if cr_list:
                    FoodAvailablity().qset.create_all(cr_list)
                if up_list:
                    FoodAvailablity().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'availability'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
