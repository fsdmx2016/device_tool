#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 18:41
@Desc    :
"""
import subprocess

from Base import common


class Base_Device(object):
    def get_device_info(self):
        rsp = common.raw_shell("tidevice info")
        return rsp

def raw_shell(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    stdout = result.stdout
    return stdout