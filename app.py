import streamlit as st
import torch
from PIL import Image
import cv2
import torch
from tqdm import tqdm
import clip
from torchvision.transforms import functional as F
from transformers import CLIPProcessor, CLIPModel

import os
import requests
from zipfile import ZipFile
from io import BytesIO

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


# # Load pre-trained CLIP model and processor
# model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
# processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

# # Function to preprocess input image
# def preprocess_image(image):
#     image = image.resize((224, 224))
#     image = F.to_tensor(image)
#     image = F.normalize(image, mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
#     image = image.unsqueeze(0)
#     return image

def download_dataset():
    st.text("Downloading the dataset. Please wait...")

    # Replace the following URL with the actual download link for your dataset
    dataset_url = "<your_dataset_download_link>"
    response = requests.get(dataset_url, stream=True)

    # Get total file size from the Content-Length header
    total_size = int(response.headers.get("content-length", 0))

    # Create a progress bar
    progress_bar = st.progress(0)

    # Create a BytesIO object to store downloaded data
    buffer = BytesIO()

    with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
        for data in response.iter_content(chunk_size=1024):
            buffer.write(data)
            pbar.update(len(data))
            # Update the Streamlit progress bar
            progress_bar.progress(buffer.tell() / total_size)

    st.success("Download completed.")

    # Extract the downloaded ZIP file
    with ZipFile(buffer, "r") as zip_ref:
        zip_ref.extractall(folder_path)

    st.success("Extraction completed.")

def display_images(folder_path, num_images_per_row=10):
    # Đọc danh sách tất cả các tệp hình ảnh trong thư mục
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Lấy danh sách 50 ảnh đầu tiên
    selected_images = image_files[:50]

    # Số dòng và số cột
    num_rows = len(selected_images) // num_images_per_row
    num_columns = num_images_per_row

    # Kích thước ảnh
    image_size = (100, 100)

    # Tạo một hình ảnh mới để vẽ khung
    result_image = Image.new('RGB', (num_columns * (image_size[0] + 10), num_rows * (image_size[1] + 10)), color='white')
    draw = ImageDraw.Draw(result_image)

    # Vị trí hiện tại của ảnh trong danh sách
    current_index = 0

    # Vẽ khung và chèn ảnh vào hình ảnh kết quả
    for row in range(num_rows):
        for col in range(num_columns):
            if current_index >= len(selected_images):
                break

            # Đọc ảnh
            image_path = os.path.join(folder_path, selected_images[current_index])
            img = Image.open(image_path)

            # Vẽ khung cho ảnh
            draw.rectangle([col * (image_size[0] + 10), row * (image_size[1] + 10),
                            (col + 1) * (image_size[0] + 10) - 10, (row + 1) * (image_size[1] + 10) - 10],
                           outline='green', width=10)

            # Chèn ảnh vào hình ảnh kết quả
            result_image.paste(img, (col * (image_size[0] + 10), row * (image_size[1] + 10)))

            current_index += 1

    return result_image


# Streamlit app
def main():
    st.title("Mineral Fashion Image Retrieval System")
    
    uploaded_image = st.file_uploader("Please upload your query image!", type=["jpg", "png"])
    text_input = st.text_input("Enter a description for retrieval", max_chars=50)
    search_btt = st.button(label="Search")

    if uploaded_image is not None:
        st.image(uploaded_image)
        image = Image.open(uploaded_image)
        # processed_image = preprocess_image(image)
   
    if search_btt:
        # Check if text_input is empty
        if not text_input.strip():
            st.error("Error: Description cannot be empty. Please enter a description.")     
    else:
        display_images("images")    
                
        # Perform image retrieval
        # if st.button("Retrieve Images"):
        #     # Encode text
        #     text_encoding = processor(text_input, return_tensors="pt")["input_ids"]

        #     # Forward pass for image and text
        #     with torch.no_grad():
        #         image_encoding = model(pixel_values=processed_image).last_hidden_state[:, 0, :]
        #         text_encoding = model(**processor(text_input, return_tensors="pt")).last_hidden_state[:, 0, :]

        #     # Perform retrieval based on similarity (you need to implement your own retrieval logic here)
        #     # For simplicity, let's just print the encoded vectors for now
        #     st.write("Image Encoding:", image_encoding.numpy())
        #     st.write("Text Encoding:", text_encoding.numpy())

if __name__ == "__main__":
    main()

