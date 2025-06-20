import os

# 設定資料夾路徑（請確認路徑正確）
neg_folder = r"C:\Users\Racso\OneDrive\桌面\my_project\negatives"

# 設定輸出文字檔路徑
output_txt = os.path.join(neg_folder, "..", "negatives.txt")

# 只處理 .jpg 檔案
with open(output_txt, 'w') as f:
    for filename in os.listdir(neg_folder):
        if filename.lower().endswith(".jpg"):
            relative_path = os.path.join("negatives", filename)
            f.write(relative_path + "\n")
            print(f"✅ 已加入: {relative_path}")

print(f"\n🎯 所有 .jpg 檔案已寫入：{output_txt}")
