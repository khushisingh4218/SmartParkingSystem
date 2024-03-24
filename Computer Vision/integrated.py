import numpy as np
import time
import cv2
from datetime import datetime

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

def aruco_display(corners, ids, image, slot_timers, slot_occupancy, slot_records, final_time_list):
    if len(corners) > 0:
        slots = [0] * 5  # Initialize slots for different X-coordinate ranges
        slot_ranges = [(100, 200), (201, 300), (301, 400), (401, 500), (501, 600)]

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            # Convert coordinates to integers
            topLeft = tuple(map(int, topLeft))
            topRight = tuple(map(int, topRight))
            bottomRight = tuple(map(int, bottomRight))
            bottomLeft = tuple(map(int, bottomLeft))

            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
            cv2.putText(image, str(markerID), topLeft, cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

            # Update slots based on marker IDs
            if markerID == 1:
                slot_index = 0
            elif markerID == 2:
                slot_index = 1
            elif markerID == 3:
                slot_index = 2
            elif markerID == 4:
                slot_index = 3
            elif markerID == 5:
                slot_index = 4

            else:
                slot_index = -1

            if slot_index != -1:
                if slot_timers[slot_index] is None:
                    slot_timers[slot_index] = time.time()  # Start timer when a tag enters the slot
                    slot_occupancy[slot_index] = "Occupied"
                else:
                    slots[slot_index] = time.time() - slot_timers[slot_index]  # Calculate total time in the slot
            else:
                # Reset the slot timer if the tag leaves the slot or has an unsupported ID
                slot_timers[slot_index] = None
                slot_occupancy[slot_index] = "Not Occupied"

        return image, slots, slot_occupancy
    else:
        return image, None, None


