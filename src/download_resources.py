from pathlib import Path
import gdown
import os
import shutil
import zipfile
import json
from config import *


def download_process_query(query_url: str, query_file: Path) -> None:
    gdown.download(query_url, str(query_file), quiet=False, fuzzy=True)

    with open(query_file, 'r') as file:
        data = json.load(file)

    targets = [obj['target'] for obj in data]
    filtered_gallery = [obj for obj in data if obj['candidate'] not in targets]
    
    output_json_path = DATA_DIR / "filtered_gallery.json"

    with open(output_json_path, 'w') as output_file:
        json.dump(filtered_gallery, output_file, indent=2)

    print("Query file downloaded and processed")

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

    query_file = DATA_DIR / "text_query.json"
    download_process_query(QUERY_URL, query_file)

if __name__ == "__main__":
    main()