import cv2
import os
import numpy as np

# === CONFIG ===
face_dir = r"C:\Users\USER\Documents\ATTNDB\facerecongnition"
captured_path = r"C:\Users\USER\Documents\ATTNDB\captured.jpg"
output_txt = r"C:\Users\USER\Documents\recognized_name.txt"

# === PREPARE TRAINING DATA ===
faces = []
labels = []
label_map = {}
label_counter = 0

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

for file in os.listdir(face_dir):
    if file.endswith(('.jpg', '.png')):
        img_path = os.path.join(face_dir, file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        faces_rect = detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces_rect:
            face_img = img[y:y+h, x:x+w]
            faces.append(face_img)
            labels.append(label_counter)
        label_map[label_counter] = os.path.splitext(file)[0]
        label_counter += 1

# === TRAIN LBPH MODEL ===
if not faces:
    print("❌ No training faces found.")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

# === READ CAPTURED FACE ===
test_img = cv2.imread(captured_path, cv2.IMREAD_GRAYSCALE)
if test_img is None:
    print("❌ Could not read captured image.")
    exit()

faces_rect = detector.detectMultiScale(test_img, 1.3, 5)

name = "Unknown"
for (x, y, w, h) in faces_rect:
    roi = test_img[y:y+h, x:x+w]
    label, confidence = recognizer.predict(roi)
    if confidence < 70:
        name = label_map[label]

# === WRITE RESULT ===
with open(output_txt, "w") as f:
    f.write(name)
print(f"✔ Result: {name}")
