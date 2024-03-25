import cv2
import os
import math
import pandas as pd
from osgeo import gdal, osr

# Define global variables
INPUT_IMAGE_PATH = 'Path to georenferenced TIF'
OUTPUT_FOLDER = 'Path to output folder'

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_and_threshold_image(image_path):
    """Load an image and apply thresholding to segment white objects."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresholded = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
    return image, thresholded

def find_contours(thresholded_image):
    """Find contours of white objects in the thresholded image."""
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def setup_coordinate_transformation(image_path):
    """Setup coordinate transformation using a GeoTIFF file."""
    try:
        dataset = gdal.Open(image_path)
        if dataset is None:
            raise Exception(f"Failed to open the GeoTIFF file at {image_path}.")
        
        geotransform = dataset.GetGeoTransform()
        source_crs = osr.SpatialReference()
        target_crs = osr.SpatialReference()

        # Set up source CRS from dataset
        wkt = dataset.GetProjection()
        source_crs.ImportFromWkt(wkt)

        # Set up target CRS to WGS 84
        target_crs.ImportFromEPSG(4326)  # EPSG code for WGS 84

        # Initialize coordinate transformation
        # Correctly create the transformation by ensuring both spatial references are valid
        transform = osr.CoordinateTransformation(source_crs, target_crs)
        return geotransform, transform
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None


def calculate_objects_data(contours, geotransform, transform):
    """Calculate area, center, and real-world coordinates for each object."""
    data = {"Contour": [], "Area": [], "Real_area": [], "Center_X": [], "Center_Y": [], "Center_lat": [], "Center_long": []}
    for contour in contours:
        M = cv2.moments(contour)
        center_x = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
        center_y = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
        pixel_area = cv2.contourArea(contour)
        real_area = pixel_area * geotransform[1] * abs(geotransform[5])
        center_lat, center_long = transform_point(center_x, center_y, geotransform, transform)
        
        data["Contour"].append(contour)
        data["Area"].append(pixel_area)
        data["Real_area"].append(real_area)
        data["Center_X"].append(center_x)
        data["Center_Y"].append(center_y)
        data["Center_lat"].append(center_lat)
        data["Center_long"].append(center_long)
    return data

def transform_point(x, y, geotransform, transform):
    """Transform a point from pixel coordinates to real-world coordinates."""
    lat = geotransform[0] + x * geotransform[1] + y * geotransform[2]
    long = geotransform[3] + x * geotransform[4] + y * geotransform[5]
    if transform is not None:
        long, lat, _ = transform.TransformPoint(lat, long)
    return lat, long

def save_data_and_image(data, image):
    """Save the DataFrame as a CSV file and optionally save an image with labeled instances."""
    df = pd.DataFrame(data)
    df["Label"] = range(1, len(df) + 1)
    output_csv_path = os.path.join(OUTPUT_FOLDER, 'farmponds_data.csv')
    df.to_csv(output_csv_path, index=False)
    print(f'Object data saved in "{output_csv_path}".')

    # Save the image with labeled instances
    for i, contour in enumerate(data["Contour"]):
        label = i + 1
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, str(label), (data["Center_X"][i], data["Center_Y"][i]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    output_image_path = os.path.join(OUTPUT_FOLDER, 'labeled_farmponds.png')
    cv2.imwrite(output_image_path, image)
    print(f'Labeled image saved in "{output_image_path}".')

def main():
    """Main function to execute the program."""
    image, thresholded = load_and_threshold_image(INPUT_IMAGE_PATH)
    contours = find_contours(thresholded)
    geotransform, transform = setup_coordinate_transformation(INPUT_IMAGE_PATH)
    if geotransform and transform:
        data = calculate_objects_data(contours, geotransform, transform)
        save_data_and_image(data, image)
    else:
        print("Failed to perform coordinate transformation. Exiting.")

if __name__ == '__main__':
    main()
