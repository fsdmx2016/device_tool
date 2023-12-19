#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:11
@Desc    :
"""
import subprocess
import sys


def raw_shell(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    stdout = result.stdout
    return stdout


# 运行ADB命令
def run_adb_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("运行ADB命令时出错:", e)
        return None


def get_sys_info():
    if sys.platform.startswith('win'):
        return "windows"
    else:
        return "linux"


# 获取应用的内存信息
def get_app_memory(package_name: str):
    output = run_adb_command("adb shell dumpsys meminfo " + package_name + "")
    if output:
        # 解析输出并提取内存信息
        lines = output.splitlines()
        for line in lines:
            if line.__contains__("TOTAL"):
                memory_info = line.split()[1]
                return int(int(memory_info) / 1024)
        return None
