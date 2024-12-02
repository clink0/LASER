import os
import numpy as np
import open3d as o3d
from calculate_projection_area import calculate_projection_area
from point_cloud_filtering import cleanAndClusterPointCloud
def processFolder(folderPath, outputFolder, dynamic_z_offset=0.5, calculateBoundingBox=True):
    """
    Processes all PCD files in a given folder:
    - Runs the updated `cleanAndClusterPointCloud` for dynamic Z filtering and bounding box calculations.
    - Uses the 2D projection method to calculate the bounding area.

    Parameters:
    - folderPath (str): Path to the input folder containing PCD files.
    - outputFolder (str): Path to the output folder for filtered files and images.
    - dynamic_z_offset (float): Offset for the Z-axis filter (based on the furthest Z value).
    - calculateBoundingBox (bool): Whether to calculate bounding box dimensions for each file.

    Returns:
    - dict: Contains:
        - 'bounding_boxes': Array of bounding box dimensions (XYZ) for each processed file.
        - 'projection_areas': Array of 2D bounding areas for each projection.
    """
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    boundingBoxDimensions = []  # To store bounding box dimensions for all files
    projectionAreas = []  # To store 2D projection areas for all files

    for fileName in os.listdir(folderPath):
        if fileName.endswith(".pcd"):
            inputFile = os.path.join(folderPath, fileName)
            filteredOutputFile = os.path.join(outputFolder, f"filtered_{fileName}")
            projectionImageFile = os.path.join(outputFolder, f"{fileName}_projection.png")

            print(f"\nProcessing file: {inputFile}")

            # Step 1: Run the updated PCD filter for bounding box calculations
            cleanedPcd, boundingBox, dimensions = cleanAndClusterPointCloud(
                inputFile, filteredOutputFile,
                useStatisticalFilter=True,
                useRadiusFilter=True,
                dynamic_z_offset=dynamic_z_offset,
                eps=0.2,
                minPoints=1000,
                minClusterSize=500,
                finalRadiusFilter=True
            )

            if cleanedPcd is not None and dimensions is not None:
                boundingBoxDimensions.append(dimensions)
                print(f"Bounding box dimensions for {fileName}: {dimensions}")
            else:
                print(f"Skipping {fileName}: Could not generate bounding box.")
                boundingBoxDimensions.append(np.zeros(3))  # Append [0, 0, 0] for skipped files

            # Step 2: Calculate 2D projection area using the cleaned PCD
            if cleanedPcd is not None:
                area = calculate_projection_area(filteredOutputFile, image_size=500, output_image=projectionImageFile)
                projectionAreas.append(area)
                print(f"2D projection area for {fileName}: {area}")
            else:
                projectionAreas.append(0.0)  # Append 0 for skipped files

    return {
        'bounding_boxes': np.array(boundingBoxDimensions),  # Converts to consistent NumPy array
        'projection_areas': np.array(projectionAreas),  # Converts to consistent NumPy array
    }