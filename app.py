import os
import streamlit as st
from PIL import Image
from streamlit_image_select import image_select
from src.utils.search import search_top_k
from config import *

import sys
sys.path.insert(0, UTILS_DIR)

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

# This markdown makes the button with primary kind look like a clickable line of text
st.markdown(
    """
    <style>
    button[kind="primary"] {
        background: none!important;
        border: none;
        padding: 0!important;
        color: black !important;
        text-decoration: none;
        cursor: pointer;
        border: none !important;
    }
    button[kind="primary"]:hover {
        text-decoration: none;
        color: black !important;
    }
    button[kind="primary"]:focus {
        outline: none !important;
        box-shadow: none !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def load_first_images(folder_path):
    # Đọc danh sách tất cả các tệp hình ảnh trong thư mục
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg'))]

    # Lấy danh sách 60 ảnh đầu tiên
    selected_images_files = image_files[:60]
    images = []
    image_names = []
    for image_file in selected_images_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        images.append(image)
        image_names.append(image_file)
        
    return images, image_names

def display_images(label: str, images: list, image_names: list, use_container_width=False):
    img = image_select(
            label = label,
            images = images,
            captions = image_names, 
            use_container_width=False
        )          
    return img

# Streamlit app
def main():   
    # if st.button("Click me", type="primary"):
    #     st.write("Clicked")
     
    query_image = None
    source = True
    
    st.title("Mineral Fashion Image Retrieval System")   
    images, images_name = load_first_images(DATASET_DIR / "val")
    
    # Adđ select box to choose whether using uploaded images or recommended ones
    selected_image_source = st.selectbox("Select image source:", ["Upload", "Recommended gallery"])
    
    if selected_image_source == "Upload":            
        uploaded_image = st.file_uploader("Please upload your query image!", type=["jpg", "png"])
        query_image = uploaded_image
        
    elif selected_image_source == "Recommended gallery": 
        img = display_images("OR Choose one", images, images_name)
        query_image = img
        source = False
        
    # col1, col2 = st.columns(2)
    # # Thêm text_input vào cột 1
    # with col1:
    #     query_text = st.text_input("Enter a description for retrieval", max_chars=50)
    # # Thêm slider vào cột 2
    # with col2:
    #     top_k = st.slider("How many results do you want to have?", min_value=10, max_value=100, value=50, step=10)

    if query_image is not None:
        if(source):
            query_image = Image.open(uploaded_image)
            st.image(query_image, width=300)    
        else:
            st.markdown("---") 
            st.write("Query image: " + os.path.basename(query_image.filename))
            
        query_text = st.text_input("Enter a description for retrieval", max_chars=50)
        top_k = st.slider("How many results do you want to have?", min_value=10, max_value=100, value=50, step=10)
        search_btt = st.button(label="Search")
        
        if search_btt:
            # Check if text_input is empty
            if not query_text.strip():
                st.error("Error: Description cannot be empty. Please enter a valid description.")     
            else:            
                result_images, result_filenames = search_top_k(query_image, str(query_text), top_k)
                # st.write("Here are the top " + str(top_k) + " results")
                title = "Here are the top " + str(top_k) + " results"
                display_images(title, result_images, result_filenames)    
                
if __name__ == "__main__":
    main()