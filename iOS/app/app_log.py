#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 18:25
@Desc    :
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QProcess, pyqtSignal
from PyQt5.QtGui import QTextCursor

class OutputReader(QProcess):
    # 定义一个自定义信号用于传递命令输出内容
    outputReady = pyqtSignal(str)

    def __init__(self, label,parent=None):
        self.label=label
        super(OutputReader, self).__init__(parent)
        self.readyReadStandardOutput.connect(self.handle_stdout)
        self.readyReadStandardError.connect(self.handle_stderr)

    def handle_stdout(self):
        data = self.readAllStandardOutput().data().decode()
        self.outputReady.emit(data)

    def handle_stderr(self):
        data = self.readAllStandardError().data().decode()
        self.outputReady.emit(data)


    def update_output(self, text):
        # 将新的输出内容追加到文本编辑器中
        cursor = self.label.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.label.setTextCursor(cursor)
        self.label.ensureCursorVisible()


def get_current_log(label):
    process = OutputReader(label)
    process.outputReady.connect(process.update_output)
