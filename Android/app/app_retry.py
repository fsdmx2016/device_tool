import os
import threading
import time
import shutil

from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QMessageBox

from Android.app.app_performance import Appa_Performance

select_script = ""


class AppRetry:
    def __init__(self, dev):
        super().__init__()
        self.dev = dev

    def run_script_by_name(self, retry_script_list, retry_num, cpu_layout, mem_layout):
        is_has_select = self.is_select_script(retry_script_list)
        if is_has_select:
            self.run_script_(retry_script_list, retry_num)
            # run_script_thread = threading.Thread(target=self.run_script_(retry_script_list, retry_num))
            # # app_performance = Appa_Performance(self.dev, cpu_layout, mem_layout)
            # # package_name = str(self.dev.get_top_activity_name()).split("/")[0]
            # # thread1 = threading.Thread(target=app_performance.make_cpu_canvas(cpu_layout, package_name))
            # # thread2 = threading.Thread(target=app_performance.make_mem_canvas(cpu_layout, package_name))
            # run_script_thread.start()
            # thread1.start()
            # thread2.start()

    def delete_script(self, retry_script_list):
        delete_count = 0
        for i in range(retry_script_list.count()):
            item = retry_script_list.item(i)
            check_box = retry_script_list.itemWidget(item)
            if check_box.isChecked():
                script_name = check_box.text()
                file_path = os.path.join(os.getcwd(), "script_file", "circulate", )
                script_path = os.path.join(file_path, script_name + ".txt")
                os.remove(script_path)
                retry_script_list.takeItem(retry_script_list.row(item))
                delete_count = delete_count + 1
        if delete_count == 0:
            messageBox = QMessageBox(QMessageBox.Information, "提示", "请先选择要删除的脚本")
            messageBox.button(QMessageBox.Ok)
            messageBox.exec()

    def get_select_script(self, retry_script_list):
        for i in range(retry_script_list.count()):
            item = retry_script_list.item(i)
            check_box = retry_script_list.itemWidget(item)
            if check_box.isChecked():
                return check_box.text()

    def is_select_script(self, retry_script_list):
        select_count = 0
        for i in range(retry_script_list.count()):
            item = retry_script_list.item(i)
            check_box = retry_script_list.itemWidget(item)
            if check_box.isChecked():
                select_count = select_count + 1
        if select_count == 1:
            return True
        elif select_count > 1:
            messageBox = QMessageBox(QMessageBox.Information, "提示", "每次只能执行一个")
            messageBox.button(QMessageBox.Ok)
            messageBox.exec()
            return False
        elif select_count == 0:
            messageBox = QMessageBox(QMessageBox.Information, "提示", "请先选择要执行的脚本")
            messageBox.button(QMessageBox.Ok)
            messageBox.exec()
            return False

    def run_script_(self, retry_script_list, retry_num):
        script_name = self.get_select_script(retry_script_list)
        file_path = os.path.join(os.getcwd(), "script_file", "circulate", )
        script_path = os.path.join(file_path, script_name + ".txt")
        for i in range(int(retry_num)):
            with open(script_path, 'r') as f_input:
                for line in f_input:
                    # 判断是不是首行
                    first_line = 1
                    if line.__contains__("first_line"):
                        first_line_time = line.split(" ")[3]
                        latest_time = first_line_time
                        self.dev.shell("input tap " + line.split(" ")[1] + " " + line.split(" ")[2] + "")
                    else:
                        # 等待时间为2次click的间隔
                        time.sleep(float(line.split(' ')[2]) - float(latest_time))
                        first_line = float(line.split(' ')[2])
                        self.dev.shell("input tap " + line.split(" ")[0] + " " + line.split(" ")[1] + "")

    def is_has_save(self, script_name, layout):
        for i in range(layout.count()):
            item = layout.item(i)
            check_box = layout.itemWidget(item)
            if check_box.text() == script_name:
                messageBox = QMessageBox(QMessageBox.Information, "提示", "脚本名称已存在！")
                messageBox.button(QMessageBox.Ok)
                messageBox.exec()
                return False
        return True

    def save_script_(self, script_name, layout):
        is_has_save = self.is_has_save(script_name, layout)
        if is_has_save:
            temporary_path = os.path.join(os.getcwd(), "script_file", "temporary")
            circulate_path = os.path.join(os.getcwd(), "script_file", "circulate")
            # 重命名文件
            old_name = os.path.join(temporary_path, self.get_temporary_path(temporary_path))
            new_name = os.path.join(temporary_path, script_name + ".txt")
            os.rename(old_name, new_name)
            time.sleep(0.5)
            # 移动文件
            destination = os.path.join(circulate_path, script_name + ".txt")
            shutil.move(new_name, destination)
            # 脚本添加到列表中
            check_box = QCheckBox(script_name)
            item = QListWidgetItem()
            layout.addItem(item)
            layout.setItemWidget(item, check_box)

    def get_temporary_path(self, file_path):
        files = os.listdir(file_path)
        for file in files:
            file_path = os.path.join(file_path, file)
            break
        return file_path
