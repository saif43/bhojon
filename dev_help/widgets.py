from tkinter import *
from tkinter import ttk
from dev_help.timepicker import TimePicker
from ntk.objects import gv as gv
import requests, pyperclip

def w(w=0.1):
	return int(w*gv.wpc)

def h(h=0.1):
	return int(h*gv.hpc)

gv.w = w
gv.h = h

def ltext(t):
	if t not in gv.phases:
		gv.set_setting()

	if t in gv.phases:
		ind = gv.phases.index(t)
		lt = gv.labels[ind] if gv.labels[ind] not in [None, ""] else gv.elabels[ind]
	else:
		return (" ".join(s for s in t.split('_'))).capitalize()
	return lt if lt else ""

def mousewheel_scroll(canv, event):
	canv.yview_scroll(int(-1*(event.delta/120)), "units")

def add_tab(nb, child, text, width=16):
	width = width
	sp = ""
	for i in range(0, width-len(text) if width > len(text) else 1):
		sp = sp + " "
	nb.add(child, text = "{}{}{}".format(sp, text, sp))

def get_a_notebook(master, row=0, column=0, sticky="wn", rowspan=1, columnspan=1, padx=(20, 20), pady=(20, 20), style=None):
	notebook = ttk.Notebook(master)
	notebook.grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady)
	if style: notebook.config(style=style)

	return notebook

def get_a_panedwindow(master, row=0, column=0, orient=0, width=1000, height=1000, sticky='wn', rowspan=1, padx=(20, 20), pady=(20, 20), columnspan=1, ignore_ttk=False, background="#FFFFFF", style=None):
	if ignore_ttk:
		panedwindow = PanedWindow(master, background=background)
	else: panedwindow = ttk.PanedWindow(master)

	if orient: panedwindow.config(orient=orient)

	panedwindow.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=columnspan)
	if style: panedwindow.config(style=style)

	return panedwindow

def get_a_frame(master, background="#FFFFFF", ignore_ttk=None, use_pack=False, side=None, width=1, height=1, row=0, column=0, rowspan=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky='w', style=None):
	if ignore_ttk:
		frame = Frame(master, width = w(width), height = h(height), bg=background)
	else: frame = ttk.Frame(master, width = w(width), height = h(height))

	frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
	if style: frame.config(style=style)

	return frame

def canvas_mouse_el(canvas, item, cursor="hand2", cursor_out="arrow", tip=False, text=""):
	def entered():
		canvas.config(cursor=cursor)
		if tip:
			cs = canvas.coords(item)
			ws = (cs[0]+(((len(text)*8) if len(text) < 16 else 16*8)+20))
			hs = cs[1]+(((len(text) if len(text)>15 else 16)/16)*24)

			gv.gbl['{}-tipr-{}'.format(canvas, item)] = canvas.create_rectangle(cs[0]+20, cs[1], ws, hs, fill="#000000", outline="#37A000")
			gv.gbl['{}-tipt-{}'.format(canvas, item)] = canvas.create_text(cs[0]+24, cs[1]+6, fill="#FFFFFF", text=text, anchor='nw', width=ws-(cs[0]+24), font=('Calibri', 9, 'bold'))

	def leaved():
		canvas.config(cursor=cursor_out)
		if tip:
			canvas.delete(gv.gbl['{}-tipr-{}'.format(canvas, item)])
			canvas.delete(gv.gbl['{}-tipt-{}'.format(canvas, item)])

			gv.gbl.pop('{}-tipr-{}'.format(canvas, item))
			gv.gbl.pop('{}-tipt-{}'.format(canvas, item))

	canvas.tag_bind(item, '<Enter>', lambda x: entered())
	canvas.tag_bind(item, '<Leave>', lambda x: leaved())

def get_a_canvas(master, background="#FFFFFF", highlightbackground="#FFFFFF", scrollregion=[0,0,720,0], relief=FLAT, width=1, height=1, row=0, column=0, rowspan=1, columnspan=1, padx=(0, 0), pady=(0, 0), mousescroll=True):
	canvas = Canvas(master, width=w(width), height=h(height), scrollregion=[w(i) for i in scrollregion], relief=relief, background=background, highlightbackground=highlightbackground, highlightcolor=highlightbackground, selectbackground="#37A000")
	canvas.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady)
	if mousescroll: canvas.bind("<MouseWheel>", lambda e, canv=canvas: mousewheel_scroll(canv, e))

	def set_focus(e):
		if canvas.type(CURRENT) != "text":
			return

		canvas.focus_set()
		canvas.focus(CURRENT)
		canvas.select_from(CURRENT, 0)
		canvas.select_to(CURRENT, END)

		canvas.bind("<Control-c>", lambda e: pyperclip.copy("{}".format(canvas.selection_get())))

	canvas.bind("<Double-Button-1>", lambda e: set_focus(e))

	return canvas

def get_a_combobox(frame, values, width=20, height=10, font=("Calibri", 10), row=0, column=0, padx=(10, 10), pady=(10, 10), sticky='w', default=False, readonly=False, rest=1):
	if rest: font = (font[0], h(font[1])-1, font[2] if len(font)>2 else 'normal')
	cobmocheck = ttk.Combobox(frame, values=values, width=w(width), height=h(height), font=font)
	cobmocheck.grid(row=row, column=column, padx=padx, pady=pady, ipady=2, sticky=sticky)
	if default: cobmocheck.set(values[0])
	if readonly: cobmocheck.config(state="readonly")

	return cobmocheck

def get_a_foreign_combo(frame, values, width=20, height=10, row=0, column=0, padx=(10, 10), pady=(10, 10), sticky='w'):
	foreigncheck = ttk.Combobox(frame, values=values, width=w(width), height=h(height))
	foreigncheck.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

	return foreigncheck

