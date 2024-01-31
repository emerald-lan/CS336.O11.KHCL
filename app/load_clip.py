import clip
import torch
from PIL import Image
from data_preprocessing import targetpad_transform
from typing import Tuple, List

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_clip_model(checkpoint_path: str) -> Tuple(torch.nn.Module, callable)
    model, preprocess = clip.load("RN50", device=device)

    state_dict = torch.load(checkpoint_path, map_location=device, weights_only=True)
    model.load_state_dict(state_dict["CLIP"])

    input_dim = model.visual.input_resolution # 224
    preprocess = targetpad_transform(1.25, input_dim)

    return model, preprocess