from order.__main__ import Order, PosInvoice, EditOrder
from threading import Thread

def order(realself, master):
	def get_start():
		order 		= Order(realself, master)

	order_thread = Thread(target=get_start, daemon=True)
	order_thread.start()

def pos_order(realself, master):
	def get_start():
		pos_order 		= PosInvoice(realself, master)

	pos_order_thread = Thread(target=get_start, daemon=True)
	pos_order_thread.start()

def update_order(realself, master, order):
	def get_start():
		update_order 	= EditOrder(realself, master, order)

	update_order_thread = Thread(target=get_start, daemon=True)
	update_order_thread.start()