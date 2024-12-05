import numpy as np

def calculateAverageDimensions(dimensions_file, output_file=None):
    """
    Calculates the average dimensions (X, Y, Z) from bounding box data.

    Parameters:
    - dimensions_file (str): Path to the .npy file containing bounding box dimensions (num_frames x 3 array).
    - output_file (str, optional): Path to save the average dimensions as a .npy file.

    Returns:
    - np.array: Array containing the average dimensions [avg_X, avg_Y, avg_Z].
    """
    try:
        # Step 1: Load the bounding box dimensions
        dimensions = np.load(dimensions_file)  # Shape: (num_frames, 3)

        # Step 2: Calculate the average dimensions
        average_dimensions = np.mean(dimensions, axis=0)  # Mean along the rows (frames)

        # Step 3: Save the average dimensions if output_file is specified
        if output_file:
            np.save(output_file, average_dimensions)

        return average_dimensions

    except Exception as e:
        print(f"Error calculating average dimensions: {e}")
        return None