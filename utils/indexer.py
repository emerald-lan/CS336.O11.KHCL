import faiss
from pathlib import Path
import torch
import numpy as np
from typing import List
import pandas as pd

device = "cuda" if torch.cuda.is_available() else "cpu"

class VectorIndexer:
    def __init__(self, features_file: Path, images_ids_file: Path) -> None:
        self.features = np.load(features_file)
        self.images_ids = pd.read_csv(images_ids_file)
        self.index = None
    
    def build_index(self) -> None:
        n, d = self.features.shape # n: number of images, d: dimension of each image feature
        index = faiss.IndexFlatIP(d)
        index.add(self.features)
        self.index = index
        print(f"The index contains {index.ntotal} vectors.")
    
    def save_index(self, index_path: Path) -> None:
        faiss.write_index(self.index, str(index_path))

    def load_index(self, index_path: Path) -> None:
        self.index = faiss.read_index(str(index_path))

    def search(self, query_features: np.ndarray, k: int) -> List[dict]:
        distances, indices = self.index.search(query_features, k)

        return [
            {
                "image": self.images_ids.iloc[index].values[0] + ".png",
                "similarity": 1 - distances[0][i]
            }
            for i, index in enumerate(indices[0])
        ]