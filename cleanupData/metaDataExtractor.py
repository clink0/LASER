# MetaData Extractor
# The file takes in text files, specifically from a Realsense L515 Cam
# and extractors the metadata which includes the frame number, and timestamps in micro seconds
import os
import numpy as np

folder_path = r"C:\Users\olson\Documents\Location\metaDataTest" # NOTE make a folder that only contains the metaData files
                 # Enter folder path that contains Metadata.
numFrames = 300 # Number of frames user wants to check
x = 0 # Counter Varible
#Intializing needed arrays to store data
timeStamps, counter, framesPerSec = np.zeros(numFrames), np.zeros(numFrames), np.zeros(numFrames-2)

        # Loop through all items in the folder
for filename in os.listdir(folder_path):
    if x >= numFrames:
        break
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r') as file:
        content = file.read()
    lines = content.splitlines()  # Split the content into lines
    for line in lines:
        #Extracts Given timestamp from metaData
        if 'Frame Timestamp' in line:
            timeVal = ""
            for char in line:
                if char.isdigit():
                    timeVal += char
            time_Val = float(timeVal)/10**6 # Converting TimeStamp from micro seconds to seconds
            timeStamps[x] = time_Val
        #Extracts Frame Number
        if 'Frame Counter' in line:
            frameNum = ""
            for char in line:
                if char.isdigit():
                    frameNum += char
            frame_Num = float(frameNum)
            counter[x] = frame_Num
            if (x != 0 ) and not(counter[x] >= counter[x-1]):
            # Checks if frames are in order
                raise SystemExit("ERROR: FRAMES OUT OF ORDER")
    x += 1 # Iterate through frames
x = 0 # Iterator
for x in range(0,numFrames-2):
    framesPerSec[x] = (counter[x+1] - counter[x])/(timeStamps[x+1] - timeStamps[x])
    print(framesPerSec[x])
    x += 1 # Iterate through frames