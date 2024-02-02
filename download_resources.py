from pathlib import Path
import gdown
import os
import shutil
import zipfile


# Get the root directory of the project
root_dir = Path(__file__).parent.absolute()

def download_clip(model_url: str, model_file: Path) -> None:
    if not model_file.parent.exists():
        os.makedirs(model_file.parent)

    gdown.download(model_url, str(model_file), quiet=False, fuzzy=True)
    print("Model downloaded")

def download_extract_dataset(dataset_url: str, dataset_file: Path) -> None:
    if Path(dataset_file.parent / "splited_fashionIQ").exists():
        shutil.rmtree(dataset_file.parent / "splited_fashionIQ")

    if not dataset_file.parent.exists():
        os.makedirs(dataset_file.parent)

    gdown.download(dataset_url, str(dataset_file), quiet=False, fuzzy=True)

    with zipfile.ZipFile(dataset_file,"r") as zip_ref:
        zip_ref.extractall(dataset_file.parent)

    os.remove(dataset_file)
    print("Dataset downloaded and extracted")

def main():
    model_url = 'https://drive.google.com/file/d/1K8QuwOpoufjx9Y1_56vrk2ynd6Y3FjZW/view?usp=sharing'
    model_file = root_dir / Path('src/resources/finetuned_RN50.pt')
    download_clip(model_url, model_file)

    dataset_url = 'https://drive.google.com/file/d/1ueW5JoJA-nCWEENeElq-kg36l9GHrZyZ/view?usp=sharing'
    dataset_file = root_dir / Path('data/dataset.zip')
    download_extract_dataset(dataset_url, dataset_file)

if __name__ == "__main__":
    main()