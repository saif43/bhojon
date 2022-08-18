
from threading import Thread
from user.login import LoginForm
from menu import ResturantMenu

from dev_help.widgets import *
from ntk.objects import gv as gv

from order.list import OrderList
from order.list_pending import PendingOrderList
from order.list_complete import CompleteOrderList
from order.list_cancel import CancelOrderList
from order.list_online import OnlineOrderList
from order.list_qr import QROrder

from order.new_pos import PosOrder
from order.list_today import TodayOrderList
from order.list_ongoing import OngoingOrderList
from order.list_qr import QROrderList
from order.update import UpdateOrder
from order.snippets.cashcounter import OpenCashCounter, CloseCashCounter

from ntk import PanedWindow, Notebook, Button, Frame, SelectBox, ImageFile, Toplevel, Canvas
from database.table import OnlineOrder, QROrder, Language, CashRegister, Bill
import os, requests

# gv.error_log(str(f"File: order/__main__.py"))

class Order:
	def __init__(self, realself, master, *args, **kwargs):
		super(Order, self).__init__(*args, **kwargs)

		# gv.error_log(str(f"self: {self} --> realself: {realself} --> master: {master} --> args: {args} --> kwargs: {kwargs}"))
		
		realself.master.title("{} - {}".format(
											ltext("order_section"),
											gv.st['storename']
										)
									)

		self.realself = realself
		self.master = master
		self.realself.cart_table_created = False
		self.calendar_order_date = None
		self.add_order_cart_initialized = False
		self.toplevel_category_item = None
		self.add_customer_toplevel = False
		self.viewordertoplevel = None
		self.vieworderinvoicelevel = None
		self.updateordertoplevel = None
		self.cart_table_created = False

		gv.cart_data = {}

		self.order_depend_thread = Thread(target=lambda: \
												self.get_dependency_master(),
												daemon=True
											)
		self.order_depend_thread.start()

	def get_dependency_master(self):
		def order_list_popup():
			destroy_child(self.order_list_paned)

			self.order_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')
			self.pending_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.complete_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.cancel_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			OrderList(self)

		def pending_order_list_popup():
			destroy_child(self.order_list_paned)

			self.order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.pending_order_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')
			self.complete_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.cancel_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			PendingOrderList(self)

		def complete_order_list_popup():
			destroy_child(self.order_list_paned)

			self.order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.pending_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.complete_order_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')
			self.cancel_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			CompleteOrderList(self)

		def cancel_order_list_popup():
			destroy_child(self.order_list_paned)

			self.order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.pending_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.complete_order_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.cancel_order_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')

			CancelOrderList(self)

		self.order_list_buttons = Frame(self.master, height=48, width=280)

		self.order_list_popup_button = Button(
			self.order_list_buttons, width=12, height=1, text="Order List",
			bg="bg-light", fg="fg-dark", command=lambda: order_list_popup())
		self.pending_order_list_popup_button = Button(
			self.order_list_buttons, column=1, width=13, height=1
			, text="Pending", bg="bg-primary", command=lambda: pending_order_list_popup())
		self.complete_order_list_popup_button = Button(
			self.order_list_buttons, column=2, width=12, height=1
			, text="Complete", bg="bg-primary", command=lambda: complete_order_list_popup())
		self.cancel_order_list_popup_button = Button(
			self.order_list_buttons, column=3, width=12, height=1, padx=(5, 0)
			, text="Cancel", bg="bg-primary", command=lambda: cancel_order_list_popup())

		self.order_list_paned = PanedWindow(
			self.master, orient='vertical', height=gv.h(630),
			width=gv.device_width, row=1, columnspan=4)

		order_list_popup()


