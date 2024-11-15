import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

# convert PLY to PCD



# Given data (current dimensions)
current_width = 0.97151
current_height = 0.77428
current_depth = 0.48616

# Desired dimensions
desired_width = 18.5
desired_height = 8
desired_depth = 1.5

# Step 1: Calculate the scaling factors for each dimension
scaling_factors = np.array([desired_width / current_width,
                            desired_height / current_height,
                            desired_depth / current_depth])
# Load the point cloud
# clean_pcd = o3d.io.read_point_cloud("C:\\xt-pcds\\20241113-11-36-01_Binary.pcd") # this is the rectangle data with scaling factor is right
# clean_pcd = o3d.io.read_point_cloud("C:\\xt-pcds\\20241113-12-02-43_Binary.pcd") # this is the lidar box
# clean_pcd = o3d.io.read_point_cloud("C:\\xt-pcds\\20241113-12-05-18_Binary.pcd")# Test 1
# clean_pcd = o3d.io.read_point_cloud("C:\\xt-pcds\\20241113-13-01-59_Binary.pcd")# Test 2
# clean_pcd = o3d.io.read_point_cloud("C:\\xt-pcds\\20241114-10-07-40_Binary.pcd") # Test 3
clean_pcd = o3d.io.read_point_cloud("C:\\xt-pcds\\20241114-10-26-32_Binary.pcd")# Test 1 without curtain
if clean_pcd.is_empty():
    print("The point cloud is empty.")


points = np.asarray(clean_pcd.points)

# Check for NaN or Inf values
if np.any(np.isnan(points)) or np.any(np.isinf(points)):
    print("The point cloud contains invalid points.")
    # Remove invalid points
    clean_pcd = clean_pcd.select_by_index(np.where(np.isfinite(points).all(axis=1))[0])
# Check the number of points
num_points = len(clean_pcd.points)
print(f"Number of points in the point cloud: {num_points}")

# Only segment if there are enough points
if num_points >= 3:
    # plane_model, inliers = clean_pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
    # # Example: Reduce the distance threshold
    plane_model, inliers = clean_pcd.segment_plane(distance_threshold=0.005, ransac_n=3, num_iterations=1000)

    print("Plane model:", plane_model)
else:
    print("Point cloud is too sparse for plane segmentation.")


# Extract the inliers and outliers
inlier_cloud = clean_pcd.select_by_index(inliers, invert=True)

# Color the inlier cloud as green (the object being measured)
inlier_cloud.paint_uniform_color([0, 1.0, 0])  # Green for inliers

# Compute the axis-aligned bounding box
aabb = clean_pcd.get_axis_aligned_bounding_box()

# Get the extent (dimensions) of the bounding box
dimensions = aabb.get_extent()
scaled_dimensions = dimensions * scaling_factors

print(f"Dimensions (Width, Height, Depth): {scaled_dimensions}")
print(f"Dimensions (Width, Height, Depth): {dimensions}")

# Visualize the point clouds
o3d.visualization.draw_geometries([inlier_cloud])


# 18.5 cm width
#  8 cm height
# 1.5 cm depth