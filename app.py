from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
from PIL import Image
import pathlib
import textwrap

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(prompt,query,image):
    response =model.generate_content([prompt,query,image[0]])
    return response.text

def get_Image_data(image):
    if image is not None:
        byte_data = image.getvalue()
        image_parts = [
            {
            "mime_type": image.type,
            "data" : byte_data
            }
        ]
        return image_parts
  
prompt ="""
         you are multilanguage expert invoice extractor and 
         you are very good at extracting data within image.
         think twise before giving answers.
        you will receive an image and from that only answer the queries.

    """

st.title("Gemini")
# input = st.text_input("Enter query:")
upload_image = st.file_uploader("Choose an image...",type=["jpg", "jpeg", "png"])

if upload_image:
    image = Image.open(upload_image)
    st.image(image, caption='Uploaded Image.',use_column_width=True)

input = st.text_input("Enter query:")
submit=st.button("Tell me about the image")
if submit:
    with st.spinner("Generating response..."):
        image_data = get_Image_data(upload_image)
        response=get_gemini_response(prompt,input,image_data)
        st.subheader("The Response is")
        st.write(response)
    
 