import os, requests
from ntk.objects import gv as gv
from ntk import Button as nButton
from dev_help.widgets import destroy_child


def download_and_save(source, destination, ftype=False):
    if not os.path.exists(destination.rsplit('\\', 1)[0]):
        os.makedirs(destination.rsplit('\\', 1)[0])

    try:
        r = requests.get(source, allow_redirects=True)
        with open(destination + (".{}".format(ftype) if ftype else ""), "wb+") as fl:
            fl.write(r.content)
    except Exception as e:
        gv.error_log(str(e))


def paginator(self, master, obs, canv, target):
    destroy_child(master)

    divider = gv.st["row_per_page"]
    if len(obs)/divider >= gv.st["max_page_per_sheet"]:
        divider = len(obs)//gv.st["max_page_per_sheet"]

    def pagination_command(st):
        def reset_but_st():
            for key, value in master.children.items():
                if key.startswith("!button"):
                    value.config(text="..", bg="#FAFAFA", fg="#337AB7", width=1, state="normal")

            if atm > 1:
                if st != 1:
                    globals()["paginator_but_{}".format(st-1)].config(text="{}".format(st-1), width=4)

                globals()["paginator_but_{}".format(st)].config(text="{}".format(st), width=4, state="active")

                if st != atm:
                    globals()["paginator_but_{}".format(st+1)].config(text="{}".format(st+1), width=4)

                globals()["paginator_but_1"].config(text=gv.ltext("first"), width=4)
                globals()["paginator_but_{}".format(atm)].config(text=gv.ltext("last"), width=4)

        if int(st) == 1:
            target(self, canv, obs[0:divider], obs)
            reset_but_st()

        else:
            reset_but_st()

            sales = obs[(st-1)*divider:st*divider]
            target(self, canv, sales, all=obs)

    if len(obs) % divider == 0:
        atm = int(len(obs)/divider)
    else:
        atm = int(len(obs)/divider)+1

    if atm > 1:
        for sat in range(1, atm+1):
            if sat == 1:
                tx = "First"
            elif sat == atm:
                tx = "Last"
            else:
                tx = sat

            globals()["paginator_but_{}".format(sat)] = nButton(
                master, text="{}".format(tx if sat < 4 or sat == atm else ".."), column=sat, padx=1,
                ipady=10, ipadx=0, width=4 if sat < 4 or sat == atm else 1, height=1, bg="#FAFAFA",
                fg="#007BFF", hoverbg="#EEEEEE", abg="#007BFF", afg="#FFFFFF", hlbg="#000000",
                hlc="#000000", hlt=2, command=lambda st=sat: pagination_command(st), font=("Calibri", 9, 'bold')
            )

    pagination_command(1)


gv.paginator = paginator
