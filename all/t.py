#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
from PIL import Image
import os

KNOWN_FACES_DIR = r"C:\Users\USER\Documents\ATTNDB\facerecongnition"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

st.title("Webcam Registration Test")

name = st.text_input("Enter your full name")

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    if not name.strip():
        st.warning("Please enter your name before capturing.")
    else:
        img = Image.open(img_file_buffer)
        save_path = os.path.join(KNOWN_FACES_DIR, f"{name.strip()}.jpg")
        img.save(save_path)
        st.success(f"Image saved for {name}")
        st.image(img)


# In[ ]:





# In[ ]:




