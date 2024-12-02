import numpy as np
import numpy as np
def compute_centroid(points):
    return np.mean(points, axis=0)

def compute_rotation_matrix(points1, points2):
    # Center the points
    centroid1 = compute_centroid(points1)
    centroid2 = compute_centroid(points2)
    centered_points1 = points1 - centroid1
    centered_points2 = points2 - centroid2

    # Compute covariance matrix
    H = np.dot(centered_points1.T, centered_points2)
    U, _, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # Ensure proper rotation (det(R) = 1)
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = np.dot(Vt.T, U.T)
    return R
# Example: Simulated object points in two frames
points_frame1 = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
theta = np.radians(45)  # 45-degree rotation
rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                             [np.sin(theta), np.cos(theta)]])
points_frame2 = np.dot(points_frame1, rotation_matrix.T)

# Compute rotation matrix
R = compute_rotation_matrix(points_frame1, points_frame2)

# Extract rotation angle
angle = np.arctan2(R[1, 0], R[0, 0])
print(f"Rotation angle: {np.degrees(angle):.2f} degrees")