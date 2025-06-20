import cv2
import os

# 設定資料夾
image_folder = "positives"
output_txt = "annotations/positives.txt"

# 建立輸出資料夾
os.makedirs("annotations", exist_ok=True)

# 取得圖片清單
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png'))]

index = 0
drawing = False
ix, iy = -1, -1
rectangles = []

# 顯示寬度上限（根據這個縮放）
display_width = 800

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rectangles
    scale = param["scale"]
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = int(ix / scale), int(iy / scale)
        x2, y2 = int(x / scale), int(y / scale)
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        rectangles.append((x_min, y_min, w, h))

while index < len(image_files):
    img_path = os.path.join(image_folder, image_files[index])
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ 無法讀取圖片：{img_path}")
        index += 1
        continue

    h, w = img.shape[:2]
    scale = display_width / w if w > display_width else 1.0
    display_img = cv2.resize(img, (int(w * scale), int(h * scale)))

    temp_img = display_img.copy()
    rectangles = []

    cv2.namedWindow("Label", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Label", draw_rectangle, param={"scale": scale})

    while True:
        show_img = temp_img.copy()
        for (x, y, w_box, h_box) in rectangles:
            cv2.rectangle(show_img, (int(x * scale), int(y * scale)),
                          (int((x + w_box) * scale), int((y + h_box) * scale)), (0, 255, 0), 2)

        cv2.imshow("Label", show_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):  # 儲存
            error_found = False
            for (x, y, w_box, h_box) in rectangles:
                if x < 0 or y < 0 or w_box <= 0 or h_box <= 0 or x + w_box > w or y + h_box > h:
                    print(f"⚠️ 錯誤：框框超出範圍或大小不合法 → x={x}, y={y}, w={w_box}, h={h_box}")
                    print("🔁 請重新標註此圖片（按 r 重設）")
                    error_found = True
                    break

            if not error_found:
                with open(output_txt, "a") as f:
                    line = f"{image_folder}/{image_files[index]} {len(rectangles)}"
                    for (x, y, w_box, h_box) in rectangles:
                        line += f" {x} {y} {w_box} {h_box}"
                    f.write(line + "\n")
                print(f"✅ 儲存完成：{image_files[index]}")
                break

        elif key == ord("r"):  # 重設
            temp_img = display_img.copy()
            rectangles = []
            print("↺ 重設標註")

        elif key == ord("n"):  # 跳過
            print(f"⏭️ 跳過圖片：{image_files[index]}")
            break

        elif key == ord("q"):  # 離開
            exit()

    index += 1
    cv2.destroyAllWindows()
