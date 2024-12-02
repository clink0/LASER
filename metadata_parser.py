import os
import numpy as np


def timeStamps(folder_path):
    """
    Extracts metadata from text files in a folder, specifically frame timestamps and counters,
    and ensures they are sorted by frame counter.

    Parameters:
    - folder_path (str): Path to the folder containing metadata text files.

    Returns:
    - np.ndarray: Array of timestamps in seconds, sorted by frame counter.
    """
    numFrames = 300  # Number of frames to process
    x = 0  # Counter Variable

    # Initializing lists to store data
    timestamps = []
    counters = []

    # Loop through all items in the folder
    for filename in os.listdir(folder_path):
        if x >= numFrames:
            break
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            content = file.read()
        lines = content.splitlines()  # Split the content into lines
        timestamp = None
        frame_counter = None
        for line in lines:
            # Extract timestamp from metadata
            if 'Frame Timestamp' in line:
                timeVal = "".join(char for char in line if char.isdigit())
                timestamp = float(timeVal) / 10 ** 6  # Convert from microseconds to seconds
            # Extract frame counter
            if 'Frame Counter' in line:
                frameNum = "".join(char for char in line if char.isdigit())
                frame_counter = int(frameNum)
        if timestamp is not None and frame_counter is not None:
            timestamps.append(timestamp)
            counters.append(frame_counter)
        x += 1  # Iterate through frames

    # Combine timestamps and counters into a structured array
    frame_data = np.array(list(zip(counters, timestamps)), dtype=[('counter', int), ('timestamp', float)])

    # Sort the array by frame counter
    sorted_data = np.sort(frame_data, order='counter')

    # Extract the sorted timestamps
    sorted_timestamps = sorted_data['timestamp']

    # Log unordered frames (optional)
    if not np.all(np.diff(sorted_data['counter']) >= 0):
        print("Warning: Frames were out of order. They have been sorted.")

    return sorted_timestamps