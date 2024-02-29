#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/2/29 10:53
@Desc    :
"""
import subprocess

def run_adb_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("运行ADB命令时出错:", e)
        return None
