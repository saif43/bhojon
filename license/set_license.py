from dev_help.widgets import *
from ntk.objects import gv as gv
from ntk import Button, Canvas, Entry
import os, string, random, order, requests, _help, time, socket, subprocess
from order.snippets.order import get_order_cart
from __restora__.global_ import setting, set_gv
from __restora__.dependancy import setting_table
from dev_help.ph_entry import PHEntry
from dev_help.tooltip import ToolTip
from threading import Thread
from PIL import Image, ImageTk
from database.table import *


class SetLicense:
    def __init__(self, realself, *args, **kwargs):
        super(SetLicense, self).__init__(*args)
        self.realself       = realself

        self.get_dependency_master()

    def debug(this, n):
        li_f = os.path.join(gv.file_dir, "license.txt")
        with open(li_f, "a+") as f:
            f.write('Debug =====>' + str(n) + '\n')
        
        f.close()

    def start_setup(this, domain):
        # this.debug(1.1)
        self                = this.realself
        self.ProgressValue  = DoubleVar()
        # this.debug(1.2)

        def now_go():
            # this.debug(1.3)
            this.set_phases(domain=domain)
            # this.debug(1.4)

        this.sph_th         = Thread(target=now_go, daemon=True)
        this.sph_th.start()

    def set_phases(this, domain):
        # this.debug('1.3.1')
        self = this.realself
        path = os.path.join(gv.install_path, "phrase.txt")

        with open(path, "r+") as ptf:
            # this.debug('1.3.2')
            rd          = ptf.read()
            ph_l        = rd.split(", ")

            self.setup_bar      = get_a_progressbar(self.lse_w_paned, self.ProgressValue, length=400, max=len(ph_l), row=2)

            self.progres_canv.itemconfig(self.brand_text, text="Please wait ({}%)".format(0))
            self.license_submit_button.config(state="disabled")

            w = self.progres_canv.winfo_width()

            self.progres_canv.create_window(int(int(w)/2), 40, window=self.setup_bar, height=18)

            text="Setting up database, please wait.."
            self.progres_canv.itemconfig(self.brand_text, text=text)
            self.ProgressValue.set(0)
            cr_list = []

            Language().initialize()
            Language().qset.delete_all()

            # this.debug('1.3.3')

            static_website = domain

            for i, t in enumerate(ph_l):
                while True:
                    try:
                        label, ph_done, la_done = "", False, False


                        try:
                            # this.debug('1.3.4')
                            data 	= {"phrase[]": "{}".format(t)}
                            # this.debug(data)
                            r 		= requests.post(static_website + "app/addPhrase", data=data)
                            # this.debug('1.3.6')
                            Language().qset.create(phrase=t)
                            ph_done = True
                            # this.debug('1.3.7')
                        except Exception as e: 
                            gv.error_log(str(e))

                        for s in t.split("_"):
                            label = label + s + " "

                        try:
                            # this.debug('1.3.8')
                            data 	= {
                                "language": "english",
                                "phrase[]": "{}".format(t),
                                "lang[]": label.capitalize()
                            }

                            # this.debug('1.3.9')
                            
                            result = requests.post(static_website + "app/addLebel", data=data)

                            # this.debug('1.3.10')

                            Language().qset.update(**{'english':label.capitalize(), 'phrase': t}, where='phrase')
                            la_done = True
                            # this.debug('1.3.11')
                        except Exception as e: 
                            # this.debug('1.3.12')
                            gv.error_log(str(e))
                            
                            # ! Throw Error from here

                        # this.debug('1.3.13')
                        self.ProgressValue.set(i)
                        self.progres_canv.itemconfig(self.brand_text, text="Please wait ({}%)".format(int(self.ProgressValue.get()/(len(ph_l)/100))))
                        gv.rest.master.update_idletasks()

                        # this.debug('1.3.14')

                        if ph_done is True and la_done is True: break

                    except Exception as e:
                        # this.debug('1.3.15')
                        gv.error_log(str(e))
                        time.sleep(1)

            
            # this.debug('1.3.16')
            Language().qset.create_all(cr_list)

            # this.debug('1.3.17')
            setting_table()
            # this.debug('1.3.18')

            set_gv()
            # this.debug('1.3.19')
            setting()
            # this.debug('1.3.20')

            for tbl in [
                CustomerInfo, SyncResult, CustomerType, Employee, User, FoodCategory, Food, Varient,
                FoodAvailablity, AddOn, AddOnAsign, CustomerOrder, OrderItem, Tables, Bill, PaymentMethod,
                BillCardPayment, CardTerminal, Bank, ThirdPartyCustomer, OnlineOrder, OnlineOrderItem,
                BillOnline, BillCardPaymentOnline, Language, Currency, Setting, PosSetting, MultiPay,
                CashCounter, CashRegister, ItemFoodType, SubOrder, QROrder,
                QRBill, QROrderMenu, CashRegisterPaymentHistory
            ]:
                tbl().initialize()
                time.sleep(0.1)

            # this.debug('1.3.21')

            tbl_l = [r['table_name'] for r in SyncResult().qset.filter(search='table_name').all()]

            for table in gv.tablelist:
                if not table in tbl_l:
                    SyncResult().qset.create(**{'table_name': table, 'is_active': 1})

            # this.debug('1.3.22')

            try:
                def change_status(t, s=True):
                    text = "{} {}".format(gv.tbltextlist[gv.tablelist.index(t)], "updating..." if s else "updated")
                    self.progres_canv.itemconfig(self.brand_text, text=text)

                gv.deep_sync = True
                gv.rstatus_l = Label()
                self.ProgressValue.set(0)

                for ix, tbl in enumerate(gv.tablelist):
                    change_status(tbl)
                    gv.sync_class_l[ix](self)
                    self.ProgressValue.set((180/len(gv.tablelist))*(ix+1))
                    change_status(tbl, False)
                    time.sleep(1)

                gv.deep_sync = False

            except Exception as e:
                gv.error_log(str(e))
                _help.messagew(root=gv.rest.master, msg1=ltext("synchronization_error"), msg2=ltext("synchronization_exit"), error=True)


            # this.debug('1.3.23')
            self.realself.master.iconbitmap(gv.icon_path)

            gv.get_order_cart 				= get_order_cart
            destroy_child(self.realself.resturant_frame)
            order.pos_order(self.realself, self.realself.resturant_frame)
            # this.debug('1.3.24')

        # this.debug('1.3.N')

    def set_license(this):
        try:
            socket.create_connection(("www.google.com", 80))
        except:
            _help.messagew(msg1="ERROR", msg2="Internet connection required", error=True)
            return

        self                = this.realself

        product_key         = self.ProductKey.get()
        opurchase_key       = self.PurchaseKey.get()
        domain              = self.WebAddress.get()
        domain_prefix       = domain.split('://')

        # this.debug(1)
        this.start_setup(domain=domain)
        # this.debug(2)
        return

        try:
            url = "https://store.bdtask.com/class.bhojondesktop.php?domain={}&product_key={}&purchase_key={}&is_http={}".format(
                domain_prefix[1].rsplit('/', 1)[0], product_key, opurchase_key, domain_prefix[0] + '://'
            )
            # url = "https://store.bdtask.com/alpha2/class.api.php?product_key={}&purchase_key={}&domain={}".format(product_key, opurchase_key, domain)

            r   = requests.get(url).json()
            status = r['status']

        except Exception as e:
            gv.error_log(str(e))
            status, et = False, "Something wrong, please try again later"

        if status and type(status) == bool:
            l1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']

            l2 = ['=', 'i', 'Z', "'", ' ', 'k', 'K', 'h', '{', '\x0c', 'c', '\x0c', '\x0c', '\\', ':', ']', 'V', 'T', 'G', '|', '^', ']', 'N', 'I', '`', 'r', '+', '*', ':', ' ', 'O', 'C', 'V', 'P', '<', 'M', 'o', 'F', '@', '^', 'z', "'", '+', 'K', "'", 's', 'm', '^', '&', '{', 'Q', '}', 'U', '.', 'n', 'z', '~', 'C', '#', 'V', '*', '_', 'l']

            purchase_key    = ""
            secret_key      = ""
            secret_key_in   = ""

            rk = product_key
            pk = opurchase_key
            sk = ""
            ski = ""
            sark = ""
            sarki = ""

            try:
                startupinfo             = subprocess.STARTUPINFO()
                startupinfo.dwFlags     |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

                sak                     = str(subprocess.check_output('wmic csproduct get uuid', stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT, startupinfo=startupinfo).split()[1].strip(), 'utf-8')
            except Exception as e:
                gv.error_log(str(e))
                err = _help.messagew(root=gv.rest.master, msg1=ltext("something_went_wrong"), msg2=ltext("please_try_again_later_or_contact_us"), error=True)
                if err.result == "OK":
                    gv.rest.master.destroy()

            li_f = os.path.join(gv.file_dir, "license.txt")
            with open(li_f, "w+") as f:
                f.close()

            try:
                with open(li_f, "a+") as f:
                    for c in opurchase_key:
                        sk += l2[l1.index(c)]
                        ski += str(l1.index(c)) + ":"

                    for c in sak:
                        sark += l2[l1.index(c)]
                        sarki += str(l1.index(c)) + ":"

                    ski = ski.rsplit(":", 1)[0]
                    sarki = sarki.rsplit(":", 1)[0]

                    if (len(pk) == len(sk) == len(ski.split(":"))) and (len(sak) == len(sark) == len(sarki.split(":"))):
                        dn = "restora"
                        wn = domain

                        pk = ''.join((str(b) + '\'') for b in bytes(pk, 'ascii'))
                        sak = ''.join((str(s) + '\'') for s in bytes(sak, 'ascii'))
                        pk = pk.rsplit('\'', 1)[0]
                        sak = sak.rsplit('\'', 1)[0]

                        f.write("product_key: " + rk + "\n")
                        f.write("purchase_key: " + pk + "\n")
                        f.write("secret_key: " + sk + "\n")
                        f.write("secret_key_in: " + str(ski) + "\n")
                        f.write("secret_app_key: " + sak + "\n")
                        f.write("secret_app_rkey: " + sark + "\n")
                        f.write("secret_app_rkey_in: " + sarki + "\n")
                        f.write("database: " + dn + "\n")
                        f.write("website: " + wn)

                    f.close()

                gv.db_name              = dn + ".db"
                gv.db_timeout           = 10
                static_website              = wn

                this.start_setup()
            except Exception as e: gv.error_log(str(e))

        else:
            _help.messagew(msg1="Invalid", msg2="{}".format("Please input right license and product key \nAnd input your full url. ex: https://bdtask.com/"), error=True)

    def get_dependency_master(this):
        self                            = this.realself

        file_path 	= os.path.join(gv.assets_path, "img", "bg.jpg")
        img_file 	= Image.open(file_path)
        img_file.thumbnail((gv.device_height, gv.device_height), Image.ANTIALIAS)
        globals()["background_image_1"] = ImageTk.PhotoImage(file=file_path)

        self.lse_w_canv                 = Canvas(self.lse_w_paned, width=gv.device_width, height=gv.device_height, bg="#000000", highlightbackground="#000000", mousescroll=False)
        self.form_canv                  = Canvas(self.lse_w_paned, width=gv.wpc*464, height=gv.hpc*364, bg="#EEFFE6", highlightbackground="#EEFFE6", mousescroll=False)

        self.lse_w_canv.create_window(int(gv.device_width/2), int(gv.device_height/2)-100, window=self.form_canv, height=364)
        self.lse_w_canv.create_image(gv.device_width/2, gv.device_height/2, image=globals()["background_image_1"])

        self.progres_canv                   = Canvas(self.lse_w_paned, width=gv.wpc*464, height=gv.hpc*124, bg="#EEFFE6", highlightbackground="#EEFFE6", mousescroll=False)
        self.lse_w_canv.create_window(int(gv.device_width/2), int(gv.device_height/2)+160, window=self.progres_canv, height=124)

        w = gv.wpc*464
        self.brand_text                 = self.progres_canv.create_text(int(int(w)/2), 80, text="Fill up all the field with valid license and url", font=('Arial', int(gv.wpc*10)), fill='#374767')

        self.form_canv.create_text(int(int(w)/2)-196, 50, text="Purchase key *", font=("Arial", int(gv.wpc*10)), anchor="w", fill='#374767')
        self.purchase_key_data          = PHEntry(self.lse_w_paned, placeholder="Please enter your purchase key", column=1, textvariable=self.PurchaseKey, width=48, font=("Arial", 11), padx=(10, 3))
        self.form_canv.create_window(int(int(w)/2), 80, window=self.purchase_key_data, height=36)

        trl = [self.purchase_key_data.foc_in, self.purchase_key_data.focus, self.purchase_key_data.focus_displayof, self.purchase_key_data.focus_force, self.purchase_key_data.focus_get, self.purchase_key_data.focus_lastfor, self.purchase_key_data.focus_set]

        self.form_canv.create_text(int(int(w)/2)-196, 130, text="Product key *", font=("Arial", int(gv.wpc*10)), anchor="w", fill='#374767')
        self.product_key_data           = PHEntry(self.lse_w_paned, placeholder="Please enter your product key", row=1, column=1, textvariable=self.ProductKey, width=48, font=("Arial", 11), padx=(10, 3))
        self.form_canv.create_window(int(int(w)/2), 160, window=self.product_key_data, height=36)

        self.form_canv.create_text(int(int(w)/2)-196, 210, text="Website url *", font=("Arial", int(gv.wpc*10)), anchor="w", fill='#374767')
        self.website_address_data       = PHEntry(self.lse_w_paned, placeholder="Please give your url", row=1, column=1, textvariable=self.WebAddress, width=48, font=("Arial", 11), padx=(10, 3))
        self.form_canv.create_window(int(int(w)/2), 240, window=self.website_address_data, height=36)

        self.license_submit_button      = Button(self.lse_w_paned, row=2, column=1, text="Activate Software", bg="bg-success", hoverbg='bg-light', ipadx=10, ipady=8, pady=36, command=lambda: this.set_license(), hlc='bg-success', bd=2)
        self.form_canv.create_window(int(int(w)/2)+112, 304, window=self.license_submit_button, width=128, height=26)

        for ent in [self.purchase_key_data, self.product_key_data, self.website_address_data]:
            ent.config(bd=0, bg="#F5F5F5", highlightbackground="#85E0FB", highlightthickness=1)
            ent.bind('<Return>', lambda e: this.set_license())

    def cancel(self):
        li_f = os.path.join(gv.file_dir, "license.txt")
        with open(li_f, "w+") as f:
            f.close()

        gv.rest.master.destroy()