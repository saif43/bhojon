from license.__main__ import License
from threading import Thread

def license(realself=None, master=None):
    if realself and master:
        def get_start():
            lw      = License(realself, master)

        lth         = Thread(target=get_start, daemon=True)
        lth.start()
