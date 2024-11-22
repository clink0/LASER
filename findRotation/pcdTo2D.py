import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

# Load the PCD file
pcd = o3d.io.read_point_cloud("background.pcd")

# Extract points as a NumPy array
points = np.asarray(pcd.points)

# Project the points onto a 2D plane (e.g., XY plane)
# Drop Z-axis for projection (modify if you want a different axis projection)
x = points[:, 0]
y = points[:, 1]

# Normalize the data to fit into an image size
image_size = 500  # Size of the output image
x_normalized = ((x - np.min(x)) / (np.max(x) - np.min(x)) * (image_size - 1)).astype(int)
y_normalized = ((y - np.min(y)) / (np.max(y) - np.min(y)) * (image_size - 1)).astype(int)

# Create a blank image
image = np.ones((image_size, image_size), dtype=np.uint8) * 255  # Start with white background

# Mark the points on the image
image[y_normalized, x_normalized] = 0  # Black points

# Display the image
plt.imshow(image, cmap='gray')
plt.title("2D Projection of Point Cloud")
plt.axis("off")
plt.show()

# Save the image
plt.imsave("point_cloud_projection.png", image, cmap='gray')
