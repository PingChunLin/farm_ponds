# Farmponds

Farmponds is a repository for an application that can recognize farm ponds based on satellite images from in Western India. Our goal is to provide a easy and straight forward application for environmental researchers, NPOs and local governments to easily asses the impact of climate change on agriculture and its societal impact.

We developed the computer vision pipeline based on pre-trained models and created a framework that includes data preprocessing, model training, and georeferencing for users to monitor the changes without extensive labor. The application takes a satellite image (TIF, PNG) and labels artificial farm pond structures. The complete pipeline is currently work in progress, so here is the public repository where we show case how the application can work.


## How to run whole application
### What you need and what to expect (I/O): 
- Input: A satellite image (TIF) that has coordinates (Default: EPSG:4326 WGS 84)
- Output: A spreadsheet (CSV) with number, location and area estimates of the farm ponds in the area. 

### STEPS:
0. (Extra step before processing): Use path_manager.py to manage the output files for the application.
1. Preprocess the data. Preprocessing.py takes a TIF and splits the images into tiles with a fixed size (Default is 256 px * 256 px).
2. Run the Jupyter notebook (pond_kadwanchi_app.ipynb) with the pretrained model. Users can customize the input image and fine-tune the model for optimal results.
3. Run mosaicking.py to stich the prediction for tiles into the full image of the region. The PNG image is ready for georefereccing in the next step. If you don't need to georeference the predictions and only need the mask as a PNG, you can stop here.
4. Run georeferencing.py to georeference the mask. To get the best results, the current version of georeferencing.py requires manually entered Ground Control Points (GCPs). If you do not have GCPs, we recommend use GIS software such as QGIS to manually georeference the raster instead. 
Please see the georeferencing tutorial for QGIS here: [https://docs.qgis.org/3.34/en/docs/user_manual/working_with_raster/georeferencer.html](https://docs.qgis.org/3.34/en/docs/user_manual/working_with_raster/georeferencer.html)
5. Run the area_calculator.py to receive a list of labels, locations of the pond in (latitude, longitude) and area estimates. The ouput of this script creates a spreadsheet that has the number, coordinates of the center of the each farmpond, and the area estimate based on the pixel resolution of the  image. The script also creates a png that has the labeled ponds on the maske created from Step #2 (optional). 

