import cv2
import os
# 视频分帧方法
def video_cut(video_file, target_dir):
    cap = cv2.VideoCapture(video_file)
    isOpened = cap.isOpened
    temp = os.path.split(video_file)[-1]
    dir_name = temp.split('.')[0]
    single_pic_store_dir = os.path.join(target_dir, dir_name)
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
            res = cv2.imwrite(save_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        else:
            break
    return single_pic_store_dir
