from threading import Thread

def login(realself=None, master=None):
	if realself and master:
		def get_start():
			login 	= Login(realself, master)

		login_thr  	= Thread(target=get_start, daemon=True)
		login_thr.start()
