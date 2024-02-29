#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:31
@Desc    :
"""
import re

from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem

from iOS.app.base import raw_shell


class App_Crash_Log():
    def get_crash_log_list(self, tab_name):
        rsp = raw_shell("tidevice crashreport --list")
        file_names_list = re.findall(r'\S+\.txt', rsp)
        final_list = file_names_list
        # for index, i in enumerate(final_list):
        #     newItem = QTableWidgetItem(i)
        #     tab_name.setItem(0, index, newItem)
        for row_index, data in enumerate(final_list):
            tab_name.insertRow(row_index)
            new_item = QTableWidgetItem(data)
            tab_name.setItem(row_index, row_index, new_item)


    def export_crash_log_list(self, file_path):
        rsp = raw_shell("tidevice crashreport --keep " + file_path)


import sys



