"""
This program takes satellite images and divides them into smaller tiles.
These tiles can then be used as test data for the Kadwanchi models.
The output is a folder of images ready for model application.
"""

import os
from PIL import Image
import random
import shutil

def divide_and_save_image(input_image_path, output_folder, tile_width, tile_height):
    """
    Divides the input image into smaller tiles of specified width and height and saves them to the output folder.

    Parameters:
    - input_image_path (str): The path to the input image file.
    - output_folder (str): The path to the folder where the image tiles will be saved.
    - tile_width (int): The width of each tile.
    - tile_height (int): The height of each tile.
    """
    image = Image.open(input_image_path)
    img_width, img_height = image.size

    # Ensuring output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Calculating the number of tiles in each dimension
    for x in range(0, img_width, tile_width // 2):
        for y in range(0, img_height, tile_height // 2):
            # Defining box for crop operation
            box = (x, y, x+tile_width if x+tile_width < img_width else img_width, y+tile_height if y+tile_height < img_height else img_height)
            # Cropping and saving the image
            tile = image.crop(box)
            tile.save(os.path.join(output_folder, f"tile_{x}_{y}.png"))

def filter_tiles_by_size(folder_path, min_file_size):
    """
    Removes files from a folder that are below a specified file size.

    Parameters:
    - folder_path (str): The path to the folder containing the files to be filtered.
    - min_file_size (int): The minimum file size (in bytes). Files smaller than this will be removed.
    """
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            file_size = os.path.getsize(file_path)
            if file_size < min_file_size:
                os.remove(file_path)
                print(f"Removed file '{file_name}' due to its small size ({file_size} bytes).")
        except OSError as e:
            print(f"Error while processing '{file_name}': {e}")


# Configuration
input_image_path = 'path_to_your_large_image.png' 
tile_folder = 'path_to_tiles_folder'
tile_width, tile_height = 256, 256  # Example tile size
min_file_size = 6496  # Minimum file size in bytes

# Executing the image cutting
divide_and_save_image(input_image_path, tile_folder, tile_width, tile_height)
# Filtering the tiles by file size
filter_tiles_by_size(tile_folder, min_file_size)


