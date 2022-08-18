from _help.__main__ import MessageW

class messagew:
    def __init__(self, root=None, *args, **kwargs):
        super(messagew, self).__init__()
        self.root   = root
        self.args   = args
        self.kwargs = kwargs

        try:
            if kwargs.get("info") == True:
                self.info   = MessageW(self.root, self.args, self.kwargs, info=True)
                self.get_result()

            if kwargs.get("error") == True:
                self.info   = MessageW(self.root, self.args, self.kwargs, error=True)
                self.get_result()

            if kwargs.get("yesno") == True:
                self.info   = MessageW(self.root, self.args, self.kwargs, yesno=True)
                self.get_result()

            if kwargs.get("question") == True:
                self.info   = MessageW(self.root, self.args, self.kwargs, question=True)
                self.get_result()

            else: pass
        except Exception as e: gv.error_log(str(e))

    def get_result(self):
        self.result = self.info.result
