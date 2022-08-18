from ntk.objects import gv as gv
import _help, requests, os, datetime

from database.table import SyncResult, Setting as tbSetting


class Setting:
    def __init__(self, rself, *arg, **kwargs):
        super(Setting, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_setting_table(rself)

    def sync_down_setting_table(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'setting'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/setinginfo"
                r = requests.post(url, data=data)
                setinginfo = r.json().get("data").get("setinginfo")[0]
            except:
                setinginfo = None

            if setinginfo:
                pset = tbSetting().qset.filter().first()
                set = setinginfo

                if pset:
                    logoi = set.get("logo")
                    args = list(logoi.split("/"))

                    if set.get("logo") and set.get("logo") != "":
                        try:
                            mainpath = os.path.join(gv.file_dir + "/application/" + "modules/" + "dependancy/" + "images/")
                            webpath = gv.website + logoi
                            if not os.path.exists(mainpath): os.makedirs(mainpath)

                            r = requests.get(webpath, allow_redirects=True)
                            with open(os.path.join(mainpath + args[len(args)-1]), "wb+") as fl:
                                fl.write(r.content)

                        except Exception as e:
                            gv.error_log(str(e))

                    set['id'] = pset['id']
                    set['logo'] = (gv.depend_image_dir + "/" + args[len(args)-1]) if set.get("logo") and set.get("logo") != "" else ""
                    set['currency'] = set.pop('currencyname')

                    tbSetting().qset.update(**set, where='id')

                    SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'setting'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
