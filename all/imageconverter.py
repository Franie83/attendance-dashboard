#!/usr/bin/env python
# coding: utf-8

# In[5]:


from PIL import Image
import os

FOLDER_PATH = r"C:\Users\USER\Documents\ATTNDB\facerecognition"
print(f"📂 Scanning folder: {FOLDER_PATH}")

for file in os.listdir(FOLDER_PATH):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        full_path = os.path.join(FOLDER_PATH, file)

        try:
            with Image.open(full_path) as img:
                rgb_image = Image.new("RGB", img.size)
                rgb_image.paste(img)

                new_path = os.path.join(FOLDER_PATH, f"cleaned_{file}")
                rgb_image.save(new_path, format="JPEG", quality=95)
                print(f"✅ Cleaned and resaved: {file} ➜ cleaned_{file}")

        except Exception as e:
            print(f"❌ Failed to fix {file}: {e}")


# In[ ]:




