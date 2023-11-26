# coding=utf-8

import csv
import os
import re
import sys
import threading
import time
from builtins import *
from airtest.core.android import Android


class ParseNetworkInfo(object):
    def __init__(self, package, networkinfo):
        self.networkinfo = networkinfo
        self.package = package
        self.network_data = self.get_network_data("wlan0")

    def get_network_data(self, regexp):
        network_info = self.networkinfo.splitlines()[2:]
        acc_downFlow = 0
        acc_upFlow = 0
        for line in network_info:
            line_info = line.strip().split()
            if re.search(regexp, line_info[0]):
                acc_downFlow += float(line_info[2]) / 1024  # bytes  -> kb
                acc_upFlow += float(line_info[10]) / 1024
        network_info = [acc_downFlow, acc_upFlow]
        return network_info


class NetworkMonitor():
    def __init__(self, test_time=-1, interval=1):
        super().__init__()
        self.test_time = test_time
        self.interval = interval
        self.dev = Android()

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

    def get_network_info(self, pid):
        network_info = self.dev.shell(f"cat proc/" + pid + "/net/dev")
        network_info = network_info.strip()
        network_info = ParseNetworkInfo("com.mt.mtxx.mtxx", network_info, ).network_data
        time.sleep(0.5)
        network_info2 = self.dev.shell(f"cat proc/" + pid + "/net/dev")
        network_info2 = network_info2.strip()
        network_info2 = ParseNetworkInfo("com.mt.mtxx.mtxx", network_info2, ).network_data
        print("获取到的network信息是：{}".format(network_info2[0]-network_info[0],network_info2[1]-network_info[1]))
        return network_info


if __name__ == '__main__':
    demo = NetworkMonitor()
    pid = demo.get_PID("com.mt.mtxx.mtxx")
    for i in range(5):
        demo.get_network_info(pid)

    # def run(self):
    #     '''
    #     按照指定频率，循环搜集network的信息
    #     :return:
    #     '''
    #     network_title = ["timestamp", "realtime_downFlow", "realtime_upFlow", "sum_realtimeFlow",
    #                      "accumulate_downFlow", "accumulate_upFlow", "sum_accumFlow", ]
    #     network_file = self.save_file
    #     with open(network_file, 'w+') as df:
    #         csv.writer(df, lineterminator='\n').writerow(network_title)
    #
    #     last_timestamp = None
    #     last_acc_downFlow = None
    #     last_acc_upFlow = None
    #     accumulate_downFlow = 0
    #     accumulate_upFlow = 0
    #     network_list = []
    #     try:
    #
    #         before = time.time()
    #
    #         network_list.append(before)
    #         network_info = self.get_network_info()
    #         if last_timestamp and last_acc_downFlow:
    #             realtime_downFlow = (diff_downFlow := (network_info[0] - last_acc_downFlow)) / (
    #                     before - last_timestamp)
    #             realtime_upFlow = (diff_upFlow := (network_info[1] - last_acc_upFlow)) / (before - last_timestamp)
    #             if diff_upFlow < 0 or diff_downFlow < 0 or network_info is None:
    #                 last_timestamp = None
    #
    #             else:
    #                 accumulate_downFlow += diff_downFlow
    #                 accumulate_upFlow += diff_upFlow
    #         else:
    #             last_timestamp = before
    #             last_acc_downFlow = network_info[0]
    #             last_acc_upFlow = network_info[1]
    #         network_list.extend([realtime_downFlow, realtime_upFlow, realtime_downFlow + realtime_upFlow])
    #         network_list.extend([accumulate_downFlow, accumulate_upFlow, accumulate_downFlow + accumulate_upFlow])
    #         last_timestamp = before
    #         last_acc_downFlow = network_info[0]
    #         last_acc_upFlow = network_info[1]
    #         after = time.time()
    #         time_consume = after - before
    #
    #         with open(network_file, 'a+', encoding="utf-8") as df:
    #             csv.writer(df, lineterminator='\n').writerow(network_list)
    #             del network_list[:]
    #         delta_inter = self.interval - time_consume
    #         if delta_inter > 0:
    #             time.sleep(delta_inter)
    #     except Exception as e:
    #         print(e)
