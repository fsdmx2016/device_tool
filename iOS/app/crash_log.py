#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:31
@Desc    :
"""
from Base import common


class App_Crash_Log(object):
    def get_crash_log_list(self):
        rsp = common.raw_shell("tidevice crashreport --list")


    def export_crash_log_list(self,file_path):
        rsp = common.raw_shell("tidevice crashreport --keep " + file_path)

