import cv2
import numpy as np
from scipy.spatial.distance import pdist, squareform



def plot_pedestrian_boxes_on_image(frame, pedestrian_boxes):
    frame_h = frame.shape[0]
    frame_w = frame.shape[1]
    thickness = 2
    # color_node = (192, 133, 156)
    color_node = (160, 48, 112)
    # color_10 = (80, 172, 110)

    for i in range(len(pedestrian_boxes)):
        pt1 = (
            int(pedestrian_boxes[i][1] * frame_w),
            int(pedestrian_boxes[i][0] * frame_h),
        )
        pt2 = (
            int(pedestrian_boxes[i][3] * frame_w),
            int(pedestrian_boxes[i][2] * frame_h),
        )

        frame_with_boxes = cv2.rectangle(frame, pt1, pt2, color_node, thickness)


    return frame_with_boxes
