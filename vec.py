import cv2
import os
import numpy as np
from pathlib import Path

# 設定參數
vec_output = "samples.vec"
annotation_path = Path("C:/Users/Racso/OneDrive/桌面/my_project/annotations/positives.txt")
image_base = Path("C:/Users/Racso/OneDrive/桌面/my_project")

# 每張圖片轉換的寬高（OpenCV Haar cascade 建議 24x24 或 48x48）
width = 24
height = 24

def read_annotations(annotation_file):
    samples = []
    with open(annotation_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            img_path = image_base / parts[0]
            objects = int(parts[1])
            boxes = [tuple(map(int, parts[i:i+4])) for i in range(2, 2 + 4*objects, 4)]
            samples.append((img_path, boxes))
    return samples

def extract_objects(samples):
    objects = []
    for img_path, boxes in samples:
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Warning: Cannot read image {img_path}")
            continue
        for (x, y, w, h) in boxes:
            if w < 1 or h < 1:
                print(f"Warning: Invalid bbox in {img_path} -> ({x},{y},{w},{h})")
                continue
            roi = img[y:y+h, x:x+w]
            if roi.shape[0] < 1 or roi.shape[1] < 1:
                print(f"Warning: Empty ROI extracted from {img_path}")
                continue
            try:
                roi_resized = cv2.resize(roi, (width, height))
                objects.append(roi_resized)
            except Exception as e:
                print(f"Error resizing ROI from {img_path}: {e}")
    return objects

def save_vec_file(objects, output_file):
    num = len(objects)
    with open(output_file, 'wb') as f:
        f.write(b'\x00\x00\x0a\x00')  # vec version
        f.write(num.to_bytes(4, 'little'))
        f.write(width.to_bytes(4, 'little'))
        f.write(height.to_bytes(4, 'little'))
        for obj in objects:
            gray = cv2.cvtColor(obj, cv2.COLOR_BGR2GRAY)
            vec = gray.flatten()
            f.write(vec.tobytes())

# 主程式
if __name__ == "__main__":
    samples = read_annotations(annotation_path)
    objects = extract_objects(samples)
    if len(objects) == 0:
        print("❌ 沒有有效的樣本可以儲存，請確認標註檔與圖片無誤。")
    else:
        save_vec_file(objects, os.path.join(image_base, vec_output))
        print(f"✅ 已成功建立 {vec_output}，共 {len(objects)} 張樣本，大小 {width}x{height}")
