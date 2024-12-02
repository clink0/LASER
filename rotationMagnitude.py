import numpy as np


def calRotationMagnitude(area,timeStamp):
    # Calculates the magnitude of the rotation of an object
    areas = np.load(area)
    timeStamps = np.load(timeStamp)
    idelChecker = 0
    # Initalizing Arrays for local mins and maxs
    minArr = np.zeros(int(len(timeStamps)))
    maxArr = np.zeros(int(len(timeStamps)))
    areaVar = .01
    # Finding local mins and maxs
    for w in range(0, len(areas) - 2):
        if w >= len(areas) - 2:
            break

        if (areas[w]+areaVar <= areas[w + 1]  and areas[w]+areaVar <= areas[w - 1])  or (areas[w]-areaVar >= areas[w + 1]  and areas[w]-areaVar >= areas[w - 1]) :
            idelChecker += 1
        else:
            idelChecker = 0
        if idelChecker >= 5:
            return 0
        #Local maxs
        if areas[w] > areas[w - 1] and areas[w] > areas[w + 1] and areas[w] > areas[
            w - 2] and areas[w] > areas[w + 2]:
            maxArr[w] = areas[w]
            continue
        # Local Mins
        if (areas[w] < areas[w - 1]) and (areas[w] < areas[w + 1]) and (
                areas[w] < areas[w - 2]) and (areas[w] < areas[w + 2]):
            minArr[w] = areas[w]
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