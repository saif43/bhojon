from dev_help.widgets import *
from dev_help.database import *
from ntk.objects import gv as gv

class Notify:
    def __init__(self, realself, *args, **kwargs):
        super(Notify, self).__init__(*args)
        self.master               = master = Toplevel()
        master.geometry("{}x320+{}+{}".format(w(520), int((gv.device_width-w(520))/2), int((gv.device_height-320)/2)))
        master.resizable(0, 0)
        self.realself             = realself
        self.var                  = kwargs.get("var")
        self.text                 = kwargs.get("text")
        self.text_2               = kwargs.get("text_2")
        self.title                = kwargs.get("title")
        self.returned             = kwargs.get("returned")
        self.button               = kwargs.get("button")

        if self.button and self.button != 0:
            def close_notify(iv):
                self.master.destroy()
                self.returned(iv)
                gv.rest.master.bind("<Return>", lambda e: close_notify(4))
                return iv

            self.data 						= kwargs.get("data")
            gv.notify 	                    = self
            master.configure(background="#FFFFFF")
            master.title(self.title if self.title else ltext("notification"))
            self.master.iconbitmap(gv.icon_path)

            master.grid_rowconfigure(0, weight=1)
            master.grid_columnconfigure(0, weight=1)

            self.modal_canv 		        = get_a_canvas(master, width=520, height=320, mousescroll=False, background='#FFFFFF')

            self.modal_canv.create_text(w(520)/2, 64, fill='#000000', font=('Calibri', h(15), 'bold'), text=self.text, width=w(500))
            self.modal_canv.create_text(w(520)/2, 144, fill='#000000', font=('Calibri', h(14), 'bold'), text=self.text_2, width=w(500))

            for i in range(0, int(self.button)):
                globals()["button_%s_text"%i] = kwargs.get("button_{}_text".format(i+1)) if kwargs.get("button_{}_text".format(i+1)) else "Button 1"

                globals()['btr_%s'%i] = self.modal_canv.create_rectangle(w(60) if i==0 else w(280), 208, w(240) if i==0 else w(460), 272, fill=kwargs["background_%s"%(i+1)] if kwargs.get("background_%s"%(i+1), 0) else '#37A000', outline='#F1F3F6')
                globals()['btt_%s'%i] = self.modal_canv.create_text(w(150) if i==0 else w(370), 240, fill='#FFFFFF', font=('Calibri', h(10), 'bold'), text=globals()["button_%s_text"%i], anchor='center')

                canvas_mouse_el(self.modal_canv, globals()['btr_%s'%i])
                canvas_mouse_el(self.modal_canv, globals()['btt_%s'%i])

                self.modal_canv.tag_bind(globals()['btr_%s'%i], '<Button-1>', lambda e, iv=i: close_notify(iv))
                self.modal_canv.tag_bind(globals()['btt_%s'%i], '<Button-1>', lambda e, iv=i: close_notify(iv))

            gv.rest.master.bind("<Return>", lambda e: close_notify(1))
