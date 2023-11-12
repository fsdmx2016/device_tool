import cv2
import os
# 视频分帧方法
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
class Video_Cut():
    def video_cut(self, video_file):
        temp = os.path.split(video_file)[-1]
        dir_name = temp.split('.')[0]
        single_pic_store_dir = os.path.split(video_file)[0] + "\\" + dir_name
        if not os.path.exists(single_pic_store_dir):
            os.mkdir(single_pic_store_dir)
            # 打开视频文件
            video = cv2.VideoCapture(video_file)
            # 获取视频的帧率
            fps = video.get(cv2.CAP_PROP_FPS)
            # 计算每隔多少帧取一帧图像
            frame_interval = round(fps / 1)
            # 初始化帧计数器
            frame_count = 0
            while True:
                # 读取当前帧
                ret, frame = video.read()
                # 如果无法读取帧，说明视频已经结束
                if not ret:
                    break
                # 如果当前帧是需要保留的帧，则保存为图像文件
                if frame_count % frame_interval == 0:
                    output_path = f"{single_pic_store_dir}/frame_{frame_count}.jpg"
                    cv2.imwrite(output_path, frame)
                # 增加帧计数器
                frame_count += 1
            # 释放视频对象
            video.release()
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
    def start_covert_video(self, video_file, scroll_areas):
        file_path = Video_Cut.video_cut(self, video_file)
        Video_Cut.show_image(self, file_path, scroll_areas)

