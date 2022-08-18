from ntk.objects import gv as gv
import _help, requests, os, datetime

from database.table import Food as tbFood, SyncResult


class Food:
    def __init__(self, rself, *arg, **kwargs):
        super(Food, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_food_list(rself)

    def sync_down_food_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'food'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/foodlist"
                r = requests.post(url, data=data)
                foodlist = r.json().get("data").get("foodinfo")
            except Exception as e:
                gv.error_log(str(e))
                foodlist = None

            if foodlist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from food")
                    tbFood().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from food")

                pcidl = [str(r['id']) for r in tbFood().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(foodlist):
                    c['id'] = c.pop('ProductsID')
                    c['position'] = c.pop('Position')

                    c = dict((k,v.replace("\'", '')) for k,v in c.items())

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for food {} {}/{}".format(c['ProductName'], ix+1, len(foodlist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for food {} {}/{}".format(c['ProductName'], ix+1, len(foodlist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for food {} {}/{}".format(c['ProductName'], ix+1, len(foodlist)))
                            cr_list.append(c)

                    if c.get("ProductImage") and c.get("ProductImage") != "":
                        try:
                            productimage = c.get("ProductImage")

                            r_path 	= str(productimage).replace("application/modules/itemmanage/assets/images/", "")
                            args  	= list(r_path.split("/"))
                            path 	= ""

                            for arg in args:
                                if (args.index(arg)+1) != len(args): path = path + (arg + "/")
                                mainpath = os.path.join(gv.file_dir + "/application/" + "modules/" + "itemmanage/" + "assets/" + "images/" + path)
                                if not os.path.exists(mainpath): os.mkdir(mainpath)

                            webpath = gv.website + "/application/" + "modules/" + "itemmanage/" + "assets/" + "images/" + path + args[len(args)-1]

                            r = requests.get(webpath, allow_redirects=True)
                            with open(os.path.join(mainpath + args[len(args)-1]), "wb+") as fl:
                                fl.write(r.content)
                        except Exception as e:
                            gv.error_log(str(e))

                if cr_list:
                    tbFood().qset.create_all(cr_list)
                if up_list:
                    tbFood().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'food'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
