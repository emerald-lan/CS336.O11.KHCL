import os
import gdown
import zipfile

def download_files():
    dataset_name = "splited_fashionIQ"  # Replace with your desired dataset folder name
    finetune_name = "finetuned_RN50.pt"
    
    dataset_url = 'https://drive.google.com/file/d/1ueW5JoJA-nCWEENeElq-kg36l9GHrZyZ/view?usp=sharing'
    finetune_url = 'https://drive.google.com/file/d/1K8QuwOpoufjx9Y1_56vrk2ynd6Y3FjZW/view'
    
    folder_path = "./"
    zip_path = os.path.join(folder_path, "splited_fashionIQ_val_test.zip")
    extract_path = os.path.join(folder_path, dataset_name)
    finetune_path = os.path.join(folder_path, finetune_name)
    
    print("Loading files...")
    # Check if the folder already exists
    if not os.path.exists(finetune_path):   
        print("Downloading the fine-tuned model. Please wait...")  
        gdown.download(finetune_url, finetune_path, quiet=False, fuzzy=True)
    
    if not os.path.exists(extract_path):     
        if not os.path.exists(zip_path):
            print("Downloading the dataset. Please wait...")
            gdown.download(dataset_url, zip_path, quiet=False, fuzzy=True)
        else:
            print("Loading the splited_fashionIQ_val_test.zip")
            
        print("Extracting... Path: " + extract_path)
        # Extract the downloaded ZIP file
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(folder_path)

        # Remove the downloaded ZIP file
        os.remove(zip_path)

        print(f"Extraction completed. =")
        
    print("Everything is downloaded!")
    
def main():
    download_files()

if __name__ == "__main__":
    main()
