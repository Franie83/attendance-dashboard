#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import face_recognition
import cv2
import numpy as np
import os
from PIL import Image

# Constants
KNOWN_FACES_DIR = os.path.expanduser(r"C:\Users\USER\Documents\ATTNDB\facerecognition")
OUTPUT_TXT_FILE = os.path.expanduser(r"C:\Users\USER\Documents\ATTNDB\recognized_name.txt")

os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

st.set_page_config(page_title="Face Recognition Attendance", layout="centered")
st.title("📸 Face Recognition Attendance System")

page = st.sidebar.radio("Choose page", ["🔐 Register via Camera", "✅ Face Recognition"])

# Registration Page
if page == "🔐 Register via Camera":
    st.subheader("Register New Person via Webcam")

    name = st.text_input("Enter Full Name")

    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        if not name.strip():
            st.warning("⚠️ Please enter a name before capturing.")
        else:
            # Convert to RGB to avoid unsupported image errors
            img = Image.open(img_file_buffer).convert('RGB')
            save_path = os.path.join(KNOWN_FACES_DIR, f"{name.strip()}.jpg")
            img.save(save_path)
            st.success(f"✅ {name} registered successfully.")
            st.image(img, caption="Captured Image", use_column_width=True)

# Face Recognition Page
elif page == "✅ Face Recognition":
    st.subheader("Face Recognition from Webcam")

    if st.button("🎥 Start Webcam for Recognition"):
        known_encodings = []
        known_names = []

        # Load and encode known faces
        for file in os.listdir(KNOWN_FACES_DIR):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(KNOWN_FACES_DIR, file)
                try:
                    # Load image forcing RGB mode
                    image = face_recognition.load_image_file(path, mode='RGB')
                    # Remove alpha channel if present
                    if image.shape[2] == 4:
                        image = image[:, :, :3]
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_encodings.append(encodings[0])
                        known_names.append(os.path.splitext(file)[0])
                except Exception as e:
                    st.warning(f"❌ Error loading {file}: {e}")

        if not known_encodings:
            st.warning("⚠️ No registered faces found. Please register first.")
        else:
            cap = cv2.VideoCapture(0)
            stframe = st.empty()
            recognized = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("❌ Failed to read from webcam.")
                    break

                rgb_frame = frame[:, :, ::-1]  # BGR to RGB
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding)
                    distances = face_recognition.face_distance(known_encodings, face_encoding)

                    if matches and any(matches):
                        best_match_index = np.argmin(distances)
                        if matches[best_match_index]:
                            name = known_names[best_match_index]
                            with open(OUTPUT_TXT_FILE, "w") as f:
                                f.write(name)
                            st.success(f"✅ {name} recognized and written to file.")
                            recognized = True
                            break

                stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

                if recognized:
                    break

            cap.release()
import streamlit as st
import face_recognition
import cv2
import numpy as np
import os
from PIL import Image

# Constants
KNOWN_FACES_DIR = os.path.expanduser(r"C:\Users\USER\Documents\ATTNDB\facerecognition")
OUTPUT_TXT_FILE = os.path.expanduser(r"C:\Users\USER\Documents\ATTNDB\recognized_name.txt")

os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

st.set_page_config(page_title="Face Recognition Attendance", layout="centered")
st.title("📸 Face Recognition Attendance System")

page = st.sidebar.radio("Choose page", ["🔐 Register via Camera", "✅ Face Recognition"])

# Registration Page
if page == "🔐 Register via Camera":
    st.subheader("Register New Person via Webcam")

    name = st.text_input("Enter Full Name")

    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        if not name.strip():
            st.warning("⚠️ Please enter a name before capturing.")
        else:
            # Convert to RGB to avoid unsupported image errors
            img = Image.open(img_file_buffer).convert('RGB')
            save_path = os.path.join(KNOWN_FACES_DIR, f"{name.strip()}.jpg")
            img.save(save_path)
            st.success(f"✅ {name} registered successfully.")
            st.image(img, caption="Captured Image", use_column_width=True)

# Face Recognition Page
elif page == "✅ Face Recognition":
    st.subheader("Face Recognition from Webcam")

    if st.button("🎥 Start Webcam for Recognition"):
        known_encodings = []
        known_names = []

        # Load and encode known faces
        for file in os.listdir(KNOWN_FACES_DIR):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(KNOWN_FACES_DIR, file)
                try:
                    # Load image forcing RGB mode
                    image = face_recognition.load_image_file(path, mode='RGB')
                    # Remove alpha channel if present
                    if image.shape[2] == 4:
                        image = image[:, :, :3]
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_encodings.append(encodings[0])
                        known_names.append(os.path.splitext(file)[0])
                except Exception as e:
                    st.warning(f"❌ Error loading {file}: {e}")

        if not known_encodings:
            st.warning("⚠️ No registered faces found. Please register first.")
        else:
            cap = cv2.VideoCapture(0)
            stframe = st.empty()
            recognized = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("❌ Failed to read from webcam.")
                    break

                rgb_frame = frame[:, :, ::-1]  # BGR to RGB
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding)
                    distances = face_recognition.face_distance(known_encodings, face_encoding)

                    if matches and any(matches):
                        best_match_index = np.argmin(distances)
                        if matches[best_match_index]:
                            name = known_names[best_match_index]
                            with open(OUTPUT_TXT_FILE, "w") as f:
                                f.write(name)
                            st.success(f"✅ {name} recognized and written to file.")
                            recognized = True
                            break

                stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

                if recognized:
                    break

            cap.release()

