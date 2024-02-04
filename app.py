import os
import random
import json
import streamlit as st
from PIL import Image
from streamlit_image_select import image_select
from src.utils.search import search_top_k
from config import *

import sys
sys.path.insert(0, UTILS_DIR)

st.set_page_config(layout="wide")
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

# # This markdown makes the button with primary kind look like a clickable line of text
# st.markdown(
#     """
#     <style>
#     button[kind="primary"] {
#         background: none!important;
#         border: none;
#         padding: 0!important;
#         color: black !important;
#         text-decoration: none;
#         cursor: pointer;
#         border: none !important;
#     }
#     button[kind="primary"]:hover {
#         text-decoration: none;
#         color: black !important;
#     }
#     button[kind="primary"]:focus {
#         outline: none !important;
#         box-shadow: none !important;
#         color: black !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

def load_images_statics(folder_path, begin=0, top_k=25):
    # Đọc danh sách tất cả các tệp hình ảnh trong thư mục
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg'))]

    selected_images_files = image_files[begin:(begin+top_k)]
    images = []
    image_names = []
    for image_file in selected_images_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        images.append(image)
        image_names.append(image_file)
        
    return images, image_names

def load_queries_rcm(folder_path, image_filename):
    queries = None
    image_name, image_extention = os.path.splitext(image_filename)
    
    json_path = os.path.join(folder_path, "filtered_gallery.json")
    with open(json_path, 'r') as file:
        query_list = json.load(file)    
    
    for obj in query_list:
        if obj['candidate'] == image_name:
            queries = obj['captions']
            break
    return queries
    
def display_images_rcm(label: str, images: list, image_names: list, use_container_width=False):
    img = image_select(
            label = label,
            images = images,
            captions = image_names, 
            use_container_width=False
        )          
    return img

def display_results(result_images, result_filenames, top_k = 50):
    # Resize all images to the same dimensions
    target_size = (300, 300)
    resized_result_images = [image.resize(target_size) for image in result_images]

    # Display the results with 8 images per row
    n_cols = 8  # Number of images per row
    n_rows = 1 + top_k // n_cols
    rows = [st.container() for _ in range(n_rows)]
    cols_per_row = [r.columns(n_cols) for r in rows]
    cols = [column for row in cols_per_row for column in row]

    for image_index, (image, filename) in enumerate(zip(resized_result_images, result_filenames)):
        cols[image_index].image(image, caption=filename)

# Streamlit app
def main():   
    query_image = None
    source = True
    st.title("Mineral Fashion Image Retrieval System")   
    
    col1, col2 = st.columns(2)
    # Add select box to choose whether using uploaded images or recommended ones
    selected_image_source = col1.selectbox("Select image source:", ["Upload", "Recommended gallery"])

    if selected_image_source == "Upload":
        uploaded_image = col1.file_uploader("Please upload your query image!", type=["jpg", "png"])
        query_image = uploaded_image
        
    elif selected_image_source == "Recommended gallery":
        source = False
        with col2:
            n_rcm = 20
            begin_index = col2.slider("Slide this for different galleries", min_value=0, max_value=14890-n_rcm, value=0, step=n_rcm)
            images, images_name = load_images_statics("./splited_fashionIQ/val", begin_index, n_rcm)
            img = display_images_rcm("OR Choose one", images, images_name)
            
        query_image = img        
        
    with col1:
        cola, colb = st.columns(2)
        if query_image is not None:
            with cola:
                if source:
                    query_image = Image.open(uploaded_image)
                    query_image_filename = os.path.basename(query_image.filename)
                    st.markdown("Query image: **" + query_image_filename + "**")
                    st.image(query_image, width=300)
                else:
                    query_image_filename = os.path.basename(query_image.filename)
                    st.markdown("Query image: **" + query_image_filename + "**")
                    st.image(query_image, width=300)
            
            queries_rcm = load_queries_rcm("./", query_image_filename)
            
            if queries_rcm:
                colb.markdown("**Recommended queries:**")
                for idx, query in enumerate(queries_rcm, start=1):
                    colb.write(f"Query {idx}: {query}")
                    
            query_text = st.text_input("Enter a description for retrieval", max_chars=50)
            top_k = st.slider("How many results do you want to have?", min_value=10, max_value=100, value=50, step=10)
            search_btt = st.button(label="Search")

    # Check if search_btt is defined before using it
    if 'search_btt' in locals():
        if search_btt:
            # Check if text_input is empty
            if not query_text.strip():
                col1.error("Error: Description cannot be empty. Please enter a valid description.")
            else:            
                # Perform the search and display the results
                result_images, result_filenames = search_top_k(query_image, str(query_text), top_k)
                st.write("Here are the top " + str(top_k) + " results")
                display_results(result_images, result_filenames, top_k)
                     
if __name__ == "__main__":
    main()