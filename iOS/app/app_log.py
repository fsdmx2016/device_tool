#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 18:25
@Desc    :
"""
import subprocess
from typing import Optional
#
#
# class App_Log():
#     content = None
#
#     def realtime_syslog(self, exit, log_find: Optional[str] = None):
#         if log_find:
#             command = 'tidevice syslog |grep ' + log_find
#         else:
#             command = 'tidevice syslog'
#         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#
#         while True:
#             global content
#             output = process.stdout.readline().decode().strip()
#             if output == '' and process.poll() is not None:
#                 break
#             if output:
#                 self.update_line_edit(exit, text=output)
#
#     def update_line_edit(self, exit, text):
#         exit.append(str(text))
#         scrollbar = exit.verticalScrollBar()
#         scrollbar.setValue(scrollbar.maximum())


import sys

from Android.app.common import run_adb_command
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class LogThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, label, parent=None):
        super(LogThread, self).__init__(parent)
        self.label = label
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
        # 循环获取最新1s的日志
        run_shell='tidevice syslog'
        output = run_adb_command(run_shell)
        if output:
            lines = output.splitlines()
            return lines

    def run_adb_command(self,command):
        try:
            output = subprocess.check_output(command, shell=True)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            print("运行ADB命令时出错:", e)
            return None

    def update_text_edit(self, data):
        self.show_log.append(str(data))
        scrollbar = self.show_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())