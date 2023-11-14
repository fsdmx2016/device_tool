#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/14 14:03
@Desc    :
"""
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage


class InitMethod:
    def __init__(self, dev, label):
        self.dev = dev
        self.label = label

    def show_img(self):
        timer = QTimer()
        timer.timeout.connect(self.update_screen)
        timer.start(500)  # 每0.5秒更新一次屏幕

    def update_screen(self):
        img = self.dev.snapshot(quality=10)
        image = QImage(
            img,
            img.shape[1],
            img.shape[0],
            img.shape[1] * 3,
            QImage.Format_BGR888,
        )
        pixmap = QPixmap(image)
        self.label.setPixmap(pixmap.scaled(self.label.size()))

    # 加载启动动画
    def show_loading_img(self, label):
        self.movie = QMovie("../../source/loading.gif")
        label.setMovie(self.movie)
        self.movie.start()
