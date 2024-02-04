from pathlib import Path

DATASET_URL = 'https://drive.google.com/file/d/1D9aydHJeKCv4ZU8qH67ZZ2b7uoMc7uie/view?usp=sharing'
MODEL_URL = 'https://drive.google.com/file/d/1K8QuwOpoufjx9Y1_56vrk2ynd6Y3FjZW/view?usp=sharing'
QUERY_URL = 'https://drive.google.com/file/d/1wt8I5zeHysjQNuLYJLBGHn39g_F9LE5S/view?usp=sharing'

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