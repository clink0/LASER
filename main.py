import os
import numpy as np
from folder_processor import processFolder
from ply_to_pcd_converter import convertPLYtoPCD  # Ensure this is implemented
from extract_metadata import timeStamps  # Ensure this is implemented
import rotationMagnitude as rotMag


def main():
    # Define input and output folders
    plyInputFolder = r"C:\Users\olson\Documents\Location\TEST7\ply_files"
    pcdIntermediateFolder = r"C:\Users\olson\PycharmProjects\LASER2\Data\pcd_files"  # Folder for converted PCD files
    outputPCDFolder = r"C:\Users\olson\PycharmProjects\LASER2\OutputPCD\Test_1"
    metadataFolder = r"C:\Users\olson\Documents\Location\TEST7\txt_files"

    # Step 1: Convert PLY files to PCD
    print("Converting PLY files to PCD...")
    convertPLYtoPCD(plyInputFolder, pcdIntermediateFolder)  # Ensure this function is implemented correctly
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
        dynamic_z_offset=0.25,  # Adjust this value as needed
        calculateBoundingBox=True
    )

    # Step 4: Save results
    dimensions_file = os.path.join(outputPCDFolder, "bounding_box_dimensions.npy")
    areas_file = os.path.join(outputPCDFolder, "projection_areas.npy")
    timestamps_file = os.path.join(outputPCDFolder, "timestamps.npy")

    np.save(dimensions_file, results['bounding_boxes'])
    np.save(areas_file, results['projection_areas'])  # Save new projection areas
    np.save(timestamps_file, np.array(timestamps))

    print(f"\nBounding box dimensions saved to: {dimensions_file}")
    print(f"Projection areas saved to: {areas_file}")
    print(f"Timestamps saved to: {timestamps_file}")

    # Step 5: Print bounding box dimensions and projection areas in the terminal
    print("\nResults for Each Processed File:")
    for i, (dimensions, projection_area) in enumerate(zip(results['bounding_boxes'], results['projection_areas'])):
        print(f"File {i + 1}: Bounding Box Dimensions: {dimensions}, Projection Area: {projection_area}")

    # Step 6: Calculating the Average Rpms over the course of the recording period
    rpm = rotMag.calRotationMagnitude(areas_file, timestamps_file)
    print(f"\nRotation Magnitude saved to: {rpm}")
    print("\nProcessing complete.")


if __name__ == "__main__":
    main()