import streamlit as st
import face_recognition
import cv2
import numpy as np
import os
from PIL import Image
from datetime import datetime

# 📁 Folder for storing known face images
KNOWN_FACES_DIR = r"C:\Users\USER\Documents\ATTNDB\facerecognition"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

st.set_page_config(page_title="📸 Face Recognition Attendance", layout="centered")
st.title("📸 Face Recognition Attendance System")

page = st.sidebar.radio("Choose Page", ["🔐 Register via Camera", "✅ Live Face Recognition", "📷 Test Face Image"])

# -------------------------
# 🔐 Registration Section
# -------------------------
if page == "🔐 Register via Camera":
    st.subheader("Register New Person via Webcam")

    name = st.text_input("Enter Full Name")

    img_file_buffer = st.camera_input("📷 Take a picture")

    if img_file_buffer is not None:
        if not name:
            st.warning("⚠️ Please enter a name before capturing.")
        else:
            # Save the image with person's name (overwrite if exists)
            img = Image.open(img_file_buffer).convert("RGB")
            save_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
            img.save(save_path, format="JPEG")
            st.success(f"✅ {name} registered successfully.")


# -------------------------
# ✅ Live Face Recognition
# -------------------------
elif page == "✅ Live Face Recognition":
    st.subheader("Live Face Recognition")

    known_encodings = []
    known_names = []

    # Load all face encodings
    st.write("🧹 Scanning registered faces...")
    for file in os.listdir(KNOWN_FACES_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(KNOWN_FACES_DIR, file)
            try:
                image = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(image)[0]
                known_encodings.append(encoding)
                known_names.append(os.path.splitext(file)[0])
            except Exception as e:
                st.warning(f"⚠️ Could not load {file}: {e}")

    if len(known_encodings) == 0:
        st.error("⚠️ No registered faces found. Please register first.")
    else:
        run = st.checkbox("Start Camera")

        FRAME_WINDOW = st.image([])

        camera = cv2.VideoCapture(0)

        while run:
            ret, frame = camera.read()
            if not ret:
                st.error("❌ Could not access webcam.")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                top, right, bottom, left = [v * 4 for v in face_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        else:
            camera.release()
            st.warning("🛑 Camera stopped.")


# -------------------------
# 📷 Test Face Image Section
# -------------------------
elif page == "📷 Test Face Image":
    st.subheader("Test a Registered Image")

    files = [f for f in os.listdir(KNOWN_FACES_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files:
        st.error("⚠️ No registered images found.")
    else:
        selected_file = st.selectbox("Select a face image", files)
        img_path = os.path.join(KNOWN_FACES_DIR, selected_file)
        st.image(img_path, caption=f"Testing {selected_file}", use_container_width=True)

        try:
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) == 0:
                st.error("❌ No face detected in this image.")
            else:
                st.success("✅ Face encoding successful.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
