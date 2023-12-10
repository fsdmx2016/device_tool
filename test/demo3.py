import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox


class QmyWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类的构造函数，创建QWidget窗体
        self.setupUi()

    def setupUi(self):
        """页面初始化"""
        # 设置窗体大小及标题
        self.resize(500, 400)
        self.setWindowTitle("QMessageBox组件示例")
        # 创建布局
        self.layout = QVBoxLayout()
        # 创建两个按钮组件
        self.button = QPushButton("消息对话框测试", self)
        self.button.clicked.connect(self.msg_box_information)  # 为button绑定消息对话框
        # 将组件添加到布局中
        self.layout.addWidget(self.button)
        # 为窗体添加布局
        self.setLayout(self.layout)

    def msg_box_information(self):
        """消息对话框"""
        # QMessageBox组件定义
        messageBox = QMessageBox(QMessageBox.Information, "标题", "这是内容信息", QMessageBox.Ok, self)
        # QMessageBox组件设置
        messageBox.button(QMessageBox.Ok).setText("确定")                    # 为按钮设置文本
        reply = messageBox.exec()                                           # 显示一个模式对话框，有返回值
        if reply == QMessageBox.Ok:
            print("消息对话框选择了确定！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myMain = QmyWidget()
    myMain.show()
    sys.exit(app.exec_())
