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


# changed format to calulate hourly_Slot_Set
def merge_time_periods(time_list):
    if not time_list:
        return []

    merged = [time_list[0]]
    for current in time_list[1:]:
        last = merged[-1]
        if last[1] == current[0]:
            merged[-1] = (last[0], current[1])  # merge with last period
        else:
            merged.append(current)  # start a new period

    return merged


def aruco_display(corners, ids, image, slot_timers, slot_occupancy, slot_records, final_time_list, slot_counters, hourly_slot_sets):
    if len(corners) > 0:
        slots = [0] * 5  # Initialize slots for different X-coordinate ranges

        current_time = datetime.now()

        for slot_index in range(5):
            if slot_timers[slot_index] is not None and (current_time - slot_timers[slot_index]).total_seconds() >= 5:
                # Slot was occupied for more than 5 seconds, record exit time and update status
                exit_time = current_time
                slot_records[slot_index].append(
                    (slot_timers[slot_index], exit_time))
                final_time_list[slot_index].append(
                    # Update final time list
                    (slot_timers[slot_index], exit_time))

                slot_occupancy[slot_index] = "Not Occupied"
                slot_timers[slot_index] = None

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
            slot_index = markerID[0] - 1  # Slot index is 0-based

            if 0 <= slot_index < 5:
                if slot_timers[slot_index] is None and slot_occupancy[slot_index] == "Not Occupied":
                    # Slot was unoccupied and is now occupied, record entry time
                    slot_timers[slot_index] = current_time
                    slot_occupancy[slot_index] = "Occupied"
                    slot_counters[slot_index] += 1  # Increment the counter
                elif slot_timers[slot_index] is not None and (current_time - slot_timers[slot_index]).total_seconds() >= 5:
                    # Slot was occupied for more than 5 seconds, record exit time and update status
                    exit_time = current_time
                    slot_records[slot_index].append((slot_timers[slot_index], exit_time))
                    final_time_list[slot_index].append(
                        (slot_timers[slot_index], exit_time))  # Update final time list


                    slot_occupancy[slot_index] = "Not Occupied"
                    slot_timers[slot_index] = None

        return image, slots, slot_occupancy, final_time_list, hourly_slot_sets
    else:
        current_time = datetime.now()
        for slot_index in range(5):
            if slot_timers[slot_index] is not None and (current_time - slot_timers[slot_index]).total_seconds() >= 5:
                # Slot was occupied for more than 5 seconds, record exit time and update status
                exit_time = current_time
                slot_records[slot_index].append(
                    (slot_timers[slot_index], exit_time))
                final_time_list[slot_index].append(
                    # Update final time list
                    (slot_timers[slot_index], exit_time))

                slot_occupancy[slot_index] = "Not Occupied"
                slot_timers[slot_index] = None

        return image, None, None, final_time_list, hourly_slot_sets


aruco_type = "DICT_4X4_250"
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])
arucoParams = cv2.aruco.DetectorParameters_create()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

slot_timers = [None] * 5  # Initialize slot timers
slot_occupancy = ["Not Occupied"] * 5  # Initialize slot occupancy status
slot_records = [[] for _ in range(5)]  # Initialize slot_records list
# Initialize final time list for each slot
final_time_list = [[] for _ in range(5)]
slots = [0] * 5
slot_counters = [0] * 5
# Initialize hourly slot sets for each slot
hourly_slot_sets = [[] for _ in range(5)]


start_time = time.time()
slot_reset_interval = 5     # Reset slots after 5 seconds of inactivity
print_interval = 10         # Print slot contents every 10 seconds
last_print_time = start_time

while cap.isOpened():
    ret, img = cap.read()
    h, w, _ = img.shape
    width = 1000
    height = int(width * (h / w))
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    corners, ids, _ = cv2.aruco.detectMarkers(
        img, arucoDict, parameters=arucoParams)

    if len(corners) > 0:
        detected_markers, updated_slots, updated_occupancy, final_time_list, hourly_slot_sets = aruco_display(
            # Pass slot_counters and hourly_slot_sets as arguments
            corners, ids, img, slot_timers, slot_occupancy, slot_records, final_time_list, slot_counters, hourly_slot_sets)
        if updated_slots is not None:
            slots = updated_slots
            slot_occupancy = updated_occupancy
        cv2.imshow("Image", detected_markers)
    else:
        cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    current_time = time.time()

    if current_time - last_print_time >= print_interval:
        last_print_time = current_time
        print("Slot contents after {} seconds:".format(print_interval))
        for i in range(5):
            merged_time_list = merge_time_periods([(entry.strftime(
                '%Y-%m-%d %H:%M:%S'), exit.strftime('%Y-%m-%d %H:%M:%S')) for entry, exit in final_time_list[i]])
            slot_counters[i] = len(merged_time_list)  # Update the slot counter



            if len(merged_time_list) > 0:
                if len(merged_time_list) != len(hourly_slot_sets[i]):
                    # If size has changed, append a new set from the last interval
                    last_interval = merged_time_list[-1]
                    start_hour = datetime.strptime(last_interval[0], '%Y-%m-%d %H:%M:%S').hour
                    end_hour = datetime.strptime(last_interval[1], '%Y-%m-%d %H:%M:%S').hour + 1
                    hours_in_last_interval = list(range(start_hour, end_hour))
                    # Exclude the last hour if the minute is 00 for the end hour
                    if datetime.strptime(last_interval[1], '%Y-%m-%d %H:%M:%S').minute == 0:
                        hours_in_last_interval = hours_in_last_interval[:-1]

                    hourly_slot_sets[i].append(set(hours_in_last_interval))
                else:
                    # If size has not changed, recalculate set for the last interval
                    last_interval = merged_time_list[-1]
                    start_hour = datetime.strptime(last_interval[0], '%Y-%m-%d %H:%M:%S').hour
                    end_hour = datetime.strptime(last_interval[1], '%Y-%m-%d %H:%M:%S').hour + 1
                    hours_in_last_interval = list(range(start_hour, end_hour))
                    # Exclude the last hour if the minute is 00 for the end hour
                    if datetime.strptime(last_interval[1], '%Y-%m-%d %H:%M:%S').minute == 0:
                        hours_in_last_interval = hours_in_last_interval[:-1]

                    # Update the last set in the hourly_slot_sets
                    hourly_slot_sets[i][-1] = set(hours_in_last_interval)




            # Print the updated slot counter
            # Print the updated slot counter and occupancy
            print(f"Slot {i + 1} Counter:", slot_counters[i])
            print(f"Slot {i + 1} Occupancy:", slot_occupancy[i])

            # Print the hourly slot set for the current slot
            print(f"Slot {i + 1} Hourly Set:", hourly_slot_sets[i])

            # print("In and Out Info for Slot {}: {}".format(
            #     i + 1, slot_records[i]))
            print("Final Time List for Slot {}: {}".format(
                i + 1, merged_time_list))

        print("\n")

cv2.destroyAllWindows()
cap.release()
