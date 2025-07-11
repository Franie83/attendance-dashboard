import os
import cv2
from PIL import Image
import face_recognition

# Set the folder path
FOLDER_PATH = r"C:\Users\USER\Documents\ATTNDB\facerecognition"

print(f"📂 Deep cleaning: {FOLDER_PATH}\n")

for file in os.listdir(FOLDER_PATH):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        file_path = os.path.join(FOLDER_PATH, file)
        print(f"🔍 Processing: {file}")

        try:
            # Load using OpenCV
            img_cv = cv2.imread(file_path)

            if img_cv is None:
                print(f"❌ OpenCV failed to load: {file}\n")
                continue

            # Force RGB conversion
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

            # Convert to PIL and force save as strict JPEG
            img_pil = Image.fromarray(img_rgb)
            strict_path = os.path.join(FOLDER_PATH, f"strict_{file}")
            img_pil.save(strict_path, format="JPEG", quality=95)

            print(f"✅ Re-encoded and saved: strict_{file}")

            # Test if face_recognition now accepts it
            try:
                image = face_recognition.load_image_file(strict_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    print(f"✅ Face detected in: strict_{file}")
                else:
                    print(f"⚠️ No face found in: strict_{file}")
            except Exception as fe:
                print(f"❌ face_recognition failed on strict_{file}: {fe}")

        except Exception as e:
            print(f"❌ Failed processing {file}: {e}")

        print()

print("✅ All images processed.\n")
