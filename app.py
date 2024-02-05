import os
import random
import json
import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit_image_select import image_select
from src.utils.search import *
from src.utils.query_reformulate import *
from src.utils.config import *

# Set page config
st.set_page_config(
    page_title="Mineral Fashion Image Retrieval System",
    layout="wide"
)

def paginator(label, items, items_per_page=20):
    # This function creates a pagination selectbox in the sidebar.
    items = list(items)
    n_pages = (len(items) - 1) // items_per_page + 1  # Calculate the number of pages
    page_format_func = lambda i: "Page %s" % (i+1)  # Format the page numbers
    page_number = st.sidebar.selectbox(label, range(n_pages), index=0, format_func=page_format_func)  # Create the selectbox
    return page_number

@st.cache_data
def load_batch(page_number, items, items_per_page=20):
    # This function loads a batch of items for the given page number.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    return items[min_index : max_index]  # Return the items for the current page

@st.cache_data
def load_gallery():
    # This function loads the gallery from a JSON file.
    with open(FILTERED_JSON, 'r') as file:
        gallery = json.load(file)
    return gallery

def display_images_rcm(label: str, batch, use_container_width=False):
    # This function displays a batch of images.
    images = [Path(DATASET_DIR / 'val' / str(obj['candidate'] + '.png')) for obj in batch]  # Load the images
    images_name = [str(obj['candidate'] + '.png') for obj in batch]  # Get the image names

    img = image_select(
            label = label,
            images = images,
            captions = images_name, 
            use_container_width=False
        )          
    return img

@st.cache_data
def search(_query_image, query_text, top_k=50):
    # This function performs a search and returns the top k results.
    result_images, result_filenames = search_top_k(_query_image, query_text, top_k)
    return result_images, result_filenames

def display_results(result_images, result_filenames, top_k = 50):
    # This function displays the search results.
    target_size = (300, 300)  # The target size for the images
    resized_result_images = [image.resize(target_size) for image in result_images]  # Resize the images

    # Display the results with 8 images per row
    n_cols = 8  # Number of images per row
    n_rows = 1 + top_k // n_cols  # Calculate the number of rows
    rows = [st.container() for _ in range(n_rows)]  # Create the rows
    cols_per_row = [r.columns(n_cols) for r in rows]  # Create the columns for each row
    cols = [column for row in cols_per_row for column in row]  # Flatten the list of columns

    for idx, (image, filename) in enumerate(zip(resized_result_images, result_filenames)):
        cols[idx].image(image, caption=filename)  # Display each image

# Streamlit app
st.title("Mineral Fashion Image Retrieval System")


# Query image
with st.sidebar:
    st.header("Query Panel")
    selected_image_source = st.selectbox("Select image source", ("Upload", "Recommended gallery"))
    if selected_image_source == "Upload":
        query_image = st.file_uploader("Upload your query image", type=["jpg", "png", "jpeg"])

    elif selected_image_source == "Recommended gallery":
        gallery = load_gallery()
        page_number = paginator("Pagination", gallery)
        batch = load_batch(page_number, gallery)

if selected_image_source == "Upload":
    pass
elif selected_image_source == "Recommended gallery":
    query_image_path = display_images_rcm("Choose one of the recommended images:", batch)
    query_image_name = query_image_path.name.split('.')[0]
    query_image = Image.open(query_image_path)

# Show query image
if query_image is not None:
    st.sidebar.image(query_image, width=200)
    if selected_image_source == "Upload":
        query_image = Image.open(query_image)
    elif selected_image_source == "Recommended gallery":
        query_obj = [obj for obj in batch if obj['candidate'] == query_image_name][0]

    # Query text
    with st.sidebar:
        query_text = st.text_input("Enter a description for retrieval", max_chars=76)
        if selected_image_source == "Upload":
            pass
        elif selected_image_source == "Recommended gallery":
            # Recommended text queries
            st.write("Recommended descriptions:")
            for text in query_obj['captions']:
                st.write("`" + text + "`")

        # top_k slider
        top_k = st.slider("How many results do you want to receive?", min_value=10, max_value=100, value=50, step=10)
        search_btt = st.sidebar.button("Search", type="primary", use_container_width=True)

    if search_btt:
        # Check if text_input is empty
        if not query_text.strip():
            st.toast("Error: Description cannot be empty. Please enter a valid description.")
        else:
            # Perform the search and display the results
            result_images, result_filenames = search(query_image, str(query_text), top_k)
            st.write("Here are the top " + str(top_k) + " results")
            display_results(result_images, result_filenames, top_k)
