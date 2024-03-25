"""
This program takes satellite images and divides them into smaller tiles.
These tiles can then be used as test data for the Kadwanchi models.
The output is a folder of images ready for model application.
"""

import os
from PIL import Image 
import random
import shutil
from path_manager import get_path  

def divide_and_save_image(input_image_path, output_folder, tile_width, tile_height):
    """
    Divides the input image into smaller tiles of specified width and height.
    
    Parameters:
    - input_image_path: The path to the input image to be divided.
    - output_folder: The folder where the tiles will be saved.
    - tile_width: The width of each tile.
    - tile_height: The height of each tile.
    """
    # Open the input image
    image = Image.open(input_image_path)
    img_width, img_height = image.size

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate tiles by iterating over the image in steps of half the tile size for overlap
    for x in range(0, img_width, tile_width // 2):
        for y in range(0, img_height, tile_height // 2):
            # Define the box for the current tile
            box = (x, y, x+tile_width if x+tile_width < img_width else img_width, y+tile_height if y+tile_height < img_height else img_height)
            # Crop the image to the box dimensions and save
            tile = image.crop(box)
            tile.save(os.path.join(output_folder, f"tile_{x}_{y}.png"))

def filter_tiles_by_size(folder_path, min_file_size):
    """
    Filters out tiles smaller than a specified file size.
    
    Parameters:
    - folder_path: The path to the folder containing the tiles.
    - min_file_size: The minimum file size (in bytes) for the tiles to be kept.
    """
    # List all files in the folder
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            # Check the file size
            file_size = os.path.getsize(file_path)
            # Remove the file if it's smaller than the minimum size
            if file_size < min_file_size:
                os.remove(file_path)
                print(f"Removed file '{file_name}' due to its small size ({file_size} bytes).")
        except OSError as e:
            print(f"Error while processing '{file_name}': {e}")

# Main function
if __name__ == "__main__":
    # Configuration settings
    input_image_path =  get_path('data')  # Path to the input image
    tile_folder = get_path('tiles')  # Output folder for tiles
    tile_width, tile_height = 256, 256  # Tile dimensions
    min_file_size = 6496  # Minimum tile file size in bytes

    # Processing pipeline
    # Step 1: Divide the input image into smaller tiles
    divide_and_save_image(input_image_path, tile_folder, tile_width, tile_height)
    # Step 2: Filter the generated tiles by their file size
    filter_tiles_by_size(tile_folder, min_file_size)


