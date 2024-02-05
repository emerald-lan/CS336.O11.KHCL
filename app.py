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
    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % (i+1)
    page_number = st.sidebar.selectbox(label, range(n_pages), index=0, format_func=page_format_func)
    return page_number

@st.cache_data
def load_batch(page_number, items, items_per_page=20):
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    return items[min_index : max_index]


@st.cache_data
def load_gallery():
    with open(FILTERED_JSON, 'r') as file:
        gallery = json.load(file)
    return gallery


def display_images_rcm(label: str, batch, use_container_width=False):
    images = [Path(DATASET_DIR / 'val' / str(obj['candidate'] + '.png')) for obj in batch]
    images_name = [str(obj['candidate'] + '.png') for obj in batch]

    img = image_select(
            label = label,
            images = images,
            captions = images_name, 
            use_container_width=False
        )          
    return img

@st.cache_data
def search(_query_image, query_text, top_k=50):
    result_images, result_filenames = search_top_k(_query_image, query_text, top_k)
    return result_images, result_filenames

def display_results(result_images, result_filenames, top_k = 50):
    # Resize all images to the same dimensions
    target_size = (300, 300)
    resized_result_images = [image.resize(target_size) for image in result_images]

    # Display the results with 8 images per row
    n_cols = 5  # Number of images per row
    n_rows = 1 + top_k // n_cols
    rows = [st.container() for _ in range(n_rows)]
    cols_per_row = [r.columns(n_cols) for r in rows]
    cols = [column for row in cols_per_row for column in row]

    feedback_values = {}

    def on_change_feedback():
        st.session_state.is_feedback = True

    for idx, (image, filename) in enumerate(zip(resized_result_images, result_filenames)):
        cols[idx].image(image, caption=filename)
        # Add a dropdown menu for each image
        feedback_values[idx] = cols[idx].selectbox("Your feedback", ("none", "relevant", "irrelevant"), key=filename, on_change=on_change_feedback)

    return feedback_values

def map_feedback_values_to_images(feedback_values, result_images):
    rel_images = [image for idx, image in enumerate(result_images) if feedback_values[idx] == "relevant"]
    irr_images = [image for idx, image in enumerate(result_images) if feedback_values[idx] == "irrelevant"]
    return rel_images, irr_images

# Streamlit app
st.title("Mineral Fashion Image Retrieval System")

# Initialize session state variables
st.write(st.session_state)
if "result_images" not in st.session_state:
    st.session_state.result_images = []
if "result_filenames" not in st.session_state:
    st.session_state.result_filenames = []
if "feedback_values" not in st.session_state:
    st.session_state.feedback_values = {}
if "is_feedback" not in st.session_state:
    st.session_state.is_feedback = False


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
        def on_click_search():
            st.session_state.is_feedback = False
            st.session_state.result_images = []
            st.session_state.result_filenames = []
            st.session_state.feedback_values = {}
        search_btt = st.sidebar.button("Search", type="primary", use_container_width=True, on_click=on_click_search)
        if st.session_state.is_feedback == True:
            search_btt = True

    if search_btt:
        # Check if text_input is empty
        if not query_text.strip():
            st.toast("Error: Description cannot be empty. Please enter a valid description.")
        else:
            # Perform the search and display the results
            st.session_state.result_images, st.session_state.result_filenames = search(query_image, str(query_text), top_k)
            st.write("Here are the top " + str(top_k) + " results")
            st.session_state.feedback_values = display_results(st.session_state.result_images, st.session_state.result_filenames, top_k)
            st.write(st.session_state.feedback_values)

    # Add a submit button for feedback
    submit_btt = st.sidebar.button("Submit Feedback")
    if submit_btt:
        # Process the feedback values here
        rel_images, irr_images = map_feedback_values_to_images(st.session_state.feedback_values, st.session_state.result_images)
        st.image(rel_images)
        st.image(irr_images)
