from threading import Thread
from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv
from payment.list_method import PaymentMethod
from payment.list_terminal import CardTerminal
from payment.list_bank import Bank

class PaymentSetting:
	def __init__(self, realself, master, *args, **kwargs):
		super(PaymentSetting, self).__init__(*args, **kwargs)
		realself.master.title("{} - {}".format(ltext("payment_setting"), gv.st['storename']))
		self.master 							= master
		self.realself 							= realself

		self.editbnktoplevel 					= None
		self.addbnktoplevel 					= None
		self.editpmtoplevel 					= None
		self.editcttoplevel 					= None
		self.addcttoplevel 						= None

		self.purchase_depend_thread 	= Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.purchase_depend_thread.start()

	def get_dependency_master(self):
		def pm_popup():
			PaymentMethod(self)

		def ct_popup():
			CardTerminal(self)

		def bnk_popup():
			Bank(self)

		self.pm_tab 			= get_a_notebook(self.master, row=1, padx=5, pady=5, sticky = "wse", style="Custom.TFrame")

		self.pm_paned 			= get_a_panedwindow(self.pm_tab, padx=0, style="Custom.TFrame")
		self.ct_paned 			= get_a_panedwindow(self.pm_tab, padx=0, style="Custom.TFrame")
		self.bnk_paned 			= get_a_panedwindow(self.pm_tab, padx=0, style="Custom.TFrame")

		add_tab(self.pm_tab, self.pm_paned, ltext("payment_method"))
		add_tab(self.pm_tab, self.ct_paned, ltext("card_terminal"))
		add_tab(self.pm_tab, self.bnk_paned, ltext("bank"))

		pmdt 	= Thread(target = pm_popup, daemon = True)
		ctdt 	= Thread(target = ct_popup, daemon = True)
		bnkdt 	= Thread(target = bnk_popup, daemon = True)

		pmdt.start()
		ctdt.start()
		bnkdt.start()
