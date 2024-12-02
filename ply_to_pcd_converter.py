import open3d as o3d
import os


def convertPLYtoPCD(input_folder, output_folder):
    """
    Converts all PLY files in the input_folder to PCD format
    and saves them in the output_folder.

    Parameters:
    - input_folder (str): Path to the folder containing PLY files.
    - output_folder (str): Path to the folder where PCD files will be saved.

    Returns:
    - List of converted files with their output paths.
    """
    converted_files = []

    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".ply"):
            input_file = os.path.join(input_folder, filename)

            # Load the PLY file
            pcd = o3d.io.read_point_cloud(input_file)

            # Define output file path
            output_file = os.path.join(output_folder, filename.replace(".ply", ".pcd"))

            # Save the PCD file
            o3d.io.write_point_cloud(output_file, pcd)
            converted_files.append(output_file)

    return converted_files
