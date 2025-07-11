# opencv_cleaner.py
import cv2
import os

FOLDER_PATH = r"C:\Users\USER\Documents\ATTNDB\facerecognition"
print(f"🧹 Scanning and cleaning folder: {FOLDER_PATH}")

valid_count = 0
deleted_count = 0

for file in os.listdir(FOLDER_PATH):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        full_path = os.path.join(FOLDER_PATH, file)
        try:
            # Read and re-encode image using OpenCV
            img = cv2.imread(full_path)
            if img is None or len(img.shape) != 3:
                raise ValueError("Unreadable or not a 3-channel image")

            new_path = os.path.join(FOLDER_PATH, f"cv2_{file}")
            cv2.imwrite(new_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            os.remove(full_path)  # Remove original
            os.rename(new_path, full_path)  # Replace with cleaned one

            print(f"✅ Cleaned and overwritten: {file}")
            valid_count += 1

        except Exception as e:
            print(f"🗑️ Corrupt or unreadable: {file} — Deleting... ({e})")
            os.remove(full_path)
            deleted_count += 1

print(f"\n✅ Done. {valid_count} image(s) valid, {deleted_count} deleted.")
