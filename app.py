import streamlit as st
import torch
from PIL import Image
import torch
import clip
from torchvision.transforms import functional as F
from transformers import CLIPProcessor, CLIPModel

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

# Streamlit app
def main():
    st.title("Mineral Fashion Image Retrieval System")

    # Upload image through Streamlit
    uploaded_image = st.file_uploader("Please upload your query image!", type=["jpg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image)
        image = Image.open(uploaded_image)
        # processed_image = preprocess_image(image)

        # Text input
        text_input = st.text_input("Enter a description for retrieval", max_chars=50)

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
