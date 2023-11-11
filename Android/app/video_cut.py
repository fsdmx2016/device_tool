import cv2
import os
# 视频分帧方法
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Video_Cut():

    # def video_to_frames(self,video_path):
    #     # 打开视频文件
    #     video = cv2.VideoCapture(video_path)
    #     frame_rate = video.get(cv2.CAP_PROP_FPS)  # 获取视频帧率
    #     count = 0  # 计数器，用于命名保存的图片文件
    #     temp = os.path.split(video_path)[-1]
    #     dir_name = temp.split('.')[0]
    #     single_pic_store_dir = os.path.split(video_path)[0] + "/" + dir_name
    #     while True:
    #         # 读取视频中的一帧
    #         ret, frame = video.read()
    #
    #         # 当读取到视频末尾时，退出循环
    #         if not ret:
    #             break
    #         # 计算当前帧的时间（秒）
    #         current_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000
    #         # 每隔一秒保存一帧图片
    #         if int(current_time) % 1 == 0:
    #             # 保存图片
    #
    #             frame_path = os.path.join(single_pic_store_dir, fileName) + "/frame_" + str(count) + ".jpg"
    #             cv2.imwrite(frame_path, frame)
    #             count += 1
    #
    #     # 释放视频对象
    #     video.release()


    def video_cut(self, video_file):
        cap = cv2.VideoCapture(video_file)
        isOpened = cap.isOpened
        temp = os.path.split(video_file)[-1]
        dir_name = temp.split('.')[0]
        single_pic_store_dir =os.path.split(video_file)[0]+"/"+dir_name
        if not os.path.exists(single_pic_store_dir):
            os.mkdir(single_pic_store_dir)
        i = 0
        while isOpened:
            i += 1
            (flag, frame) = cap.read()  # 读取一张图像
            fileName = 'image' + str(i) + ".jpg"
            if (flag == True):
                # 设置保存路径
                save_path = os.path.join(single_pic_store_dir, fileName)
                cv2.imwrite(save_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            else:
                break
        return single_pic_store_dir

    def show_image(slef, path: str, scroll_areas):
        image_files = [file for file in os.listdir(path) if
                       file.endswith(('.jpg', '.jpeg', '.png'))]
        picture_list = []
        for i in image_files:
            picture_list.append(path + "\\" + i)
        # 创建一个QWidget作为中心部件
        central_widget = QWidget()
        # self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建一个滚动区域
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # 创建一个水平布局
        image_layout = QHBoxLayout()
        image_layout.setAlignment(Qt.AlignLeft)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(QWidget())

        # 在水平布局中添加图片
        for image_path in picture_list:
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap.scaledToWidth(500))  # 根据需要设置图片宽度
            image_layout.addWidget(image_label)

        # 将水平布局设置为滚动区域的子控件
        scroll_area.widget().setLayout(image_layout)
        scroll_areas.setLayout(layout)

    def select_file(self, text_edit):
        self.cwd = os.getcwd()

        filename, filetype = QFileDialog.getOpenFileName(self, '选择文件',
                                                         self.cwd,  # 起始路径
                                                         'Text Files(*.mp4);;All Files(*)')  # 文件扩展名过滤器
        if filename == '':
            self.statusBar.showMessage('取消选择', 2000)
            return
        #
        # # file_dialog.setNameFilter("Text Files (*.mp4)")
        # if filename.exec():
        #     file_path = fd.selectedFiles()[0]
        #     # with open(file_path, 'r') as file:
        #     #     file_content = file.read()
        #     #     text_edit.setText(file_content)
        #     text_edit.setText(file_path)

    def start_covert_video(self, video_file,scroll_areas):
        file_path = Video_Cut.video_cut(self, video_file)
        Video_Cut.show_image(self,file_path,scroll_areas)