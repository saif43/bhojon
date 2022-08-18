from tkinter import Variable
from ntk.objects import gv as gv
import os, sys

from database.synchronization.down.addon import Addon
from database.synchronization.down.addonasign import AddonAsign
from database.synchronization.down.availability import Availability
from database.synchronization.down.bank import Bank
from database.synchronization.down.cardterminal import CardTerminal
from database.synchronization.down.category import Category
from database.synchronization.down.customer import Customer
from database.synchronization.down.customertype import CustomerType
from database.synchronization.down.food import Food
from database.synchronization.down.language import Language
from database.synchronization.down.onlineorder import OnlineOrder
from database.synchronization.down.payment import Payment
from database.synchronization.down.setting import Setting
from database.synchronization.down.table import Table
from database.synchronization.down.thirdparty import ThirdParty
from database.synchronization.down.varient import Varient
from database.synchronization.down.waiter import Waiter
from database.synchronization.down.toggleorder import ToggleOrder
from database.synchronization.down.possetting import PosSetting
from database.synchronization.down.counter import ResCounter
from database.synchronization.down.qrorder import QROrder
from database.synchronization.up.cashregister import CashRegister

from database.synchronization.up.order import Order

from database.table import Setting as tbSetting, Language as tbLanguage, PosSetting as tbPosSetting


def check_ico_filetype():
	if not gv.st['favicon'].endswith('ico'):
		mfp = gv.st['favicon'].rsplit('.', 1)
		mfpp = os.path.join(gv.file_dir, mfp[0] + '.' + 'ico')
		if not os.access(mfpp, os.F_OK):
			img = Image.open(os.path.join(gv.file_dir, gv.st['favicon']))
			img.save(mfpp, 'ico')
		gv.st['favicon'] = mfp[0] + '.' + 'ico'


def setting(init=0):
	gv.setting_table = gv.st = tbSetting(init=init).qset.filter().first()
	gv.pos_setting = gv.pst = tbPosSetting(init=init).qset.filter().first()

	if not gv.setting_table:
		tbSetting().qset.create(id=1)
		gv.setting_table = gv.st = tbSetting().qset.filter().first()

	if not gv.pos_setting:
		tbPosSetting().qset.create(id=1)
		gv.setting_table = gv.st = tbSetting().qset.filter().first()

	if gv.st['favicon'] != "":
		check_ico_filetype()
		gv.icon_dir = gv.st['favicon']
		gv.icon_path = os.path.join(gv.file_dir, gv.st['favicon'])

	if gv.st['language'] == "": gv.st['language'] = "english"
	if gv.custom_language: gv.st['language'] = gv.custom_language

	try:
		gv.phases = [r['phrase'] for r in tbLanguage().qset.filter(search="phrase").all()]
		gv.elabels = [r['english'] for r in tbLanguage().qset.filter(search="english").all()]
		gv.labels = [r[gv.st['language']] for r in tbLanguage().qset.filter(search=gv.st['language']).all()]
	except Exception as e: gv.error_log(str(e))


def user(data=None):
	if not data: return

	gv.user_id = data['id'] if data else 00
	gv.user_firstname = data['firstname'] if data else "No User"
	gv.user_lastname = (data['lastname'] if data['lastname'] else "") if data else ""
	gv.user_about = data['about'] if data else ""
	gv.user_email = data['email'] if data else ""
	gv.user_password = data['password'] if data else ""
	gv.user_last_login = data['last_login'] if data else ""
	gv.user_last_logout = data['last_logout'] if data else ""
	gv.user_ip_address = data['ip_address'] if data else ""
	gv.user_status = data['status'] if data else 0
	gv.user_is_admin = data['is_admin'] if data else 0
	gv.user_picture_url = data['image'] if data else 0

	gv.user_is_authenticated = True


