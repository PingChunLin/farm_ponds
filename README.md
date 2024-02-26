# farmponds

This is a repository for an application for that can recognize farm ponds based on farm ponds in Western India. Our goal is to provide a easy and straight forward application for environmental researchers, NPOs and local governments to easily asses the impact of climate change on agriculture and its societal impact.  We developed the computer vision model based on pre-trained models and created a framework that includes data preprocessing, model training, and georeferencing for users to monitor the changes without extensive labor. The application takes a satellite image and labels artificial farm pond structures. The pipeline is currently work in progress so here is the public repository we can showcase how the application works.


# how to run whole application with user data from scratch
1. preprocess the data (preprocessing.py takes a TIFF and splits the images into tiles with a fixed size)
2. run the notebook with the pretrained model
3. run the area_calculator.py to receive a list of labels and area estimates. Here we only provide the pixel version.
