import os
import time

from PyQt5 import QtWidgets, uic, QtCore
import sys

from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
from airtest.core.android import Android
from Android.app import app_start, video_cut, base, network
from Android.app.app_log import LogThread
from Android.app.app_phone import ClickableLabel


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('/Users/sunpeng/Documents/review/device_tool/ui/android.ui', self)
        self.dev = Android()

        time.sleep(3)
        # 安卓投屏相关服务
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(500)
        self.phone_show.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.phone_show.show()

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


class MyLabel(ClickableLabel):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.pixmap() is not None:
            x = event.x()
            y = event.y()
            print("鼠标点击的坐标：", x, y)
            # 执行ADB点击操作，替换为你的ADB点击代码
            os.system(f"adb shell input tap {x} {y}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())
