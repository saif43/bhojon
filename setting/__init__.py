from setting.__main__ import ApplicationSetting
from threading import Thread

def appsetting(realself, master):
	def get_start():
		appsetting 			= ApplicationSetting(realself, master)

	appsetting_thread = Thread(target=get_start, daemon=True)
	appsetting_thread.start()