class PosInvoice:
	def __init__(self, realself, master, login=False, *args, **kwargs):
		super(PosInvoice, self).__init__(*args, **kwargs)

		realself.master.title("{} - {}".format(
										ltext("pos"),
										gv.st['storename']
									)
								)

		self.realself = realself
		gv.pos_invoice = self
		self.master = master
		self.cart_table_created = False
		self.food_item_data_toplevel = None
		self.add_customer_toplevel = False
		gv.cart_data = {}
		self.view_order_window = None
		self.pos_view_order_window = None
		self.calculator_toplevel = None
		self.viewordertoplevel = None
		self.vieworderinvoicelevel = None
		self.shortcut_key_window_toplevel = None

		self.Customer = StringVar()
		self.CustomerType = StringVar()
		self.Waiter = StringVar()
		self.Table = StringVar()
		self.DelivaryCompany = StringVar()
		self.CookingTime = StringVar()

		if not gv.user_is_authenticated:
			self.EmailField = StringVar()
			self.PasswordField = StringVar()
			self.PasswordData = StringVar()

			realself.master.title("{} - {}".format(
												ltext("login"),
												gv.st['storename']
											)
										)

			self.login_modal_paned = PanedWindow(self.master, bd=0)
			LoginForm(self)

		else:
			realself.master.title("{} - {}".format(
												ltext("pos"),
												gv.st['storename']
											)
										)

			ResturantMenu(gv.rest, gv.rest.master)

			self.pos_order_depend_thread = Thread(
											target=lambda:\
											self.get_dependency_master(),
											daemon=True
										)

			self.pos_order_depend_thread.start()

	def get_dependency_master(self):
		def pos_order_popup():
			destroy_child(self.new_order_paned)

			self.new_order_button.config(bg="#F8F9FA", fg="#000000", state='active')
			self.ongoing_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.today_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.online_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			pop_thr = Thread(target=lambda this=self: PosOrder(this), daemon=True)
			pop_thr.start()

		def ongoing_order_list_popup():
			destroy_child(self.new_order_paned)

			self.ongoing_order_button.config(bg="#F8F9FA", fg="#000000", state='active')

			self.new_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.today_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.online_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			if gv.st['qrmodule']:
				self.qr_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			OngoingOrderList(self)

		def online_order_list_popup():
			destroy_child(self.new_order_paned)

			self.online_order_button.config(bg="#F8F9FA", fg="#000000", state='active')

			self.new_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.ongoing_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.today_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			if gv.st['qrmodule']:
				self.qr_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			OnlineOrderList(self)

		def today_order_list_popup():
			destroy_child(self.new_order_paned)

			self.today_order_button.config(bg="#F8F9FA", fg="#000000", state='active')

			self.new_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.ongoing_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.online_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			if gv.st['qrmodule']:
				self.qr_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			TodayOrderList(self)

		def change_language():
			lang = self.pos_multi_lang.get().lower()

			gv.custom_language = lang
			gv.set_setting()

			pos_order_popup()

		def shortcut_key_window():
			if self.shortcut_key_window_toplevel:
				self.shortcut_key_window_toplevel.destroy()

			self.shortcut_key_window_toplevel = Toplevel(
				width=480, height=(len(gv.shortcut_commands)*30)+8, x=self.shortcut_key_button.winfo_rootx()-416,
				y=self.shortcut_key_button.winfo_rooty()+36, topbar=False)
			self.shortcut_key_window_paned_window = PanedWindow(self.shortcut_key_window_toplevel)

			self.shortcut_key_window_canvas = Canvas(
				self.shortcut_key_window_paned_window, bg='bg-light', mousescroll=False)
			self.shortcut_key_window_paned_window.add(self.shortcut_key_window_canvas)

			gv.main_window.bind('<Button-1>', lambda event: self.shortcut_key_window_toplevel.destroy())

			self.shortcut_key_window_toplevel.transient(gv.main_window)

			item = 0
			for shortcut_key, command in gv.shortcut_commands.items():
				self.shortcut_key_window_canvas.create_rectangle(
					0, item*30, 474, (item+1)*30, fill='#FFF' if item%2==0 else '#DDD', outline='#CCC')

				self.shortcut_key_window_canvas.create_text(
					16, (item * 30) + 14, fill='#374767' if item % 2 == 0 else '#333',
					font=('Calibri', 11), anchor='w', text="{}".format(
						shortcut_key.replace('<', '').replace('>', '')))

				self.shortcut_key_window_canvas.create_text(
					148, (item * 30) + 14, fill='#374767' if item % 2 == 0 else '#333',
					font=('Calibri', 11), anchor='w', text="{}".format(command['name']))

				item += 1

		def cash_counter_check():
			gv.cash_counter = CashRegister().qset.filter(userid=gv.user_id, status=1, sep='and').first()
			if gv.cash_counter:
				globals()['close_counter_icon'] = PhotoImage(
					file=os.path.join(gv.fi_dir, 'cus', 'x-mark-24.png')).subsample(2, 2)
				self.cashcounter_button = Button(
					self.pos_setting_inner, width=56, height=26, compound='center'
					, text='', bg='bg-info', image=globals()['close_counter_icon'],
					pady=0, bd=2, hlbg='black', command=lambda: CloseCashCounter())
			else:
				try:
					url = gv.website + "app/checkregister"
					web_response = requests.post(url, data={'userid': gv.user_id})
					data = web_response.json()['data']
					data.pop('id')

					if data.get('counterstatus'):
						raise Exception('User not registered')
					elif data.get('id'):
						if data.get('status') == 0:
							raise Exception('User not registered')

						register = CashRegister().qset.create(**data)

						gv.shortcut_commands['<Control-p>']['lambda'](None)
					else:
						raise Exception('User not registered')

				except Exception as e:
					gv.error_log(str(e))
					self.open_cash_counter = OpenCashCounter()

		self.pos_button_paned = PanedWindow(self.master, height=40, orient='horizontal')

		self.pos_buttons = Frame(self.pos_button_paned, height=48, width=280)
		self.pos_setting = Frame(self.pos_button_paned, height=48, width=280)

		self.new_order_button = Button(
			self.pos_buttons, width=12, height=1, text="POS Order", font=('Calibri', 11, 'bold'),
			bg="bg-light", fg="fg-dark", command=lambda: pos_order_popup(), abg='fg-light', afg='#37A000')

		self.ongoing_order_button = Button(
			self.pos_buttons, column=1, width=13, height=1,
			font=('Calibri', 11, 'bold'), text="Ongoing Order",
			bg="bg-primary", command=lambda: ongoing_order_list_popup(), abg='fg-light', afg='#37A000')

		self.today_order_button = Button(
			self.pos_buttons, column=2, width=12, height=1,
			font=('Calibri', 11, 'bold'), text="Today Order",
			bg="bg-primary", command=lambda: today_order_list_popup(), abg='fg-light', afg='#37A000')

		self.online_order_button = Button(
			self.pos_buttons, column=3, width=12, height=1, padx=(5, 0),
			font=('Calibri', 11, 'bold'), text="Online Order",
			bg="bg-primary", command=lambda: online_order_list_popup(), abg='fg-light', afg='#37A000')

		self.total_order_count = Button(
			self.pos_buttons, column=4, width=6, padx=0, height=1, text="0",
			bg="#37a000", font=('Calibri', 11, 'bold'),
			hoverbg="#37a000", abg="#37a000", hoverfg="#FFFFFF", command=lambda: online_order_list_popup())

		if gv.st['qrmodule']:
			def qr_order_list_popup():
				destroy_child(self.new_order_paned)

				self.qr_order_button.config(bg="#F8F9FA", fg="#000000", state='active')

				self.new_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
				self.ongoing_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
				self.online_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
				self.today_order_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

				QROrderList(self)

			self.qr_order_button = Button(
				self.pos_buttons, column=5, width=12, height=1, padx=(5, 0), font=('Calibri', 11, 'bold')
				, text="QR Order", bg="bg-primary", command=lambda: qr_order_list_popup(), abg='fg-light', afg='#37A000')
			self.total_qr_order_count = Button(
				self.pos_buttons, column=6, width=6, padx=0, height=1, text="0", bg="#37a000", font=('Calibri', 11, 'bold'),
				hoverbg="#37a000", abg="#37a000", hoverfg="#FFFFFF", command=lambda: qr_order_list_popup())

			orders = QROrder().qset.filter().all()
			self.total_qr_order_count.config(text=len(orders))

		self.pos_setting_inner = Frame(self.pos_setting, sticky='e', height=48, padx=16, pady=0)

		self.shortcut_key_button = Button(
			self.pos_setting_inner, column=1, compound='center', width=56, height=26
			, text='', bg='bg-light', image=ImageFile(os.path.join(gv.fi_dir, 'cus', 'keyboard-3-24.png')).main,
			pady=0, bd=2, hlbg='black', command=lambda: shortcut_key_window())

		langlist = [lang.capitalize() for lang in Language().columns()[2:]]
		self.pos_multi_lang = SelectBox(
			self.pos_setting_inner, width=8, padx=16, ipady=3, column=2,
			font=('Calibri', 12), values=langlist, selectcommand=lambda: change_language())

		self.pos_button_paned.add(self.pos_buttons)
		self.pos_button_paned.add(self.pos_setting)

		self.new_order_paned = PanedWindow(
			self.master, orient='vertical', height=gv.h(630),
			width=gv.device_width, row=1, columnspan=4)

		pop_thr = Thread(target=pos_order_popup, daemon=True)
		pop_thr.start()

		cash_counter_thr = Thread(target=cash_counter_check, daemon=True)
		cash_counter_thr.start()

		orders = OnlineOrder().qset.filter().all()
		self.total_order_count.config(text=len(orders))


