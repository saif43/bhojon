from dev_help.widgets import *
from ntk.objects import gv as gv
from license.set_license import SetLicense
from order.snippets.order import get_order_cart
from __restora__.global_ import setting, set_gv

import os, string, random, subprocess, order, time, _help

l1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']

l2 = ['=', 'i', 'Z', "'", ' ', 'k', 'K', 'h', '{', '\x0c', 'c', '\x0c', '\x0c', '\\', ':', ']', 'V', 'T', 'G', '|', '^', ']', 'N', 'I', '`', 'r', '+', '*', ':', ' ', 'O', 'C', 'V', 'P', '<', 'M', 'o', 'F', '@', '^', 'z', "'", '+', 'K', "'", 's', 'm', '^', '&', '{', 'Q', '}', 'U', '.', 'n', 'z', '~', 'C', '#', 'V', '*', '_', 'l']

class CheckLicense:
    def __init__(self, realself=None, *args, **kwargs):
        super(CheckLicense, self).__init__(*args)
        self.realself           = realself

        self.get_dependency_master()

    def get_dependency_master(this):
        try:
            self          = this.realself
            fdone         = False
            lfd           = {}

            startupinfo             = subprocess.STARTUPINFO()
            startupinfo.dwFlags     |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            lfd['udk']              = str(subprocess.check_output('wmic csproduct get uuid', stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT, startupinfo=startupinfo).split()[1].strip(), 'utf-8')

            # lfd['udk']      = str(subprocess.check_output('wmic csproduct get uuid').split()[1].strip(), 'utf-8')
        except Exception as e:
            gv.error_log(str(e))
            err = _help.messagew(root=gv.rest.master, msg1=ltext("something_went_wrong"), msg2=ltext("please_try_again_later_or_contact_us"), error=True)
            if err.result == "OK":
                gv.rest.master.destroy()

        li_f = os.path.join(gv.file_dir, "license.txt")
        if os.path.exists(li_f):
            with open(li_f, "r+") as f:
                for line in f.readlines():
                    k, v = line.split(': ')
                    lfd[k] = v.replace('\n', '')

            def done_on(ie, il, rie):
                fdone = True
                for i,c in enumerate(ie):
                    if l1.index(c) == il[i] and l2[l1.index(c)] == rie[i]:
                        continue
                    else:
                        fdone = False
                        break
                return fdone

            try:
                lfd['fski'] = [int(i) for i in lfd['secret_key_in'].split(':')] if lfd.get('secret_key_in', False) else []
                lfd['fsdrki'] = [int(i) for i in lfd['secret_app_rkey_in'].split(':')] if lfd.get('secret_app_rkey_in', False) else []
                fdone = True
            except Exception as e:
                gv.error_log(str(e))
                fdone = False

            try:
                pk = bytes([int(k) for k in lfd.get('purchase_key', '').split('\'')]).decode()
                sk = lfd.get('secret_key', '')
                fski = lfd['fski']
                sak = bytes([int(k) for k in lfd.get('secret_app_key', '').split('\'')]).decode()
                sark = lfd.get('secret_app_rkey', '')
                fsdrki = lfd['fsdrki']
            except Exception as e:
                gv.error_log(str(e))
                pk, sk, fski, sak, sark, sarki, fdone = '', '', [], '', '', [], False

            if pk != "BDTASK-bhojon-OFFLINE-DEMO-000000" and sak != "NO-DEVICE-ATTACHED-WITH-DEMO-bhojon-OFFLINE":
                if len(pk) == 0 or len(sk) == 0 or len(fski) == 0 or len(sak) == 0 or len(sark) == 0 or len(fsdrki) == 0 or len(pk.split('-')) == 0:
                    fdone = False
                elif (len(pk) == len(sk) == len(fski)) and (len(sak) == len(sark) == len(fsdrki)) and (len(pk.split('-')) == 5) and fdone:
                    if sak == lfd['udk']:
                        fdone = done_on(sak, fsdrki, sark)
                    else: fdone = False

                    if fdone:
                        fdone = done_on(pk, fski, sk)
            else: fdone = False
        
        fdone = False

        if fdone:
            gv.db_name              = (lfd['database'] if lfd.get('database', False) else "restora") + ".db"
            gv.db_timeout           = 10
            gv.website              = lfd['website']

            set_gv()
            setting()

            self.realself.master.iconbitmap(gv.icon_path)

            gv.get_order_cart 				= get_order_cart
            destroy_child(self.realself.resturant_frame)
            order.pos_order(self.realself, self.realself.resturant_frame)

        else:
            setlic = SetLicense(this.realself)