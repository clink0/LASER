
import pcdTo2D
import isolateBackground
from cleanupData import metaDataExtractor as meta
import os
import numpy as np

def calRotationMagnitude(folder_path,timeStamps):
    # Calculates the magnitude of the rotation of an object
    x = 0
    whiteSpace = np.zeros(len(timeStamps)) # Array of the white space amount for the area of each frame
    for filename in os.listdir(folder_path):
        if filename.startswith("._"):
            continue
        if x >= len(timeStamps):
            break
        file_path = os.path.join(folder_path, filename)
        whiteSpace[x] = pcdTo2D.pcd2dWhitespace(isolateBackground.findWhiteSpace(file_path))
        # finding area of white pixels for each frame
        x += 1  # Iterate through frames
    # Initalizing Arrays for local mins and maxs
    minArr = np.zeros(int(len(timeStamps)))
    maxArr = np.zeros(int(len(timeStamps)))
    # Finding local mins and maxs
    for w in range(0, len(whiteSpace) - 1):
        if w >= len(whiteSpace) - 1:
            break
        # Local maxs
        if whiteSpace[w] > whiteSpace[w - 1] and whiteSpace[w] > whiteSpace[w + 1] and whiteSpace[w] > whiteSpace[
            w - 2] and whiteSpace[w] > whiteSpace[w + 2]:
            maxArr[w] = whiteSpace[w]
            continue
        # Local Mins
        if (whiteSpace[w] < whiteSpace[w - 1]) and (whiteSpace[w] < whiteSpace[w + 1]) and (
                whiteSpace[w] < whiteSpace[w - 2]) and (whiteSpace[w] < whiteSpace[w + 2]):
            minArr[w] = whiteSpace[w]
    maxAve = np.zeros(0)
    minAve = np.zeros(0)
    prevValM, prevValm = 0, 0
    for y in range(0, len(maxArr) - 1):
        # Finding the average change from min to min and from max to max
        if maxArr[y] != 0:
            currentValM = y
            if prevValM != 0:
                diffM = timeStamps[currentValM] - timeStamps[prevValM]
                maxAve = np.append(maxAve, diffM)
            prevValM = y
        if minArr[y] != 0:
            currentValm = y
            if prevValm != 0:
                diffm = timeStamps[currentValm] - timeStamps[prevValm]
                minAve = np.append(minAve, diffm)
            prevValm = y
    aveMaxDiff = np.average(maxAve)
    aveMinDiff = np.average(minAve)
    aveTimeDiff = (aveMaxDiff + aveMinDiff) / 2 # Combing the averages
    rpm = (1 / (2 * aveTimeDiff)) * 60 # Converting to Rotations per minute
    return rpm

calRotationMagnitude(r'C:\Users\olson\Documents\Location\lukeFixedData',meta.timeStamps(r'C:\Users\olson\Documents\Location\NewBG60\txt_files'))