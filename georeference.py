from osgeo import gdal, osr
import numpy as np

def open_source_image(input_png):
    """
    Open the input PNG image and return the source dataset.
    """
    src_ds = gdal.Open(input_png)
    if src_ds is None:
        raise FileNotFoundError(f"Unable to open input PNG file: {input_png}")
    return src_ds

def create_geotiff_copy(input_png, output_geotiff):
    """
    Create a copy of the input PNG as a GeoTIFF.
    """
    src_ds = open_source_image(input_png)
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.CreateCopy(output_geotiff, src_ds, 0)
    if dst_ds is None:
        raise Exception(f"Unable to create output GeoTIFF file: {output_geotiff}")
    return dst_ds

def calculate_geotransform_parameters(dst_ds, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    """
    Calculate and return geotransform parameters based on the dataset and corner coordinates.
    """
    num_cols = dst_ds.RasterXSize
    num_rows = dst_ds.RasterYSize
    pixel_size_x = (bottom_right_x - top_left_x) / num_cols
    pixel_size_y = (top_left_y - bottom_right_y) / num_rows
    return [top_left_x, pixel_size_x, 0, top_left_y, 0, -abs(pixel_size_y)]

def assign_geotransform_and_projection(dst_ds, geotransform):
    """
    Assign the calculated geotransform and the WGS84 projection to the dataset.
    """
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  # EPSG 4326 is the code for WGS84
    dst_ds.SetProjection(srs.ExportToWkt())

def main(input_png, output_geotiff, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    """
    Main function to georeference the input image.
    """
    dst_ds = create_geotiff_copy(input_png, output_geotiff)
    geotransform = calculate_geotransform_parameters(dst_ds, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    assign_geotransform_and_projection(dst_ds, geotransform)
    # Flush and close datasets
    dst_ds = None

if __name__ == "__main__":
    # Configuration - Replace these with your actual file paths and coordinates
    input_png = "Path to png created after merging all tiles back into the complete satellite image"
    output_geotiff = "path to output georeferenced TIF"
    top_left_x, top_left_y = 75.97936000, 19.94643500  # NW corner: Longitude, Latitude
    bottom_right_x, bottom_right_y = 76.02171400, 19.88961000  # SE corner: Longitude, Latitude

    main(input_png, output_geotiff, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    print(f"Georeferencing complete. Output saved to: {output_geotiff}")
