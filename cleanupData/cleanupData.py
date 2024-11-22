import open3d as o3d
import numpy as np

def cleanAndClusterPointCloud(inputFile, outputFile=None,
                              useStatisticalFilter=True, useRadiusFilter=True, removePlane=True,
                              eps=0.05, minPoints=100, minClusterSize=1000,
                              finalRadiusFilter=True, minBoundingBoxSize=20):
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

        # Filter out clusters based on the bounding box size
        bbox = cluster.get_axis_aligned_bounding_box()
        bboxSize = np.array(bbox.get_extent())

        if len(indices) >= minClusterSize and min(bboxSize) >= minBoundingBoxSize:
            print(f"Adding cluster {i} with {len(indices)} points and bounding box size {bboxSize}.")
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

    # Step 8: Save the final point cloud (optional)
    if outputFile:
        o3d.io.write_point_cloud(outputFile, clusteredPcd)
        print(f"Saved cleaned and clustered point cloud to '{outputFile}'")

    print("Processing complete.")
    return clusteredPcd

# Example usage
inputFile = "/Users/lukebray/PycharmProjects/LASER/convertToPCD/outputPCD/ply_775698.16700000001583.pcd"
outputFile = "output_filtered.pcd"

# Run the function with clustering, plane removal, and bounding box filtering
cleanAndClusterPointCloud(inputFile, outputFile,
                          useStatisticalFilter=True,
                          useRadiusFilter=True,
                          removePlane=True,
                          eps=0.02,
                          minPoints=1000,
                          minClusterSize=500,
                          finalRadiusFilter=True,
                          minBoundingBoxSize=0.05)