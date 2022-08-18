from payment.__main__ import PaymentSetting
from threading import Thread

def payment_setting(realself=None, master=None):
	if realself and master:
		def get_start():
			payment_setting = PaymentSetting(realself, master)

		pm_thread 	= Thread(target=get_start, daemon=True)
		pm_thread.start()

		return payment_setting