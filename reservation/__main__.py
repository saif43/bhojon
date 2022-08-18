from tkinter import messagebox, ttk
from threading import Thread
import datetime, time

from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv

from reservation.list_table import TableList

class Table:
	def __init__(self, realself, master, *args, **kwargs):
		super(Table, self).__init__(*args, **kwargs)
		realself.master.title("{} - {}".format(ltext("table_setting"), gv.st['storename']))
		self.master 				= master
		self.realself 				= realself
		self.addtabletoplevel 		= None
		self.edittabletoplevel 		= None

		self.table_depend_thread = Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.table_depend_thread.start()

	def get_dependency_master(self):
		def table_list_popup():
			TableList(self)

		self.table_list_panedwindow 	= get_a_panedwindow(self.master, row=1, padx=5, pady=5, style="Custom.TFrame")

		tlp 	= Thread(target=table_list_popup, daemon = True)

		tlp.start()

def main():
	root 			= Tk()
	def get_start():
		resturant 		= Reservation(root)

	thr = Thread(target=get_start, daemon=True)
	thr.start()

	root.mainloop()

if __name__ == "__main__":main()
