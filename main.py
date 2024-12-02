import os
import numpy as np
from ply_to_pcd_converter import convertPLYtoPCD  # Import the function from the external file
from folder_processor import processFolder  # Ensure this imports your processFolder function
from metadata_parser import timeStamps  # Import timeStamps function
import rotationMagnitude as rotMag


def main():
    # Define input and output folders
    plyInputFolder = "/Users/lukebray/Fall2024/CE_Design/Data/TEST3/ply_files"
    metadataFolder = "/Users/lukebray/Fall2024/CE_Design/Data/TEST3/txt_files"
    pcdIntermediateFolder = "/Users/lukebray/PycharmProjects/LASER2/Data/pcd_files_3"  # Folder for converted PCD files
    outputPCDFolder = "/Users/lukebray/PycharmProjects/LASER2/OutputPCD/Test_3"

    # Step 1: Convert PLY files to PCD
    print("Converting PLY files to PCD...")
    converted_files = convertPLYtoPCD(plyInputFolder, pcdIntermediateFolder)
    print(f"Converted PLY files: {converted_files}")
    print(f"Converted PLY files saved to: {pcdIntermediateFolder}")

    # Step 2: Extract timestamps
    print("Extracting timestamps from metadata...")
    timestamps = timeStamps(metadataFolder)
    print(f"Extracted timestamps: {timestamps}")

    # Step 3: Process PCD files to filter, create projections, and calculate bounding boxes/projection areas
    print("\nProcessing PCD files to filter and calculate bounding boxes and projection areas...")
    results = processFolder(
        folderPath=pcdIntermediateFolder,
        outputFolder=outputPCDFolder,
        dynamic_z_offset=0.5,  # Adjust this value as needed
        calculateBoundingBox=True
    )

    # Step 4: Save results
    dimensions_file = os.path.join(outputPCDFolder, "bounding_box_dimensions.npy")
    areas_file = os.path.join(outputPCDFolder, "projection_areas.npy")
    timestamps_file = os.path.join(outputPCDFolder, "timestamps.npy")
    average_z_file = os.path.join(outputPCDFolder, "overall_average_z.npy")
    scaled_dimensions_file = os.path.join(outputPCDFolder, "scaled_dimensions_cm.npy")

    np.save(dimensions_file, results['bounding_boxes'])
    np.save(areas_file, results['projection_areas'])
    np.save(timestamps_file, np.array(timestamps))
    np.save(average_z_file, np.array([results['overall_average_z']]))
    np.save(scaled_dimensions_file, results['scaled_dimensions_cm'])

    print(f"\nBounding box dimensions saved to: {dimensions_file}")
    print(f"Projection areas saved to: {areas_file}")
    print(f"Timestamps saved to: {timestamps_file}")
    print(f"Overall average Z value saved to: {average_z_file}")
    print(f"Scaled dimensions in cm saved to: {scaled_dimensions_file}")

    # Step 5: Print bounding box dimensions, projection areas, and overall average Z
    print("\nResults for Each Processed File:")
    for i, (dimensions, projection_area, avg_z) in enumerate(
            zip(results['bounding_boxes'], results['projection_areas'], results['average_z_values'])):
        print(f"File {i + 1}: Bounding Box Dimensions: {dimensions}, Projection Area: {projection_area}, Average Z: {avg_z}")

    print(f"\nOverall average Z value across all frames: {results['overall_average_z']}")
    print(f"\nScaled dimensions (X, Y, Z) in cm: {results['scaled_dimensions_cm']}")

    # Step 6: Calculate the magnitude of the rotation
    rpm = rotMag.calRotationMagnitude(areas_file, timestamps_file)
    print(f"\nRPM: {rpm}")
    print("\nProcessing complete.")


if __name__ == "__main__":
    main()
