#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/8 13:14
@Desc    :
"""
class StartMethod:
    def __init__(self, dev):
        self.dev = dev

    # 获取当前的top activity
    def get_top_activity(self):
        out = self.dev.get_top_activity()
        return str(out).split(",")[1].split("'")[1]

    # 获取启动的activity TODO
    def get_start_activity(self, ):
        return self.dev.shell("")

    # 打印所有的APP列表
    def get_list_app(self):
        return self.dev.list_app()

    # 获取启动时间
    def get_start_time(self, package_name: str, start_activity: str, num: int):
        time_list = []
        for i in range(num):
            time_list.append(self.dev.start_app_timing(package=package_name, activity=start_activity))
        time_ = ""
        for index, i in enumerate(time_list):
            time_ += "第" + str(index + 1) + "次的启动时间为" + str(i) + "ms" + "\n"
        return time_
