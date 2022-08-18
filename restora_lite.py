import socket, license, _help, time
from threading import Thread
from tkinter import ttk

from ntk.objects import gv as gv
from dev_help import ttk_style
from __restora__.global_ import set_path, setting
from ntk.utils.admin import *

from ntk import Tk, Frame, PanedWindow

# gv.file_dir = os.getcwd()
import os

root = os.path.dirname(__file__)
gv.application_dir = os.path.join(root)
gv.file_dir = os.path.join(gv.application_dir)
print(gv.file_dir)
gv.phases = []
gv.set_setting = setting
gv.db_name = "restora.db"
gv.db_timeout = 10

set_path()
sys.setswitchinterval(1)


class Restaurant:
	def __init__(self, master, *args, **kwargs):
		super(Restaurant, self).__init__(*args, **kwargs)
		master.title("Dhaka Restaurant")
		self.master = master
		# self.resturant_frame = self.master = master
		gv.rest = self

		gv.wpc = gv.device_width/1366
		gv.hpc = gv.device_height/768

		ttk_style.style(ttk)

		self.done = False
		self.data_table_created = False
		self.login_top = None

		self.resturant_frame = PanedWindow(self.master, padx=(0, 0), pady=(0, 0), sticky="wne")

		self.mainthread = Thread(target=self.get_start, daemon=True)
		self.mainthread.start()

		self.is_connected()

	def get_start(self):
		license.license(self, self.resturant_frame)

	def is_connected(self):
		connected = False
		try:
			socket.create_connection(("www.google.com", 80))
			connected = True
		except OSError as e:
			time.sleep(1)
			_help.messagew(msg1="Internet connection", msg2="Unable to connect!", error=True)
		return connected


def main():
	if is_admin():
		root = Tk(bg="#F5F5F5", mainframe=False, fullscreen=True, icon=gv.icon_path)
		root.state('zoomed')

		def get_start():
			Restaurant(root)

		thr = Thread(target=get_start, daemon=True)
		thr.start()

		root.mainloop()
	else:
		run_as_admin(sys.executable)


if __name__ == "__main__":
	main()
