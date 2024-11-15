import open3d as o3d
import numpy as np

def clean_point_cloud(input_file, output_file=None, use_statistical_filter=True, use_radius_filter=True):
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

    print(f"Cleaned NaN/Inf values, resulting in {len(cleaned_points)} points")

    # Step 3: Apply Statistical Outlier Removal (optional)
    if use_statistical_filter:
        print("Applying Statistical Outlier Removal...")
        cleaned_pcd, ind = cleaned_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        print(f"Points remaining after statistical filtering: {len(cleaned_pcd.points)}")

    # Step 4: Apply Radius Outlier Removal (optional)
    if use_radius_filter:
        print("Applying Radius Outlier Removal...")
        cleaned_pcd, ind = cleaned_pcd.remove_radius_outlier(nb_points=16, radius=0.05)
        print(f"Points remaining after radius filtering: {len(cleaned_pcd.points)}")

    # Step 5: Save the cleaned point cloud if an output file is specified
    if output_file:
        o3d.io.write_point_cloud(output_file, cleaned_pcd)
        print(f"Saved cleaned point cloud to {output_file}")

    # Step 6: Visualize the cleaned point cloud
    o3d.visualization.draw_geometries([cleaned_pcd])

    return cleaned_pcd

# Example usage
input_file = "/Users/lukebray/PycharmProjects/LASER/convertToPCD/outputPCD/PLY_197182.18200000000070.pcd"         # Replace with your .pcd file path
output_file = "/Users/lukebray/PycharmProjects/LASER/cleanupData/cleaned.pcd" # Optional output file path

# Run the cleaning function with filtering options
clean_point_cloud(input_file, output_file, use_statistical_filter=True, use_radius_filter=True)