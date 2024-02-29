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

def run_adb_command_line(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line