
# ponds
## This version is not updated to the full package yet.

Farmponds is a repository for an application that can recognize farm ponds based on satellite images from in Western India. Our goal is to provide a easy and straight forward application for environmental researchers, NPOs and local governments to easily asses the impact of climate change on agriculture and its societal impact.

We developed the computer vision pipeline based on pre-trained models and created a framework that includes data preprocessing, model training, and georeferencing for users to monitor the changes without extensive labor. The application takes a satellite image (TIF, PNG) and labels artificial farm pond structures. 



### What you need and what to expect (I/O): 
- Input: A satellite image and labeled ponds from part of the satellite image for traning. For the satellite image, we recommend a TIF image that has coordinates (Default: EPSG:4326 WGS 84). TIFs with Ground Control Points (GCPs) are recommended. 
The labeled ponds (masks) should be a single png image of the entire region of interest. For the mask of Kadwanchi, we labeled about 100 pond instances in the regions to train. 
- Output: A spreadsheet (CSV) with number, location and area estimates of the farm ponds in the area; also a image (png) of the ponds labeled in the area. 

### How the workflow looks like:
1. We identify and label the target object manually on the satellite images. (See the /data folder for more imformation)
2. We preprocess the data by cutting images into tiles, and split the tiles into two datasets: Train and Validation (See /train and /val folders for more information).
3. Once we have preprocessed the data, we train the model into 


## 
### STEPS:
0. Go to the traning folder to label the data so it is ready to be processed into a training data for the pipeline.
1. Run setup.py to install the required libraries for the ponds package. 
2. Run the Jupyter notebook (pond_demo.ipynb) with the pretrained model. Users can customize the input image and fine-tune the model in the noetbook for optimal results.

### Geolocating the ponds 
Georefercing the a part of the pipeline to make sure that the labeled farm ponds are geolocated accurately. To get the best results, the current version of georeferencing.py in the package requires manually entered Ground Control Points (GCPs). If you do not have GCPs, we recommend using GIS software such as QGIS to manually georeference the raster instead. 
Please see the georeferencing tutorial for QGIS here: [https://docs.qgis.org/3.34/en/docs/user_manual/working_with_raster/georeferencer.html](https://docs.qgis.org/3.34/en/docs/user_manual/working_with_raster/georeferencer.html)

### Repository Structure

ponds/
│
├── .gitignore                
├── LICENSE                   
├── README.md
├── setup.py
├── requirements.txt 
├── ponds_demo.ipynb   
│
├── ponds/
│   ├── README.md                      
│   ├── __init__.py   
│   ├── area_calculator.py
│   ├── georeference.py
│   ├── mosaic.py
│   ├── preprocess.py
│   └── src/                
│       ├── __init__.py
│       ├── create_annotations.py     
│
├── data/                      
│   ├── train.tif          
│   ├── mask.png            
│   └── train/                
│       ├── 
│       ├── 
│       └── 
├── output/                      
│   ├── prediction.tif          
│   ├── mask.png            
│   └── log.txt 
