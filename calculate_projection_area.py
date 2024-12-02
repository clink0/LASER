import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

def calculate_projection_area(pcd_file, image_size=500, output_image=None):
    """
    Projects a point cloud onto a 2D plane (XY), calculates the bounding area,
    and optionally creates an image representation.

    Parameters:
    - pcd_file (str): Path to the input PCD file.
    - image_size (int): Size of the output image (image_size x image_size).
    - output_image (str): Path to save the output image (optional).

    Returns:
    - float: Area of the 2D bounding box based on the projection.
    """
    # Load the PCD file
    pcd = o3d.io.read_point_cloud(pcd_file)
    if pcd.is_empty():
        print(f"Error: Failed to read the file '{pcd_file}' or the file is empty.")
        return 0.0

    # Extract points as a NumPy array
    points = np.asarray(pcd.points)

    # Project the points onto a 2D plane (e.g., XY plane)
    x = points[:, 0]
    y = points[:, 1]

    # Calculate the bounding area based on the projection
    x_range = np.max(x) - np.min(x)
    y_range = np.max(y) - np.min(y)
    area = x_range * y_range

    # Normalize the data to fit into an image size (if needed for visualization)
    if output_image:
        x_normalized = ((x - np.min(x)) / x_range * (image_size - 1)).astype(int)
        y_normalized = ((y - np.min(y)) / y_range * (image_size - 1)).astype(int)

        # Create a blank image
        image = np.ones((image_size, image_size), dtype=np.uint8) * 255  # Start with white background

        # Mark the points on the image
        image[y_normalized, x_normalized] = 0  # Black points

        # Save the image
        plt.imsave(output_image, image, cmap='gray')
        print(f"2D projection image saved to: {output_image}")

    return area
