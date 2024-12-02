import os
import numpy as np
import open3d as o3d
from calculate_projection_area import calculate_projection_area
from point_cloud_filtering import cleanAndClusterPointCloud
from rotation_calculations import get_plane_normal, calculate_rpm  # Import rotation functions


def remove_outliers_y(data):
    """
    Removes outliers from the Y-dimension data and calculates the average of the filtered data.
    """
    median_value = np.median(data)
    filtered_data = data[data >= median_value]
    filtered_average = np.mean(filtered_data) if len(filtered_data) > 0 else 0.0
    print(f"\nMedian Y value: {median_value}")
    print(f"Filtered Y values: {filtered_data}")
    print(f"Average of filtered Y values: {filtered_average}")
    return filtered_data, filtered_average


def processFolder(folderPath, outputFolder, timestamps, dynamic_z_offset=0.5, calculateBoundingBox=True):
    """
    Processes a folder of PCD files and calculates bounding boxes, projection areas, and angular velocities.
    """
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    boundingBoxDimensions = []
    projectionAreas = []
    averageZValues = []
    normalVectors = []

    for fileName in sorted(os.listdir(folderPath)):  # Ensure files are processed in order
        if fileName.endswith(".pcd"):
            inputFile = os.path.join(folderPath, fileName)
            filteredOutputFile = os.path.join(outputFolder, f"filtered_{fileName}")
            projectionImageFile = os.path.join(outputFolder, f"{fileName}_projection.png")

            print(f"\nProcessing file: {inputFile}")

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
                boundingBoxDimensions.append(np.zeros(3))

            if cleanedPcd is not None:
                area = calculate_projection_area(filteredOutputFile, image_size=500, output_image=projectionImageFile)
                projectionAreas.append(area)
                print(f"2D projection area for {fileName}: {area}")
            else:
                projectionAreas.append(0.0)

            if cleanedPcd is not None:
                points = np.asarray(cleanedPcd.points)
                average_z = np.mean(points[:, 2])
                averageZValues.append(average_z)
                print(f"Nearest average Z value for {fileName}: {average_z}")
            else:
                averageZValues.append(0.0)

            # Step 4: Extract normal vector using the imported function
            if cleanedPcd is not None:
                normal_vector = get_plane_normal(cleanedPcd)  # Imported function
                normalVectors.append(normal_vector)
                print(f"Normal vector of the largest plane for {fileName}: {normal_vector}")
            else:
                normalVectors.append([0.0, 0.0, 0.0])

    overall_average_z = np.mean(averageZValues) if averageZValues else 0.0
    print(f"\nOverall average Z value across all frames: {overall_average_z}")

    if boundingBoxDimensions:
        boundingBoxDimensions = np.array(boundingBoxDimensions)
        average_bounding_box_dimensions = np.mean(boundingBoxDimensions, axis=0)
    else:
        boundingBoxDimensions = np.zeros((0, 3))
        average_bounding_box_dimensions = np.zeros(3)

    print(f"\nAverage bounding box dimensions (X, Y, Z): {average_bounding_box_dimensions}")

    y_dimensions = boundingBoxDimensions[:, 1]
    _, filtered_y_average = remove_outliers_y(y_dimensions)

    if boundingBoxDimensions.size > 0:
        average_bounding_box_dimensions[1] = filtered_y_average

    scaling_factor = -0.0287 * overall_average_z + 0.8376
    print(f"\nCalculated scaling factor: {scaling_factor}")

    scaled_dimensions_cm = average_bounding_box_dimensions * scaling_factor * 100
    print(f"\nScaled dimensions (X, Y, Z) in cm: {scaled_dimensions_cm}")

    # Calculate RPM and angular velocities using the imported function
    rpm, angular_velocities = calculate_rpm(normalVectors, timestamps)  # Imported function
    print(f"\nCalculated RPM: {rpm}")
    print(f"\nAngular Velocities (radians/sec): {angular_velocities}")

    return {
        'bounding_boxes': np.array(boundingBoxDimensions),
        'projection_areas': np.array(projectionAreas),
        'average_z_values': np.array(averageZValues),
        'overall_average_z': overall_average_z,
        'scaled_dimensions_cm': scaled_dimensions_cm.tolist(),
        'filtered_y_average': filtered_y_average,
        'normal_vectors': np.array(normalVectors),
        'rpm': rpm,
        'angular_velocities': angular_velocities  # Include angular velocities in the result
    }
