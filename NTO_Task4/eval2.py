# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


def opred(green1, gray1, orange1, red1):
    return [0, 0, 0]


def load_tools() -> list:
    tools = []
    return tools


def count_the_types_of_cubes(image, tools) -> np.array:
    """
        Функция для детектирования сфетофоров.

        Входные данные: изображение (bgr), прочитано cv2.imread и список из функции load_tools
        Выходные данные: np.array размерности 3х3х2 с элементами типа int.
            Значения элементов определяют тип кубика на изображении.
            Возможные значения:
                0 - позиция пуста,
                1 - невидимый кубик,
                2 - красный кубик,
                3 - зелёный кубик,
                4 - серый кубик,
                5 - оранжевый кубик.


        Примеры вывода:
            [[[4, 1, 1], [0, 1, 1], [2, 0, 5]], [[5, 5, 4], [0, 5, 3], [2, 0, 0]]]

            [[[3, 1, 1], [3, 4, 1], [5, 1, 1]], [[0, 5, 4], [0, 0, 4], [0, 4, 5]]]
    """
    toolsv = tools
    otvet = []
    img = image
    iss = image
    kernel = np.ones((3, 3), np.uint8)
    iss = cv.medianBlur(iss, 3)  # ggggg
    img_gray = cv.cvtColor(iss, cv.COLOR_BGR2HLS_FULL)
    img_bin = cv.inRange(img_gray, (0, 31, 0), (360, 255, 255))
    # iss = cv.medianBlur(iss, 5)
    # canny = cv.Canny(iss, 10, 250)
    # dil = cv.dilate(img_bin, np.ones((3, 3)), iterations=1)
    opening = cv.morphologyEx(img_bin, cv.MORPH_OPEN, kernel)
    # contours, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    contours, _ = cv.findContours(
        img_bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    contours = list(filter(lambda cnt: 50000 >
                    cv.contourArea(cnt) > 200, contours))

    # cv.drawContours(img, contours, -1, (0, 255, 255), 3) # always commenting
    cv.imshow('SSSvSS', img_bin)
    cv.imshow('SSSv', img)
    # cv.waitKey(0)
    # return 0
    for contour in contours:
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        print(cv.contourArea(contour))
        cv.drawContours(iss, [box], 0, (0, 0, 255), 2)
        x, y, w, h = cv.boundingRect(box)
        cv.rectangle(iss, (x, y), (x+w, y+h), (0, 255, 0), 2)
        box1 = box[0]
        box2 = box[1]
        box3 = box[2]
        box4 = box[3]
        cv.imshow('gvs', iss)
        imge = img[y:y+h, x:x+w]
        # down_width = 150
        # down_height = 150
        # down_points = (down_width, down_height)
        resized_down = imge
        # resized_down = cv.resize(imge, down_points, interpolation=cv.INTER_LINEAR)
        imgss = cv.cvtColor(resized_down, cv.COLOR_BGR2HLS_FULL)
        green = cv.inRange(imgss, (0, 0, 0), (150, 60, 255))
        gray = cv.inRange(imgss, (0, 0, 0), (360, 70, 70))
        orange = cv.inRange(imgss, (0, 0, 0), (50, 170, 255))
        red = cv.inRange(imgss, (200, 0, 0), (360, 170, 255))
        cv.imshow('res', resized_down)

        cv.imshow('green', green)
        cv.imshow('gray', gray)
        cv.imshow('orange', orange)
        cv.imshow('red', red)
        green1 = np.sum(green == 255)
        gray1 = np.sum(gray == 255)
        orange1 = np.sum(orange == 255)
        red1 = np.sum(red == 255)
        cv.waitKey(0)
        otvet.append(opred(green1, gray1, orange1, red1))

    result = np.array([otvet])
    # result = np.array([
    # [[4, 1, 1], [0, 1, 1], [2, 0, 5]], [[5, 5, 4], [0, 5, 3], [2, 0, 0]]
    # ])

    return result


if __name__ == "__main__":
    image = cv.imread('images/image.jpg')

    print(count_the_types_of_cubes(image, 1))
