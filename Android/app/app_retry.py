import os
import threading
import time
import shutil

from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QMessageBox

from Android.app.app_performance import Appa_Performance


class AppRetry:
    def __init__(self, dev):
        super().__init__()
        self.dev = dev

    def run_script_by_name(self, script_name, cpu_layout, mem_layout):
        run_script_thread=threading.Thread(target=self.run_script_(script_name))
        app_performance=Appa_Performance(self.dev,cpu_layout,mem_layout)
        package_name = str(self.dev.get_top_activity_name()).split("/")[0]
        thread1 = threading.Thread(target=app_performance.make_cpu_canvas(cpu_layout,package_name))
        thread2 = threading.Thread(target=app_performance.make_mem_canvas(cpu_layout,package_name))
        run_script_thread.start()
        thread1.start()
        thread2.start()


    def run_script_(self, script_name):
        file_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), "script_file", "circulate",
                                 script_name + ".txt")
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
