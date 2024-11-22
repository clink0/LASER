import open3d as o3d
import numpy as np


def load_point_cloud(file_path):
    """Load a PCD file."""
    point_cloud = o3d.io.read_point_cloud(file_path)
    if point_cloud.is_empty():
        raise ValueError("Failed to load PCD file or the file is empty.")
    return point_cloud


def estimate_bounding_box(point_cloud):
    """Estimate an axis-aligned bounding box and return its dimensions."""
    # Remove noise using Statistical Outlier Removal
    point_cloud, _ = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

    # Compute the axis-aligned bounding box
    bbox = point_cloud.get_axis_aligned_bounding_box()

    # Extract the dimensions of the bounding box
    min_bound = bbox.get_min_bound()
    max_bound = bbox.get_max_bound()
    dimensions = max_bound - min_bound

    print(f"Bounding Box Dimensions (X, Y, Z): {dimensions}")
    print(f"Min Bound: {min_bound}")
    print(f"Max Bound: {max_bound}")

    return dimensions


if __name__ == "__main__":
    # Specify the path to your PCD file
    file_path = "/Users/lukebray/PycharmProjects/LASER/cleanupData/output_filtered.pcd"

    try:
        # Load the point cloud
        point_cloud = load_point_cloud(file_path)

        # Estimate bounding box dimensions
        estimate_bounding_box(point_cloud)

    except ValueError as e:
        print(e)