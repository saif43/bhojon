
from tkinter import messagebox
from ntk.objects import gv as gv
import sys, _help, os
from ntk import Model


class Model(Model):
	def __init__(self, *args, **kwargs):
		super(Model, self).__init__(*args, **kwargs)

		self.dsql = {'id': {'type': 'int', 'default': 0, 'null': 0}}

	def initialize(self):
		return super(Model, self).initialize()


class CustomerInfo(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CustomerInfo, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS customer_info ( customer_id INTEGER PRIMARY KEY, cuntomer_no text, customer_name text, customer_email text, password text, customer_address text, customer_phone text, customer_picture text, favorite_delivery_address text, is_active BOOLEAN)"

		self.slug('customer_no', null=True)
		self.text('customer_name', null=True)
		self.email('customer_email', null=True)
		self.text('password', null=True)
		self.text('customer_address', null=True)
		self.text('customer_phone', null=True)
		self.text('customer_picture', null=True)
		self.text('favorite_delivery_address', null=True)
		self.boolean('is_active', default='1')

		if init:
			self.initialize()


class SyncResult(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(SyncResult, self).__init__(*args, **kwargs)
		# cursor.execute("CREATE TABLE IF NOT EXISTS sync_result (pk INTEGER PRIMARY KEY, table_name TEXT, last_update DATETIME, last_checked DATETIME, status BOOLEAN, is_active BOOLEAN)")

		self.text('table_name')
		self.datetime('last_update', auto_now_add=True)
		self.datetime('last_checked', auto_now_add=True)
		self.boolean('status', default='0')
		self.boolean('is_active', default='1')

		if init:
			self.initialize()


class CustomerType(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CustomerType, self).__init__(*args, **kwargs)
		# cursor.execute("CREATE TABLE IF NOT EXISTS customer_type ( customer_type_id INTEGER PRIMARY KEY, customer_type text)")

		self.text('customer_type')

		if init:
			self.initialize()


class Employee(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Employee, self).__init__(*args, **kwargs)

		self.slug('employee_id')
		self.slug('pos_id', null=True)
		self.text('first_name', null=True)
		self.text('middle_name', null=True)
		self.text('last_name', null=True)
		self.email('email', null=True)
		self.text('phone', null=True)
		self.text('alter_phone', null=True)
		self.text('present_address', null=True)
		self.text('parmanent_address', null=True)
		self.text('picture', null=True)
		self.text('degree_name', null=True)
		self.text('university_name', null=True)
		self.text('cgp', null=True)
		self.text('passing_year', null=True)
		self.text('company_name', null=True)
		self.text('working_period', null=True)
		self.text('duties', null=True)
		self.text('supervisor', null=True)
		self.text('signature', null=True)
		self.boolean('is_admin', default='0')
		self.int('dept_id', default='0')
		self.int('division_id', default='0')
		self.text('maiden_name', null=True)
		self.text('state', null=True)
		self.text('city', null=True)
		self.int('zip', default='0')
		self.int('citizenship', default='0')
		self.int('duty_type', default='0')
		self.date('hire_date', null=True)
		self.date('original_hire_date', null=True)
		self.date('termination_date', null=True)
		self.text('termination_reason', null=True)
		self.int('voluntary_termination', default='0')
		self.date('rehire_date', null=True)
		self.int('rate_type', default='0')
		self.float('rate', null=True)
		self.int('pay_frequency', default='0')
		self.text('pay_frequency_txt', null=True)
		self.float('hourly_rate2', default='0')
		self.float('hourly_rate3', default='0')
		self.text('home_department', null=True)
		self.text('department_text', null=True)
		self.text('class_code', null=True)
		self.text('class_code_desc', null=True)
		self.date('class_acc_date', null=True)
		self.boolean('class_status', null=True)
		self.int('is_super_visor', default='0')
		self.text('super_visor_id', null=True)
		self.text('supervisor_report', null=True)
		self.date('dob', null=True)
		self.int('gender', default='0')
		self.text('country', null=True)
		self.int('marital_status', default='0')
		self.text('ethnic_group', null=True)
		self.text('eeo_class_gp', null=True)
		self.text('ssn', null=True)
		self.int('work_in_state', default='0')
		self.int('live_in_state', default='0')
		self.text('home_email', null=True)
		self.email('business_email', null=True)
		self.text('home_phone', null=True)
		self.text('business_phone', null=True)
		self.text('cell_phone', null=True)
		self.text('emerg_contct', null=True)
		self.text('emrg_h_phone', null=True)
		self.text('emrg_w_phone', null=True)
		self.text('emgr_contct_relation', null=True)
		self.text('alt_em_contct', null=True)
		self.text('alt_emg_h_phone', null=True)
		self.text('alt_emg_w_phone', null=True)

		if init:
			self.initialize()


class User(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS user ( id INTEGER PRIMARY KEY, firstname text, lastname text, about text, waiter_kitchenToken text, email text, password text, password_reset_token text, image text, last_login datetime, last_logout datetime, ip_address text, status BOOLEAN, is_admin BOOLEAN)"

		self.text('firstname', null=True)
		self.text('lastname', null=True)
		self.text('about', null=True)
		self.text('waiter_kitchenToken', null=True)
		self.email('email')
		self.text('password')
		self.text('password_reset_token', null=True)
		self.text('image', null=True)
		self.datetime('last_login', null=True)
		self.datetime('last_logout', null=True)
		self.text('ip_address', null=True)
		self.text('counter', null=True)
		self.text('UserPictureURL', null=True)
		self.boolean('status', default='1')
		self.boolean('is_admin', default='0')

		if init:
			self.initialize()


class FoodCategory(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(FoodCategory, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS item_category (CategoryID INTEGER PRIMARY KEY, Name TEXT, CategoryImage TEXT, Position INT, CategoryIsActive BOOLEAN, offerstartdate DATETIME, offerendate DATETIME, isoffer BOOLEAN, parentid INT, UserIDInserted INT, UserIDUpdated INT, UserIDLocked INT, DateInserted DATETIME, DateUpdated DATETIME, DateLocked DATETIME)"

		self.text('Name', null=True)
		self.text('CategoryImage', null=True)
		self.int('position', default='0')
		self.boolean('CategoryIsActive', default='1')
		self.datetime('offerstartdate', null=True)
		self.datetime('offerendate', null=True)
		self.boolean('isoffer', default='0')
		self.int('parentid', null=True)
		self.int('UserIDInserted', null=True)
		self.int('UserIDUpdated', null=True)
		self.int('UserIDLocked', null=True)
		self.datetime('DateInserted', auto_now_add=True)
		self.datetime('DateUpdated', auto_now=True)
		self.datetime('DateLocked', null=True)

		if init:
			self.initialize()


class Food(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Food, self).__init__(*args, **kwargs)
		# CREATE TABLE IF NOT EXISTS item_foods (ProductsID INTEGER PRIMARY KEY, CategoryID INT, ProductName TEXT, ProductImage TEXT, bigthumb TEXT, medium_thumb TEXT, small_thumb TEXT, component TEXT, descrip TEXT, itemnotes TEXT, productvat INT, special BOOLEAN, OffersRate INT, offerIsavailable BOOLEAN, offerstartdate DATETIME, offerendate DATETIME, Position INT, ProductsIsActive BOOLEAN, UserIDInserted INT, UserIDUpdated INT, UserIDLocked INT, DateInserted DATETIME, DateUpdated DATETIME, DateLocked DATETIME, FOREIGN KEY (CategoryID) REFERENCES item_category(CategoryID))

		self.int('CategoryID', default='0')
		self.text('ProductName', null=True)
		self.text('ProductImage', null=True)
		self.text('bigthumb', null=True)
		self.text('medium_thumb', null=True)
		self.text('small_thumb', null=True)
		self.text('component', null=True)
		self.text('descrip', null=True)
		self.text('itemnotes', null=True)
		self.float('productvat', default='0.0')
		self.boolean('special', default='0')
		self.int('OffersRate', default='0')
		self.boolean('offerIsavailable', default='0')
		self.datetime('offerstartdate', null=True)
		self.datetime('offerendate', null=True)
		self.int('position', default='0')
		self.boolean('ProductsIsActive', default='1')
		self.int('UserIDInserted', default='0')
		self.int('UserIDUpdated', default='0')
		self.int('UserIDLocked', default='0')
		self.datetime('DateInserted', auto_now_add=True)
		self.datetime('DateUpdated', auto_now=True)
		self.datetime('DateLocked', null=True)

		self.text('menutype', null=True)
		self.int('kitchenid', null=True)
		self.int('isgroup', null=True)
		self.boolean('is_customqty', default='0')
		self.time('cookedtime', default='00:00:00')

		self.foreign('CategoryID', 'FoodCategory', 'id')

		if init:
			self.initialize()


class Varient(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Varient, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS variant (variantid INTEGER PRIMARY KEY, menuid INT, variantName TEXT, price REAL, FOREIGN KEY (menuid) REFERENCES item_foods(ProductsID))"

		self.int('menuid')
		self.text('variantName', null=True)
		self.float('price', default='0.0')
		self.foreign('menuid', 'Varient', 'id')

		if init:
			self.initialize()


class FoodAvailablity(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(FoodAvailablity, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS foodvariable (availableID INTEGER PRIMARY KEY, foodid INT, availtime TEXT, availday TEXT, is_active BOOLEAN, FOREIGN KEY (foodid) REFERENCES item_foods(ProductsID))"

		self.int('foodid')
		self.text('availtime')
		self.text('availday')
		self.boolean('is_active', default='1')
		self.foreign('foodid', 'Food', 'id')

		if init:
			self.initialize()


class AddOn(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(AddOn, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS add_ons (add_on_id INTEGER PRIMARY KEY, add_on_name TEXT, price REAL, is_active BOOLEAN)"

		self.text('add_on_name')
		self.float('price', default='0.0')
		self.boolean('is_active', default='1')

		if init:
			self.initialize()


class AddOnAsign(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(AddOnAsign, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS menu_add_on (row_id INTEGER PRIMARY KEY, menu_id INT, add_on_id INT, is_active BOOLEAN, FOREIGN KEY (add_on_id) REFERENCES add_ons(add_on_id), FOREIGN KEY (menu_id) REFERENCES item_foods(ProductsID))"

		self.int('menu_id')
		self.int('add_on_id')
		self.boolean('is_active', default='1')
		self.foreign('add_on_id', 'AddOn', 'id')
		self.foreign('menu_id', 'Food', 'id')

		if init:
			self.initialize()


class CustomerOrder(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CustomerOrder, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS customer_order (order_id INTEGER PRIMARY KEY, saleinvoice TEXT, customer_id INT, cutomertype INT, isthirdparty INT, waiter_id INT, kitchen INT, order_date DATE, order_time TIME, table_no INT, tokenno TEXT, totalamount REAL, customerpaid REAL, customer_note TEXT, order_status BOOLEAN, order_id_online INT, sync_status BOOLEAN, anyreason TEXT, cookingtime TEXT)"

		self.slug('saleinvoice')
		self.text('marge_order_id', null=True)
		self.int('customer_id')
		self.int('customer_type')
		self.int('isthirdparty', default='0')
		self.int('waiter_id', null=True)
		self.int('kitchen', null=True)
		self.date('order_date', auto_now_add=True)
		self.time('order_time')
		self.int('table_no', default='0')
		self.slug('tokenno', null=True)
		self.float('totalamount', default='0.0')
		self.float('customerpaid', default='0.0')
		self.text('customer_note', null=True)
		self.int('order_status', default='1')
		self.int('order_id_online', default='0')
		self.boolean('sync_status', default='0')
		self.text('anyreason', null=True)
		self.time('cookingtime', null=True)

		if init:
			self.initialize()


class OrderItem(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(OrderItem, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS order_menu (row_id INTEGER PRIMARY KEY, order_id INT, menu_id INT, menuqty REAL, add_on_id TEXT, addonsqty TEXT, varientid INT, food_status BOOLEAN)"

		self.int('order_id')
		self.int('menu_id')
		self.float('menuqty', default='0')
		self.text('add_on_id', null=True)
		self.text('addonsqty', null=True)
		self.int('varientid')
		self.boolean('food_status', default='0')

		if init:
			self.initialize()


class Tables(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Tables, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS rest_table (tableid INTEGER PRIMARY KEY, tablename TEXT, person_capicity INT, table_icon TEXT, status INT)"

		self.text('tablename', null=True)
		self.int('person_capicity', default='0')
		self.text('table_icon', null=True)
		self.boolean('status', default='1')

		if init:
			self.initialize()


class Bill(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Bill, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS bill (bill_id INTEGER PRIMARY KEY, customer_id INT, order_id INT, total_amount REAL, discount REAL, service_charge REAL, VAT REAL, bill_amount REAL, bill_date DATE, bill_time TIME, bill_status BOOLEAN, payment_method_id INT, create_by INT, create_date DATE, update_by INT, update_date DATE)"

		self.int('customer_id')
		self.int('order_id')
		self.float('total_amount', default='0.0')
		self.float('discount', default='0.0')
		self.float('service_charge', default='0.0')
		self.float('VAT', default='0.0')
		self.float('bill_amount', default='0.0')
		self.date('bill_date', null=True)
		self.time('bill_time', null=True)
		self.boolean('bill_status', default='1')
		self.int('payment_method_id', default='4')
		self.int('create_by')
		self.date('create_date', auto_now_add=True)
		self.int('update_by', null=True)
		self.date('update_date', auto_now=True)

		if init:
			self.initialize()


class PaymentMethod(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(PaymentMethod, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS payment_method (payment_method_id INTEGER PRIMARY KEY, payment_method TEXT, is_active BOOLEAN)"

		self.text('payment_method')
		self.boolean('is_active', default='1')

		if init:
			self.initialize()


class BillCardPayment(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(BillCardPayment, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS bill_card_payment (row_id INTEGER PRIMARY KEY, bill_id INT, card_no TEXT, terminal_name INT, bank_name INT)"

		self.int('bill_id')
		self.text('card_no', null=True)
		self.int('terminal_name', default='0')
		self.int('bank_name', default='0')
		self.int('multipay_id', null=True)

		if init:
			self.initialize()


class CardTerminal(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CardTerminal, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS tbl_card_terminal (card_terminalid INTEGER PRIMARY KEY, terminal_name TEXT)"

		self.text('terminal_name')

		if init:
			self.initialize()


class Bank(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Bank, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS tbl_bank (bankid INTEGER PRIMARY KEY, bank_name TEXT, ac_name TEXT, ac_number TEXT, branch TEXT, signature_pic TEXT)"

		self.text('bank_name')
		self.text('ac_name')
		self.text('ac_number')
		self.text('branch')
		self.text('signature_pic', null=True)

		if init:
			self.initialize()


class ThirdPartyCustomer(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(ThirdPartyCustomer, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS tbl_thirdparty_customer (companyId INTEGER PRIMARY KEY, company_name TEXT, address TEXT, commision REAL)"

		self.text('company_name')
		self.text('address', null=True)
		self.float('commision', default='0.0')

		if init:
			self.initialize()


class OnlineOrder(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(OnlineOrder, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS customer_order_onl_ord (order_id INTEGER PRIMARY KEY, saleinvoice TEXT, customer_id INT, cutomertype INT, isthirdparty INT, waiter_id INT, kitchen INT, order_date DATE, order_time TIME, table_no INT, tokenno TEXT, totalamount REAL, customerpaid REAL, customer_note TEXT, order_status BOOLEAN, anyreason TEXT, cookingtime TEXT)"

		self.slug('saleinvoice')
		self.int('customer_id', default='0')
		self.int('cutomertype', default='0')
		self.int('isthirdparty', default='0')
		self.int('waiter_id', default='0')
		self.int('kitchen', default='0')
		self.date('order_date', null=True)
		self.time('order_time', null=True)
		self.int('table_no', default='0')
		self.text('tokenno', null=True)
		self.float('totalamount', default='0.0')
		self.float('customerpaid', default='0.0')
		self.text('customer_note', null=True)
		self.int('order_status', default='0')
		self.text('anyreason', null=True)
		self.time('cookingtime', null=True)

		if init:
			self.initialize()


class OnlineOrderItem(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(OnlineOrderItem, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS order_menu_onl_ord (row_id INTEGER PRIMARY KEY, order_id INT, menu_id INT, menuqty REAL, add_on_id TEXT, addonsqty TEXT, varientid INT, food_status BOOLEAN)"

		self.int('order_id')
		self.int('menu_id')
		self.int('menuqty', default='0')
		self.text('add_on_id', null=True)
		self.text('addonsqty', null=True)
		self.int('varientid', default='0')
		self.boolean('food_status', default='0')

		if init:
			self.initialize()


class BillOnline(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(BillOnline, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS bill_onl_ord (bill_id INTEGER PRIMARY KEY, customer_id INT, order_id INT, total_amount REAL, discount REAL, service_charge REAL, VAT REAL, bill_amount REAL, bill_date DATE, bill_time TIME, bill_status BOOLEAN, payment_method_id INT, create_by INT, create_date DATE, update_by INT, update_date DATE)"

		self.int('customer_id', default='0')
		self.int('order_id', default='0')
		self.float('total_amount', default='0.0')
		self.float('discount', default='0.0')
		self.float('service_charge', default='0.0')
		self.float('VAT', default='0.0')
		self.float('bill_amount', default='0.0')
		self.date('bill_date', null=True)
		self.time('bill_time', null=True)
		self.boolean('bill_status', default='1')
		self.int('payment_method_id', default='0')
		self.int('create_by', null=True)
		self.datetime('create_date', null=True)
		self.int('update_by', null=True)
		self.datetime('update_date', null=True)

		if init:
			self.initialize()


class BillCardPaymentOnline(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(BillCardPaymentOnline, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS bill_card_payment_onl_ord (row_id INTEGER PRIMARY KEY, bill_id INT, card_no TEXT, terminal_name INT, bank_name INT)"

		self.int('bill_id')
		self.text('card_no')
		self.int('terminal_name', default='0')
		self.int('bank_name', default='0')

		if init:
			self.initialize()


class Language(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Language, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS language (id INTEGER PRIMARY KEY, phrase TEXT, english TEXT DEFAULT '')"

		self.text('phrase', null=True)
		self.text('english', null=True)

		if init:
			self.initialize()


class Currency(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Currency, self).__init__(*args, **kwargs)
		# "CREATE TABLE IF NOT EXISTS currency (currencyid INTEGER PRIMARY KEY, currencyname TEXT, curr_icon TEXT, position TEXT, curr_rate REAL)"

		self.text('currencyname')
		self.text('curr_icon', null=True)
		self.text('position', null=True)
		self.float('curr_rate', default='0.0')

		if init:
			self.initialize()


class Setting(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(Setting, self).__init__(*args, **kwargs)
		# cursor.execute("CREATE TABLE IF NOT EXISTS setting (id INTEGER PRIMARY KEY, title TEXT, storename TEXT, address TEXT, email TEXT, phone TEXT, logo TEXT, favicon TEXT, opentime TEXT, closetime TEXT, vat REAL, discount_type BOOLEAN, service_chargeType BOOLEAN, currency INT, min_prepare_time TEXT, language TEXT, timezone TEXT, dateformat TEXT, site_align TEXT, powerbytxt TEXT, footer_text TEXT, row_per_page INT, max_page_per_sheet INT, sync_short_delay TEXT, sync_long_delay TEXT, stock_validation BOOLEAN)")

		self.text('title', default="Bhojon")
		self.text('storename', default="Dhaka Restaurant")
		self.text('address', default="Dhaka")
		self.email('email', default="bhojon@gmail.com")
		self.text('phone', default="8801845400000")
		self.text('logo', default=os.path.join("application", "modules", "dependancy", "images", "logo.png"))
		self.text('favicon', default=os.path.join("application", "modules", "dependancy", "images", "favicon"))
		self.time('opentime', default="09:00:00")
		self.time('closetime', default="22:00:00")
		self.float('vat', default=5.0)
		self.boolean('discount_type', default='0')
		self.boolean('service_chargeType', default='0')
		self.float('service_charge', default='0')
		self.int('currency', default="BDT")
		self.text('min_prepare_time', default="1 hour")
		self.text('language', default="english")
		self.text('timezone', null=True)
		self.text('dateformat', default="yyyy/mm/dd")
		self.text('powerbytxt', default="Powered By: BDTASK, www.bdtask.com")
		self.text('footer_text', default="2017©Copyright")
		self.int('row_per_page', default=30)
		self.int('max_page_per_sheet', default=20)
		self.text('sync_short_delay', default="00:05")
		self.text('sync_long_delay', default="01:00")
		self.boolean('stock_validation', default='0')
		self.int('position', default='0')
		self.float('curr_rate', default='0.0')
		self.text('site_align', default='LTR')
		self.text('curr_icon', null=True)
		self.boolean('qrmodule', default='0')

		if init:
			self.initialize()


class MultiPay(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(MultiPay, self).__init__(*args, **kwargs)

		self.int('order_id')
		self.text('marge_order_id', null=True)
		self.int('payment_type_id')
		self.int('amount', default='0')
		self.boolean('is_active', default='1')

		if init:
			self.initialize()


class PosSetting(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(PosSetting, self).__init__(*args, **kwargs)

		self.boolean('waiter', default=1)
		self.boolean('tableid', default=1)
		self.boolean('cooktime', default=1)

		if init:
			self.initialize()


class CashCounter(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CashCounter, self).__init__(*args, **kwargs)

		self.int('counterno', default=1)

		if init:
			self.initialize()


class CashRegister(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CashRegister, self).__init__(*args, **kwargs)

		self.int('userid', null=True)
		self.int('counter_no', null=True)
		self.float('opening_balance', default='0.0')
		self.float('closing_balance', default='0.0')
		self.date('openclosedate', null=True)
		self.datetime('opendate', default='1970-01-01 01:01:01')
		self.datetime('closedate', default='1970-01-01 01:01:01')
		self.boolean('status', default='1')
		self.text('openingnote', default=' ')
		self.text('closing_note', default=' ')
		self.foreign('userid', 'User', 'id')
		self.foreign('counter_no', 'CashCounter', 'id')

		if init:
			self.initialize()


class CashRegisterPaymentHistory(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(CashRegisterPaymentHistory, self).__init__(*args, **kwargs)

		self.int('register_number')
		self.int('payment_method')
		self.float('amount', default='0.0')
		self.foreign('payment_method', 'PaymentMethod', 'id')
		self.foreign('register_number', 'CashRegister', 'id')

		if init:
			self.initialize()


class ItemFoodType(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(ItemFoodType, self).__init__(*args, **kwargs)

		self.text('menutype', default=' ')
		self.text('menu_icon', default=' ')
		self.boolean('status', default=True)

		if init:
			self.initialize()


class SubOrder(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(SubOrder, self).__init__(*args, **kwargs)

		self.int('order_id')
		self.int('customer_id')
		self.float('vat', default=0.0)
		self.float('discount', default=0.0)
		self.float('s_charge', default=0.0)
		self.float('total_price', default=0.0)
		self.boolean('status', default=True)
		# self.int('order_variant_id')
		self.int('order_menu_id')
		# self.float('order_menu_quantity')
		self.text('adons_id', null=True)
		self.text('adons_qty', null=True)

		if init:
			self.initialize()


class QROrder(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(QROrder, self).__init__(*args, **kwargs)

		self.text('cooked_time', default="00:15:00")
		self.int('customer_id')
		self.text('customer_note', null=True)
		self.text('cuntomer_no', null=True)
		self.int('cutomertype', null=True)
		self.int('saleinvoice', null=True)
		self.text('kitchen', null=True)
		self.date('order_date')
		self.int('order_status')
		self.time('order_time')
		self.int('orderd')
		self.float('paidamount', default=0.0)
		self.text('reason', null=True)
		self.int('table_no')
		self.int('thirdparty', default=0)
		self.int('token', default=0)
		self.float('totalamount', default=0.0)
		self.int('waiter_id', null=True)

		if init:
			self.initialize()


class QRBill(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(QRBill, self).__init__(*args, **kwargs)

		self.float('VAT', default=0.0)
		self.float('bill_amount', default=0.0)
		self.date('bill_date')
		self.int('bill_id')
		self.int('bill_status', default='0')
		self.date('bill_time')
		self.int('create_by')
		self.date('create_date', auto_now_add=True)
		self.int('customer_id')
		self.date('delivarydate', null=True)
		self.float('discount', default=0.0)
		self.int('order_id')
		self.int('payment_method_id', null=True)
		self.float('service_charge', default=0.0)
		self.int('shipping_type', null=True)
		self.float('total_amount', default=0.0)
		self.int('update_by', default='0')
		self.date('update_date', auto_now=True)

		if init:
			self.initialize()


class QROrderMenu(Model):
	def __init__(self, init=0, *args, **kwargs):
		super(QROrderMenu, self).__init__(*args, **kwargs)

		self.text('add_on_id', default=' ')
		self.text('addonsqty', default=' ')
		self.int('food_status', default='0')
		self.int('menu_id')
		self.int('menuqty')
		self.int('order_id')
		self.int('row_id', null=True)
		self.int('varientid')

		if init:
			self.initialize()
