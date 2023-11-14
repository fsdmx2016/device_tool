#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:11
@Desc    :
"""
import subprocess


def raw_shell(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    stdout = result.stdout
    return stdout


# 运行ADB命令
def run_adb_command( command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("运行ADB命令时出错:", e)
        return None
