# coding=utf-8

import csv
import os
import re
import sys
import threading
import time
from builtins import *
from PyQt5.QtWidgets import QSpacerItem
from matplotlib.figure import Figure
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

net_X = []
net_Y = []


class ParseNetworkInfo(object):
    def __init__(self, package, networkinfo, network_type):
        self.networkinfo = networkinfo
        self.package = package
        self.network_data = self.get_network_data(network_type)

    def get_network_data(self, regexp):
        network_info = self.networkinfo.splitlines()[2:]
        # 对数据类型做判断
        if regexp == "WLAN":
            regexp = "wlan0"
        else:
            regexp = "rmnet_ipa0"
        acc_downFlow = 0
        acc_upFlow = 0
        for line in network_info:
            line_info = line.strip().split()
            if re.search(regexp, line_info[0]):
                acc_downFlow = float(line_info[2]) / 1024  # bytes  -> kb
                acc_upFlow += float(line_info[10]) / 1024

        network_info = [self.operate_num(acc_downFlow), self.operate_num(acc_upFlow)]
        return network_info

    def operate_num(self, megabytes):
        rounded_megabytes = round(megabytes, 1)
        shifted_megabytes = rounded_megabytes * 100
        trimmed_megabytes = shifted_megabytes % 1000  # 取模1000，去掉前两位整数部分
        return trimmed_megabytes


class NetworkMonitor:
    def __init__(self, dev, network_type):
        super().__init__()
        self.dev = dev
        self.network_type = network_type

    def make_network_canvas(self, btn, layout1, layout2, package_name):
        if btn.text() == "开始测试":
            self.pid = self.get_PID(package_name=package_name)
            self.deleteAll(layout1)
            self.deleteAll(layout2)
            btn.setText("停止测试")
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            layout1.addWidget(self.canvas)
            layout2.addWidget(self.canvas)
            self.package_name = package_name
            self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
            self.timer.add_callback(self.update_plot_network_up)
            self.timer.start()
        else:
            self.timer.stop()
            btn.setText("开始测试")

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

    def update_plot_network_up(self, ):
        global net_X, net_Y
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        net_X.append(current_time)
        net_Y.append(NetworkMonitor.get_network_info(self, self.pid, self.package_name, self.network_type)[0])
        if len(net_X) > 5:
            net_X = net_X[-5:]
            net_Y = net_Y[-5:]
        ax.set_xlabel('Time')
        ax.set_ylabel('Network')
        ax.plot(net_X, net_Y)
        self.canvas.draw()

    def get_sys_info(self):
        if sys.platform.startswith('win'):
            return "windows"
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return "linux"

    def get_PID(self, package_name):
        pid = ''
        for app in package_name:
            if NetworkMonitor.get_sys_info(self) == "windows":
                result = os.popen('adb shell ps | findstr {}'.format(app))
            else:
                result = os.popen('adb shell ps | grep {}'.format(app))
            for line in result.readlines():
                line = '#'.join(line.split()) + '#'
                appstr = app + '#'
                if appstr in line:
                    pid = line.split('#')[1]
        return pid

    def get_network_info(self, pid, package_name, network_type):
        network_info = self.dev.shell(f"cat /proc/" + pid + "/net/dev")
        network_info = network_info.strip()
        network_info = ParseNetworkInfo(package_name, network_info, network_type).network_data
        time.sleep(1)
        network_info2 = self.dev.shell(f"cat /proc/" + pid + "/net/dev")
        network_info2 = network_info2.strip()
        network_info2 = ParseNetworkInfo(package_name, network_info2, network_type).network_data
        up_net = network_info2[1] - network_info[1]
        do_net = network_info2[0] - network_info[0]
        print("获取到的network信息是：{},{}".format(network_info2[0] - network_info[0],
                                                   network_info2[1] - network_info[1]))
        return do_net, up_net
