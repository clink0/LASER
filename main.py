import os
import numpy as np
from ply_to_pcd_converter import convertPLYtoPCD  # Import the function from the external file
from folder_processor import processFolder  # Ensure this imports your processFolder function
from metadata_parser import timeStamps  # Import timeStamps function
from animation import display_pcd_animation  # Import the animation function


def main():
    # Define input and output folders
    plyInputFolder = "/Users/lukebray/Fall2024/CE_Design/Data/Test1/ply_files"
    metadataFolder = "/Users/lukebray/Fall2024/CE_Design/Data/Test1/txt_files"
    pcdIntermediateFolder = "/Users/lukebray/PycharmProjects/LASER2/Data/pcd_files_Test1"  # Folder for converted PCD files
    outputPCDFolder = "/Users/lukebray/PycharmProjects/LASER2/OutputPCD/Test1"

    # Step 1: Convert PLY files to PCD
    print("Converting PLY files to PCD...")
    converted_files = convertPLYtoPCD(plyInputFolder, pcdIntermediateFolder)
    print(f"Converted PLY files: {converted_files}")
    print(f"Converted PLY files saved to: {pcdIntermediateFolder}")

    # Step 2: Extract timestamps
    print("Extracting timestamps from metadata...")
    timestamps = timeStamps(metadataFolder)

    # Step 3: Process PCD files to filter, create projections, and calculate bounding boxes/projection areas
    print("\nProcessing PCD files to filter and calculate bounding boxes and projection areas...")
    results = processFolder(
        folderPath=pcdIntermediateFolder,
        outputFolder=outputPCDFolder,
        timestamps=timestamps,  # Pass the extracted timestamps here
        dynamic_z_offset=0.5,  # Adjust this value as needed
        calculateBoundingBox=True
    )

    # Step 4: Save results
    scaled_dimensions_file = os.path.join(outputPCDFolder, "scaled_dimensions_cm.npy")
    np.save(scaled_dimensions_file, results['scaled_dimensions_cm'])
    print(f"\nScaled dimensions (X, Y, Z) in cm: {results['scaled_dimensions_cm']}")

    # Step 5: Display the animation with additional information
    print("\nStarting point cloud animation...")
    average_rpm = results['rpm']
    scaled_dimensions = results['scaled_dimensions_cm']
    display_time = 0.0333333  # Time in seconds to display each point cloud
    display_pcd_animation(outputPCDFolder, display_time, average_rpm, scaled_dimensions)

    print("\nProcessing complete.")


if __name__ == "__main__":
    main()
