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
