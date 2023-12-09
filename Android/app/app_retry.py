class AppRetry:
    def __init__(self, dev):
        super().__init__()
        self.dev = dev

    # 录制循环脚本
    def start_save_circulate_script(self,is_save_step):
        is_save_step=True

    def start_script_auto(self,script_name):
        with open(script_name) as f:
            for i in f.readlines():
                pass



