from tkinter import PhotoImage

def style(obj):
	ttk_style 			= obj.Style()
	ttk_style.configure("PopUpButton.TButton", background="#3A95E4", foreground = "#374767", font=('Calibri', 8, "bold"))
	ttk_style.configure("PopUpButton2.TButton", background="#FFFFFF", foreground = "#374767", font=('Calibri', 8, "bold"))
	ttk_style.configure("PopUpButton3.TButton", background="#FFFFFF", foreground = "#45C203", font=('Calibri', 13, "bold"))
	ttk_style.configure("PopUpButton4.TButton", background="#45C203", foreground = "#ff0000", font=('Calibri', 13, "bold"))
	ttk_style.configure("bar.Horizontal.TProgressbar", foreground="#CCCCCC", troughcolor="#000000", bordercolor="red", background="blue", lightcolor="white", darkcolor="orange")
	ttk_style.configure("Title.TLabel", color="#3D9B25", font=('Calibri', 20))
	ttk_style.configure("TLabel", color="#3D9B25", font=('Calibri', 12))
	ttk_style.configure("Custom.TFrame", background="#FFFFFF", foreground="#060606", font=("Calibri", 10))
	ttk_style.configure("Custom2.TFrame", background="#F1F3F6", foreground="#060606", font=("Calibri", 10))
	ttk_style.configure("Custom3.TFrame", background="#45C203", foreground="#060606", font=("Calibri", 10))
	ttk_style.configure("Custom4.TFrame", background="#E7F7DE", foreground="#060606", font=("Calibri", 10))
	ttk_style.configure("FoodThumb.TButton", background="#e4e5e7", foreground = "#374767", font=('Calibri', 7))
	ttk_style.configure("FoodCategoryThumb.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 7))
	ttk_style.configure("FoodCategoryEditDelete.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 6))
	ttk_style.configure("IngredientThumb.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 7))
	ttk_style.configure("IngredientEditDelete.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 6))
	ttk_style.configure("UnitOfMeasurementThumb.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 7))
	ttk_style.configure("UnitOfMeasurementDelete.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 6))
	ttk_style.configure("OrderControl.TButton", background="#37a000", foreground="#060606", font=("Calibri", 10))
	ttk_style.configure("ProductionThumb.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 7))
	ttk_style.configure("ProductionDelete.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 6))
	ttk_style.configure("UnitSubmition.TButton", background="#37a000", activebackground="#45C203", foreground = "#374767", font=('Calibri', 8, "bold"))
	ttk_style.configure("UnitItemDelete.TButton", background="red", activebackground="#45C203", foreground = "red", font=('Calibri', 8, "bold"))
	ttk_style.configure("PurchaseThumb.TButton", background="#e4e5e7", foreground = "#374767", font=('Calibri', 7))
	ttk_style.configure("AddPurchaseSubmition.TButton", background="#37a000", activebackground="#45C203", foreground = "#374767", font=('Calibri', 8, "bold"))
	ttk_style.configure("AddPurchaseItemDelete.TButton", background="red", activebackground="#45C203", foreground = "red", font=('Calibri', 8, "bold"))
	ttk_style.configure("ReturnPurchaseSubmition.TButton", background="#37a000", activebackground="#45C203", foreground = "#374767", font=('Calibri', 8, "bold"))
	ttk_style.configure("ReturnPurchaseItemDelete.TButton", background="red", activebackground="#45C203", foreground = "red", font=('Calibri', 8, "bold"))
	ttk_style.configure("SupplierThumb.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 7))
	ttk_style.configure("SupplierDelete.TButton", background = "#F5F5F5", color = "#FAFAFA", font=('Calibri', 6))
	ttk_style.configure("Search.TButton", font=("Calibri", 8))
	ttk_style.configure("TButton", background="#FFFFFF", foreground = "#374767", font = ('Calibri', 10, "bold"))
	ttk_style.configure("AOPCB.TButton", background="#37a000", foreground = "#374767", font = ('Calibri', 7, "bold"))
	ttk_style.configure("TLabel", color="#3D9B25", font = ('Calibri', 11))
	ttk_style.configure("TNotebook.Tab", background="#3D9B25", foreground="#000000")
