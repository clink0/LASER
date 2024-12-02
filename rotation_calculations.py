import numpy as np

def get_plane_normal(pcd):
    """
    Extracts the normal vector of the largest plane in a given point cloud.
    """
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                             ransac_n=3,
                                             num_iterations=1000)
    a, b, c, d = plane_model
    normal_vector = np.array([a, b, c])
    normal_vector /= np.linalg.norm(normal_vector)  # Normalize the vector
    return normal_vector


def calculate_rpm(normal_vectors, timestamps):
    """
    Calculate rotations per minute (RPM) from normal vectors and timestamps.
    - normal_vectors: List of normal vectors (Nx3 array).
    - timestamps: List of timestamps corresponding to the normal vectors.

    Returns:
    - RPM value.
    - angular_velocities: List of angular velocities (radians per second).
    """
    angular_velocities = []

    for i in range(len(normal_vectors) - 1):
        # Calculate the angle between consecutive normal vectors
        n1 = normal_vectors[i]
        n2 = normal_vectors[i + 1]
        cos_theta = np.clip(np.dot(n1, n2), -1.0, 1.0)  # Dot product and clamp for numerical stability
        angle = np.arccos(cos_theta)  # Angle in radians

        # Time difference between consecutive frames
        time_diff = timestamps[i + 1] - timestamps[i]

        # Angular velocity in radians per second
        angular_velocity = angle / time_diff if time_diff > 0 else 0
        angular_velocities.append(angular_velocity)

    # Average angular velocity (radians per second)
    median_angular_velocity = np.median(angular_velocities) if angular_velocities else 0

    # Convert to RPM (revolutions per minute)
    rpm = (median_angular_velocity * 60) / (2 * np.pi)
    return rpm, angular_velocities
