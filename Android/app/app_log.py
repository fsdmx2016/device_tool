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

    def __init__(self, label, dev, parent=None):
        super(LogThread, self).__init__(parent)
        self.label = label
        self.dev = dev

    data_received = pyqtSignal()
    package_name = "com.mt.mtxx.mtxx"

    def run(self):
        while True:
            data = LogThread.get_app_memory(package_name="com.mt.mtxx.mtxx")
            self.update_signal.emit(str(data))

    # 获取应用的内存信息
    @staticmethod
    def get_app_memory(package_name):
        command = f"adb shell dumpsys meminfo {package_name}"
        output = run_adb_command(command)
        if output:
            # 解析输出并提取内存信息
            lines = output.splitlines()
            for line in lines:
                if line.__contains__("TOTAL"):
                    memory_info = line.split()[1]
                    return int(int(memory_info) / 1024)
            return None

    #
    # def run(self):
    #     # 模拟获取数据的操作
    #     while True:
    #         self.data_received.emit()
    #         self.msleep(1000)  # 暂停1秒

    def update_text_edit(self, data):
        self.log_label.append(str(data))
        scrollbar = self.log_label.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        # cursor = self.log_label.textCursor()
        # cursor.movePosition(QTextCursor.End)
        # cursor.insertText(data + "\n")
        # self.log_label .setTextCursor(cursor)
        # self.log_label .ensureCursorVisible()


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
    #
    # def get_current_log(self):
    #     data_thread = DataThread(self.dev, self.log_label)
    #     data_thread.data_received.connect(data_thread.update_text_edit)
    #     data_thread.start()

#
# def get_mem_info(self):
#     # 测试代码
#     package_name = "com.mt.mtxx.mtxx"
#     for i in range(10):
#         memory_usage = get_app_memory(package_name)
#         # if memory_usage:
#         #     print(f"{package_name}的内存占用为: {memory_usage}" + "MB")
#         # else:
#         #     print("无法获取内存占用信息")
#         time.sleep(0.5)
#         self.log_label.append(str(memory_usage))
#         # 滚动到底部
#         scrollbar = self.log_label.verticalScrollBar()
#         scrollbar.setValue(scrollbar.maximum())
