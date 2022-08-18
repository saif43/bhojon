import os, time
from ntk import gv

class PrintInvoice:
	def __init__(self, *args, **kwargs):
		super(PrintInvoice, self).__init__(*args)
		self.print_file 			= kwargs.get('print_file')
		if self.print_file:
			self.get_dependancy()

	def get_dependancy(self):
		time.sleep(2)

		try:
			os.startfile(self.print_file, "print")
		except Exception as e: gv.error_log(str(e))
