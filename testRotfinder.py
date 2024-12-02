from scipy.signal import find_peaks
import numpy as np


def rotfinder(area, timeStamp):
    areas = np.load(area)
    timeStamps = np.load(timeStamp)
    x = np.linspace(0, len(areas), len(areas))

    # Find local maxima
    maxs, _ = find_peaks(areas)
    max_locations = [(x[i], areas[i]) for i in maxs if i > 0 and i < len(areas)]

    # Find local minima by inverting the data
    mins, _ = find_peaks(-areas)
    min_locations = [(x[i], areas[i]) for i in mins if i > 0 and i < len(areas)]

    minArr = []
    maxArr = []

    for ts in range(0, len(max_locations) - 1):
        diffM = timeStamps[maxs[ts + 1]] - timeStamps[maxs[ts]]
        maxArr.append(diffM)

    for ts in range(0, len(min_locations) - 1):
        diffm = timeStamps[mins[ts + 1]] - timeStamps[mins[ts]]
        minArr.append(diffm)

    aveMaxDiff = np.average(maxArr) if maxArr else 0
    aveMinDiff = np.average(minArr) if minArr else 0
    aveTimeDiff = (aveMaxDiff + aveMinDiff) / 2 if (aveMaxDiff + aveMinDiff) > 0 else 0

    if aveTimeDiff == 0:
        return 0  # Avoid division by zero

    rpm = (1 / (2 * aveTimeDiff)) * 60  # Converting to Rotations per minute
    return rpm
