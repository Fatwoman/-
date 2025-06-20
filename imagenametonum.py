import os
from PIL import Image

# 設定圖片來源資料夾
folder_path = r"C:\Users\Racso\OneDrive\桌面\my_project\negatives"

# 可接受的圖像副檔名
valid_extensions = ['.jpg', '.jpeg', '.png']

# 取得圖檔並排序
image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_extensions]
image_files.sort()

# 開始轉換與重新命名
for idx, filename in enumerate(image_files, start=1):
    src_path = os.path.join(folder_path, filename)
    new_name = f"image{idx}negative5.jpg"
    dst_path = os.path.join(folder_path, new_name)

    try:
        # 開啟並轉為 RGB，再存成 JPG
        img = Image.open(src_path).convert("RGB")
        img.save(dst_path, "JPEG")
        print(f"✅ Converted & Renamed: {filename} → {new_name}")

        # 無論副檔名是否為 .jpg，都刪掉原始檔案（避免 EXIF、壓縮差異等殘留）
        if src_path != dst_path:
            os.remove(src_path)

    except Exception as e:
        print(f"❌ Failed to convert {filename}: {e}")

print("\n🧹 所有圖片已轉為標準 .jpg 並重新命名，原始檔案已刪除")
