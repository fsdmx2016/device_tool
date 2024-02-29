#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/2/29 15:39
@Desc    :
"""
import os
import subprocess

from PyQt5.QtCore import QProcess, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QApplication

from iOS.app.base import raw_shell
from iOS.app.crash_log import App_Crash_Log

is_save_step = False
is_start_record = False

class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), "ui", "ios.ui")
        uic.loadUi(ui_file_path, self)
        # 判断设备是否连接，且为usb


        # 加载crash_log文件
        self.init_crash_logs()
        # 日志文件相关
        self.init_logs()
        # 默认-app列表
        self.device_app_list.addItems(self.raw_shell('tidevice applist'))


    def init_crash_logs(self):
        self.crash_tab_list.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])  # 设置水平表头标签
        crash_log = App_Crash_Log()
        crash_log.get_crash_log_list(self.crash_tab_list)

    def init_logs(self):
        self.start_get_Log.clicked.connect(lambda: self.get_current_log())
        self.stop_get_Log.clicked.connect(lambda: self.process.terminate())
        self.clear_log.clicked.connect(lambda: self.show_log.setText(''))


    # app管理开始
    def init_app_manager(self):
        from iOS.app import app_manager
        app_manager.get_app_list(self.app_table_list)


    # 日志文件相关开始
    def get_current_log(self):
        self.process = OutputReader()
        self.process.outputReady.connect(self.update_output)
        # 启动命令
        self.process.start('tidevice', ['syslog'])

    def update_output(self, text):
        # 将新的输出内容追加到文本编辑器中
        cursor = self.show_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.show_log.setTextCursor(cursor)
        self.show_log.ensureCursorVisible()

    # 日志文件相关结束

    # app列表相关开始
    def raw_shell(self, command: str):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        stdout = result.stdout
        return stdout.split("\n")

    # app列表相关结束


class OutputReader(QProcess):
    outputReady = pyqtSignal(str)

    def __init__(self, parent=None):
        super(OutputReader, self).__init__(parent)
        self.readyReadStandardOutput.connect(self.handle_stdout)
        self.readyReadStandardError.connect(self.handle_stderr)

    def handle_stdout(self):
        data = self.readAllStandardOutput().data().decode()
        self.outputReady.emit(data)

    def handle_stderr(self):
        data = self.readAllStandardError().data().decode()
        self.outputReady.emit(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    myapp.setStyleSheet("#myapp{background-color:blue}")
    sys.exit(app.exec())
