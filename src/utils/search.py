import numpy as np
import torch
import torch.nn.functional as F
import clip
from PIL import Image
import matplotlib.pyplot as plt
from .load_clip import load_clip_model
from .indexer import VectorIndexer
from config import *


device = "cuda" if torch.cuda.is_available() else "cpu"

clip_model, preprocess = load_clip_model(MODEL_PATH)
features_file =  FEATURES_DIR / "features.npy"
images_ids_file = FEATURES_DIR / "images_ids.csv"
index_file = FEATURES_DIR / "dataset.index"

index = VectorIndexer(features_file, images_ids_file)
index.load_index(index_file)

def extract_query_features(image: Image, text: str) -> np.ndarray:
    image_preprocessed = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        text_features = clip_model.encode_text(clip.tokenize(text).to(device))
        # text_features /= text_features.norm(dim=-1, keepdim=True)

        image_features = clip_model.encode_image(image_preprocessed)
        # image_features /= image_features.norm(dim=-1, keepdim=True)

    combined_features = F.normalize(image_features + text_features, dim=-1)

    return combined_features.cpu().numpy()


def search_top_k(query_image, query_text: str, topk=50):
    val_dataset_path = DATASET_DIR / "val"
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

def rerank(query_features: np.ndarray, topk=50):
    val_dataset_path = DATASET_DIR / "val"

    result = index.search(query_features, k=topk)
    
    image_names = []
    images = []
    
    for obj in result:
        image_name = obj['image']
        image_names.append(image_name) 
        images.append(Image.open(val_dataset_path / image_name))
    
    return images, image_names