#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:08
@Desc    :
"""
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QVBoxLayout, QMessageBox

from Base import common


# 获取应用
def get_app_list(table):
    rsp = common.raw_shell("tidevice applist").split("\n")[:-1]
    app_list = []
    for i in rsp:
        app_info = {"包名": "", "名称": "", "版本号": ""}
        app_info["包名"] = i.split(" ")[0]
        app_info["名称"] = i.split(" ")[1]
        app_info["版本号"] = i.split(" ")[2]
        app_list.append(app_info)
    # 设置表头
    header_labels = ["包名", "名称", "版本号"]
    table.setHorizontalHeaderLabels(header_labels)

    table.setColumnCount(len(header_labels) + 1)  # 设置列数，这里需要多加一列，因为有卸载按钮展示
    table.setRowCount(len(app_list))  # 设置行数

    for row, app_info in enumerate(app_list):
        for col, label in enumerate(header_labels):
            table.setItem(row, col, QTableWidgetItem(app_info[label]))
    add_table_button(table)  # 每一行的最后一列,添加按钮
    table.show()


def add_table_button(table):
    for row in range(table.rowCount()):
        button = QPushButton("卸载")
        # 按钮点击事件
        button.clicked.connect(lambda checked, row=row: on_button_click(row,table))  # 使用lambda绑定行号
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


def on_button_click(row,table):
    un_install_app(row,table)


# app安装
def install_app(file_path):
    shell_ = "tidevice install " + file_path
    rsp = common.raw_shell(shell_)
    if rsp.__contains__("Complete"):
        messageBox = QMessageBox(QMessageBox.Information, "提示", "安装成功")
        messageBox.button(QMessageBox.Ok)
        messageBox.exec()
    else:
        messageBox = QMessageBox(QMessageBox.Information, "提示", "安装失败")
        messageBox.button(QMessageBox.Ok)
        messageBox.exec()



# app卸载
def un_install_app(app_package_name,table):
    rsp = common.raw_shell("tidevice uninstall " + app_package_name)
    if rsp.__contains__("Complete"):
        messageBox = QMessageBox(QMessageBox.Information, "提示", "卸载成功")
        messageBox.button(QMessageBox.Ok)
        messageBox.exec()
        # 重新加载一下列表
        get_app_list(table)
    else:
        messageBox = QMessageBox(QMessageBox.Information, "提示", "卸载失败")
        messageBox.button(QMessageBox.Ok)
        messageBox.exec()
