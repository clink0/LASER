import os
import numpy as np
import pandas as pd
from ply_to_pcd_converter import convertPLYtoPCD  # Import the function from the external file
from folder_processor import processFolder  # Ensure this imports your processFolder function
from metadata_parser import timeStamps  # Import timeStamps function
from animation import display_pcd_animation  # Import the animation function


def main():
    # Define the test number as a variable
    test_number = ("2")

    # Define input and output folders using the variable
    plyInputFolder = f"/Data/Test{test_number}/ply_files"
    metadataFolder = f"/Data/Test{test_number}/txt_files"
    pcdIntermediateFolder = f"/LASER2/Data/Test{test_number}"  # Folder for converted PCD files
    outputPCDFolder = f"/LASER2/OutputPCD/Test{test_number}"
    outputCSVFolder = f"/FinalDataOutput/Test{test_number}"

    # Ensure the outputCSVFolder exists
    os.makedirs(outputCSVFolder, exist_ok=True)

    # Step 1: Convert PLY files to PCD
    print("Converting PLY files to PCD...")
    converted_files = convertPLYtoPCD(plyInputFolder, pcdIntermediateFolder)
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
    dimensions_file = os.path.join(outputCSVFolder, "bounding_box_dimensions.csv")
    angular_velocities_file = os.path.join(outputCSVFolder, "angular_velocities.csv")
    timestamps_file = os.path.join(outputCSVFolder, "timestamps.csv")
    scaled_dimensions_file = os.path.join(outputCSVFolder, "scaled_dimensions_cm.csv")

    # Save bounding box dimensions
    bounding_boxes = results['scaled_bounding_boxes']  # This is an (N, 3) array
    bounding_boxes_df = pd.DataFrame(bounding_boxes, columns=["width", "height", "depth"])
    bounding_boxes_df.to_csv(dimensions_file, index=False)

    # Save timestamps
    timestamps_df = pd.DataFrame({"timestamp": timestamps})
    timestamps_df.to_csv(timestamps_file, index=False)

    # Save scaled dimensions
    scaled_dimensions = np.array(results['scaled_dimensions_cm']).reshape(1, 3)  # Reshape into (1, 3)
    scaled_dimensions_df = pd.DataFrame(scaled_dimensions, columns=["width_cm", "height_cm", "depth_cm"])
    scaled_dimensions_df.to_csv(scaled_dimensions_file, index=False)

    # Save angular velocities
    angular_velocities = results['angular_velocities']
    angular_velocities_df = pd.DataFrame({"angular_velocity": angular_velocities})
    angular_velocities_df.to_csv(angular_velocities_file, index=False)


    # Step 5: Display the animation with additional information
    print("\nStarting point cloud animation...")
    average_rpm = results['rpm']
    scaled_dimensions = results['scaled_dimensions_cm']
    display_time = 0.0333333  # Time in seconds to display each point cloud
    display_pcd_animation(outputPCDFolder, display_time)

    print("\nProcessing complete.")


if __name__ == "__main__":
    main()
