import _help, requests, datetime
from database.table import CashRegister as tblCashRegister, SyncResult
from ntk import gv


class CashRegister:
    def __init__(self, rself, *arg, **kwargs):
        super(CashRegister, self).__init__()
        self.sync_up_cash_register()

    def sync_up_cash_register(self):
        SyncResult().qset.update(
            **{
                'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 0, 'table_name': 'cashregister'
            }, where='table_name'
        )

        try:
            cashregister_list = tblCashRegister().qset.all()

            if cashregister_list:
                register_formated = []
                for ix, register in enumerate(cashregister_list):
                    register.pop('id')
                    register_formated.append(register)

                url = gv.website + "app/cashregistersync"
                r = requests.post(url, data={'cashinfo': register_formated})

            SyncResult().qset.update(
                **{
                    'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 1, 'table_name': 'cashregister'}, where='table_name'
            )

        except Exception as e:
            gv.error_log(str(e))
