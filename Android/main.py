import os
import time

from PyQt5 import QtWidgets, uic, QtCore
import sys

from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
from airtest.core.android import Android
from Android.app import app_start, video_cut, base, app_performance, app_info, app_network
from Android.app.app_log import LogThread, AppLogMethod
from Base.common import run_adb_command


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.dirname(os.path.abspath(os.getcwd())) + "/ui/android2.ui"
        uic.loadUi(ui_file_path, self)
        self.dev = Android()
        # 获取基础设备相关信息
        self.init_ui_base()
        # app_启动时间
        self.init_ui_start_time()
        # 视频相关初始化
        self.init_ui_lp()
        # 性能相关
        self.init_ui_performance()
        # log日志相关
        self.init_ui_log()
        self.init_ui_auto_test()
        # 安卓投屏相关服务
        time.sleep(3)
        self.phone_show.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.phone_show.setScaledContents(True)
        self.phone_show.installEventFilter(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(300)
        # 按键注册
        self.phone_click()
        self.init_ui_network()

    def init_ui_base(self):
        base_ = base.BaseMethod(self.dev)
        app_list = base_.get_app_list()
        self.device_app_list.addItems(app_list)
    def init_ui_network(self):
        app_ = app_network.NetworkMonitor(self.dev,self.network_select.currentText())
        self.start_network_test.clicked.connect(lambda :app_.make_network_canvas(self.network_layout_down,self.device_app_list.currentText()))
    def phone_click(self):
        self.phone_home.clicked.connect(lambda: self.dev.keyevent("3"))
        self.phone_menu.clicked.connect(lambda: self.dev.keyevent("82"))
        self.phone_back.clicked.connect(lambda: self.dev.keyevent("4"))

    def init_ui_log(self):
        # 开启日志相关
        self.start_get_Log.clicked.connect(self.start_thread)
        self.worker_thread = LogThread(self.dev, self.show_log, self.device_app_list.currentText())
        self.worker_thread.update_signal.connect(self.update_line_edit)
        self.stop_get_Log.clicked.connect(self.stop_thread)

    # 视频相关
    def init_ui_lp(self):
        app_ = video_cut.Video_Cut()
        self.lp_choice_video.clicked.connect(self.onFileChoose)
        self.lp_start_clive_video.clicked.connect(
            lambda: app_.start_covert_video(self.lp_video_file_path.text(), self.lp_pictures))

    # 加载启动时间页面的UI文件
    def init_ui_start_time(self):
        app_ = app_start.StartMethod(self.dev)

        self.start_get_current_activity.clicked.connect(
            lambda: self.start_input_activity.setText(app_.get_top_activity()))
        self.start_get_start_activity.clicked.connect(
            lambda: self.start_input_activity.setText(app_.get_top_activity()))
        self.start_time_test.clicked.connect(
            lambda: self.label_4.setText(app_.get_start_time(package_name=self.device_app_list.currentText(),
                                                             start_activity=self.start_input_activity.text(),
                                                             num=int(
                                                                 self.start_test_num.text()) if self.start_test_num.text() != "" else 3))
        )

    # 加载性能测试的页面的UI文件
    def init_ui_performance(self):
        app_ = app_performance.Appa_Performance(self.dev, self.fps_layout, self.cpu_layout, self.mem_layout)
        self.performance_start_mem_test.clicked.connect(
            lambda: app_.make_mem_canvas(self.mem_layout, self.device_app_list.currentText()))
        self.performance_start_cpu_test.clicked.connect(
            lambda: app_.make_cpu_canvas(self.cpu_layout, self.device_app_list.currentText()))

    # 加载RAM页面的UI文件
    def init_ui_auto_test(self):
        app_ = app_info.AppInfoMethod(self.dev, self.mem_layout, )
        self.start_mem_test.clicked.connect(
            lambda: app_.get_mem_info(self.mem_layout, self.device_app_list.currentText()))

    def onFileChoose(self):
        cwd = os.getcwd()
        filename, filetype = QFileDialog.getOpenFileName(self, '选择文件',
                                                         cwd,
                                                         'Text Files(*.mp4);;All Files(*)')
        self.lp_video_file_path.setText(filename)

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

    def eventFilter(self, source, event):
        if (source == self.phone_show and source.pixmap() and not source.pixmap().isNull() and
                event.type() == QtCore.QEvent.MouseButtonPress and
                event.button() == QtCore.Qt.LeftButton):
            self.getClickedPosition(event.pos())
        return super().eventFilter(source, event)

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
        x_, y_ = self.get_screen_resolution()
        x_val = str(pos.x() * x_ / pixmapRect.width())
        y_val = str(pos.y() * y_ / pixmapRect.height())
        self.dev.shell("input tap " + x_val + " " + y_val + "")

    def get_screen_resolution(self):
        result = self.dev.shell("wm size")
        resolution = result.strip().split(' ')[-1]
        width, height = resolution.split('x')
        return int(width), int(height)

    def start_thread(self):
        self.worker_thread.start()

    def stop_thread(self):
        self.worker_thread.terminate()

    def update_line_edit(self, text):
        self.show_log.append(str(text))
        # 滚动到底部
        scrollbar = self.show_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    myapp.setStyleSheet("#myapp{background-color:blue}")
    sys.exit(app.exec())
