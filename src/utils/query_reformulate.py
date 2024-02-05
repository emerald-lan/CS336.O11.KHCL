import numpy as np
from typing import List
from PIL import Image
import torch
from .load_clip import load_clip_model
from .config import *
from PIL import Image

alpha = 1
beta = 1
gamma = 1

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = load_clip_model(MODEL_PATH)


def reformulate_query(query_features: np.ndarray, relevant_features: List[np.ndarray], irrelevant_features: List[np.ndarray]) -> np.ndarray:
    if relevant_features:
        sum_relevant = np.sum(relevant_features, axis=0)
        sum_relevant = sum_relevant / np.linalg.norm(sum_relevant)
    else:
        sum_relevant = np.zeros_like(query_features)

    if irrelevant_features:
        sum_irrelevant = np.sum(irrelevant_features, axis=0)
        sum_irrelevant = sum_irrelevant / np.linalg.norm(sum_irrelevant)
    else:
        sum_irrelevant = np.zeros_like(query_features)

    reformulated_query = alpha * query_features + beta * sum_relevant - gamma * sum_irrelevant

    return reformulated_query

def extract_result_features(image: Image) -> np.ndarray:   
    image_preprocessed = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image_preprocessed)

    return image_features.cpu().numpy()