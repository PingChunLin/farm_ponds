# Farmponds

## Goal
This is a repository for an application for that can recognize farm ponds based on farm ponds in Western India. Our goal is to provide a easy and straight forward application for environmental researchers, NPOs and local governments to easily asses the impact of climate change on agriculture and its societal impact.  We developed the computer vision pipeline based on pre-trained models and created a framework that includes data preprocessing, model training, and georeferencing for users to monitor the changes without extensive labor. The application takes a satellite image (TIFF, PNG) and labels artificial farm pond structures. The complete pipeline is currently work in progress, so here is the public repository where we show case how the application can work.


## How to run whole application
1. preprocess the data (preprocessing.py takes a TIFF and splits the images into tiles with a fixed size)
2. run the notebook with the pretrained model. User can customize the input and fine-tune the model for optimal results.
3. run the area_calculator.py to receive a list of labels and area estimates. Here we only provide the pixel version.

