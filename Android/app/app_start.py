#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/8 13:14
@Desc    :
"""
from airtest.core.android import Android


class StartMethod:
    def __init__(self, dev):
        self.dev = dev

    # 获取当前的top activity
    def get_current_activity(self):
        out = self.dev.get_top_activity()
        return out

    # 获取启动的activity
    def get_start_activity(self, package_name):
        return self.dev.shell("")

    # 打印所有的APP列表
    def get_list_app(self):
        return self.dev.list_app()

    # 获取启动时间
    def get_start_time(self, package_name: str, num: int):
        time_list = []
        for i in range(num):
            start_activity = self.get_start_activity(package_name)
            time_list.append(self.dev.start_app_timing(package=package_name, activity=start_activity))
        return time_list
