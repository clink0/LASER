import open3d as o3d
import os
import time


def display_pcd_animation(pcd_folder, display_time=0.5):
    """
    Displays an animation of .pcd files from a folder.

    Parameters:
    - pcd_folder (str): Path to the folder containing .pcd files.
    - display_time (float): Time in seconds to display each .pcd file.
    """
    # List all .pcd files in the folder
    pcd_files = [os.path.join(pcd_folder, f) for f in os.listdir(pcd_folder) if f.endswith('.pcd')]
    pcd_files.sort()  # Sort files to maintain sequential order

    if not pcd_files:
        print(f"No .pcd files found in the folder: {pcd_folder}")
        return

    print(f"Found {len(pcd_files)} .pcd files. Starting animation...")

    # Create a visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="PCD Animation", width=800, height=600)

    for i, pcd_file in enumerate(pcd_files):
        print(f"Displaying file {i + 1}/{len(pcd_files)}: {pcd_file}")

        # Load the point cloud
        pcd = o3d.io.read_point_cloud(pcd_file)
        if pcd.is_empty():
            print(f"Warning: {pcd_file} is empty or invalid. Skipping.")
            continue

        # Add the point cloud to the visualizer
        vis.clear_geometries()
        vis.add_geometry(pcd)

        # Update the visualizer
        vis.poll_events()
        vis.update_renderer()

        # Wait for the specified time
        time.sleep(display_time)

    print("Animation complete. Closing visualizer.")
    vis.destroy_window()


if __name__ == "__main__":
    # Replace with your folder containing .pcd files
    pcd_folder = "/Users/lukebray/PycharmProjects/LASER2/OutputPCD/Test_1"
    display_time = 0.02  # Time in seconds to display each point cloud

    display_pcd_animation(pcd_folder, display_time)