class EditOrder:
	def __init__(self, realself, master, order, *args, **kwargs):
		super(EditOrder, self).__init__(*args, **kwargs)

		realself.master.title("Update order '{}' - {}".format(
											order['id'] if order else 0,
											gv.st['storename'])
										)

		self.realself = realself
		self.master = master
		self.order = order
		gv.pos_invoice = self
		self.cart_table_created = False
		self.food_item_data_toplevel = None
		self.add_customer_toplevel = False

		self.bill = Bill().qset.filter(order_id=order['id']).first()

		self.Customer = StringVar()
		self.CustomerType = StringVar()
		self.Waiter = StringVar()
		self.Table = StringVar()
		self.DelivaryCompany = StringVar()
		self.CookingTime = StringVar()

		self.update_order_depend_thread = Thread(target = lambda: \
									self.get_dependency_master(),
									daemon = True
								)

		self.update_order_depend_thread.start()

	def get_dependency_master(self):
		def update_order_popup():
			UpdateOrder(self, order=self.order)

		self.update_order_paned = PanedWindow(
			self.master, orient='vertical', height=gv.h(656),
			width=gv.device_width, row=1, columnspan=4)

		update_order_popup()

def main():
	root = Tk()

	def get_start():
		Order(root)

	thr = Thread(target=get_start, daemon=True)
	thr.start()

	root.mainloop()

if __name__ == "__main__":main()
