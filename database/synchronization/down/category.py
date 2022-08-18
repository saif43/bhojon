from ntk.objects import gv as gv
import _help, requests, os, datetime

from database.table import SyncResult, FoodCategory


class Category:
    def __init__(self, rself, *arg, **kwargs):
        super(Category, self).__init__()
        self.arg                = arg
        self.kwargs             = kwargs
        self.rself              = rself

        self.sync_down_category_list(rself)

    def sync_down_category_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'category'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/categorylist"
                r = requests.post(url, data=data)
                categorylist = r.json().get("data").get("categoryfo")
            except:
                categorylist = None

            if categorylist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from food category")
                    FoodCategory().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from food category")

                pcidl = [str(r['id']) for r in FoodCategory().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(categorylist):
                    c['id'] = c.pop('CategoryID')
                    c['position'] = c.pop('Position')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for food category {} {}/{}".format(c['Name'], ix+1, len(categorylist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for food category {} {}/{}".format(c['Name'], ix+1, len(categorylist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for food category {} {}/{}".format(c['Name'], ix+1, len(categorylist)))
                            cr_list.append(c)

                    if c.get("CategoryImage") and c.get("CategoryImage") != "":
                        try:
                            cateimage = c.get("CategoryImage")

                            r_path 	= str(cateimage).replace("./application/modules/itemmanage/assets/images/", "")
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
                        except:
                            pass

                if cr_list:
                    FoodCategory().qset.create_all(cr_list)
                if up_list:
                    FoodCategory().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'category'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
