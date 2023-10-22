import streamlit as st
import numpy as np
import requests
import cv2
from PIL import Image

import io

# from StringIO import StringIO

from urllib.request import urlopen

uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])

url = "http://localhost:8000/upload_image/"
if st.button("Upload image"):
    if uploaded_image is not None:
        st.header("Image before treatment")
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        files = {"file": uploaded_image}
        response = requests.post("http://127.0.0.1:8000/upload_image/", files=files)

        image_after_treatment = Image.open(io.BytesIO(response.content)).convert("RGB")
        st.header("Image after treatment")
        st.image(image_after_treatment, caption="Image after treatment", use_column_width=True)

    # except:
    #     print("Load image!")
