import math
import numpy as np
import pandas as pd
from pathlib import Path
from utils.load_clip import load_clip_model
import torch
from PIL import Image
from typing import List
import shutil
from utils.indexer import VectorIndexer
from config import *

import warnings
warnings.filterwarnings('ignore')


device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = load_clip_model(MODEL_PATH)

def load_dataset(dataset_path: Path) -> List[str]:
    if not dataset_path.exists():
        print(f"Path {dataset_path} does not exist.")
        return
    images_files = list(dataset_path.glob("*.png"))
    print(f"Images found: {len(images_files)}")
    return images_files

def extract_images_features(batch: List[str]) -> np.ndarray:
    images = [Image.open(image_file) for image_file in batch]
    
    images_preprocessed = torch.stack([preprocess(image) for image in images]).to(device)

    with torch.no_grad():
        images_features = clip_model.encode_image(images_preprocessed)
        images_features /= images_features.norm(dim=-1, keepdim=True)

    return images_features.cpu().numpy()

def process_batch(i: int, batch_files: List[str], batch_features_path: Path) -> None:
    batch_ids_file = batch_features_path / f"{i:010d}.csv"
    batch_features_file = batch_features_path / f"{i:010d}.npy"

    batch_features = extract_images_features(batch_files)
    np.save(batch_features_file, batch_features)

    batch_ids = [file.name.split(".")[0] for file in batch_files]
    batch_ids_data = pd.DataFrame(batch_ids, columns=['image_id'])
    batch_ids_data.to_csv(batch_ids_file, index=False)

def remove_batch_features(batch_features_path: Path) -> None:
    if batch_features_path.exists() and batch_features_path.is_dir():
        shutil.rmtree(batch_features_path)
    print('Unused batch features folder removed')


def main():
    val_dataset_path = DATASET_DIR / "val"
    val_images_files = load_dataset(val_dataset_path)

    features_file = FEATURES_DIR / "features.npy"
    images_ids_file = FEATURES_DIR / "images_ids.csv"

    if features_file.exists() and images_ids_file.exists():
        index = VectorIndexer(features_file, images_ids_file)
        index.build_index()
        index.save_index(FEATURES_DIR / "dataset.index")
        print(f"Index saved in {FEATURES_DIR / 'dataset.index'}")
        return

    batch_size = FEATURES_PER_BATCH
    batch_features_path = DATA_DIR / "batch_features"
    if batch_features_path.exists() and batch_features_path.is_dir():
        shutil.rmtree(batch_features_path)
    batch_features_path.mkdir(parents=True, exist_ok=True)

    batches = math.ceil(len(val_images_files) / batch_size)

    for i in range(batches):
        print(f"Processing batch {i+1}/{batches}")

        try:
            batch_files = val_images_files[i*batch_size : (i+1)*batch_size]
            process_batch(i, batch_files, batch_features_path)
        except:
            print(f'Problem with batch {i}')

    features_list = [np.load(file) for file in sorted(batch_features_path.glob("*.npy"))]
    features = np.concatenate(features_list).astype(np.float32) # (n_images, 1024)
    np.save(features_file, features)
    print(f"Features saved in {features_file}")

    images_ids = pd.concat([pd.read_csv(ids_file) for ids_file in sorted(batch_features_path.glob("*.csv"))])
    images_ids.to_csv(images_ids_file, index=False)
    print(f"Images ids saved in {images_ids_file}")

    index = VectorIndexer(features_file, images_ids_file)
    index.build_index()
    index.save_index(FEATURES_DIR / "dataset.index")
    print(f"Index saved in {FEATURES_DIR / 'dataset.index'}")

    remove_batch_features(batch_features_path)


if __name__ == '__main__':
    main()