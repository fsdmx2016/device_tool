#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/3/1 13:51
@Desc    :
"""
import os
import sys
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QWidget
import datetime
from PyQt5.QtCore import QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import threading
import time
import tidevice

mem_X = []
mem_Y = []
cpu_X = []
cpu_Y = []
path=os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'performance', "mem.txt")

# 多线程-获取性能数据
def collect_and_store_data(perf, app_bundle_id):
    def callback(_type: tidevice.DataType, value: dict):
        if _type.value == "memory":
            ss = str(value)
            memory = ss.split("'value':")[1][0:6].split("}")[0]
            with open(path, "a+") as f:
                f.writelines(memory)
            f.close()
    perf.start(app_bundle_id, callback=callback)


def process_collected_data():
    file_path=os.path.join(os.getcwd(),'performance', "mem.txt")
    with open(file_path, "r") as f:
        data_list = list(str(f.readlines()).split(" "))
        final_list = [x for x in data_list if
                      x.__contains__(".") and len(x.split(".")) == 2 and not x.__contains__("]")]
    return final_list


def run_performance(uuid,app_bundle_id):
    file_path=os.path.join(os.getcwd(),'performance', "mem.txt")
    t = tidevice.Device(uuid)
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))
    with open(file_path, "w") as f:
        f.write("")
    collector_thread = threading.Thread(target=collect_and_store_data, args=(
        perf, app_bundle_id, file_path))
    collector_thread.start()
    # # 在开启收集线程后，立即开始处理数据的线程
    time.sleep(5)
    # processor_thread = threading.Thread(target=process_collected_data,
    #                                     args=("/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt",))
    # processor_thread.start()


class DataProducer(QThread):
    new_data_signal = pyqtSignal(float)  # 定义一个信号用于传递单个Y轴新值
    def __init__(self, uuid, app_bundle_id):
        super().__init__()
        self.uuid = uuid
        self.app_bundle_id = app_bundle_id
    def run(self):
        while True:
            # 模拟来自某个持续打印数据的方法

            run_performance(self.uuid,self.app_bundle_id)
            new_value = process_collected_data()
            self.new_data_signal.emit(float(new_value[-1]))
            # 添加适当的延时，比如每秒更新一次
            QtCore.QThread.msleep(1000)


class Appa_Performance:
    def __init__(self, dev, cpu_layout, mem_layout):
        self.dev = dev
        self.cpu_layout = cpu_layout
        self.mem_layout = mem_layout
        self.x_data = []
        self.y_data = []

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

    def make_mem_canvas(self, btn, layout,uuid,app_bundle_id):
        if btn.text() == "内存测试":

            self.deleteAll(layout)
            btn.setText("停止测试")
            # self.deleteAll(layout)
            # self.figure = Figure()
            # self.canvas = FigureCanvas(self.figure)
            # layout.addWidget(self.canvas)
            # # self.package_name = "com.meitu.mtxx"
            # # self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
            # # self.data_thread = DataProducer()
            # # self.data_thread.new_data_signal.connect(self.update_plot_mem_data)
            # # self.data_thread.start()
            # # self.timer.add_callback(self.update_plot_mem)
            # # self.timer.start()
            # self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
            # self.timer.start()
            # self.data_thread = DataProducer()
            # self.data_thread.new_data_signal.connect(self.update_ui)
            # self.data_thread.start()
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)
            self.init_ui()
            self.data_thread = DataProducer(uuid,app_bundle_id)
            self.data_thread.new_data_signal.connect(self.update_ui)
            self.data_thread.start()

            self.x_data = []
            self.y_data = []

        else:
            self.timer.stop()
            btn.setText("内存测试")

    def update_plot_mem_data(self, new_y_value):
        return new_y_value

    def make_cpu_canvas(self, btn, layout, package_name):
        if btn.text() == "CPU测试":
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
            btn.setText("CPU测试")

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
        mem_Y.append(self.update_plot_mem_data())
        if len(mem_X) > 5:
            mem_X = mem_X[-5:]
            mem_Y = mem_Y[-5:]
        ax.set_xlabel('Time')
        ax.set_ylabel('Memory')
        ax.plot(mem_X, mem_Y)
        self.canvas.draw()

    def init_ui(self):
        # self.axes = self.figure.add_subplot(111)
        # self.plot_line, = self.axes.plot([], [])  # 初始化为空

        self.axes = self.figure.add_subplot(111)
        self.x_data = []  # 移至类属性，在此处初始化
        self.y_data = []
        self.plot_line, = self.axes.plot([], [])  # 初始化为空

    def update_ui(self,new_y_value):
        # self.figure.clear()
        current_time = datetime.datetime.now()
        self.x_data.append(current_time)  # 使用实例变量 x_data 和 y_data
        self.y_data.append(new_y_value)

        if len(self.x_data) > 5:
            self.x_data = self.x_data[-5:]
            self.y_data = self.y_data[-5:]

        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Memory')
        self.plot_line.set_xdata(self.x_data)
        self.plot_line.set_ydata(self.y_data)  # 更新已有折线图的数据，而不是重新绘制

        self.axes.relim()  # 更新数据范围
        self.axes.autoscale_view(True, True, True)
        self.canvas.draw_idle()  # 刷新canvas

    # def update_plot(self, new_y_value):
    #     self.x_data.append(len(self.y_data))  # X轴按数据点索引计数
    #     self.y_data.append(new_y_value)
    #
    #     self.plot_line.set_xdata(self.x_data)
    #     self.plot_line.set_ydata(self.y_data)
    #
    #     self.axes.relim()  # 更新数据范围
    #     self.axes.autoscale_view(True, True, True)
    #     self.canvas.draw_idle()  # 刷新canvas
