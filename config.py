from pathlib import Path

DATASET_URL = 'https://drive.google.com/file/d/1ueW5JoJA-nCWEENeElq-kg36l9GHrZyZ/view?usp=sharing'
MODEL_URL = 'https://drive.google.com/file/d/1K8QuwOpoufjx9Y1_56vrk2ynd6Y3FjZW/view?usp=sharing'
QUERY_URL = 'https://drive.google.com/file/d/1GPEk45RDopjWEu7I0W-W9-LADeFxP86H/view?usp=drive_link'

PROJECT_DIR = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_DIR / "data"
SRC_DIR = PROJECT_DIR / "src"
RESOURCES_DIR = PROJECT_DIR / "src/resources"
DATASET_DIR = DATA_DIR / "splited_fashionIQ"
FEATURES_DIR = DATA_DIR / "features"
UTILS_DIR = SRC_DIR / "utils"


# load_clip.py
MODEL_PATH = RESOURCES_DIR / "finetuned_RN50.pt"
MODEL_PRETRAIN = "RN50"

# dataset_process.py
FEATURES_PER_BATCH = 4