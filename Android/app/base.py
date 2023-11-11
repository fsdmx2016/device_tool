
class BaseMethod:
    def __init__(self, dev):
        self.dev = dev

    def get_app_list(self):
        o_=self.dev.list_app()
        return o_
