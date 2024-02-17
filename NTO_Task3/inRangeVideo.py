import cv2


def nott(x):
    pass


video_path1 = "videos/88c81ff7-9c48-4826-811b-e9d02f5fcc10.mp4"
video_path2 = "Ped.mp4"
cam1 = cv2.VideoCapture(video_path1)
# cam2 = cv2.VideoCapture(video_path2)

ESCAPE = 27

cv2.namedWindow("result")
cv2.createTrackbar("minB", "result", 0, 255, nott)
cv2.createTrackbar("minG", "result", 0, 255, nott)
cv2.createTrackbar("minR", "result", 0, 255, nott)
cv2.createTrackbar("maxB", "result", 0, 255, nott)
cv2.createTrackbar("maxG", "result", 0, 255, nott)
cv2.createTrackbar("maxR", "result", 0, 255, nott)

while True:
    status, frame = cam1.read()
    # status2, frame2 = cam2.read()
    if status == False:
        print("Have't frame1")
        cam1.release()
        cam1 = cv2.VideoCapture(video_path1)
    # elif status2 == False:
    #     print("Have't frame2")
    #     cam2.release()
    #     cam2 = cv2.VideoCapture(video_path2)
    else:
        # frame = cv2.imread("Ped.jpg")  # DEL
        frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))

        # frame2 = cv2.resize(frame2, (frame2.shape[1] // 3, frame2.shape[0] // 3))
        cv2.imshow("Frame", frame)
        # cv2.imshow("Frame2", frame2)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        minb = cv2.getTrackbarPos("minB", "result")
        ming = cv2.getTrackbarPos("minG", "result")
        minr = cv2.getTrackbarPos("minR", "result")
        maxb = cv2.getTrackbarPos("maxB", "result")
        maxg = cv2.getTrackbarPos("maxG", "result")
        maxr = cv2.getTrackbarPos("maxR", "result")

        binary = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))
        # binary2 = cv2.inRange(frame2, (minb, ming, minr), (maxb, maxg, maxr))

        result = cv2.bitwise_and(frame, frame, mask=binary)
        # result2 = cv2.bitwise_and(frame2, frame2, mask=binary2)

        cv2.imshow("Binary", binary)
        cv2.imshow("result", result)
        # cv2.imshow("Binary2", binary2)
        # cv2.imshow("result2", result2)

        key = cv2.waitKey(10)
        if key == ESCAPE:
            break

cam1.release()
# cam2.release()
cv2.destroyAllWindows()
