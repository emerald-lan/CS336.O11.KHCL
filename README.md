
# Mineral Fashion Image Retrieval System
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
  * [Run the Demo](#run-the-demo)
* [Demo Overview](#demo-overview)
* [Authors](#authors)

## About The Project
This is the repository for the Multimedia Information Retrieval Course Final Project **Mineral Fashion Image Retrieval System**. This project was carried out by a group of students from the Falcuty of Computer Science at University of Information Technology. 

This system was trained on the FashionIQ dataset, showing its applicability to the fashion domain for conditioned retrieval, and to more generic content considering the more general task of composed image retrieval.

### Built With
* [Python](https://www.python.org/)
* [PyTorch](https://pytorch.org/)
* [Torchvision](https://pytorch.org/vision/stable/index.html)
* [CLIP](https://github.com/openai/CLIP)
* [streamlit](https://streamlit.io/)
* [streamlit-image-select](https://github.com/jrieke/streamlit-image-select)

## Getting Started

To install and use this system demo please follow these simple steps.

### Installation
 
1. Clone the repo
```sh
git clone https://github.com/emerald-lan/CS336.O11.KHCL.git
```
2. Install dependencies
```sh
pip install -r requirements.txt
```
3. Data Preparation

The dataset and necessary files will be downloaded and prepare automatically by using the following command:

```sh
python src/download_resources.py
```
After the running of **src/download_resources.py** is done, the **splited_fashionIQ** folder (containings images for retrieval purposes), **finetuned_RN50.pt** and **filtered_gallery.json** file will be downloaded and extracted. Everything should be up-to-date now.

## Usage
Here's a brief description of every important file/folder:

* ```data```: Folder contains images, indices and captions.
* ```src```: Folder contains important resources.
  * ```src/utils```: Folder contains searching and feature extracting modules.
  * ```src/resources```: Folder contains fine-tuned file.
  * ```src/download_resources.py```: Download necessary resourses.
  * ```src/dataset_process.py```: Process dataset for purposes.
  * ```src/dataset_process.py```: Process dataset for purposes.
* ```test```: Folder contains python notebooks for testing purposes.
  * ```test/test_reformulate```: Reformulating the retrieval results using users' feedbacks (underdeveloped).
* ```app.py```: Running the application.
* ```requirements.txt```: Contains dependencies

### Run the Demo
Start the server and run the demo using the following command
```shell
python app.py
```
By default, the server run on port 8501 of localhost address: http://localhost:8501/

## Authors
* [**Nguyen Tran Hoai Bao**](https://github.com/platinumhb)
* [**Nguyen Thi Thanh Lan**](https://github.com/emerald-lan)
* [**Nguyen Do Quynh Nhu**](https://github.com/qnhu2910)


