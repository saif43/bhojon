from customer.__main__ import CustomerType
from threading import Thread

def customer_type(realself=None, master=None):
	if realself and master:
		def get_start():
			customer_type 	= CustomerType(realself, master)

		ct_thr 				= Thread(target=get_start, daemon=True)
		ct_thr.start()