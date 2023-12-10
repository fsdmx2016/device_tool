import os
import time
import shutil

from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QMessageBox


class AppRetry:
    def __init__(self, dev):
        super().__init__()
        self.dev = dev

    # 录制循环脚本
    def start_save_circulate_script(self, is_save_step):
        is_save_step = True

    def run_script_(self, script_name):
        script_name = os.getcwd() + "\\script_file\\" + script_name + ".txt"
        file_path = "D:\WorkDemo\My_Work\device_tool_git\Android\script_file\step.txt"
        with open(file_path, 'r') as f_input:
            for line in f_input:
                # 判断是不是首行
                first_time = 1
                if line.__contains__("first_line"):
                    first_line_time = line.split(" ")[3]
                    latest_time = first_line_time
                    self.dev.shell("input tap " + line.split(" ")[1] + " " + line.split(" ")[2] + "")
                else:
                    # 等待时间为2次click的间隔
                    time.sleep(float(line.split(' ')[2]) - float(latest_time))
                    first_time = float(line.split(' ')[2])
                    self.dev.shell("input tap " + line.split(" ")[0] + " " + line.split(" ")[1] + "")

    def save_script_(self, script_name, layout):
        temporary_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), "script_file", "temporary")
        circulate_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), "script_file", "circulate")
        # 重命名文件
        old_name = os.path.join(temporary_path, self.get_temporary_path(temporary_path))
        new_name = os.path.join(temporary_path, script_name + ".txt")
        os.rename(old_name, new_name)
        time.sleep(1)
        # 移动文件
        destination = os.path.join(circulate_path, script_name + ".txt")
        shutil.move(new_name, destination)
        # 脚本添加到列表中
        check_box = QCheckBox(script_name)
        item = QListWidgetItem()
        layout.addItem(item)
        layout.setItemWidget(item, check_box)
        # 添加提示
        messageBox = QMessageBox(QMessageBox.Information, "提示信息", "保存成功！", QMessageBox.Ok, self)
        # QMessageBox组件设置
        messageBox.button(QMessageBox.Ok).setText("确定")  # 为按钮设置文本
        messageBox.exec()

    def get_temporary_path(self, file_path):
        files = os.listdir(file_path)
        for file in files:
            file_path = os.path.join(file_path, file)
            break
        return file_path
