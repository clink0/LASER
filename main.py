import os
import numpy as np
from folder_processor import processFolder
from ply_to_pcd_converter import convertPLYtoPCD  # Ensure this is implemented
from extract_metadata import timeStamps  # Ensure this is implemented


def main():
    # Define input and output folders
    plyInputFolder = "/Users/lukebray/PycharmProjects/LASER2/Data/Dist70/ply_files"
    metadataFolder = "/Users/lukebray/PycharmProjects/LASER2/Data/Dist70/txt_files"
    pcdIntermediateFolder = "/Users/lukebray/PycharmProjects/LASER2/Data/pcd_files"  # Folder for converted PCD files
    outputPCDFolder = "/Users/lukebray/PycharmProjects/LASER2/OutputPCD/Test_1"

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
        dynamic_z_offset=0.5,  # Adjust this value as needed
        calculateBoundingBox=True
    )

    # Step 4: Save results
    dimensions_file = os.path.join(outputPCDFolder, "bounding_box_dimensions.npy")
    areas_file = os.path.join(outputPCDFolder, "projection_areas.npy")
    timestamps_file = os.path.join(outputPCDFolder, "timestamps.npy")
    average_z_file = os.path.join(outputPCDFolder, "overall_average_z.npy")

    np.save(dimensions_file, results['bounding_boxes'])
    np.save(areas_file, results['projection_areas'])  # Save projection areas
    np.save(timestamps_file, np.array(timestamps))
    np.save(average_z_file, np.array([results['overall_average_z']]))  # Save overall average Z value as a single-element array

    print(f"\nBounding box dimensions saved to: {dimensions_file}")
    print(f"Projection areas saved to: {areas_file}")
    print(f"Timestamps saved to: {timestamps_file}")
    print(f"Overall average Z value saved to: {average_z_file}")

    # Step 5: Print bounding box dimensions, projection areas, and overall average Z
    print("\nResults for Each Processed File:")
    for i, (dimensions, projection_area, avg_z) in enumerate(
            zip(results['bounding_boxes'], results['projection_areas'], results['average_z_values'])):
        print(f"File {i + 1}: Bounding Box Dimensions: {dimensions}, Projection Area: {projection_area}, Average Z: {avg_z}")

    print(f"\nOverall average Z value across all frames: {results['overall_average_z']}")

    print("\nProcessing complete.")


if __name__ == "__main__":
    main()
