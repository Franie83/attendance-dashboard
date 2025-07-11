import face_recognition
from PIL import Image
import matplotlib.pyplot as plt

image_path = r"C:\Users\USER\Documents\ATTNDB\facerecognition\ggg.jpg"

try:
    print(f"🔍 Loading image: {image_path}")
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image)

    print(f"🧠 Faces detected: {len(face_locations)}")

    if not face_encodings:
        print("❌ No face encodings generated.")
    else:
        print("✅ Face encoding generated successfully.")

    # Optional: Show image with matplotlib
    pil_img = Image.fromarray(image)
    plt.imshow(pil_img)
    plt.title(f"Faces detected: {len(face_locations)}")
    plt.axis("off")
    plt.show()

except Exception as e:
    print(f"❌ Failed to process image: {e}")
