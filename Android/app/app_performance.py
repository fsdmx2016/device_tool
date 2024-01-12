import os
import subprocess
import sys
import threading

from PyQt5.QtWidgets import QSpacerItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

mem_X = []
mem_Y = []
cpu_X = []
cpu_Y = []


class Appa_Performance:
    def __init__(self, dev, cpu_layout, mem_layout):
        self.dev = dev
        self.cpu_layout = cpu_layout
        self.mem_layout = mem_layout

    def get_sys_info(self):
        if sys.platform.startswith('win'):
            return "windows"
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return "linux"

    def get_PID(self, package_name):
        pid = ''
        for app in package_name:
            if self.get_sys_info() == "windows":
                result = os.popen('adb shell ps | findstr {}'.format(app))
            else:
                result = os.popen('adb shell ps | grep {}'.format(app))
            for line in result.readlines():
                line = '#'.join(line.split()) + '#'
                appstr = app + '#'
                if appstr in line:
                    pid = line.split('#')[1]
        return pid

    def get_cpu_info(self, appPID):
        # result = self.dev.shell('top -n 1')
        result = os.popen('adb shell top -n 1')
        if result:
            for line in result.readlines():
                if line.split().__contains__(appPID):
                    appCPU = round(float(line.split()[-4]) / 8, 2)
                    return appCPU
        return None

    # 获取应用的内存信息
    def get_app_memory(self, package_name: str):
        output = self.dev.shell("dumpsys meminfo " + package_name + "")
        if output:
            # 解析输出并提取内存信息
            lines = output.splitlines()
            for line in lines:
                if line.__contains__("TOTAL"):
                    memory_info = line.split()[1]
                    print("内存值"+str(memory_info))
                    return int(int(memory_info) / 1024)
            return None


    def make_mem_canvas(self, btn, layout, package_name):
        if btn.text() == "获取内存数据":
            self.deleteAll(layout)
            btn.setText("停止测试")
            self.deleteAll(layout)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)
            self.package_name = package_name
            self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
            self.timer.add_callback(self.update_plot_mem)
            self.timer.start()
        else:
            self.timer.stop()
            btn.setText("获取内存数据")

    def make_cpu_canvas(self, btn, layout, package_name):
        if btn.text() == "获取CPU数据":
            self.deleteAll(layout)
            btn.setText("停止测试")
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)
            self.package_name = package_name
            self.pid = self.get_PID(package_name)
            self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
            self.timer.add_callback(self.update_plot_cpu)
            self.timer.start()
        else:
            self.timer.stop()
            btn.setText("获取CPU数据")

    def deleteAll(self, thisLayout):
        item_list = list(range(thisLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = thisLayout.itemAt(i)
            if item is not None:
                if item.widget() is not None:
                    item.widget().deleteLater()
                elif isinstance(item, QSpacerItem):
                    thisLayout.removeItem(item)
                else:
                    self.deleteAll(item.layout())
                thisLayout.removeItem(item)

    def update_plot_cpu(self):
        global cpu_X, cpu_Y
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cpu_X.append(current_time)
        cpu_Y.append(Appa_Performance.get_cpu_info(self, self.pid))
        if len(cpu_X) > 5:
            cpu_X = cpu_X[-5:]
            cpu_Y = cpu_Y[-5:]
        ax.set_xlabel('Time')
        ax.set_ylabel('CPU')
        ax.plot(cpu_X, cpu_Y)
        self.canvas.draw()

    def update_plot_mem(self):
        global mem_X, mem_Y
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        mem_X.append(current_time)
        mem_Y.append(Appa_Performance.get_app_memory(self, self.package_name))
        if len(mem_X) > 5:
            mem_X = mem_X[-5:]
            mem_Y = mem_Y[-5:]
        ax.set_xlabel('Time')
        ax.set_ylabel('Memory')
        ax.plot(mem_X, mem_Y)
        self.canvas.draw()
