import open3d as o3d


def visualizePointCloud(inputFile):
    """
    Function to visualize a .pcd file in a 3D window.
    """
    print(f"Loading point cloud from '{inputFile}'...")
    # Step 1: Load the point cloud
    pcd = o3d.io.read_point_cloud(inputFile)
    if pcd.is_empty():
        print(f"Error: Failed to load the file '{inputFile}'.")
        return

    print(f"Successfully loaded point cloud with {len(pcd.points)} points.")

    # Step 2: Create a 3D visualization window
    print("Opening 3D visualization window...")
    o3d.visualization.draw_geometries([pcd],
                                      window_name="3D Point Cloud Viewer",
                                      width=1280,
                                      height=720,
                                      left=50,
                                      top=50,
                                      point_show_normal=False)


if __name__ == "__main__":
    # Set the input file path here
    inputFile = ("/Users/lukebray/PycharmProjects/LASER/findDimensions/output/filtered_NEWBG60_311413.10199999995530.pcd")

    # Visualize the point cloud
    visualizePointCloud(inputFile)