# MetaData Extractor
# The file takes in text files, specifically from a Realsense L515 Cam
# and extractors the metadata which includes the frame number, and timestamps in micro seconds
import os
import numpy as np
import re

def timeStamps(folder_path):
    def extract_number(filename):
        # Adjust the regex to capture the numeric part after '_metadata_'
        match = re.search(r'_metadata_(\d+\.\d+)', filename)
        return float(match.group(1)) if match else float('inf')  # Use a high value for files without numbers
    # Enter folder path that contains Metadata.
    # Get all files in the folder
    numFrames = 4000  # Number of frames user wants to check
    x = 0  # Counter Varible
    # Intializing needed arrays to store data
    timeStamps, counter = np.zeros(numFrames), np.zeros(numFrames)
    # Loop through all items in the folder
    sortedFiles = sorted(os.listdir(folder_path), key=extract_number)
    for filename in sortedFiles:
        if filename.startswith("._"):
            continue
        if x >= numFrames:
            break
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            content = file.read()
        lines = content.splitlines()  # Split the content into lines
        for line in lines:
            # Extracts Given timestamp from metaData
            if 'Frame Timestamp' in line:
                timeVal = ""
                for char in line:
                    if char.isdigit():
                        timeVal += char
                time_Val = float(timeVal) / 10 ** 6  # Converting TimeStamp from micro seconds to seconds
                timeStamps[x] = time_Val
            # Extracts Frame Number
            if 'Frame Counter' in line:
                frameNum = ""
                for char in line:
                    if char.isdigit():
                        frameNum += char
                frame_Num = float(frameNum)
                counter[x] = frame_Num
                if (x != 0) and not (counter[x] >= counter[x - 1]):
                    # Checks if frames are in order
                    raise SystemExit("ERROR: FRAMES OUT OF ORDER")
        x += 1  # Iterate through frames
    return timeStamps
