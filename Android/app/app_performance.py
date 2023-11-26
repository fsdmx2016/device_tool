import os
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

mem_X = []
mem_Y = []
cpu_X = []
cpu_Y = []

import threading
from queue import Queue
class Appa_Performance:
    def __init__(self, dev, fps_layout, cpu_layout, mem_layout):
        self.dev = dev
        self.fps_layout = fps_layout
        self.cpu_layout = cpu_layout
        self.mem_layout = mem_layout

    def start_test(self, package_name):
        # # data_queue = Queue()  # 创建队列对象
        #
        # cpu_thread = threading.Thread(target=self.make_cpu_canvas, args=(self.cpu_layout, package_name, ))
        # mem_thread = threading.Thread(target=self.make_mem_canvas, args=(self.mem_layout, package_name, ))
        #
        # cpu_thread.start()
        # mem_thread.start()
        # # 等待线程执行完成
        #
        # cpu_thread.join()
        # mem_thread.join()
        self.make_cpu_canvas(self.cpu_layout, package_name)

    def get_sys_info(self):
        if sys.platform.startswith('win'):
            return "windows"
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return "linux"

    def get_PID(self, package_name):
        pid = ''
        for app in package_name:
            if Appa_Performance.get_sys_info(self) == "windows":
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
                    return int(int(memory_info) / 1024)
            return None

    def make_mem_canvas(self, layout, package_name):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.package_name = package_name
        self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
        self.timer.add_callback(self.update_plot_mem)
        self.timer.start()

    def make_cpu_canvas(self, layout, package_name):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.package_name = package_name
        self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
        self.timer.add_callback(self.update_plot_cpu)
        self.timer.start()

    def update_plot_cpu(self):
        global cpu_X, cpu_Y
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cpu_X.append(current_time)
        cpu_Y.append(Appa_Performance.get_cpu_info(self, self.package_name))
        if len(cpu_X) > 5:
            cpu_X = cpu_X[-5:]
            cpu_Y = cpu_Y[-5:]
        ax.set_xlabel('Time')
        ax.set_ylabel('Cpu')
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
