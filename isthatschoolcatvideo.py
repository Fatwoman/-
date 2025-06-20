import cv2
import numpy as np

model = cv2.CascadeClassifier("haar0_model/cascade.xml")
video_path = "test2.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise IOError("❌ 無法開啟影片")

use_custom_resolution = False
target_width = 960

def is_mostly_green(roi, threshold=0.3):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    return cv2.countNonZero(mask) / (roi.shape[0] * roi.shape[1]) > threshold

def is_mostly_gray(roi, brightness_thresh=140, saturation_thresh=70, gray_ratio_thresh=0.15):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    brightness = hsv[:, :, 2]
    saturation = hsv[:, :, 1]
    mask = (brightness > brightness_thresh) & (saturation < saturation_thresh)
    return np.count_nonzero(mask) / (roi.shape[0] * roi.shape[1]) > gray_ratio_thresh

def is_mostly_blue(roi, threshold=0.3):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([90, 40, 40]), np.array([130, 255, 255]))
    return cv2.countNonZero(mask) / (roi.shape[0] * roi.shape[1]) > threshold

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if use_custom_resolution:
        h, w = frame.shape[:2]
        scale = target_width / w
        frame = cv2.resize(frame, (target_width, int(h * scale)))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    boxes = model.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(48, 48)
    )

    if len(boxes) > 0:
        density_map = {}
        for (x, y, w, h) in boxes:
            cx = x + w // 2
            cy = y + h // 2
            key = (cx // 10, cy // 10)
            density_map[key] = density_map.get(key, 0) + 1

        best_key = max(density_map, key=density_map.get)
        best_cx, best_cy = best_key[0] * 10, best_key[1] * 10

        best_box = None
        best_dist = float("inf")
        for (x, y, w, h) in boxes:
            cx = x + w // 2
            cy = y + h // 2
            dist = (cx - best_cx)**2 + (cy - best_cy)**2
            if dist < best_dist:
                roi = frame[y:y + h, x:x + w]
                if roi.shape[0] == 0 or roi.shape[1] == 0:
                    continue
                if is_mostly_green(roi) or is_mostly_gray(roi) or is_mostly_blue(roi):
                    continue
                best_dist = dist
                best_box = (x, y, w, h)

        if best_box:
            x, y, w, h = best_box

            # ✅ 擴大框的大小
            margin = 0.25  # 擴大25%
            new_w = int(w * (1 + margin))
            new_h = int(h * (1 + margin))
            new_x = max(x - (new_w - w) // 2, 0)
            new_y = max(y - (new_h - h) // 2, 0)

            cv2.rectangle(frame, (new_x, new_y), (new_x + new_w, new_y + new_h), (0, 255, 0), 2)
            cv2.putText(frame, "School Cat!", (new_x, new_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("School Cat Detector", frame)
    key = cv2.waitKey(10)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 