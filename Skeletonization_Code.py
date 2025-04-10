# Part 1: Terraces 

# Import Libraries
import rasterio
import numpy as np
from skimage.morphology import skeletonize
import csv

# It is important to already have a digital terrain model and a binary mask (with terraces detected) for the code to work 
# Path (replace these with your actual DTM and Binary Mask) 
terrace_mask_path = 'Binary_Terrace_Mask.tif'
dtm_path = 'DTM.tif'
skeleton_points_path = 'skeleton_points_terrace.csv'

# Open binary raster
with rasterio.open(terrace_mask_path) as mask_raster:
    # Reading the terrace mask data
    mask_data = mask_raster.read(1)
    
    # Skeletonizing the terraced areas 
    skeleton = skeletonize(mask_data == 1)
    
    # Saving the skeleton mask to a new raster file
    skeleton_profile = mask_raster.profile
    skeleton_profile.update(dtype=rasterio.uint8, nodata=None)  # Set nodata to None
    
    with rasterio.open('SKELETON_RASTER.tif', 'w', **skeleton_profile) as skeleton_raster:
        skeleton_raster.write(skeleton.astype(np.uint8), 1)

# Extracting points from the created skeleton raster mask
with rasterio.open('SKELETON_RASTER.tif') as skeleton_raster, rasterio.open(dtm_path) as dtm_raster:
    # Read the skeleton and DTM data
    skeleton_data = skeleton_raster.read(1)
    dtm_data = dtm_raster.read(1)
    
    # Getting the coordinates and elevation of the skeleton points
    skeleton_points = np.column_stack(np.where(skeleton_data == 1))
    elevations = dtm_data[skeleton_points[:, 0], skeleton_points[:, 1]]
    coords = [skeleton_raster.transform * (pt[1], pt[0]) for pt in skeleton_points]
    
    # Saving to a CSV file
    with open(skeleton_points_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Longitude', 'Latitude', 'Elevation'])
        for (lon, lat), elevation in zip(coords, elevations):
            writer.writerow([lon, lat, elevation])

print(f"Skeleton points with elevation have been saved to {skeleton_points_path}.")

# Part 2 Terrace Walls

# Import Libraries
import rasterio
import numpy as np
from skimage.morphology import skeletonize
import csv

# It is important to already have a digital terrain model and a binary mask (with terraces walls detected) for the code to work 
# Path (replace these with your actual DTM and Binary Mask) 
terrace_mask_path = 'Binary_Terrace_Walls_Mask.tif'
dtm_path = 'DTM.tif'
skeleton_points_path = 'skeleton_points_walls.csv'

# Open binary raster
with rasterio.open(terrace_mask_path) as mask_raster:
    # Reading the terrace mask data
    mask_data = mask_raster.read(1)
    
    # Skeletonizing the terraced areas 
    skeleton = skeletonize(mask_data == 1)
    
    # Saving the skeleton mask to a new raster file
    skeleton_profile = mask_raster.profile
    skeleton_profile.update(dtype=rasterio.uint8, nodata=None)  # Set nodata to None
    
    with rasterio.open('SKELETON_RASTER.tif', 'w', **skeleton_profile) as skeleton_raster:
        skeleton_raster.write(skeleton.astype(np.uint8), 1)

# Extracting points from the created skeleton raster mask
with rasterio.open('SKELETON_RASTER.tif') as skeleton_raster, rasterio.open(dtm_path) as dtm_raster:
    # Read the skeleton and DTM data
    skeleton_data = skeleton_raster.read(1)
    dtm_data = dtm_raster.read(1)
    
    # Getting the coordinates and elevation of the skeleton points
    skeleton_points = np.column_stack(np.where(skeleton_data == 1))
    elevations = dtm_data[skeleton_points[:, 0], skeleton_points[:, 1]]
    coords = [skeleton_raster.transform * (pt[1], pt[0]) for pt in skeleton_points]
    
    # Saving to a CSV file
    with open(skeleton_points_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Longitude', 'Latitude', 'Elevation'])
        for (lon, lat), elevation in zip(coords, elevations):
            writer.writerow([lon, lat, elevation])

print(f"Skeleton points with elevation have been saved to {skeleton_points_path}.")

# Use QGIS or any GIS software to merge both sets of points into a merged vector to be used in the interpolation procedure and create the smoothed digital terrain model
