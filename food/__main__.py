from tkinter import ttk
from threading import Thread

from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv

from food.list import FoodList
from food.list_availability import AvailabilityList
from food.list_variant import VariantList
from food.list_category import CategoryList
from food.list_addon import AddOnList
from food.list_addonasign import AddOnAsignList
from ntk import PanedWindow, Frame, Button

# gv.error_log(str(f"File: food/__main__.py"))

class Food:
	def __init__(self, realself, master, *args, **kwargs):
		super(Food, self).__init__(*args, **kwargs)
		realself.master.title("{} - {}".format(ltext("food_section"), gv.st['storename']))
		self.realself = realself
		self.master = master
		self.add_food_current = False
		self.have_this_add_variant = False
		self.editvarianttoplevel = None
		self.addvarianttoplevel = None
		self.addavailabilitytoplevel = None
		self.editavailabilitytoplevel = None

		self.food_depend_thread = Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.food_depend_thread.start()

	def get_dependency_master(self):
		def list_food_popup():
			destroy_child(self.food_list_paned)

			self.food_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')
			self.food_variant_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.food_availability_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')

			FoodList(self)

		def list_availability_popup():
			destroy_child(self.food_list_paned)

			self.food_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.food_variant_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.food_availability_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')

			AvailabilityList(self)

		def list_variant_popup():
			destroy_child(self.food_list_paned)

			self.food_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.food_availability_list_popup_button.config(bg="#007BFF", fg="#FFFFFF", state='normal')
			self.food_variant_list_popup_button.config(bg="#F8F9FA", fg="#000000", state='active')

			VariantList(self)

		self.food_tab_buttons = Frame(self.master, height=48, width=280)

		self.food_list_popup_button = Button(
			self.food_tab_buttons, width=12, height=1, text="Foods",
			bg="bg-light", fg="fg-dark", command=lambda: list_food_popup())
		self.food_variant_list_popup_button = Button(
			self.food_tab_buttons, column=1, width=12, height=1
			, text="Variants", bg="bg-primary", command=lambda: list_variant_popup())
		self.food_availability_list_popup_button = Button(
			self.food_tab_buttons, column=2, width=13, height=1
			, text="Availabilities", bg="bg-primary", command=lambda: list_availability_popup())

		self.food_list_paned = PanedWindow(
			self.master, orient='vertical', height=gv.device_height-106,
			width=gv.device_width, row=1, columnspan=4)

		list_food_popup()


class FoodCategory:
	def __init__(self, realself, master, *args, **kwargs):
		super(FoodCategory, self).__init__(*args, **kwargs)
		realself.master.title("Food category section - {}".format(gv.st['storename']))
		self.master = master
		self.realself = realself

		self.food_category_depend_thread = Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.food_category_depend_thread.start()

	def get_dependency_master(self):
		def list_category_popup():
			CategoryList(self)

		self.food_category_list_panedwindow = get_a_panedwindow(self.master, row=1, padx=5, pady=5, style="Custom.TFrame")

		lcp_thr = Thread(target=list_category_popup, daemon=True)
		lcp_thr.start()


class FoodAddOn:
	def __init__(self, realself, master, *args, **kwargs):
		super(FoodAddOn, self).__init__(*args, **kwargs)
		realself.master.title("Food addon section - {}".format(gv.st['storename']))
		self.master = master
		self.realself = realself
		self.editaddontoplevel = None
		self.addaddontoplevel = None
		self.addaddon_asign_toplevel = None
		self.editaddon_asign_toplevel = None

		self.food_addon_depend_thread = Thread(target = lambda: self.get_dependency_master(), daemon = True)
		self.food_addon_depend_thread.start()

	def get_dependency_master(self):
		def list_addon_asign_popup():
			AddOnAsignList(self)

		def list_addon_popup():
			AddOnList(self)

		self.addon_tab_window = get_a_notebook(self.master, row=1, sticky = "wse", pady=5, padx=5, style="Custom.TFrame")

		self.addon_list_panedwindow = get_a_panedwindow(self.addon_tab_window, padx=0, style="Custom.TFrame")
		self.addon_asign_list_panedwindow = get_a_panedwindow(self.addon_tab_window, padx=0, style="Custom.TFrame")

		add_tab(self.addon_tab_window, self.addon_list_panedwindow, ltext("addons_list"))
		add_tab(self.addon_tab_window, self.addon_asign_list_panedwindow, ltext("addons_asign_list"))

		laap_thr = Thread(target=list_addon_asign_popup, daemon=True)
		lap_thr = Thread(target=list_addon_popup, daemon=True)

		lap_thr.start()
		laap_thr.start()
