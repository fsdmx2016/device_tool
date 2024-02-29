#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:08
@Desc    :
"""
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QVBoxLayout

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
    # 设置表头,修饰数据
    header_labels = ["包名", "名称", "版本号"]
    table.setHorizontalHeaderLabels(header_labels)
    table.setColumnCount(len(header_labels)+1)  # 根据表头数量设置列数
    table.setRowCount(len(app_list))
    # 循环遍历app_list并将数据添加到表格中
    for row, app_info in enumerate(app_list):
        for col, label in enumerate(header_labels):
            table.setItem(row, col, QTableWidgetItem(app_info[label]))
    # 获取行数
    row_count = table.rowCount()
    for row in range(row_count):
        # 创建按钮
        button = QPushButton("卸载")
        button.clicked.connect(lambda checked, row=row: on_button_click(row))  # 使用lambda绑定行号
        # 创建布局并添加按钮
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.setContentsMargins(0, 0, 0, 0)  # 可能需要调整边距以适应单元格

        # 创建容器QWidget
        container_widget = QWidget()
        container_widget.setLayout(layout)

        # 计算最后一列索引
        last_column = table.columnCount() - 1

        # 将容器添加到表格的最后一列
        table.setCellWidget(row, last_column, container_widget)


    table.show()
    # return app_list

def on_button_click(row):
    print(f"Button at row {row} was clicked!")

# app安装
def install_app(self, file_path):
    shell_ = "tidevice install " + file_path
    rsp = common.raw_shell(shell_)
    if rsp.__contains__("Complete"):
        return "success"
    else:
        return "安装失败！"
# app卸载
def un_install_app(self, app_package_name):
    rsp = common.raw_shell("tidevice uninstall " + app_package_name)
    if rsp.__contains__("Complete"):
        return "success"
    else:
        return "卸载失败！"
