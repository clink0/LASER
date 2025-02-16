import numpy as np

def calculateBoundingBoxDimensions(pointCloud):
    """
    Calculates the dimensions of the oriented bounding box around the given point cloud.
    Returns the bounding box and its dimensions.
    """
    if pointCloud.is_empty():
        print("Error: Point cloud is empty.")
        return None, None

    bbox = pointCloud.get_oriented_bounding_box()
    bboxSize = np.array(bbox.extent)  # Extent gives the length, width, and height of the OBB
    return bbox, bboxSize
