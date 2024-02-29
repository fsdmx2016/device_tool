#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/2/29 15:39
@Desc    :
"""
import os
import time

from PyQt5 import QtWidgets, uic, QtCore
import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QCheckBox, QListWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtGui import QPixmap, QImage, QStandardItemModel

from iOS.app.app_log import LogThread
from iOS.app.crash_log import App_Crash_Log

is_save_step = False
is_start_record = False


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), "ui", "ios.ui")
        uic.loadUi(ui_file_path, self)
        # 加载crash_log文件
        self.init_crash_logs()
        self.init_logs()


    def init_crash_logs(self):
        self.crash_tab_list.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])  # 设置水平表头标签
        crash_log = App_Crash_Log()
        crash_log.get_crash_log_list(self.crash_tab_list)

    def init_logs(self):
        # 加载对应功能
        self.start_get_Log.clicked.connect(self.start_thread)
        self.worker_thread = LogThread( self.show_log)
        self.worker_thread.update_signal.connect(self.update_line_edit)

    def start_thread(self):
        self.worker_thread.start()

    def update_line_edit(self, text):
        self.show_log.append(str(text))
        # 滚动到底部
        scrollbar = self.show_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    myapp.setStyleSheet("#myapp{background-color:blue}")
    sys.exit(app.exec())
