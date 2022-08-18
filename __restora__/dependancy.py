from tkinter import messagebox
from ntk.objects import gv as gv
import sqlite3, os, datetime, _help
from dev_help.widgets import *

from database.table import Setting, PosSetting

def setting_table():
	res = False

	try:
		Setting(init=1).qset.create()
		PosSetting(init=1).qset.create()
		res = True
	except Exception as e:
		gv.error_log(str(e))
		_help.messagew(msg1=ltext("error_report_from_setting_application_info"), msg2="{}: {}".format(ltext("error"), e), error=True)
	return res
