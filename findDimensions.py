import open3d as o3d

# Function to convert PLY to PCD
def convert_ply_to_pcd(input_file, output_file):
    # Load the PLY file
    pcd = o3d.io.read_point_cloud(input_file)
    if not pcd:
        print("Failed to read the input file.")
        return

    print(f"Loaded {input_file}, containing {len(pcd.points)} points")

    # Save the point cloud as PCD
    o3d.io.write_point_cloud(output_file, pcd)
    print(f"Converted and saved to {output_file}")


# Example usage
input_file = "input.ply"
output_file = "output.pcd"
convert_ply_to_pcd(input_file, output_file)
