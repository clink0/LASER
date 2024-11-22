import open3d as o3d
import numpy as np


def main():
    # Step 1: Load the PCD file
    file_path = "/Users/lukebray/PycharmProjects/LASER/convertToPCD/outputPCD/PLY_197182.18200000000070.pcd"  # Replace with your PCD file path
    pcd = o3d.io.read_point_cloud(file_path)
    print("Point cloud loaded successfully.")

    # Step 2: Segment the plane using RANSAC
    distance_threshold = 0.01  # Adjust based on your data
    ransac_n = 3
    num_iterations = 1000

    print("Segmenting the largest plane...")
    plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                             ransac_n=ransac_n,
                                             num_iterations=num_iterations)
    print(
        f"Plane equation: {plane_model[0]:.4f}x + {plane_model[1]:.4f}y + {plane_model[2]:.4f}z + {plane_model[3]:.4f} = 0")

    # Step 3: Extract the plane (background) and other points
    plane_cloud = pcd.select_by_index(inliers)
    other_cloud = pcd.select_by_index(inliers, invert=True)

    # Step 4: Apply a bounding box filter to the non-plane points
    print("Applying bounding box filter...")

    # Define the bounding box limits (adjust as needed)
    min_bound = np.array([-1, -1, -0.5])  # Adjust these values
    max_bound = np.array([1, 1, 0.5])  # Adjust these values

    # Create an AxisAlignedBoundingBox object
    bounding_box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    # Filter the other_cloud using the bounding box
    filtered_cloud = other_cloud.crop(bounding_box)

    # Step 5: Visualize the results
    print("Visualizing the background (plane)...")
    o3d.visualization.draw_geometries([plane_cloud], window_name='Background', point_show_normal=False)

    print("Visualizing the objects within the bounding box...")
    o3d.visualization.draw_geometries([filtered_cloud], window_name='Filtered Objects', point_show_normal=False)

    # Step 6: Save the results (Optional)
    o3d.io.write_point_cloud("background.pcd", plane_cloud)
    o3d.io.write_point_cloud("filtered_objects.pcd", filtered_cloud)
    print("Segmented and filtered point clouds saved as 'background.pcd' and 'filtered_objects.pcd'.")


if __name__ == "__main__":
    main()