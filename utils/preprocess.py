"""
Updated 04/03/2024
This program takes satellite images and divides them into smaller tiles.
These tiles can then be used as test data for the Kadwanchi models.
The output is a folder of images ready for model application.
"""

import os, random, shutil
from PIL import Image, ImageOps 



def divide_and_save_image(input_image_path, output_folder, tile_width, tile_height):
    """
    Divides the input image into smaller tiles of specified width and height.
    
    Parameters:
    - input_image_path: The path to the input image to be divided.
    - output_folder: The folder where the tiles will be saved.
    - tile_width: The width of each tile.
    - tile_height: The height of each tile.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        with Image.open(input_image_path) as img:
            image_width, image_height = img.size
            slider_width = tile_width // 4
            slider_height = tile_height // 4
            for y in range(0, image_height, slider_height):
                for x in range(0, image_width, slider_width):
                    tile = img.crop((x, y, x + tile_width, y + tile_height))
                    tile.save(os.path.join(output_folder, f"tile_{x}_{y}.png"))

    except Exception as e:
        print(f"Error dividing and saving image: {str(e)}")


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
        except OSError as e:
            print(f"Error while processing '{file_name}': {e}")


def process_training_data(train_folder, train_mask_folder, train_not_used_folder):
    """
    Process training data by comparing files in the training and mask folders,
    and moving unmatched files to a 'not used' folder.

    Args:
        train_folder (str): Path to the training data folder.
        train_mask_folder (str): Path to the training mask data folder.
        train_not_used_folder (str): Path to the folder where unmatched training data should be moved.

    Returns:
        dict: Summary of processing including files moved and any errors.
    """
    # Ensure the "train_not_used" folder exists
    if not os.path.exists(train_not_used_folder):
        os.makedirs(train_not_used_folder)

    # List files in the "train_mask" folder
    train_mask_files = os.listdir(train_mask_folder)
    moved_files = []
    retained_files = []

    # Iterate through files in the "train" folder
    for train_file in os.listdir(train_folder):
        if train_file in train_mask_files:
            retained_files.append(train_file)
        else:
            # Move the file to the "train_not_used" folder
            train_file_path = os.path.join(train_folder, train_file)
            shutil.move(train_file_path, os.path.join(train_not_used_folder, train_file))
            moved_files.append(train_file)


def create_validation_set(train_folder, train_mask_folder, val_folder, val_mask_folder, num_images_to_select):
    """
    Randomly selects a specified number of images and their corresponding masks from training folders,
    moves them to validation folders, and lists their names in a text file.

    Args:
        train_folder (str): Path to the training images folder.
        train_mask_folder (str): Path to the training mask images folder.
        val_folder (str): Path to the validation images folder.
        val_mask_folder (str): Path to the validation mask images folder.
        num_images_to_select (int): Number of images to randomly select and move.

    Returns:
        None: Moves files and writes a list of moved image names to a text file.
    """
    # Create the destination folders if they don't exist
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(val_mask_folder, exist_ok=True)

    # Get a list of all PNG image files in the train folder
    train_image_files = [file for file in os.listdir(train_folder) if file.lower().endswith('.png')]

    # Ensure there are enough images to select
    if num_images_to_select > len(train_image_files):
        raise ValueError("Number of images to select exceeds available images.")

    # Randomly select num_images_to_select images
    selected_images = random.sample(train_image_files, num_images_to_select)

    # Move selected images and their masks
    with open(os.path.join(val_folder, "val_names.txt"), "w") as val_names_file:
        for image_file in selected_images:
            image_name_without_extension = os.path.splitext(image_file)[0]

            # Move the image file
            shutil.move(os.path.join(train_folder, image_file), os.path.join(val_folder, image_file))
            
            # Write the image name to val_names.txt
            val_names_file.write(image_name_without_extension + "\n")

            # Move the corresponding mask file
            mask_file = image_name_without_extension + ".png"
            shutil.move(os.path.join(train_mask_folder, mask_file), os.path.join(val_mask_folder, mask_file))



def invert_image_colors(folder_path, file_extension=".png"):
    """
    Invert the colors of images within a specified folder that match the given file extension.

    Args:
        folder_path (str): The directory path where image files are located.
        file_extension (str): The file extension of images to be processed. Defaults to ".png".

    Returns:
        None: Images are processed and saved in place.
    """
    # Ensure file extension starts with a dot
    if not file_extension.startswith("."):
        file_extension = "." + file_extension

    # List files in the folder with the specified extension
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(file_extension)]

    # Process each image file
    for image_file in image_files:
        image_file_path = os.path.join(folder_path, image_file)

        try:
            # Open the image
            img = Image.open(image_file_path)

            # Convert the image to grayscale and then invert
            img_gray = img.convert("L")
            inverted_img = ImageOps.invert(img_gray)

            # Save the inverted image back to the file
            inverted_img.save(image_file_path)
        except Exception as e:
            print(f"Error processing '{image_file}': {e}")

    print("All specified images have been processed.")


