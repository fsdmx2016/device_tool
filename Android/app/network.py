import os
import time

from Base import common
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class AppNetworkMethod:
    # def __init__(self, dev):
    #     self.dev = dev
    def start_(self,layout):
        # 创建一个Matplotlib图形对象
        self.figure = Figure()
        # 创建一个绘图区域对象
        self.canvas = FigureCanvas(self.figure)
        # 创建一个垂直布局
        layout.addWidget(self.canvas)
        # # 创建一个主窗口小部件，并将布局设置为垂直布局
        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)
        # 启动定时器以更新图形
        self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
        self.timer.add_callback(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # 清除图形
        self.figure.clear()

        # 创建一个绘图子区域对象
        ax = self.figure.add_subplot(111)

        # 模拟数据更新
        x = range(10)
        y = [random.randint(0, 10) for _ in range(10)]

        # 绘制折线图
        ax.plot(x, y)

        # 刷新图形
        self.canvas.draw()