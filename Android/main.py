import os
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage
from airtest.core.android import Android
from Android.app import app_start, video_cut, base, network, app_phone

# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
from Android.app.app_start import StartMethod


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('/Users/sunpeng/Documents/review/device_tool/ui/android.ui', self)
        self.dev = Android()
        # 获取基础设备相关信息
        # self.init_ui_base()
        # self.init_ui_start()
        # self.init_ui_lp()
        # self.init_ui_fps()
        # self.show_img()
        time.sleep(3)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(500)

        # 顶部设备信息相关

    def init_ui_base(self):
        base_ = base.BaseMethod(self.dev)
        app_list = base_.get_app_list()
        self.device_app_list.addItems(app_list)

    # 左侧安卓屏幕展示
    def init_phone_img(self):
        phone_info = app_phone.InitMethod(self.dev, self.phone_show)
        phone_info.show_img()

    def init_ui_lp(self):
        # 录制视频按钮点击事件
        app_ = video_cut.Video_Cut()
        self.lp_choice_video.clicked.connect(self.onFileChoose)
        self.lp_start_clive_video.clicked.connect(
            lambda: app_.start_covert_video(self.lp_video_file_path.text(), self.lp_pictures))

    # 加载启动时间页面的UI文件
    def init_ui_start(self):
        app_ = app_start.StartMethod(self.dev)

        self.start_get_current_activity.clicked.connect(
            lambda: self.start_input_activity.setText(app_.get_top_activity()))
        self.start_get_start_activity.clicked.connect(app_.get_start_activity)
        self.start_time_test.clicked.connect(
            lambda: self.label_4.setText(app_.get_start_time(package_name=self.device_app_list.currentText(),
                                                             start_activity=self.start_input_activity.text(),
                                                             num=int(
                                                                 self.start_test_num.text()) if self.start_test_num.text() != "" else 3))
        )

    # 加载FPS页面的UI文件
    def init_ui_fps(self):
        app_ = network.AppNetworkMethod()
        self.fps_start_test.clicked.connect(lambda: app_.start_(self.fps_layout))

    def onFileChoose(self):
        cwd = os.getcwd()
        filename, filetype = QFileDialog.getOpenFileName(self, '选择文件',
                                                         cwd,  # 起始路径
                                                         'Text Files(*.mp4);;All Files(*)')  # 文件扩展名过滤器
        self.lp_video_file_path.setText(filename)

    def update_screen(self):
        img = self.dev.snapshot(quality=100)
        image = QImage(
            img,
            img.shape[1],
            img.shape[0],
            img.shape[1] * 3,
            QImage.Format_BGR888,
        )
        pixmap = QPixmap(image)
        scaled_pixmap = pixmap.scaled(self.phone_show.width(), self.phone_show.height(),
                                      QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # 缩放图像以适应 QLabel 大小
        self.phone_show.setPixmap(scaled_pixmap)  # 在 QLabel 上显示缩放后的图像


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())
