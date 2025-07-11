#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

# Set the folder containing your face images
FOLDER_PATH = r"C:\Users\USER\Documents\ATTNDB\facerecognition"

print(f"🧹 Cleaning folder: {FOLDER_PATH}")

deleted = 0
kept = 0

for file in os.listdir(FOLDER_PATH):
    file_path = os.path.join(FOLDER_PATH, file)

    # Only keep files that start with "cv2_" and end with .jpg or .jpeg
    if file.lower().endswith((".jpg", ".jpeg")):
        if file.startswith("cv2_"):
            print(f"✅ Keeping: {file}")
            kept += 1
        else:
            try:
                os.remove(file_path)
                print(f"🗑️ Deleted: {file}")
                deleted += 1
            except Exception as e:
                print(f"❌ Failed to delete {file}: {e}")

print(f"\n🧾 Summary: {kept} image(s) kept, {deleted} deleted.")

