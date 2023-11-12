#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 18:41
@Desc    :
"""
from Base import common


class Base_Device(object):
    def get_device_info(self):
        rsp = common.raw_shell("tidevice info")
        return rsp

if __name__ == '__main__':
    base_d=Base_Device()
    print(base_d.get_device_info())
