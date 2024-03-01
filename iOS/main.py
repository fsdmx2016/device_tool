#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/2/29 15:39
@Desc    :
"""
import os
import subprocess
import time
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QProcess, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QListWidgetItem
from PyQt5 import QtWidgets, uic, QtCore
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from iOS.app import app_retry, app_performance
from iOS.app.crash_log import App_Crash_Log
from airtest.core.ios import IOS

is_save_step = False
is_start_record = False


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), "ui", "ios.ui")
        uic.loadUi(ui_file_path, self)
        # 判断设备是否连接，且为usb
        self.dev = IOS()

        # iOS投屏服务
        time.sleep(3)
        self.phone_show.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.phone_show.setScaledContents(True)
        self.phone_show.installEventFilter(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(300)

        # 加载crash_log文件
        self.init_crash_logs()

        # 日志文件相关
        self.init_logs()

        # app列表
        self.device_app_list.addItems(self.raw_shell('tidevice applist'))
        # app管理相关
        self.init_app_manager()
        # 自动化相关
        self.init_retry_script()
        # 加载脚本列表
        self.init_script_list()
        # 性能测试相关
        self.init_performance()

    def init_performance(self):
        app_ = app_performance.Appa_Performance(self.dev, self.cpu_layout, self.mem_layout)
        self.performance_start_mem_test.clicked.connect(
            lambda: app_.make_mem_canvas(self.performance_start_mem_test, self.mem_layout,
                                         ))
        self.performance_start_cpu_test.clicked.connect(
            lambda: app_.make_cpu_canvas(self.performance_start_cpu_test, self.cpu_layout,
                                         self.device_app_list.currentText()))

    def init_crash_logs(self):
        self.crash_tab_list.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])  # 设置水平表头标签
        crash_log = App_Crash_Log()
        crash_log.get_crash_log_list(self.crash_tab_list)

    def init_logs(self):
        self.start_get_Log.clicked.connect(lambda: self.get_current_log())
        self.stop_get_Log.clicked.connect(lambda: self.process.terminate())
        self.clear_log.clicked.connect(lambda: self.show_log.setText(''))

    def init_retry_script(self):
        retry_step = app_retry.AppRetry(self.dev)
        # 点击录制循环脚本的时候，开启记忆
        self.retry_script_cycle.clicked.connect(lambda: self.start_retry_script(self.retry_script_cycle))
        # 脚本保存
        self.retry_script_save.clicked.connect(
            lambda: retry_step.save_script_(self.retry_script_name.text(), self.retry_script_list))
        # 执行脚本
        self.start_script_auto.clicked.connect(
            lambda: retry_step.run_script_by_name(self.retry_script_list, self.retry_script_time.text(),
                                                  self.retry_cpu_layout, self.retry_mem_layout))
        # 删除脚本
        self.delete_auto_script.clicked.connect(lambda: retry_step.delete_script(self.retry_script_list))

    def init_script_list(self):
        # 循环遍历，获取脚本列表
        file_path = os.path.join(os.getcwd(), "script_file", "circulate")
        files = os.listdir(file_path)
        for file in files:
            check_box = QCheckBox(file.split(".")[0])
            item = QListWidgetItem()
            self.retry_script_list.addItem(item)
            self.retry_script_list.setItemWidget(item, check_box)

    # app管理开始
    def init_app_manager(self):
        from iOS.app import app_manager
        app_manager.get_app_list(self.app_table_list)

    # 日志文件相关开始
    def get_current_log(self):
        self.process = OutputReader()
        self.process.outputReady.connect(self.update_output)
        # 启动命令
        self.process.start('tidevice', ['syslog'])

    def update_output(self, text):
        # 将新的输出内容追加到文本编辑器中
        cursor = self.show_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.show_log.setTextCursor(cursor)
        self.show_log.ensureCursorVisible()
    # 日志文件相关结束

    # app列表相关开始
    def raw_shell(self, command: str):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        stdout = result.stdout
        return stdout.split("\n")
    # app列表相关结束

    # 投屏相关开始
    # 更新图像
    def update_screen(self):
        # 获取截图图像流
        img = self.dev.snapshot(quality=99)
        # 将图像流填充到QImage控件中
        image = QImage(
            img,
            img.shape[1],
            img.shape[0],
            img.shape[1] * 3,
            QImage.Format_BGR888,
        )
        pixmap = QPixmap(image)
        scaled_pixmap = pixmap.scaled(self.phone_show.width(), self.phone_show.height(),
                                      QtCore.Qt.AspectRatioMode.IgnoreAspectRatio)
        # QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.phone_show.setPixmap(scaled_pixmap)  # 在 QLabel 上显示缩放后的图像

    # 重写点击事件
    def eventFilter(self, source, event):
        if (source == self.phone_show and source.pixmap() and not source.pixmap().isNull() and
                event.type() == QtCore.QEvent.MouseButtonPress and
                event.button() == QtCore.Qt.LeftButton):
            self.getClickedPosition(event.pos())
        return super().eventFilter(source, event)

    # 获取点击坐标
    def getClickedPosition(self, pos):
        contentsRect = QtCore.QRectF(self.phone_show.contentsRect())
        if pos not in contentsRect:
            return
        pos -= contentsRect.topLeft()
        pixmapRect = self.phone_show.pixmap().rect()
        if self.phone_show.hasScaledContents():
            x = pos.x() * pixmapRect.width() / contentsRect.width()
            y = pos.y() * pixmapRect.height() / contentsRect.height()
            pos = QtCore.QPoint(int(x), int(y))
        else:
            align = self.phone_show.alignment()
            pixmapRect = QtCore.QRectF(pixmapRect)
            if align & QtCore.Qt.AlignRight:
                pixmapRect.moveRight(contentsRect.x() + contentsRect.width())
            elif align & QtCore.Qt.AlignHCenter:
                pixmapRect.moveLeft(contentsRect.center().x() - pixmapRect.width() / 2)
            if align & QtCore.Qt.AlignBottom:
                pixmapRect.moveBottom(contentsRect.y() + contentsRect.height())
            elif align & QtCore.Qt.AlignVCenter:
                pixmapRect.moveTop(contentsRect.center().y() - pixmapRect.height() / 2)
            if not pos in pixmapRect:
                return
            pos = (pos - pixmapRect.topLeft()).toPoint()
        # 根据屏幕尺寸,做一个坐标换算
        x_val = str(pos.x() / pixmapRect.width())
        y_val = str(pos.y() / pixmapRect.height())
        global is_save_step
        if is_save_step:
            file_path = os.path.join(os.getcwd(), "script_file", "temporary", "temporary.txt")
            with open(file_path, 'a') as f_output:
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    f_output.write("first_line " + str(x_val) + " " + str(y_val) + " " + str(time.time()))
                    f_output.write('\n')
                else:
                    # 如果是个新文件，写入第一行
                    f_output.write(str(x_val) + " " + str(y_val) + " " + str(time.time()))
                    f_output.write('\n')
        self.dev.touch((float(x_val), float(y_val)), duration=1)

    def start_retry_script(self, btn):
        global is_save_step
        print(btn.text())
        if btn.text() != "停止录制":
            file_path = os.path.join(os.getcwd(), "script_file", "temporary", "temporary.txt")
            # 先清空文件
            with open(file_path, 'w') as file:
                file.truncate(0)
            is_save_step = True
            btn.setText("停止录制")
        else:
            is_save_step = False
            btn.setText("录制循环脚本")


class OutputReader(QProcess):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    myapp.setStyleSheet("#myapp{background-color:blue}")
    sys.exit(app.exec())
