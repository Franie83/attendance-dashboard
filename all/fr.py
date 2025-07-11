import streamlit as st
import face_recognition
import numpy as np
import os
import cv2
from PIL import Image
import tempfile

# Directory to store face images
KNOWN_DIR = r"C:\Users\USER\Documents\ATTNDB\facerecognition"
os.makedirs(KNOWN_DIR, exist_ok=True)

st.set_page_config(page_title="Face Recognition Attendance", layout="centered")
st.title("📸 Face Recognition Attendance System")

# Helper: get face encoding
def get_face_encoding(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        if image.dtype != np.uint8 or image.ndim != 3:
            raise ValueError("Unsupported image format")
        encodings = face_recognition.face_encodings(image)
        return encodings[0] if encodings else None
    except Exception as e:
        st.warning(f"❌ Failed to encode {os.path.basename(image_path)}: {e}")
        return None

# Helper: fix image to proper format
def fix_image_format(image_pil, save_path):
    image_rgb = image_pil.convert("RGB")
    image_rgb.save(save_path, format="JPEG")

# Sidebar
page = st.sidebar.radio("Choose page", ["🔐 Register", "✅ Recognize"])

# -----------------------------
# 🔐 PAGE 1: Register
# -----------------------------
if page == "🔐 Register":
    st.subheader("Register a New Person")
    name = st.text_input("Enter Full Name")

    camera_input = st.camera_input("Capture your face")

    if camera_input is not None:
        if not name.strip():
            st.warning("⚠️ Please enter a name before capturing.")
        else:
            save_path = os.path.join(KNOWN_DIR, f"{name.strip()}.jpg")
            image = Image.open(camera_input)
            fix_image_format(image, save_path)
            st.success(f"✅ {name} registered successfully!")

# -----------------------------
# ✅ PAGE 2: Recognize
# -----------------------------
elif page == "✅ Recognize":
    st.subheader("Live Face Recognition")

    # Load registered face encodings
    known_encodings = []
    known_names = []
    known_images = {}

    for file in os.listdir(KNOWN_DIR):
        if file.lower().endswith(".jpg"):
            path = os.path.join(KNOWN_DIR, file)
            encoding = get_face_encoding(path)
            if encoding is not None:
                known_encodings.append(encoding)
                name = os.path.splitext(file)[0]
                known_names.append(name)
                known_images[name] = path

    if not known_encodings:
        st.warning("⚠️ No registered faces found. Please register first.")
    else:
        run = st.checkbox("Start Webcam")

        FRAME_WINDOW = st.image([])

        cap = cv2.VideoCapture(0)

        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Webcam error.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                name = "Unknown"
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                    # Draw rectangle & name
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Show registered image
                    st.image(known_images[name], caption=f"✅ Recognized: {name}", use_container_width=True)

            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)

        cap.release()
