from food.__main__ import Food, FoodCategory, FoodAddOn
from threading import Thread

def food(realself, master):
	if realself and master:
		def get_start():
			food 				= Food(realself=realself, master=master)

		food_thread 			= Thread(target=get_start, daemon=True)
		food_thread.start()

def food_category(realself, master):
	if realself and master:
		def get_start():
			food_category		= FoodCategory(realself=realself, master=master)

		food_category_thread 	= Thread(target=get_start, daemon=True)
		food_category_thread.start()

def food_addon(realself, master):
	if realself and master:
		def get_start():
			food_addon			= FoodAddOn(realself=realself, master=master)

		food_addon_thread 		= Thread(target=get_start, daemon=True)
		food_addon_thread.start()