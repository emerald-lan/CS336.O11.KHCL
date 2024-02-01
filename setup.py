import streamlit as st
import os
import gdown
import rarfile
import clip
import torch
from PIL import Image

def download_files():
    dataset_name = "splited_fashionIQ"  # Replace with your desired dataset folder name
    finetune_name = "finetuned_RN50.pt"
    folder_path = "./data"
    dataset_url = 'https://drive.google.com/file/d/1B_ahBg0B7nUJE2dYROxdpXpqicMfcyu7/view?usp=sharing'
    finetune_url = 'https://drive.google.com/file/d/1K8QuwOpoufjx9Y1_56vrk2ynd6Y3FjZW/view'
    rar_path = os.path.join(folder_path, "splited_fashionIQ.rar")
    extract_path = os.path.join(folder_path, dataset_name)
    finetune_path = os.path.join(folder_path, finetune_name)

    st.write("Loading files...")
    # Check if the folder already exists
    if not os.path.exists(finetune_path):     
        gdown.download(finetune_url, finetune_path, quiet=False, fuzzy=True)
    
    if not os.path.exists(extract_path):     
        print("Downloading the dataset. Please wait...")
        gdown.download(dataset_url, rar_path, quiet=False, fuzzy=True)

        # Extract the downloaded RAR file
        with rarfile.RarFile(rar_path, 'r') as rf:
            rf.extractall(extract_path)

        # Remove the downloaded RAR file
        os.remove(rar_path)

        print(f"Extraction completed. Path = {folder_path}")
        
    st.write("Everything is downloaded!")
    
def main():
    download_files()
    if not os.path.exists("./data/features"):
        os.makedirs("./data/features")

if __name__ == "__main__":
    main()

