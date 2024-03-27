import os
import shutil
from PIL import Image
import numpy as np
from skimage import io, color, morphology, segmentation
from path_manager import get_path

def process_image(input_path, threshold=0.5, min_object_size=2400):
    """
    Processes an image by clearing the border, removing small objects, and converting it to a binary image.
    
    Parameters:
    - input_path: Path to the input image.
    - threshold: Threshold value for binarization.
    - min_object_size: Minimum size of objects to retain in the image.
    
    Returns:
    - cleared_image: The processed binary image as a NumPy array.
    """
    # Load the image
    image_original = io.imread(input_path)
    
    # Convert the image to grayscale if it's in color
    if image_original.ndim == 3:
        image = color.rgb2gray(image_original)
    else:
        image = image_original.copy()

    # Convert the image to binary
    binary_image = image > threshold

    # Remove objects touching the border
    cleared_image = segmentation.clear_border(binary_image)

    # Remove small objects
    cleared_image = morphology.remove_small_objects(cleared_image, min_size=min_object_size)
    
    return cleared_image

def save_processed_image(image, output_path):
    """
    Saves the processed image to the specified path.

    Parameters:
    - image: The processed image to save.
    - output_path: The path to save the processed image to.
    """
    # Convert boolean array to uint8 and save as .npy file
    np.save(output_path, image.astype(np.uint8))

def process_directory(input_folder_path, output_folder_path):
    """
    Processes all images in a directory and saves the processed images to another directory.

    Parameters:
    - input_folder_path: Path to the folder containing input images.
    - output_folder_path: Path to the folder where processed images will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # List all PNG images in the input directory
    image_files = [f for f in os.listdir(input_folder_path) if f.lower().endswith('.png')]

    # Process each image
    for image_file in image_files:
        input_image_path = os.path.join(input_folder_path, image_file)
        output_array = os.path.splitext(image_file)[0] + '.npy'
        output_array_path = os.path.join(output_folder_path, output_array)
        
        # Process the image
        cleared_image = process_image(input_image_path)
        
        # Save the processed image
        save_processed_image(cleared_image, output_array_path)

# array merge tiles
    
def load_and_sort_filenames(directory):
    """
    Loads and sorts image filenames from a directory based on custom sorting criteria.
    
    Parameters:
    - directory: The path to the directory containing the files.
    
    Returns:
    - A list of sorted filenames.
    """
    def custom_sort(filename):
        x, y = map(int, os.path.splitext(filename)[0].split("_")[1:])
        return x, y
    
    return sorted(os.listdir(directory), key=custom_sort)

def merge_tiles(filenames, input_dir, canvas_size):
    """
    Merges tiles into a single large array based on their filenames.
    
    Parameters:
    - filenames: A list of sorted filenames.
    - input_dir: Directory containing the npy files.
    - canvas_size: Tuple of (width, height) for the canvas size.
    
    Returns:
    - The merged array and a list of filenames that failed to merge.
    """
    canvas_width, canvas_height = canvas_size
    merged_array = np.zeros((canvas_height, canvas_width), dtype=np.uint8)
    failed_list = []

    for filename in filenames:
        if filename.endswith(".npy"):
            tile = np.load(os.path.join(input_dir, filename))
            y, x = map(int, os.path.splitext(filename)[0].split("_")[1:])
            window_height, window_width = tile.shape
            window = merged_array[x:x+window_width, y:y+window_height]
            tile_vector = tile.reshape((-1, 1))
            window_vector = window.reshape((-1, 1))

            if tile_vector.shape == window_vector.shape:
                mask = (window_vector == 0) & (tile_vector != 0)
                window_vector[mask] = tile_vector[mask]
                transformed_array = window_vector.reshape((window_height, window_width))
                merged_array[x:x+window_width, y:y+window_height] = transformed_array
            else: 
                failed_list.append(filename)
    
    return merged_array, failed_list

def save_merged_image(array, output_path):
    """
    Saves a NumPy array as a PNG image.
    
    Parameters:
    - array: The NumPy array to save.
    - output_path: The output file path for the image.
    """
    uint8_array = (array * 255).astype(np.uint8)
    rgba_array = np.zeros((*array.shape, 4), dtype=np.uint8)
    rgba_array[:, :, :3] = uint8_array[:, :, None]
    rgba_array[:, :, 3] = (array == 1) * 255
    image = Image.fromarray(rgba_array, 'RGBA')
    image.save(output_path)

def save_failed_list(failed_list, output_path):
    """
    Saves the list of filenames that failed to merge to a text file.
    
    Parameters:
    - failed_list: A list of filenames that failed to merge.
    - output_path: The output file path for the text file.
    """
    with open(output_path, 'w') as file:
        for failedfile in failed_list:
            file.write(failedfile + '\n')


# Example usage
if __name__ == "__main__":
    input_folder = get_path('predicted_tiles')
    output_folder = get_path('predicted_arrays')
    process_directory(input_folder, output_folder)

    input_dir = get_path('predicted_arrays')
    output_dir = get_path('output')
    os.makedirs(output_dir, exist_ok=True)

    sorted_filenames = load_and_sort_filenames(input_dir)
    merged_array, failed_list = merge_tiles(sorted_filenames, input_dir, (14849, 20937))
    output_file_path = get_path('merged.png')
    save_merged_image(merged_array, output_file_path)
    output_txt_path = get_path('log')
    save_failed_list(failed_list, output_txt_path)

    print(f"Images merged successfully. Saved as {output_file_path}.")
    print("Filenames of tiles failed to count saved to:", output_txt_path)
