#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 18:41
@Desc    :
"""
import subprocess

from typing import Optional
# shell执行
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QVBoxLayout, QWidget

from iOS.app.app_manager import on_button_click


def raw_shell(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    stdout = result.stdout
    return stdout

# 操作表格
def operate_table(table,rsp_data,header_labels:Optional[list]=None,):
    # 设置表头
    if header_labels:
        table.setHorizontalHeaderLabels(header_labels)
    table.setColumnCount(len(header_labels) + 1)  # 设置列数，这里需要多加一列，因为有卸载按钮展示
    table.setRowCount(len(rsp_data))  # 设置行数
    for row, app_info in enumerate(rsp_data):
        for col, label in enumerate(header_labels):
            table.setItem(row, col, QTableWidgetItem(app_info[label]))

    # add_table_button(table,function,button_name)  # 每一行的最后一列,添加按钮
    # table.show()

def add_table_button(table,function,button_name):
    for row in range(table.rowCount()):
        button = QPushButton(button_name)
        # 按钮点击事件
        button.clicked.connect(lambda checked, row=row: function(row,table))  # 使用lambda绑定行号
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.setContentsMargins(0, 0, 0, 0)
        # 创建容器QWidget
        container_widget = QWidget()
        container_widget.setLayout(layout)
        # 计算最后一列索引
        last_column = table.columnCount() - 1
        # 将容器添加到表格的最后一列
        table.setCellWidget(row, last_column, container_widget)
