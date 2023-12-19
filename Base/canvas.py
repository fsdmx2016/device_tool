import copy
import datetime

from PyQt5.QtWidgets import QSpacerItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import Optional

from Base import common
mem_X = []
mem_Y = []
cpu_x = []
cpu_y = []
class AppCanvas:

    # 参数：布局、包名、方法名、title值
    def make_canvas(self, layout, title_val, package_name: Optional[str] = None):
        # 先清空布局内容
        self.deleteAll(layout)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.title_val = title_val
        self.package_name = package_name
        self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
        self.timer.add_callback(self.update_plot_cpu)
        self.timer.start()

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

    def update_plot_cpu(self, ):
        if self.title_val == "mem":
            global mem_X, mem_Y
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            mem_X.append(current_time)
            mem_Y.append(common.get_app_memory(self.package_name))
            if len(mem_X) > 5:
                mem_X = mem_X[-5:]
                mem_Y = mem_Y[-5:]
            ax.set_xlabel('Time')
            ax.set_ylabel('Memory')
            ax.plot(mem_X, mem_Y)
            self.canvas.draw()
        elif self.title_val == "cpu":
            global cpu_x, cpu_y
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            cpu_x.append(current_time)
            cpu_y.append(common.get_app_memory(self.dev,self.package_name))
            if len(cpu_x) > 5:
                cpu_x = cpu_x[-5:]
                cpu_y = cpu_y[-5:]
            ax.set_xlabel('Time')
            ax.set_ylabel('Memory')
            ax.plot(cpu_x, cpu_y)
            self.canvas.draw()