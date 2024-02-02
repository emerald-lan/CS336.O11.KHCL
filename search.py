import sys
sys.path.insert(0, '.')

import numpy as np
import torch
from pathlib import Path
import torch.nn.functional as F
import clip
from PIL import Image
import matplotlib.pyplot as plt

from utils.load_clip import load_clip_model
from utils.indexer import VectorIndexer

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = load_clip_model("./finetuned_RN50.pt")
features_file =  Path("./features") / "features.npy"
images_ids_file = Path("./features") / "images_ids.csv"
index_file = Path("./features") / "dataset.index"

index = VectorIndexer(features_file, images_ids_file)
index.load_index(index_file)

def extract_query_features(query, text):
    query_preprocessed = preprocess(query).unsqueeze(0).to(device)

    with torch.no_grad():
        text_features = model.encode_text(clip.tokenize(text).to(device))
        text_features /= text_features.norm(dim=-1, keepdim=True)

        image_features = model.encode_image(query_preprocessed)
        image_features /= image_features.norm(dim=-1, keepdim=True)

    combined_features = F.normalize(image_features + text_features, dim=-1)

    return combined_features.cpu().numpy()

def show_image_list(list_images, list_titles=None, grid=False, num_cols=5, figsize=(20, 10), title_fontsize=24):
    if list_titles is not None:
        assert isinstance(list_titles, list)
        assert len(list_images) == len(list_titles), '%d imgs != %d titles' % (len(list_images), len(list_titles))

    num_images  = len(list_images)
    num_cols    = min(num_images, num_cols)
    num_rows    = int(num_images / num_cols) + (1 if num_images % num_cols != 0 else 0)

    # Create a grid of subplots.
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    
    # Create list of axes for easy iteration.
    if isinstance(axes, np.ndarray):
        list_axes = list(axes.flat)
    else:
        list_axes = [axes]

    for i in range(num_images):

        img    = list_images[i]
        title  = list_titles[i] if list_titles is not None else 'Image %d' % (i)
        
        list_axes[i].imshow(img)
        list_axes[i].set_title(title, fontsize=title_fontsize) 
        list_axes[i].grid(grid)

    for i in range(num_images, len(list_axes)):
        list_axes[i].set_visible(False)

    fig.tight_layout()
    _ = plt.show()

def search_top_k(query_image, query_text: str, topk=50):
    val_dataset_path = Path("./splited_fashionIQ") / "val"
    # query_path = val_dataset_path / "B000AYI3L4.png"
    # text = query_text

    query_features = extract_query_features(query_image, query_text)
    result = index.search(query_features, k=topk)
    
    image_names = []
    images = []
    
    for obj in result:
        image_name = obj['image']
        image_names.append(image_name) 
        images.append(Image.open(val_dataset_path / image_name))
    
    return images, image_names