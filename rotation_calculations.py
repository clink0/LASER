import numpy as np
from scipy import stats

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

def calculate_rpm(normal_vectors, timestamps, precision=2):
    """
    Calculate rotations per minute (RPM) from normal vectors and timestamps.
    - normal_vectors: List of normal vectors (Nx3 array).
    - timestamps: List of timestamps corresponding to the normal vectors.
    - precision: Rounding precision for angular velocities.

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

    # Round angular velocities to handle "close enough" values
    rounded_angular_velocities = [round(val, precision) for val in angular_velocities]

    # Calculate mode
    if rounded_angular_velocities:
        mode_result = stats.mode(rounded_angular_velocities)
        mode_angular_velocity = np.atleast_1d(mode_result.mode)[0] if mode_result.mode.size > 0 else 0
    else:
        mode_angular_velocity = 0

    # Convert to RPM (revolutions per minute)
    rpm = (mode_angular_velocity * 60) / (2 * np.pi)
    return rpm, angular_velocities
