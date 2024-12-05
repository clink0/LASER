import numpy as np

# Set print options to display everything
np.set_printoptions(threshold=np.inf)

# Load the .npy file
file_path = '/Users/lukebray/PycharmProjects/LASER2/OutputPCD/Test2/angular_velocities.npy'  # Replace with your file path
data = np.load(file_path)

# Print the full array
print("Full contents of the .npy file:")
print(data)


# Check the shape and data type
print("\nShape of the array:", data.shape)
print("Data type of the array:", data.dtype)