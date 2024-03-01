import sys

import tidevice
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import threading
import time
import tidevice


def get_mem():
    app_bundle_id = "com.meitu.mtxx"
    t = tidevice.Device("00008030-0006250A362B802E")  # iOS设备
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))
    rsp = perf.start(app_bundle_id)
    ss = str(rsp)
    memory = ss.split("'value':")[1][0:6].split("}")[0]
    return memory

def get_performance_data():
    uuid = "00008030-0006250A362B802E"
    app_bundle_id = "com.meitu.mtxx"
    type = "memory"
    t = tidevice.Device(uuid)
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))

    def callback(_type: tidevice.DataType, value: dict):
        if type == "memory":
            if _type.value == "memory":
                ss = str(value)
                memory = ss.split("'value':")[1][0:6].split("}")[0]
                print(memory)
                file = "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"
                with open(file, "a+") as f:
                    f.writelines(memory.strip())
                f.close()

    perf.start(app_bundle_id, callback=callback)
    file = "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"
    with open(file, "r") as f:
        data_list = list(str(f.readlines()).split(" "))
        final_list = [x for x in data_list if x.__contains__(".") and len(x.split(".")) == 2]
    # 假设这是后台任务得到的新数据点
    f.close()
    return final_list


def collect_and_store_data(perf, app_bundle_id, output_file):
    def callback(_type: tidevice.DataType, value: dict):
        if _type.value == "memory":
            ss = str(value)
            print(ss)
            memory = ss.split("'value':")[1][0:6].split("}")[0]
            with open(output_file, "a+") as f:
                f.writelines(memory)

    perf.start(app_bundle_id, callback=callback)


def process_collected_data(input_file):
    with open(input_file, "r") as f:
        data_list = list(str(f.readlines()).split(" "))
        final_list = [x for x in data_list if
                      x.__contains__(".") and len(x.split(".")) == 2 and not x.__contains__("]")]
    print(final_list[-1])
    return final_list


def run_performance():
    uuid = "00008030-0006250A362B802E"
    app_bundle_id = "com.meitu.mtxx"
    t = tidevice.Device(uuid)
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))
    path = "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"
    with open(path, "w") as f:
        f.write("")
    collector_thread = threading.Thread(target=collect_and_store_data, args=(
        perf, app_bundle_id, "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"))
    collector_thread.start()
    # # 在开启收集线程后，立即开始处理数据的线程
    time.sleep(5)
    # processor_thread = threading.Thread(target=process_collected_data,
    #                                     args=("/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt",))
    # processor_thread.start()


class DataProducer(QThread):
    new_data_signal = pyqtSignal(float)  # 定义一个信号用于传递单个Y轴新值

    def run(self):
        while True:
            # 模拟来自某个持续打印数据的方法
            run_performance()
            path = "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"
            new_value = process_collected_data(path)
            self.new_data_signal.emit(float(new_value[-1]))
            # 添加适当的延时，比如每秒更新一次
            QtCore.QThread.msleep(1000)


class DynamicPlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.data_thread = DataProducer()
        self.data_thread.new_data_signal.connect(self.update_plot)
        self.data_thread.start()

        self.x_data = []
        self.y_data = []

    def init_ui(self):
        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.figure = self.canvas.figure
        self.axes = self.figure.add_subplot(111)

        self.plot_line, = self.axes.plot([], [])  # 初始化为空

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_plot(self, new_y_value):
        self.x_data.append(len(self.y_data))  # X轴按数据点索引计数
        self.y_data.append(new_y_value)

        self.plot_line.set_xdata(self.x_data)
        self.plot_line.set_ydata(self.y_data)

        self.axes.relim()  # 更新数据范围
        self.axes.autoscale_view(True, True, True)
        self.canvas.draw_idle()  # 刷新canvas


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DynamicPlotWindow()
    window.show()

    sys.exit(app.exec_())
