import open3d as o3d
import numpy as np

def clean_and_cluster_point_cloud(input_file, output_file=None,
                                  use_statistical_filter=True, use_radius_filter=True, remove_plane=True,
                                  eps=0.05, min_points=100, min_cluster_size=500,
                                  final_radius_filter=True):
    # Step 1: Load the point cloud from the PCD file
    pcd = o3d.io.read_point_cloud(input_file)
    if not pcd:
        print(f"Failed to read the file: {input_file}")
        return

    print(f"Loaded {input_file}, containing {len(pcd.points)} points")

    # Step 2: Remove NaN or Inf values
    points = np.asarray(pcd.points)
    valid_indices = np.isfinite(points).all(axis=1)
    cleaned_points = points[valid_indices]
    cleaned_pcd = o3d.geometry.PointCloud()
    cleaned_pcd.points = o3d.utility.Vector3dVector(cleaned_points)

    # Step 3: Apply Statistical Outlier Removal (optional)
    if use_statistical_filter:
        cleaned_pcd, _ = cleaned_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

    # Step 4: Apply Radius Outlier Removal (optional)
    if use_radius_filter:
        cleaned_pcd, _ = cleaned_pcd.remove_radius_outlier(nb_points=16, radius=0.05)

    # Step 5: Apply Euclidean Clustering to isolate objects
    labels = np.array(cleaned_pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))

    max_label = labels.max()
    clustered_pcd = o3d.geometry.PointCloud()
    for i in range(max_label + 1):
        indices = np.where(labels == i)[0]
        if len(indices) >= min_cluster_size:
            clustered_pcd += cleaned_pcd.select_by_index(indices)

    # Step 6: Apply final Radius Outlier Removal (optional)
    if final_radius_filter:
        clustered_pcd, _ = clustered_pcd.remove_radius_outlier(nb_points=50, radius=0.02)

    # Step 7: Calculate object size using the Axis-Aligned Bounding Box (AABB)
    if len(clustered_pcd.points) > 0:
        # Calculate the Axis-Aligned Bounding Box
        aabb = clustered_pcd.get_axis_aligned_bounding_box()
        aabb_extent = aabb.get_extent()
        print(f"AABB dimensions (Length x Width x Height): {aabb_extent}")

        # Visualize the AABB
        aabb.color = (0, 1, 0)  # Color the AABB green for visualization
        o3d.visualization.draw_geometries([clustered_pcd, aabb])
    else:
        print("No points left in the point cloud after filtering.")

    # Step 8: Save the final point cloud (optional)
    if output_file:
        o3d.io.write_point_cloud(output_file, clustered_pcd)
        print(f"Saved cleaned and clustered point cloud to {output_file}")

    return clustered_pcd

# Example usage
input_file = "path/to/inputFile.pcd"
output_file = "output.pcd"

# Run the function with clustering and AABB size calculation
clean_and_cluster_point_cloud(input_file, output_file,
                              use_statistical_filter=True,
                              use_radius_filter=True,
                              remove_plane=True,
                              eps=0.02,
                              min_points=1000,
                              min_cluster_size=2000,
                              final_radius_filter=True)