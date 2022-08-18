from _help.showinfo import ShowInfo
from _help.showerror import ShowError
from _help.askyesno import AskYesNo
from _help.askquestion import AskQuestion
from ntk.objects import gv as gv


class MessageW:
    def __init__(self, r, *args, **kwargs):
        super(MessageW, self).__init__()

        if kwargs.get("info") == True:
            if gv.msi: gv.msi.destroy()

            ShowInfo(r, self, args, kwargs)

        if kwargs.get("error") == True:
            if gv.mse: gv.mse.destroy()

            ShowError(r, self, args, kwargs)

        if kwargs.get("yesno") == True:
            if gv.mayn: gv.mayn.destroy()

            AskYesNo(r, self, args, kwargs)

        if kwargs.get("question") == True:
            if gv.maq: gv.maq.destroy()

            AskQuestion(r, self, args, kwargs)

        else: pass
