from ntk.objects import gv as gv
import _help, requests, datetime

from database.table import CardTerminal as tbCardTerminal, SyncResult


class CardTerminal:
    def __init__(self, rself, *arg, **kwargs):
        super(CardTerminal, self).__init__()
        self.arg = arg
        self.kwargs = kwargs
        self.rself = rself

        self.sync_down_cardterminal_list(rself)

    def sync_down_cardterminal_list(this, self):
        SyncResult().qset.update(**{'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 0, 'table_name': 'cardterminal'}, where='table_name')

        try:
            data = {"android": 123}

            try:
                url = gv.website + "app/cardterminallist"
                r = requests.post(url, data=data)
                cdtmllist = r.json().get("data").get("bankinfo")
            except:
                cdtmllist = None

            if cdtmllist:
                if gv.deep_sync:
                    gv.rstatus_l.config(text="Deleting all records from card terminal")
                    tbCardTerminal().qset.delete_all()
                    gv.rstatus_l.config(text="Deleted all records from card terminal")

                pcidl = [str(r['id']) for r in tbCardTerminal().qset.filter(search='id').all()]
                cr_list, up_list = [], []

                for ix, c in enumerate(cdtmllist):
                    c['id'] = c.pop('card_terminalid')

                    if gv.deep_sync:
                        gv.rstatus_l.config(text="Adding record for card terminal {} {}/{}".format(c['terminal_name'], ix+1, len(cdtmllist)))
                        cr_list.append(c)
                    else:
                        if c['id'] in pcidl:
                            gv.rstatus_l.config(text="Updating record for card terminal {} {}/{}".format(c['terminal_name'], ix+1, len(cdtmllist)))
                            up_list.append(c)
                        else:
                            gv.rstatus_l.config(text="Adding record for card terminal {} {}/{}".format(c['terminal_name'], ix+1, len(cdtmllist)))
                            cr_list.append(c)

                if cr_list:
                    tbCardTerminal().qset.create_all(cr_list)
                if up_list:
                    tbCardTerminal().qset.update_all(up_list, where='id')

            SyncResult().qset.update(**{'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status': 1, 'table_name': 'cardterminal'}, where='table_name')

        except Exception as e:
            gv.error_log(str(e))
