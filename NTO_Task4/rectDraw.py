import cv2


def nott(x):
    pass


img_path = "images/baa25339-ea6f-4e29-a6b7-0acb6c68ca28.jpg"

frame = cv2.imread(img_path)

ESCAPE = 27
im_height = frame.shape[0]
im_width = frame.shape[1]
cv2.namedWindow("result")
cv2.createTrackbar("y", "result", 0, im_height, nott)
cv2.createTrackbar("x", "result", 0, im_width, nott)
cv2.createTrackbar("height", "result", 0, im_height, nott)
cv2.createTrackbar("width", "result", 0, im_width, nott)

while True:
    frame = cv2.imread(img_path)
    # frame = cv2.resize
    # (frame, (frame.shape[1]//2, frame.shape[0]//2))
    x = cv2.getTrackbarPos("x", "result")
    y = cv2.getTrackbarPos("y", "result")
    width = cv2.getTrackbarPos("width", "result")
    height = cv2.getTrackbarPos("height", "result")

    cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(10)
    if key == ESCAPE:
        break


cv2.destroyAllWindows()