def get_a_button(frame, text="Button", width=20, row=0, column=0, columnspan=1, bg="#37a000", fg="#FFFFFF", padx=(7, 7), pady=(0, 0), ipadx=0, ipady=10, cursor="hand2", relief="groove", use_ttk=True, style=None, image=None, compound="image", font=("Calibri", 10, "bold"), abg="#F0F0F0", afg="#374767", rest=1):
	if rest: font = (font[0], w(font[1])-1, font[2] if len(font)>2 else 'normal')
	if use_ttk:
		button = ttk.Button(frame, text=text, width=w(width), cursor=cursor)
	else:
		button = Button(frame, text=text, width=w(width), bg=bg, fg=fg, cursor=cursor, relief=relief, bd=0, font=font, activebackground=abg, activeforeground=afg)
	button.grid(row=row, column=column, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
	if style: button.config(style=style)
	if image: button.config(image=image, compound=compound)

	return button

def get_a_entry(frame, textvariable=None, width=24, font=('Calibri', 11), row=0, column=0, columnspan=1, rowspan=1, padx=(10, 10), pady=(10, 10), ipady=2, justify="left", sticky='w', default="", use_ttk=True, state="normal", rest=1):
	if rest: font = (font[0], h(font[1])-1, font[2] if len(font)>2 else 'normal')
	if use_ttk:
		entry = ttk.Entry(frame, width=w(width), font=font, justify=justify)
		entry.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=pady, ipady=ipady, sticky=sticky)
	else:
		entry = Entry(frame, width=w(width), font=font, justify=justify, fg="#374767", bg="#F0F0F0")
		entry.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=pady, ipady=ipady, sticky=sticky)
		entry.config(state=state)
	entry.insert(0, default)
	if textvariable is not None: entry.config(textvariable=textvariable)
	return entry

def get_a_text(frame, width=24, height=20, font=('Calibri', 10), row=0, column=0, columnspan=1, rowspan=1, padx=(10, 10), pady=(10, 10), relief=FLAT, sticky='w', rest=1):
	if rest: font = (font[0], h(font[1])-1, font[2] if len(font)>2 else 'normal')
	text = Text(frame, width=w(width), height=height, font=font, relief=relief)
	text.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=pady, sticky=sticky)
	return text

def get_a_label(frame, text="Label", textvariable=None, decoration="lower", width=None, image = None, compound = "center", font=('Calibri', 8), row=0, column=0, rowspan=1, columnspan=1, padx=(10, 10), pady=(10, 10), ipady=0, sticky='w', ignore_ttk=None, style=None, rest=1):
	if rest: font = (font[0], w(font[1])-1, font[2] if len(font)>2 else 'normal')
	if image is not None:
		if ignore_ttk:
			label = Label(frame, text=text.capitalize() if decoration=="lower" else text.upper(), image = image, compound = compound, font=font)
		else: label = ttk.Label(frame, text=text.capitalize() if decoration=="lower" else text.upper(), image = image, compound = compound, font=font)

	else:
		if ignore_ttk:
			label = Label(frame, text=text.capitalize() if decoration=="lower" else text.upper(), font=font)
		else: label = ttk.Label(frame, text=text.capitalize() if decoration=="lower" else text.upper(), font=font)

	label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, ipady=ipady, sticky=sticky)
	if style: label.config(style=style)
	if width: label.config(width=w(width))
	if textvariable: label.config(textvariable=textvariable)

	return label

def get_a_radio(frame, text="Radio", variable=None, value=None, row=0, column=0, padx=(10, 10), pady=(10, 10), sticky='w'):
	radio = ttk.Radiobutton(frame, text=text, variable=variable)
	radio.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
	if value is not None: radio.config(value=value)

	return radio

def get_a_checkbutton(frame, text="", variable=None, row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="w", use_ttk=True, style=None):
	if use_ttk:
		check = ttk.Checkbutton(frame, text=text, variable=variable)
	else: check = Checkbutton(frame, text=text, variable=variable)

	check.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
	if style: check.config(style=style)

	return check

def get_a_scrollbar(frame, frame_on, orient = VERTICAL, width=4, row = 0, column = 1, columnspan = 1, padx = (0, 0), pady = (0, 0), sticky = "ns"):
	bar = Scrollbar(frame, orient = orient, width=4)
	bar.grid(row = row, column = column, columnspan = columnspan, padx = padx, pady = pady, sticky = sticky)
	if orient == HORIZONTAL:
		bar.config(command = frame_on.xview)
		frame_on.config(xscrollcommand = bar.set)
	else:
		bar.config(command = frame_on.yview)
		frame_on.config(yscrollcommand = bar.set)

	return bar

def get_a_progressbar(frame, variable, orient=HORIZONTAL, max=100, length=100, row=0, column=0, columnspan=1, padx=(0, 0), pady=(0, 0)):
	pbar = ttk.Progressbar(frame, orient=orient, max=max, length=length, variable=variable)
	pbar.grid(row = row, column = column, columnspan = columnspan, padx = padx, pady = pady)

	return pbar

def show_clock(event, widget, u=0, d=0, r=0, l=0):
	if gv.timepicker: gv.timepicker.destroy()

	x, y, h = (widget.winfo_rootx() + (r if r!=0 else 0)) - (l if l!=0 else 0), (widget.winfo_rooty() - (u if u!=0 else 0)) + (d if d!=0 else 0), widget.winfo_height()

	window = TimePicker(x, y + h, widget)
	return window

def destroy_child(master):
	try:
		for child in master.winfo_children(): child.destroy()
	except Exception as e: gv.error_log(str(e))

gv.ltext = ltext
