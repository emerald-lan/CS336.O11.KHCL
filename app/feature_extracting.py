import torch
from PIL import Image
from load_clip import load_clip_model
from typing import List
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = load_clip_model("../finetuned_RN50.pt")

def extract_images_features(batch: List[str]) -> np.ndarray:
    images = [Image.open(image_file) for image_file in batch]
    
    images_preprocessed = torch.stack([preprocess(image) for image in images]).to(device)

    with torch.no_grad():
        images_features = clip_model.encode_image(images_preprocessed)
        images_features /= images_features.norm(dim=-1, keepdim=True)

    return images_features.cpu().numpy()