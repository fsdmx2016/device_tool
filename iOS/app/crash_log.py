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
    def get_crash_log_list(self, table):
        rsp = raw_shell("tidevice crashreport --list")
        file_names_list = re.findall(r'\S+\.txt', rsp)
        final_list = file_names_list

        # 设置表头
        header_labels = ["名称"]
        table.setHorizontalHeaderLabels(header_labels)
        table.setColumnCount(len(header_labels) + 1)  # 设置列数，这里需要多加一列，因为有卸载按钮展示
        table.setRowCount(len(final_list))  # 设置行数

        for row, app_info in enumerate(final_list):
            for col, label in enumerate(header_labels):
                table.setItem(row, col, QTableWidgetItem(app_info[label]))
        # add_table_button(table)  # 每一行的最后一列,添加按钮
        table.show()


    def export_crash_log_list(self, file_path):
        pass



