
import pcdTo2D
import isolateBackground
import os
import numpy as np

def calRotationMagnitude(folder_path,timeStamps):
    x = 0
    whiteSpace = np.zeros(len(timeStamps))
    for filename in os.listdir(folder_path):
        if x >= len(timeStamps):
            break
        file_path = os.path.join(folder_path, filename)
        whiteSpace[x] = pcdTo2D.pcd2dWhitespace(isolateBackground.findWhiteSpace(file_path))
        x += 1  # Iterate through frames
    minArr = np.zeros(int(len(timeStamps)))
    maxArr = np.zeros(int(len(timeStamps)))
    for w in range(0, len(whiteSpace) - 1):
        if x >= len(whiteSpace) - 1:
            break
        if whiteSpace[w] > whiteSpace[w - 1] and whiteSpace[w] > whiteSpace[w + 1] and whiteSpace[w] > whiteSpace[
            w - 2] and whiteSpace[w] > whiteSpace[w + 2]:
            maxArr[w] = whiteSpace[w]
            continue
        if (whiteSpace[w] < whiteSpace[w - 1]) and (whiteSpace[w] < whiteSpace[w + 1]) and (
                whiteSpace[w] < whiteSpace[w - 2]) and (whiteSpace[w] < whiteSpace[w + 2]):
            minArr[w] = whiteSpace[w]
    maxAve = np.zeros(0)
    minAve = np.zeros(0)
    prevValM, prevValm = 0, 0
    for y in range(0, len(maxArr) - 1):
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
    aveTimeDiff = (aveMaxDiff + aveMinDiff) / 2
    rpm = (1 / (2 * aveTimeDiff)) * 60
    return rpm