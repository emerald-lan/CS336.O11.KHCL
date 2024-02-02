from pathlib import Path
import gdown
import os
import shutil
import zipfile
from config import *


def download_clip(model_url: str, model_file: Path) -> None:
    if not RESOURCES_DIR.exists():
        os.makedirs(RESOURCES_DIR)

    gdown.download(model_url, str(model_file), quiet=False, fuzzy=True)
    print("Model downloaded")

def download_extract_dataset(dataset_url: str, dataset_file: Path) -> None:
    if DATASET_DIR.exists():
        shutil.rmtree(DATASET_DIR)

    if not DATA_DIR.exists():
        os.makedirs(DATA_DIR)

    gdown.download(dataset_url, str(dataset_file), quiet=False, fuzzy=True)

    with zipfile.ZipFile(dataset_file,"r") as zip_ref:
        zip_ref.extractall(DATA_DIR)

    os.remove(dataset_file)
    print("Dataset downloaded and extracted")

def main():
    model_file = RESOURCES_DIR / "finetuned_RN50.pt"
    download_clip(MODEL_URL, model_file)

    dataset_file = DATA_DIR / "dataset.zip"
    download_extract_dataset(DATASET_URL, dataset_file)

if __name__ == "__main__":
    main()