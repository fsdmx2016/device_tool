#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 18:25
@Desc    :
"""
import subprocess
from typing import Optional


class App_Log(object):
    content = None
    def realtime_syslog(self, log_find: Optional[str] = None):
        if log_find:
            command = 'tidevice syslog |grep ' + log_find
        else:
            command = 'tidevice syslog'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            global content
            output = process.stdout.readline().decode().strip()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output)
            file = open("文件路径/文件名.txt", "w")  # "w"表示以写入模式打开文件
            file.write(output)


    def export_syslog(self, file_path):
        global content



if __name__ == '__main__':
    app_ = App_Log()
    app_.realtime_syslog("mtxx")
