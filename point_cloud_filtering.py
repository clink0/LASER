import open3d as o3d
import numpy as np
from bounding_box import calculateBoundingBoxDimensions

def cleanAndClusterPointCloud(inputFile, outputFile=None,
                              useStatisticalFilter=True, useRadiusFilter=True,
                              dynamic_z_offset=0.0,  # Offset for Z filter from the furthest Z
                              eps=0.05, minPoints=100, minClusterSize=1000,
                              finalRadiusFilter=True):
    """
    Function to clean, dynamically crop, and cluster a point cloud.
    The Z-axis filter is dynamically applied at the beginning, and plane removal is disabled.
    If no valid points remain after filtering, returns default values and continues.
    """

    # Default output if filtering fails
    default_bbox = np.zeros(3)  # [0, 0, 0] for bounding box dimensions
    print(f"Loading point cloud from '{inputFile}'...")

    # Step 1: Load the point cloud from the PCD file
    pcd = o3d.io.read_point_cloud(inputFile)
    if pcd.is_empty():
        print(f"Error: Failed to read the file '{inputFile}' or file is empty.")
        return None, None, default_bbox

    print(f"Successfully loaded point cloud with {len(pcd.points)} points.")

    # Step 2: Remove NaN or Inf values
    print("Removing NaN and Inf values...")
    points = np.asarray(pcd.points)
    validIndices = np.isfinite(points).all(axis=1)
    cleanedPoints = points[validIndices]
    cleanedPcd = o3d.geometry.PointCloud()
    cleanedPcd.points = o3d.utility.Vector3dVector(cleanedPoints)
    print(f"Removed invalid points. Remaining points: {len(cleanedPoints)}.")

    if cleanedPcd.is_empty():
        print("Error: No valid points after NaN/Inf removal.")
        return None, None, default_bbox

    # Step 3: Dynamically assign and apply the Z-axis filter
    z_values = np.asarray(cleanedPcd.points)[:, 2]
    max_z = np.min(z_values) + dynamic_z_offset
    print(f"Applying dynamic Z filter: Z <= {max_z}...")
    within_bounds = z_values >= max_z
    filteredPoints = np.asarray(cleanedPcd.points)[within_bounds]

    if len(filteredPoints) == 0:
        print("Error: No points left after dynamic Z filtering.")
        return None, None, default_bbox

    filteredPcd = o3d.geometry.PointCloud()
    filteredPcd.points = o3d.utility.Vector3dVector(filteredPoints)
    cleanedPcd = filteredPcd  # Update the cleaned point cloud to the Z-filtered version
    print(f"Points remaining after Z filter: {len(filteredPoints)}.")

    # Step 4: Apply Statistical Outlier Removal (optional)
    if useStatisticalFilter:
        print("Applying Statistical Outlier Removal...")
        cleanedPcd, _ = cleanedPcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        print(f"Points remaining after Statistical Outlier Removal: {len(cleanedPcd.points)}")

        if cleanedPcd.is_empty():
            print("Error: No points left after Statistical Outlier Removal.")
            return None, None, default_bbox

    # Step 5: Apply Radius Outlier Removal (optional)
    if useRadiusFilter:
        print("Applying Radius Outlier Removal...")
        cleanedPcd, _ = cleanedPcd.remove_radius_outlier(nb_points=16, radius=0.05)
        print(f"Points remaining after Radius Outlier Removal: {len(cleanedPcd.points)}")

        if cleanedPcd.is_empty():
            print("Error: No points left after Radius Outlier Removal.")
            return None, None, default_bbox

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
        return None, None, default_bbox

    # Step 7: Apply final Radius Outlier Removal (optional)
    if finalRadiusFilter:
        print("Applying final Radius Outlier Removal...")
        clusteredPcd, _ = clusteredPcd.remove_radius_outlier(nb_points=50, radius=0.02)
        print(f"Points remaining after final Radius Outlier Removal: {len(clusteredPcd.points)}")

        if clusteredPcd.is_empty():
            print("Error: No points left after the final filtering.")
            return None, None, default_bbox

    # Step 8: Calculate bounding box dimensions and save final point cloud
    bbox, bboxSize = calculateBoundingBoxDimensions(clusteredPcd)

    if outputFile:
        o3d.io.write_point_cloud(outputFile, clusteredPcd)
        print(f"Saved cleaned and clustered point cloud to '{outputFile}'")

    print("Processing complete.")
    return clusteredPcd, bbox, bboxSize
