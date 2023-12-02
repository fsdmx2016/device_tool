import os
import subprocess
import time

from PyQt5.QtCore import QThread

from Base import common
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from Base.common import run_adb_command
from PyQt5.QtGui import QTextCursor


class LogThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, dev,label, package_name,parent=None):
        super(LogThread, self).__init__(parent)
        self.label = label
        self.dev = dev
        self.package_name=package_name

    data_received = pyqtSignal()

    def run(self):
        while True:
            data = LogThread.get_app_memory(self)
            self.update_signal.emit(str(data))

    # 获取应用的日志信息
    def get_app_memory(self):
        package_name=str(self.dev.get_top_activity_name()).split("/")[0]
        command = f"adb logcat |grep {package_name}"
        # output = run_adb_command(command)
        output=self.dev.logcat(grep_str=package_name)
        if output:
            # 解析输出并提取内存信息
            lines = str(output).splitlines()
            for line in lines:
                return line
            return None



    def update_text_edit(self, data):
        self.log_label.append(str(data))
        scrollbar = self.log_label.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())



class AppLogMethod():

    def __init__(self, dev, log_label):
        self.dev = dev
        self.log_label = log_label

    # 获取当前的top activity
    def get_log_cat(self, level: str, grep: str, ):
        self.dev.logcat(grep, "*:" + level)

    # 获取指定包名的app_cache日志文件
    def get_app_cache_log(self, package_name: str):
        file_name = str(time.time()).split(".")[0]
        export_log_file_path = os.path.dirname(os.getcwd()) + "\\file" + "\\app_log\\" + file_name + ".txt"
        common.raw_shell("adb logcat -b cache -s " + package_name + " > log.txt")
