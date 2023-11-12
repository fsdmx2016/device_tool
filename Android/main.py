import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

from airtest.core.android import Android
from Android.app import app_start, video_cut, base, network

# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
from Android.app.app_start import StartMethod


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('D:\\WorkDemo\\device_tool\\ui\\android.ui', self)
        # self.dev = Android()
        # 获取基础设备相关信息
        # self.init_ui_base()
        # self.init_ui_start()
        # self.init_ui_lp()
        self.init_ui_fps()

    def init_ui_base(self):
        base_ = base.BaseMethod(self.dev)
        app_list = base_.get_app_list()
        self.device_app_list.addItems(app_list)

    def init_ui_lp(self):
        # 录制视频按钮点击事件
        app_ = video_cut.Video_Cut()
        self.lp_choice_video.clicked.connect(self.onFileChoose)
        self.lp_start_clive_video.clicked.connect(
            lambda: app_.start_covert_video(self.lp_video_file_path.text(), self.lp_pictures))

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

    def init_ui_fps(self):
        app_ = network.AppNetworkMethod()
        self.fps_start_test.clicked.connect(lambda: app_.start_(self.fps_layout))

    def onFileChoose(self):
        self.cwd = os.getcwd()
        filename, filetype = QFileDialog.getOpenFileName(self, '选择文件',
                                                         self.cwd,  # 起始路径
                                                         'Text Files(*.mp4);;All Files(*)')  # 文件扩展名过滤器
        self.lp_video_file_path.setText(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())
