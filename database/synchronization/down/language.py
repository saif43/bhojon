from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import SyncResult, Language as tbLanguage


class Language:
    def __init__(self, rself, *arg, **kwargs):
        super(Language, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_language_list(rself)

    def sync_down_language_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'language'}, where='table_name')

        try:
            data = {"android": "123"}
            try:
                langlist = requests.post(gv.website + "app/languagelist", data=data).json().get("data")
            except:
                langlist = None

            lphaseslist = [r['phrase'] for r in tbLanguage().qset.filter(search='phrase').all()]

            if gv.deep_sync:
                gv.rstatus_l.config(text="Deleting all records from language")
                tbLanguage().reset_table()
                gv.rstatus_l.config(text="Deleted all records from language")

                gv.rstatus_l.config(text="Resetting phrase for language")
                tbLanguage().qset.create_all([{'phrase': v} for v in lphaseslist])
                gv.rstatus_l.config(text="Reset successful for language")

            col_l = tbLanguage().columns()

            for key, value in langlist.items():
                up_list = []
                if not key in col_l:
                    gv.rstatus_l.config(text="Adding record for language {}".format(key))
                    tbLanguage().add_column('TEXT', key, default='', null=True)

                try:
                    data = {"language": "{}".format(key)}
                    r = requests.post(gv.website + "app/editPhrase", data=data)
                    labellist = r.json().get("data").get("label")
                    phaseslist = r.json().get("data").get("phrase")
                except:
                    labellist = None
                    phaseslist = None

                for i, phase in enumerate(phaseslist):
                    if phase in lphaseslist:
                        up_list.append({key: str(labellist[i]), 'phrase': phase})

                if up_list:
                    tbLanguage().qset.update_all(up_list, where='phrase')

            SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'language'}, where='table_name')
            gv.phases = []
        except Exception as e:
            gv.error_log(str(e))
