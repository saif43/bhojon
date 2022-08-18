from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv

from customer.list_third_party import ThirdPartyCustomerList
from customer.list_type import CustomerTypeList
from threading import Thread

class CustomerType:
	def __init__(self, realself, master, *args, **kwargs):
		super(CustomerType, self).__init__(*args, **kwargs)
		realself.master.title("{} - {}".format(ltext("customer_type_setting"), gv.st['storename']))
		self.master 							= master
		self.realself 							= realself

		self.edittpctop 						= None
		self.addtpctop 							= None
		self.editcttop 							= None

		self.tpc_dep_thr = Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.tpc_dep_thr.start()

	def get_dependency_master(self):
		def list_tpc_popup():
			ThirdPartyCustomerList(self)

		def list_ct_popup():
			CustomerTypeList(self)

		self.tpc_tab 		= get_a_notebook(self.master, row=1, padx=5, pady=5, sticky = "wse", style="Custom.TFrame")

		self.tpc_li_paned 	= get_a_panedwindow(self.tpc_tab, padx=0, style="Custom.TFrame")
		self.ct_li_paned 	= get_a_panedwindow(self.tpc_tab, padx=0, style="Custom.TFrame")

		add_tab(self.tpc_tab, self.tpc_li_paned, ltext("third_party_customer"))
		add_tab(self.tpc_tab, self.ct_li_paned, ltext("customer_type"))

		ctdt 	= Thread(target = list_ct_popup, daemon = True)
		tpcdt 	= Thread(target = list_tpc_popup, daemon = True)

		ctdt.start()
		tpcdt.start()
