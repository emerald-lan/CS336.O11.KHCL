import streamlit as st
import torch
from PIL import Image
import cv2
import torch
from tqdm import tqdm
import clip
from torchvision.transforms import functional as F
from transformers import CLIPProcessor, CLIPModel
from streamlit_image_select import image_select

import os
import requests
from zipfile import ZipFile
from io import BytesIO
import gdown
import rarfile

from setup import main as download_files

# Hide the streamlit hamburger and footer
st.markdown("""
<style>
.css-1rs6os.edgvbvh3
{
    visibility: hidden;
}
.css-cio0dv.egzxvld1
{
    visibility: hidden;
}
<\style>
""", unsafe_allow_html=True)

# def download_dataset():
#     dataset_name = "splited_fashionIQ"  # Replace with your desired dataset folder name
#     folder_path = "./data"
#     dataset_url = 'https://drive.google.com/file/d/1B_ahBg0B7nUJE2dYROxdpXpqicMfcyu7/view?usp=sharing'
#     rar_path = "splited_fashionIQ.rar"
#     extract_path = os.path.join(folder_path, dataset_name)

#     # Check if the folder already exists
#     if os.path.exists(extract_path):     
#         return
    
#     st.text("Downloading the dataset. Please wait...")
#     gdown.download(dataset_url, 'splited_fashionIQ.rar', quiet=False, fuzzy=True)
#     st.success("Download completed.")

#     # Extract the downloaded RAR file
#     with rarfile.RarFile(rar_path, 'r') as rf:
#         rf.extractall(extract_path)

#     # Remove the downloaded RAR file
#     os.remove(rar_path)

#     st.success(f"Extraction completed. Path = {folder_path}")

def load_first_images(folder_path):
    # Đọc danh sách tất cả các tệp hình ảnh trong thư mục
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg'))]

    # Lấy danh sách 50 ảnh đầu tiên
    selected_images_files = image_files[:20]
    images = []
    images_name = []
    for image_file in selected_images_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        images.append(image)
        images_name.append(image_file)
        
    return images, images_name

def display_images(label: str, images: list, images_name: list, use_container_width=False):
    img = image_select(
            label = label,
            images = images,
            captions = images_name, 
            use_container_width=False
        )          
    return img

# Streamlit app
def main():   
    query_image = None
    source = True
    
    st.title("Mineral Fashion Image Retrieval System")   
    images, images_name = load_first_images("data/splited_fashionIQ/test")
    
    # Adđ select box to choose whether using uploaded images or recommended ones
    selected_image_source = st.selectbox("Select image source:", ["Upload", "Recommended gallery"])
    
    if selected_image_source == "Upload":            
        uploaded_image = st.file_uploader("Please upload your query image!", type=["jpg", "png"])
        query_image = uploaded_image
        
    elif selected_image_source == "Recommended gallery": 
        img = display_images("OR Choose one", images, images_name)
        query_image = img
        source = False

    if query_image is not None:
        if(source):
            query_image = Image.open(uploaded_image)
            st.image(query_image, width=300)    
        else:
            st.markdown("---") 
            st.write("Query image: " + os.path.basename(query_image.filename))
            
        text_input = st.text_input("Enter a description for retrieval", max_chars=50)
        search_btt = st.button(label="Search")
        

        if search_btt:
            # Check if text_input is empty
            if not text_input.strip():
                st.error("Error: Description cannot be empty. Please enter a description.")     
            else:
                # display_images("images")  
                st.error("200 OK")       
                

if __name__ == "__main__":
    main()
