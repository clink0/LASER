import os
import numpy as np
import open3d as o3d
from calculate_projection_area import calculate_projection_area
from point_cloud_filtering import cleanAndClusterPointCloud

def remove_outliers_y(data):
    """
    Removes outliers from the Y-dimension data based on the median.
    - Retains only values greater than or equal to the median.
    - Calculates the average of the filtered data.

    Parameters:
    - data (array-like): Y-dimension data (e.g., bounding box Y-dimensions).

    Returns:
    - filtered_data (np.ndarray): Filtered Y-dimension data.
    - filtered_average (float): Average of the filtered data.
    """
    median_value = np.median(data)
    filtered_data = data[data >= median_value]
    filtered_average = np.mean(filtered_data) if len(filtered_data) > 0 else 0.0
    print(f"\nMedian Y value: {median_value}")
    print(f"Filtered Y values: {filtered_data}")
    print(f"Average of filtered Y values: {filtered_average}")
    return filtered_data, filtered_average

def processFolder(folderPath, outputFolder, dynamic_z_offset=0.5, calculateBoundingBox=True):
    """
    Processes all PCD files in a given folder:
    - Runs the updated cleanAndClusterPointCloud for dynamic Z filtering and bounding box calculations.
    - Uses the 2D projection method to calculate the bounding area.
    - Calculates the nearest average Z value for each frame and across all frames.
    - Calculates the average X, Y, and Z dimensions of all bounding boxes.
    - Scales the average dimensions using a scaling factor derived from the overall average Z value.
    - Removes outliers from Y-dimensions before calculating their average.

    Parameters:
    - folderPath (str): Path to the input folder containing PCD files.
    - outputFolder (str): Path to the output folder for filtered files and images.
    - dynamic_z_offset (float): Offset for the Z-axis filter (based on the furthest Z value).
    - calculateBoundingBox (bool): Whether to calculate bounding box dimensions for each file.

    Returns:
    - dict: Contains:
        - 'bounding_boxes': Array of bounding box dimensions (XYZ) for each processed file.
        - 'projection_areas': Array of 2D bounding areas for each projection.
        - 'average_z_values': Array of average Z values for filtered points for each file.
        - 'overall_average_z': The overall average Z value across all frames.
        - 'scaled_dimensions_cm': The scaled dimensions (X, Y, Z) in centimeters.
        - 'filtered_y_average': Average of Y-dimensions after outlier removal.
    """
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    boundingBoxDimensions = []  # To store bounding box dimensions for all files
    projectionAreas = []  # To store 2D projection areas for all files
    averageZValues = []  # To store average Z values for all files

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

            # Step 3: Calculate the nearest average Z value
            if cleanedPcd is not None:
                points = np.asarray(cleanedPcd.points)
                average_z = np.mean(points[:, 2])  # Calculate the average of the Z values
                averageZValues.append(average_z)
                print(f"Nearest average Z value for {fileName}: {average_z}")
            else:
                averageZValues.append(0.0)  # Append 0 for skipped files

    # Calculate the overall average Z value across all frames
    overall_average_z = np.mean(averageZValues) if averageZValues else 0.0
    print(f"\nOverall average Z value across all frames: {overall_average_z}")

    # Calculate the average bounding box dimensions
    if boundingBoxDimensions:
        boundingBoxDimensions = np.array(boundingBoxDimensions)  # Convert to NumPy array
        average_bounding_box_dimensions = np.mean(boundingBoxDimensions, axis=0)
    else:
        boundingBoxDimensions = np.zeros((0, 3))  # Empty array if no data
        average_bounding_box_dimensions = np.zeros(3)

    print(f"\nAverage bounding box dimensions (X, Y, Z): {average_bounding_box_dimensions}")

    # Perform outlier removal and filtered Y-dimension average
    y_dimensions = boundingBoxDimensions[:, 1]  # Extract Y-dimensions
    _, filtered_y_average = remove_outliers_y(y_dimensions)

    # Replace the Y-dimension in the average bounding box dimensions with the filtered Y average
    if boundingBoxDimensions.size > 0:
        average_bounding_box_dimensions[1] = filtered_y_average

    # Scaling factor calculation
    # Derived from the formula: S = -0.0287 * Z + 0.8376
    scaling_factor = -0.0287 * overall_average_z + 0.8376
    print(f"\nCalculated scaling factor: {scaling_factor}")

    # Apply the scaling factor to average bounding box dimensions to get scaled dimensions in cm
    scaled_dimensions_cm = average_bounding_box_dimensions * scaling_factor * 100
    print(f"\nScaled dimensions (X, Y, Z) in cm: {scaled_dimensions_cm}")

    return {
        'bounding_boxes': np.array(boundingBoxDimensions),  # Converts to consistent NumPy array
        'projection_areas': np.array(projectionAreas),  # Converts to consistent NumPy array
        'average_z_values': np.array(averageZValues),  # Converts to consistent NumPy array
        'overall_average_z': overall_average_z,  # Overall average Z value across all frames
        'scaled_dimensions_cm': scaled_dimensions_cm.tolist(),  # Scaled dimensions in cm
        'filtered_y_average': filtered_y_average,  # Average of Y-dimensions after outlier removal
    }