def set_path():
	# gv hocche global Variable
	gv.application_dir = "application"
	gv.install_dir = os.path.join("application", "install") 
	gv.modules_dir = os.path.join("application", "modules")
	gv.fi_dir = os.path.join("application", "icons")
	gv.itemmanage_dir = os.path.join("application", "modules", "itemmanage")
	gv.assets_dir = os.path.join("application", "modules", "itemmanage", "assets")
	gv.image_dir = os.path.join("application", "modules", "itemmanage", "assets", "images")
	gv.user_image_dir = os.path.join("application", "modules", "itemmanage", "assets", "images", "user")
	gv.depend_dir = os.path.join("application", "modules", "dependancy")
	gv.depend_image_dir = os.path.join("application", "modules", "dependancy", "images")
	gv.invoice_dir = os.path.join("application", "modules", "invoices")

	if not os.path.exists(gv.install_dir): os.makedirs(gv.install_dir)
	if not os.path.exists(gv.user_image_dir): os.makedirs(gv.user_image_dir)
	if not os.path.exists(gv.depend_image_dir): os.makedirs(gv.depend_image_dir)
	if not os.path.exists(gv.invoice_dir): os.makedirs(gv.invoice_dir)

	gv.application_path = os.path.join(gv.file_dir, gv.application_dir)
	gv.install_path = os.path.join(gv.file_dir, gv.install_dir)
	gv.modules_path = os.path.join(gv.file_dir, gv.modules_dir)
	gv.fi_path = os.path.join(gv.file_dir, gv.fi_dir)
	gv.itemmanage_path = os.path.join(gv.file_dir, gv.itemmanage_dir)
	gv.assets_path = os.path.join(gv.file_dir, gv.assets_dir)
	gv.image_path = os.path.join(gv.file_dir, gv.image_dir)
	gv.user_image_path = os.path.join(gv.file_dir, gv.user_image_dir)
	gv.depend_image_path = os.path.join(gv.file_dir, gv.depend_image_dir)
	gv.depend_path = os.path.join(gv.file_dir, gv.depend_dir)
	gv.invoice_path = os.path.join(gv.file_dir, gv.invoice_dir)

	try:
		gv.icon_dir = gv.store_favicon + ".ico"
	except: gv.icon_dir = os.path.join(gv.depend_image_dir, "favicon.ico")

	try:
		gv.icon_path = os.path.join(gv.file_dir, gv.store_favicon) + ".ico"
	except: gv.icon_path = os.path.join(gv.depend_image_path, "favicon.ico")

	gv.msi = None
	gv.maq = None
	gv.mse = None
	gv.mayn = None

	gv.language = "english"

	sys.path.append(os.path.join(gv.install_path, 'gs'))


def set_gv():
	# gv.static_root = gv.file_dir
	gv.user_is_authenticated = False
	gv.cash_counter = False
	gv.sync_loop_stop = False
	gv.sync_list = []
	gv.gl, gv.gbl = {}, {}
	gv.cancel_reason_master = None
	gv.timepicker = None
	gv.sds_lab = None
	gv.lds_lab = None
	gv.sodu_lab = None
	gv.s_sdbt = None
	gv.custom_language = None
	gv.split_order_window = None
	gv.split_order_payment_top = None
	gv.sub_order_list_view_window = None
	gv.split_order_invoice_view_window = None
	gv.split_order_session = {
		'orders': {}
	}

	# Not working with gv.website
	# if gv.website != "":
	# 	if not gv.website.endswith("/"):
	# 		gv.website = gv.website + "/"
	# 	if not gv.website.startswith("http"):
	# 		gv.website  = "https://" + gv.website

	gv.tablelist = [
		"addon", "addonasign", "availability", "bank", "cardterminal", "category", "customer", "customertype",
		"food", "language", "onlineorder", "payment", "setting", "table", "thirdparty", "varient", "waiter",
		"order", "synced_order", "pos_setting", "counter", "qr_order", "cashregister"
	]

	gv.tbltextlist = [
		gv.ltext("food_addons"), gv.ltext("asigned_addon"), gv.ltext("food_availabilities"),
		gv.ltext("bank_list"), gv.ltext("card_terminal_list"), gv.ltext("food_categories"),
		gv.ltext("customer_list"), gv.ltext("customer_types"), gv.ltext("foods"), gv.ltext("languages"),
		gv.ltext("online_orders"), gv.ltext("payment_method"), gv.ltext("application_settings"),
		gv.ltext("table_list"), gv.ltext("delivary_companies"), gv.ltext("food_varients"),
		gv.ltext("staff_user_list"), gv.ltext("offline_orders"), gv.ltext("synced_order"),
		gv.ltext("pos_setting"), gv.ltext("counter"), gv.ltext("qr_order"), gv.ltext('cashregister')
	]

	gv.sync_class_l = [
		Addon, AddonAsign, Availability, Bank, CardTerminal, Category, Customer,
		CustomerType, Food, Language, OnlineOrder, Payment, Setting, Table, ThirdParty,
		Varient, Waiter, Order, ToggleOrder, PosSetting, ResCounter, QROrder, CashRegister
	]
