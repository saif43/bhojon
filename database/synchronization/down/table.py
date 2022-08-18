from ntk.objects import gv as gv
import _help, requests, os, datetime

from database.table import SyncResult, Tables


class Table:
    def __init__(self, rself, *arg, **kwargs):
        super(Table, self).__init__()
        self.arg                = arg
        self.kwargs             = kwargs
        self.rself              = rself

        self.sync_down_table_list(rself)

    def sync_down_table_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'table'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/tablelist"
                r = requests.post(url, data=data)
                tablelist = r.json().get("data").get("tableinfo")
            except:
                tablelist = None

            if tablelist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from reservation table")
                    Tables().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from reservation table")

                pcidl = [str(r['id']) for r in Tables().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, table in enumerate(tablelist):
                    table['id'] = table.pop('tableid')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for reservation table {} {}/{}".format(table['tablename'], ix+1, len(tablelist)))
                        cr_list.append(table)
                    else:
                        if table['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for reservation table {} {}/{}".format(table['tablename'], ix+1, len(tablelist)))
                            up_list.append(table)
                        else:
                            gv.rstatus_l.config(text="Adding record for reservation table {} {}/{}".format(table['tablename'], ix+1, len(tablelist)))
                            cr_list.append(table)

                    if table.get("table_icon") and table.get("table_icon") != "":
                        try:
                            tableimage = table.get("table_icon")

                            args  	= list(tableimage.split("/"))
                            path 	= ""

                            for arg in args:
                                if (args.index(arg)+1) != len(args): path = path + (arg + "/")
                                mainpath = os.path.join(gv.file_dir + "/application/" + "modules/" + "itemmanage/" + path)
                                if not os.path.exists(mainpath): os.mkdir(mainpath)

                            webpath = gv.website + tableimage

                            r = requests.get(webpath, allow_redirects=True)
                            with open(os.path.join(mainpath + args[len(args)-1]), "wb+") as fl:
                                fl.write(r.content)
                        except:
                            pass

                if cr_list:
                    Tables().qset.create_all(cr_list)
                if up_list:
                    Tables().qset.update_all(up_list, where='id')

                SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'table'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
