import sys

from Android.app.common import run_adb_command
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class LogThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, dev, label, package_name, parent=None):
        super(LogThread, self).__init__(parent)
        self.label = label
        self.dev = dev
        self.package_name = package_name

    data_received = pyqtSignal()

    def run(self):
        while True:
            data = LogThread.get_app_memory(self)
            self.update_signal.emit(str(data))

    def get_sys_info(self):
        if sys.platform.startswith('win'):
            return "windows"
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return "linux"

    # 获取应用的日志信息
    def get_app_memory(self):
        package_name = str(self.dev.get_top_activity_name()).split("/")[0]
        # 循环获取最新1s的日志

        run_shell = "adb logcat -v time -T $(date +%s) -d | grep -F \"$(date --date='1 second ago' +%s)\" | grep \""+package_name+"\""

        output = run_adb_command(run_shell)
        if output:
            lines = output.splitlines()
            return lines


    def update_text_edit(self, data):
        self.log_label.append(str(data))
        scrollbar = self.log_label.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
#
#
# class AppLogMethod():
#
#     def __init__(self, dev, log_label):
#         self.dev = dev
#         self.log_label = log_label
#
#     # 获取当前的top activity
#     def get_log_cat(self, level: str, grep: str, ):
#         self.dev.logcat(grep, "*:" + level)
#
#     # 获取指定包名的app_cache日志文件
#     def get_app_cache_log(self, package_name: str):
#         file_name = str(time.time()).split(".")[0]
#         export_log_file_path = os.path.dirname(os.getcwd()) + "\\file" + "\\app_log\\" + file_name + ".txt"
#         common.raw_shell("adb logcat -b cache -s " + package_name + " > log.txt")
