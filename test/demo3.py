import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        for i in range(10):
            self.update_signal.emit(str(i))
            self.msleep(1000)  # 暂停1秒

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Multi-threading Example")
        self.setGeometry(300, 300, 300, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_thread)
        self.layout.addWidget(self.start_button)

        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.update_line_edit)

    def start_thread(self):
        self.worker_thread.start()

    def update_line_edit(self, text):
        self.line_edit.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
