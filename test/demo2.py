from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import subprocess
import cv2
import airtest.core.api as air_api
from airtest.core.helper import G

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_device()

        self.setWindowTitle("Android Screen Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 1600, 1200)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(500)  # 每0.5秒更新一次屏幕

    def update_screen(self):
        img = G.DEVICE.snapshot(quality=10)
        image = QImage(
            img,
            img.shape[1],
            img.shape[0],
            img.shape[1] * 3,
            QImage.Format_BGR888,
        )
        pixmap = QPixmap(image)
        self.label.setPixmap(pixmap.scaled(self.label.size()))

    def init_device(self):
        air_api.auto_setup(__file__, logdir=True, devices=["Android:///", ])


if __name__ == "__main__":

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
