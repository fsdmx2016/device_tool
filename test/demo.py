import cv2

def extract_frames(video_path, output_folder, frame_rate):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)
    # 获取视频的帧率
    fps = video.get(cv2.CAP_PROP_FPS)

    # 计算每隔多少帧取一帧图像
    frame_interval = round(fps / frame_rate)

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
            output_path = f"{output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(output_path, frame)

        # 增加帧计数器
        frame_count += 1

    # 释放视频对象
    video.release()

# 示例用法
video_path = "D:\WorkDemo\device_tool\deo.mp4"
output_folder = "D:\WorkDemo\device_tool\ss"
frame_rate = 1

extract_frames(video_path, output_folder, frame_rate)
