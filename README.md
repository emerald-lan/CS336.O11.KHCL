
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

This system was trained on the FashionIQ dataset, 
showing its applicability to the fashion domain for conditioned retrieval, and to more generic content considering the 
more general task of composed image retrieval.

### Built With
* [Python](https://www.python.org/)
* [PyTorch](https://pytorch.org/)
* [Torchvision](https://pytorch.org/vision/stable/index.html)
* [CLIP](https://github.com/openai/CLIP)

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
python setup.py
```

After the running of **setup.py** is done, the **splited_fashionIQ** folder (containings images for retrieval purposes) and **finetuned_RN50.pt** file will be put in ./ (or your root repo name) and should have the following structure:

```
./ (or root)       
└───  splited_fashionIQ
  └─── val
          | B000BQ0A4E.png
          | B000AS2OVA.png
          | B000AY2892.png
          | ...
  └─── test
          | 9789812442.png
          | 9789814232.png
          | 9800531750.png
          | ...   
└─── finetuned_RN50.pt
| ...
```

## Usage
Here's a brief description of each and every file

* ```setup.py```: Download and set everything up-to-date file
* ```features_extracting.py```: Feature extraction file
* ```data_preprocessing.py```: Data preprocessing file
* ```app.py```: Flask server file
* ```search.py```: Search for the top-k result file

### Run the Demo
Start the server and run the demo using the following command
```shell
python app.py
```
By default, the server run on port 8501 of localhost address: http://localhost:8501/


## Demo overview

<!-- ![](images/dataset_choice.png "Dataset choice")

* Choose the reference image 

![](images/reference_choice.png "Reference choice")

* Choose or manually insert the relative caption

![](images/relative_caption.png "Caption choice")

* Check out the results. By clicking on a
retrieved image you can use such image as reference image in a
new query

![](images/results.png "Results") -->


## Authors



