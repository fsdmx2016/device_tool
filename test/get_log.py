#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/2/29 17:57
@Desc    :
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QProcess, pyqtSignal
from PyQt5.QtGui import QTextCursor

class OutputReader(QProcess):
    # 定义一个自定义信号用于传递命令输出内容
    outputReady = pyqtSignal(str)

    def __init__(self, parent=None):
        super(OutputReader, self).__init__(parent)
        self.readyReadStandardOutput.connect(self.handle_stdout)
        self.readyReadStandardError.connect(self.handle_stderr)

    def handle_stdout(self):
        data = self.readAllStandardOutput().data().decode()
        self.outputReady.emit(data)

    def handle_stderr(self):
        data = self.readAllStandardError().data().decode()
        self.outputReady.emit(data)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.process = OutputReader()
        self.process.outputReady.connect(self.update_output)

        # 启动命令
        self.process.start('tidevice', ['syslog'])

    def update_output(self, text):
        # 将新的输出内容追加到文本编辑器中
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())