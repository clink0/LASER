import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

def project_pcd_to_2d_with_whitespace(pcd_file, image_size=500, output_image="point_cloud_projection.png"):
    # Load the PCD file
    pcd = o3d.io.read_point_cloud(pcd_file)

    # Extract points as a NumPy array
    points = np.asarray(pcd.points)

    # Project the points onto a 2D plane (e.g., XY plane)
    x = points[:, 0]
    y = points[:, 1]

    # Normalize the data to fit into an image size
    x_normalized = ((x - np.min(x)) / (np.max(x) - np.min(x)) * (image_size - 1)).astype(int)
    y_normalized = ((y - np.min(y)) / (np.max(y) - np.min(y)) * (image_size - 1)).astype(int)

    # Create a blank image
    image = np.ones((image_size, image_size), dtype=np.uint8) * 255  # Start with white background

    # Mark the points on the image
    image[y_normalized, x_normalized] = 0  # Black points

    # Count whitespace pixels (255 value)
    whitespace_count = np.sum(image == 255)

    # Display the image
    plt.imshow(image, cmap='gray')
    plt.title("2D Projection of Point Cloud")
    plt.axis("off")
    plt.show()

    # Save the image
    plt.imsave(output_image, image, cmap='gray')

    return whitespace_count


# Usage
pcd_file = "background.pcd"  # Replace with your PCD file path
image_size = 500  # Size of the output image
output_image = "point_cloud_projection.png"

whitespace_count = project_pcd_to_2d_with_whitespace(pcd_file, image_size, output_image)
print(f"Whitespace pixels in the image: {whitespace_count}")
