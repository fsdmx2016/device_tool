from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
import sys

from airtest.core.android import Android
from Android.app import app_start
# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.dev = Android()
        start_ac=start.StartMethod(self.dev)
        self.page2_get_current_activity.clicked.connect(start_ac.get_current_activity)  # 绑定按钮的点击信号和对应的槽函数


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())
