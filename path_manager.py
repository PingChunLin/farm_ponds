"""
This is a script that keeps track the paths for inputs for the data pipeline.
Call the get_path(key) function in the code to get the path of a given input/output
for the code. Users can modify or add paths.  
"""

import os

# Base directory (e.g., project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths relative to the base directory
DATA_DIR = os.path.join(BASE_DIR, 'data')  # input TIF
TILES_DIR = os.path.join(DATA_DIR, 'tiles')  # Preprocessing ouput, image tiles
MASK_TILES_DIR = os.path.join(DATA_DIR, 'tiles_masks') # Preprocessing ouput, mask tiles
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
PREDICTED_TILES_DIR = os.path.join(OUTPUT_DIR, 'predicted_tiles') # where main ipynb saves prediction results
PREDICTED_ARRAYS_DIR = os.path.join(OUTPUT_DIR, 'predicted_tiles') # where prediction results are changed into np arrays
MASK_MERGED = os.path.join(OUTPUT_DIR, 'merged.png')
LOG = os.path.join(OUTPUT_DIR, 'tiles_failed_to_count.txt') # log for filtered out tiles in the mosaic
GEOREF_TIF = os.path.join(OUTPUT_DIR, 'output_georeferenced_image3_modified.tif') # georeferenced TIF
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

# Export paths through a dictionary for easy access
paths = {
    'base': BASE_DIR,
    'data': DATA_DIR,
    'tiles': TILES_DIR,
    'mask_tiles': MASK_TILES_DIR,
    'output': OUTPUT_DIR,
    'predicted_tiles': PREDICTED_TILES_DIR,
    'predicted_arrays': PREDICTED_ARRAYS_DIR,
    'georef_input': MASK_MERGED,
    'calc_input': GEOREF_TIF,
    'config': CONFIG_DIR,
}

def get_path(key):
    """Return the full path for a given key."""
    return paths.get(key, None)

if __name__ == '__main__':
    # Example usage
    for key, path in paths.items():
        print(f'{key}: {path}')
