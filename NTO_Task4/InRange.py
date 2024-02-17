import cv2


def nott(x):
    pass


frame = cv2.imread('images/4a7fc809-1de8-4de9-bc0b-90bb6300c752.jpg')
ESCAPE = 27

cv2.namedWindow("result")
cv2.createTrackbar("minB", "result", 0, 255, nott)
cv2.createTrackbar("minG", "result", 0, 255, nott)
cv2.createTrackbar("minR", "result", 0, 255, nott)
cv2.createTrackbar("maxB", "result", 0, 255, nott)
cv2.createTrackbar("maxG", "result", 0, 255, nott)
cv2.createTrackbar("maxR", "result", 0, 255, nott)

while True:

    cv2.imshow("Frame", frame)
    minb = cv2.getTrackbarPos("minB", "result")
    ming = cv2.getTrackbarPos("minG", "result")
    minr = cv2.getTrackbarPos("minR", "result")
    maxb = cv2.getTrackbarPos("maxB", "result")
    maxg = cv2.getTrackbarPos("maxG", "result")
    maxr = cv2.getTrackbarPos("maxR", "result")

    binary = cv2.inRange(frame, (minb, ming, minr), (maxb, maxg, maxr))

    result = cv2.bitwise_and(frame, frame, mask=binary)

    cv2.imshow("Binary", binary)
    cv2.imshow("result", result)
    print(binary)

    key = cv2.waitKey(10)
    if key == ESCAPE:
        break


cv2.destroyAllWindows()
