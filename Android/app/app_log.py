import os
import time

from Base import common


class AppLogMethod:
    def __init__(self, dev):
        self.dev = dev

    # 获取当前的top activity
    def get_log_cat(self, level: str, grep: str, ):
        self.dev.logcat(grep, "*:" + level)

    # 获取指定包名的app_cache日志文件
    def get_app_cache_log(self, package_name: str):
        file_name = str(time.time()).split(".")[0]
        export_log_file_path = os.path.dirname(os.getcwd()) + "\\file" + "\\app_log\\" + file_name + ".txt"
        common.raw_shell("adb logcat -b cache -s " + package_name + " > log.txt")
