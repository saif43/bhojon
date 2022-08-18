from reservation.__main__ import Table
from threading import Thread

def table(realself=None, master=None):
	if realself and master:
		def get_start():
			table 					= Table(realself=realself, master=master)

		table_thread 				= Thread(target=get_start, daemon=True)
		table_thread.start()
