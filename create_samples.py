import cv2
import os

info_file = 'annotations/positives.txt'
output_vec = 'annotations/samples.vec'
img_width = 64
img_height = 64
num_samples = 561  # 你標註了幾張就寫幾張

# 讀入所有的標註資料
with open('C:/Users/Racso/OneDrive/桌面/my_project/annotations/positives.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 建立一個命令格式檔案
with open('temp_info.txt', 'w') as f:
    for line in lines:
        f.write(line)

# 呼叫 OpenCV 的 Python 接口來建立 .vec 檔
os.system(f'opencv_createsamples -info temp_info.txt -num {num_samples} -w {img_width} -h {img_height} -vec {output_vec}')