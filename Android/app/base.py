class BaseMethod:
    def __init__(self, dev):
        self.dev = dev

    def get_app_list(self):
        app_list = self.dev.list_app()
        return app_list
