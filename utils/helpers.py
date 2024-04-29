import os, json, cv2, random, sys, re
import cloudpickle
from detectron2.config import CfgNode


def check_and_create_folder(folder_path):
    """Check if a folder exists, and if not, create the folder."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def load_from_cloudpickle(file_path):
    with open(file_path, 'rb') as f:
        data = cloudpickle.load(f)
    return data


def read_paths_from_file(file_path):
    paths = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace and newline characters, then store the line
            clean_path = line.strip()
            if clean_path:  # Ensure the line is not empty
                paths.append(clean_path)
    return paths


