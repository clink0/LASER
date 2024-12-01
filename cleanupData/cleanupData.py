import open3d as o3d
import numpy as np
import os

def calculateBoundingBoxDimensions(pointCloud):
    """
    Calculates the dimensions of the oriented bounding box around the given point cloud.
    Returns the bounding box and its dimensions.
    """
    if pointCloud.is_empty():
        print("Error: Point cloud is empty.")
        return None, None

    print("Calculating oriented bounding box dimensions...")
    bbox = pointCloud.get_oriented_bounding_box()
    bboxSize = np.array(bbox.extent)  # Extent gives the length, width, and height of the OBB
    print(f"Oriented bounding box dimensions: {bboxSize}")
    return bbox, bboxSize

def cleanAndClusterPointCloud(inputFile, outputFile=None,
                              useStatisticalFilter=True, useRadiusFilter=True, removePlane=True,
                              eps=0.05, minPoints=100, minClusterSize=1000,
                              finalRadiusFilter=True):
    """
    Function to clean and cluster a point cloud.
    """
    # Step 1: Load the point cloud from the PCD file
    print(f"Loading point cloud from '{inputFile}'...")
    pcd = o3d.io.read_point_cloud(inputFile)
    if pcd.is_empty():
        print(f"Error: Failed to read the file '{inputFile}' or file is empty.")
        return None

    print(f"Successfully loaded point cloud with {len(pcd.points)} points.")

    # Step 2: Remove NaN or Inf values
    print("Removing NaN and Inf values...")
    points = np.asarray(pcd.points)
    validIndices = np.isfinite(points).all(axis=1)
    cleanedPoints = points[validIndices]
    cleanedPcd = o3d.geometry.PointCloud()
    cleanedPcd.points = o3d.utility.Vector3dVector(cleanedPoints)
    print(f"Removed invalid points. Remaining points: {len(cleanedPoints)}.")

    # Step 3: Remove the largest plane (optional)
    if removePlane:
        print("Removing flat background using plane segmentation...")
        planeModel, inliers = cleanedPcd.segment_plane(distance_threshold=0.01,
                                                       ransac_n=3,
                                                       num_iterations=1000)
        print(f"Detected plane with coefficients: {planeModel}")
        cleanedPcd = cleanedPcd.select_by_index(inliers, invert=True)
        print(f"Points remaining after plane removal: {len(cleanedPcd.points)}")

    if cleanedPcd.is_empty():
        print("Error: No points left after plane removal.")
        return None

    # Step 4: Apply Statistical Outlier Removal (optional)
    if useStatisticalFilter:
        print("Applying Statistical Outlier Removal...")
        cleanedPcd, _ = cleanedPcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        print(f"Points remaining after Statistical Outlier Removal: {len(cleanedPcd.points)}")

    # Step 5: Apply Radius Outlier Removal (optional)
    if useRadiusFilter:
        print("Applying Radius Outlier Removal...")
        cleanedPcd, _ = cleanedPcd.remove_radius_outlier(nb_points=16, radius=0.05)
        print(f"Points remaining after Radius Outlier Removal: {len(cleanedPcd.points)}")

    if cleanedPcd.is_empty():
        print("Error: No points left after filtering.")
        return None

    # Step 6: Apply Euclidean Clustering to isolate objects
    print("Applying Euclidean Clustering...")
    labels = np.array(cleanedPcd.cluster_dbscan(eps=eps, min_points=minPoints, print_progress=True))
    maxLabel = labels.max()
    print(f"Found {maxLabel + 1} clusters.")

    clusteredPcd = o3d.geometry.PointCloud()
    for i in range(maxLabel + 1):
        indices = np.where(labels == i)[0]
        cluster = cleanedPcd.select_by_index(indices)

        if len(indices) >= minClusterSize:
            clusteredPcd += cluster
        else:
            print(f"Skipping small/insignificant cluster {i}.")

    if clusteredPcd.is_empty():
        print("Error: No clusters found after filtering.")
        return None

    # Step 7: Apply final Radius Outlier Removal (optional)
    if finalRadiusFilter:
        print("Applying final Radius Outlier Removal...")
        clusteredPcd, _ = clusteredPcd.remove_radius_outlier(nb_points=50, radius=0.02)
        print(f"Points remaining after final Radius Outlier Removal: {len(clusteredPcd.points)}")

    if clusteredPcd.is_empty():
        print("Error: No points left after the final filtering.")
        return None

    # Step 8: Calculate bounding box dimensions and save final point cloud
    bbox, bboxSize = calculateBoundingBoxDimensions(clusteredPcd)

    if outputFile:
        o3d.io.write_point_cloud(outputFile, clusteredPcd)
        print(f"Saved cleaned and clustered point cloud to '{outputFile}'")

    print("Processing complete.")
    return clusteredPcd, bbox, bboxSize

def processFolder(folderPath, outputFolder):
    """
    Processes all PCD files in a given folder and saves the results in the output folder.
    """
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    for fileName in os.listdir(folderPath):
        if fileName.endswith(".pcd"):
            inputFile = os.path.join(folderPath, fileName)
            outputFile = os.path.join(outputFolder, f"filtered_{fileName}")
            print(f"\nProcessing file: {inputFile}")
            cleanedPcd, boundingBox, dimensions = cleanAndClusterPointCloud(
                inputFile, outputFile,
                useStatisticalFilter=True,
                useRadiusFilter=True,
                removePlane=True,
                eps=0.2,
                minPoints=1000,
                minClusterSize=500,
                finalRadiusFilter=True
            )
            if dimensions is not None:
                print(f"Processed {fileName}: Bounding box dimensions: {dimensions}")
            else:
                print(f"Failed to process {fileName}")

# Example usage
inputFolder = "/Users/lukebray/PycharmProjects/LASER/convertToPCD/outputPCD"
outputFolder = "/Users/lukebray/PycharmProjects/LASER/findDimensions/output"

# Process all files in the folder
processFolder(inputFolder, outputFolder)
