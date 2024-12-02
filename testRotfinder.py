from scipy.signal import find_peaks
import numpy as np

from metadata_parser import timeStamps


def rotfinder(area, timeStamp):
    areas = np.load(area)
    timeStamps = np.load(timeStamp)
    x = np.linspace(0, len(areas))
    # Find local maxima
    maxs, _ = find_peaks(areas)
    max_locations = [(x[i], areas[i]) for i in maxs]
    # Find local minima by inverting the data
    mins, _ = find_peaks(-areas)
    min_locations = [(x[i], areas[i]) for i in mins]
    minArr = np.zeros(int(len(timeStamps)))
    maxArr = np.zeros(int(len(timeStamps)))

    for ts in range(0,len(max_locations)):
        if ts >= len(max_locations)-1:
            break
        diffM = timeStamps[max_locations[ts+1]] - timeStamps[max_locations[ts]]
        maxArr = np.append(maxArr, diffM)
        diffm = timeStamps[min_locations[ts+1]] - timeStamps[min_locations[ts]]
        minArr = np.append(minArr, diffm)

    aveMaxDiff = np.average(maxArr)
    aveMinDiff = np.average(minArr)
    aveTimeDiff = (aveMaxDiff + aveMinDiff) / 2  # Combing the averages
    rpm = (1 / (2 * aveTimeDiff)) * 60  # Converting to Rotations per minute
    return rpm

