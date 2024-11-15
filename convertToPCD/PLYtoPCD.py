import open3d as o3d
import os


def convert_ply_to_pcd(input_folder, output_folder):
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".ply"):
            input_file = os.path.join(input_folder, filename)

            # Load the PLY file
            pcd = o3d.io.read_point_cloud(input_file)
            if not pcd:
                print(f"Failed to read the file: {input_file}")
                continue

            # Extract the base file name without the extension
            base_name = os.path.splitext(filename)[0]

            # Set the output file path in the output folder with .pcd extension
            output_file = os.path.join(output_folder, f"{base_name}.pcd")

            # Save the point cloud as a .pcd file
            o3d.io.write_point_cloud(output_file, pcd)
            print(f"Converted {input_file} to {output_file}")

    print(f"Conversion completed! All files saved in {output_folder}")


# Example usage
input_folder = "/Users/lukebray/PycharmProjects/LASER/convertToPCD/inputPLY"  # Specify your input folder containing .ply files
output_folder = "/Users/lukebray/PycharmProjects/LASER/convertToPCD/outputPCD"  # Specify your desired output folder for .pcd files

convert_ply_to_pcd(input_folder, output_folder)
