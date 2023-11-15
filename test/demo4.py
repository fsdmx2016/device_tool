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
        self.phone_show.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # I'm assuming the following...
        self.phone_show.setScaledContents(True)
        # self.phone_show.setFixedSize(701, 451)

        # install an event filter to "capture" mouse events (amongst others)
        self.phone_show.installEventFilter(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(500)


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

        # adjust the position to the contents margins
        pos -= contentsRect.topLeft()

        pixmapRect = self.phone_show.pixmap().rect()
        if self.phone_show.hasScaledContents():
            x = pos.x() * pixmapRect.width() / contentsRect.width()
            y = pos.y() * pixmapRect.height() / contentsRect.height()
            pos = QtCore.QPoint(x, y)
        else:
            align = self.phone_show.alignment()
            pixmapRect = QtCore.QRectF(pixmapRect)
            if align & QtCore.Qt.AlignRight:
                pixmapRect.moveRight(contentsRect.x() + contentsRect.width())
            elif align & QtCore.Qt.AlignHCenter:
                pixmapRect.moveLeft(contentsRect.center().x() - pixmapRect.width() / 2)
            # the pixmap is not top aligned (note that the default for QLabel is
            # Qt.AlignVCenter, the vertical center)
            if align & QtCore.Qt.AlignBottom:
                pixmapRect.moveBottom(contentsRect.y() + contentsRect.height())
            elif align & QtCore.Qt.AlignVCenter:
                pixmapRect.moveTop(contentsRect.center().y() - pixmapRect.height() / 2)

            if not pos in pixmapRect:
                return
            pos = (pos - pixmapRect.topLeft()).toPoint()
        x_val=pos.x()
        y_val=pos.y()
        os.system(f"adb shell input tap {x_val} {y_val}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())
