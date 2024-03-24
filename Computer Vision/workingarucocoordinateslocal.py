import numpy as np
import cv2

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

def aruco_display(corners, ids, image):
    if len(corners) > 0:
        for i in range(len(ids)):
            markerID = ids[i][0]  
            markerCorner = corners[i][0]

            if len(markerCorner) == 4:
                cX = int(np.mean(markerCorner[:, 0]))
                cY = int(np.mean(markerCorner[:, 1]))
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                
                cv2.putText(image, "Coordinate: ({}, {})".format(cX, cY), (cX, cY - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image

def main():
    aruco_type = "DICT_5X5_1000"
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])
    arucoParams = cv2.aruco.DetectorParameters_create()
    arucoParams.adaptiveThreshWinSizeMin = 10
    arucoParams.adaptiveThreshWinSizeMax = 30
    arucoParams.adaptiveThreshConstant = 7

    image_path = r"C:\Users\Dell\Desktop\innovation lab\ArucoMarkers\demo.png"
    img = cv2.imread(image_path)

    h, w, _ = img.shape
    width = 1000
    height = int(width * (h / w))
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    corners, ids, _ = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

    if ids is not None and len(ids) > 0:
        detected_markers = aruco_display(corners, ids, img)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  
        cv2.imshow("Image", detected_markers)
        cv2.resizeWindow("Image", width, height)  
        cv2.waitKey(0)
    else:
        print("No ArUco markers detected.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()