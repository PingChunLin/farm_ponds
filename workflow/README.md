# Installing the Environment

## 1. Set up Anaconda
This workflow uses Anaconda to set up the environment for the program. If you already have Anaconda install on you machine, please skip this step, otherwise, please see the [official installation guide](https://docs.anaconda.com/free/anaconda/install/). The environment setup is currently limted to linux and Windows Subsystem for Linux (WSL).

If you use WSL, here is a great [step by step guide](https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da). 

## 2. Set up the virtual environment
Navigate to the root folder (ponds/) and type the line below to create the environment **ponds_env**
```bash
conda env create -f environment.yml
```
Then run this line to activate the environment: 
```bash
conda activate ponds_env
```
The series of Jupyter notebooks in this workflow are modified from [Meta Research's tutorial notebook](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5) We stil need the package in **detectron2** to run the workflow. We will install detectron2 seperately in the notebooks. If you need to turn off the ponds_env environment, you can type:
```bash
conda deactivate
```

