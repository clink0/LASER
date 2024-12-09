import os
import numpy as np
import open3d as o3d
from point_cloud_filtering import cleanAndClusterPointCloud
from rotation_calculations import get_plane_normal, calculate_rpm  # Import rotation functions


def remove_outliers_y(data):
    """
    Removes outliers from the Y-dimension data and calculates the average of the filtered data.
    """
    median_value = np.median(data)
    filtered_data = data[data >= median_value]
    filtered_average = np.mean(filtered_data) if len(filtered_data) > 0 else 0.0
    return filtered_data, filtered_average


def update_loading_bar(processed, total):
    """
    Updates the loading bar with the current progress.
    """
    percentage = (processed / total) * 100
    bar_length = 20  # Adjust the bar length as needed
    filled_length = int(bar_length * processed // total)
    bar = f"[{'|' * filled_length}{' ' * (bar_length - filled_length)}] {int(percentage)}%"
    print(f"\r{bar}", end="", flush=True)


def processFolder(folderPath, outputFolder, timestamps, dynamic_z_offset=0.5, calculateBoundingBox=True):
    """
    Processes a folder of PCD files and calculates bounding boxes and angular velocities.
    """
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    boundingBoxDimensions = []
    averageZValues = []
    normalVectors = []

    files = [f for f in os.listdir(folderPath) if f.endswith(".pcd")]
    total_files = len(files)

    for i, fileName in enumerate(sorted(files)):  # Ensure files are processed in order
        inputFile = os.path.join(folderPath, fileName)
        filteredOutputFile = os.path.join(outputFolder, f"filtered_{fileName}")

        # Process the point cloud and cluster it
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
        else:
            boundingBoxDimensions.append(np.zeros(3))

        if cleanedPcd is not None:
            points = np.asarray(cleanedPcd.points)
            average_z = np.mean(points[:, 2])
            averageZValues.append(average_z)
        else:
            averageZValues.append(0.0)

        if cleanedPcd is not None:
            normal_vector = get_plane_normal(cleanedPcd)  # Imported function
            normalVectors.append(normal_vector)
        else:
            normalVectors.append([0.0, 0.0, 0.0])

        # Update the loading bar
        update_loading_bar(i + 1, total_files)

    print()  # Move to the next line after the loading bar

    overall_average_z = np.mean(averageZValues) if averageZValues else 0.0

    if boundingBoxDimensions:
        boundingBoxDimensions = np.array(boundingBoxDimensions)
        average_bounding_box_dimensions = np.mean(boundingBoxDimensions, axis=0)
    else:
        boundingBoxDimensions = np.zeros((0, 3))
        average_bounding_box_dimensions = np.zeros(3)

    y_dimensions = boundingBoxDimensions[:, 1]
    _, filtered_y_average = remove_outliers_y(y_dimensions)

    if boundingBoxDimensions.size > 0:
        average_bounding_box_dimensions[1] = filtered_y_average

    scaling_factor = -0.0287 * overall_average_z + 0.8376

    scaled_dimensions_cm = average_bounding_box_dimensions * scaling_factor * 100
    scaled_bounding_box_dimensions = boundingBoxDimensions * scaling_factor * 100

    rpm, angular_velocities = calculate_rpm(normalVectors, timestamps)  # Imported function
    print(f"\nCalculated RPM: {rpm}")

    return {
        'scaled_bounding_boxes': np.array(scaled_bounding_box_dimensions),
        'average_z_values': np.array(averageZValues),
        'overall_average_z': overall_average_z,
        'scaled_dimensions_cm': scaled_dimensions_cm.tolist(),
        'filtered_y_average': filtered_y_average,
        'normal_vectors': np.array(normalVectors),
        'rpm': rpm,
        'angular_velocities': angular_velocities  # Include angular velocities in the result
    }