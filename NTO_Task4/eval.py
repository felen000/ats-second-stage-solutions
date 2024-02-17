# -*- coding: utf-8 -*-
import sys
import cv2 as cv
import numpy as np

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
    np.set_printoptions(threshold=sys.maxsize)
    img_hls = cv.cvtColor(image, cv.COLOR_BGR2HLS_FULL)
    img_bin = cv.inRange(img_hls, (0, 31, 0), (360, 255, 255))
    print(img_bin)
    # arr = np.sum(image, axis=2)
    arr = img_bin != [255]
    arr = img_bin[arr]
    print(arr)
    # for i in image:
    #   print(i)
    # print(image)
    colors = [2, 3, 4, 5]
    front = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    back = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    img = image
    # cv.imshow('i', img)
    x = 73
    y = 71
    height = 152
    width = 152
    area = width*height
    for i in range(3):
        for j in range(3):
            y0 = y+height*i
            x0 = x+width*j
            cropped = img[y0:y0+height, x0:x0+width]

            img_hls = cv.cvtColor(cropped, cv.COLOR_BGR2HLS_FULL)
            img_bin = cv.inRange(img_hls, (0, 31, 0), (360, 255, 255))
            contours, _ = cv.findContours(
                img_bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            contours = list(filter(lambda cnt: 50000 >
                                   cv.contourArea(cnt) > 200, contours))
            # contours = sorted(contours, key=cv.contourArea, reverse=True)
            # cv.drawContours(cropped, contours, -1, (0, 0, 255), 2)
            # print(len(contours))
            if (len(contours) == 1):
                # img_hls = cv.cvtColor(cropped, cv.COLOR_BGR2HLS_FULL)
                green = cv.inRange(img_hls, (0, 0, 0), (150, 60, 255))
                gray = cv.inRange(img_hls, (0, 0, 0), (360, 70, 70))
                orange = cv.inRange(img_hls, (0, 0, 0), (50, 170, 255))
                red = cv.inRange(img_hls, (200, 0, 0), (360, 170, 255))
                binarys = [red, green, gray, orange]

                green1 = np.sum(green == 255)
                gray1 = np.sum(gray == 255)
                orange1 = np.sum(orange == 255)
                red1 = np.sum(red == 255)
                s = np.array([red1, green1, gray1, orange1])
                index = np.argmax(s)
                if s[index] > 14000:
                    front[i, j] = colors[index]
                else:
                    front[i, j] = 0
                    back[i, j] = 0
            else:
                front[i, j] = 0
                back[i, j] = 0

                for contour in contours:
                    rect = cv.minAreaRect(contour)
                    box = cv.boxPoints(rect)
                    box = np.int0(box)
                    boxX, boxY, boxW, boxH = cv.boundingRect(box)
                    area = cv.contourArea(contour)
                    # cv.drawContours(cropped, [box], 0, (0, 0, 255), 2)
                    img_hls = cv.cvtColor(cropped, cv.COLOR_BGR2HLS_FULL)
                    green = cv.inRange(img_hls, (0, 0, 0), (150, 60, 255))
                    gray = cv.inRange(img_hls, (0, 0, 0), (360, 70, 70))
                    orange = cv.inRange(img_hls, (0, 0, 0), (50, 170, 255))
                    red = cv.inRange(img_hls, (200, 0, 0), (360, 170, 255))
                    binarys = [red, green, gray, orange]

                    green1 = np.sum(green[boxY:boxY+boxH, boxX:boxX+boxW] == 255)
                    gray1 = np.sum(gray[boxY:boxY+boxH, boxX:boxX+boxW] == 255)
                    orange1 = np.sum(orange[boxY:boxY+boxH, boxX:boxX+boxW] == 255)
                    red1 = np.sum(red[boxY:boxY+boxH, boxX:boxX+boxW] == 255)
                    s = np.array([red1, green1, gray1, orange1])
                    index = np.argmax(s)
                    if 9000 < area < 13000:
                        if s[index] > 2000:
                            back[i, j] = colors[index]
                    elif area < 900:
                        binary = binarys[index]
                        changed_bin = np.zeros_like(binary)
                        changed_bin[boxY:boxY+boxH, boxX:boxX+boxW] = 255
                        binary = changed_bin
                        # cv.imshow('bin', binary)
                        # cv.imshow('bin1', binary[:76, :])
                        # cv.imshow('bin2', binary[76:, :])
                        # cv.imshow('bin3', binary[:, :76])
                        # cv.imshow('bin4', binary[:, 76:])
                        sum1 = np.sum(binary[:76, :]) #Верхняя половина изображения
                        sum2 = np.sum(binary[76:, :]) #Нижняя половина изображения
                        sum3 = np.sum(binary[:, :76]) #Левая половина изображения
                        sum4 = np.sum(binary[:, 76:]) #Правая половина изображения
                        ind = np.argmax([sum1, sum2, sum3, sum4])
                        # print(sum1, sum2, sum3, sum4)
                        k, l = 0, 0
                        if ind == 0:
                            l = -1
                        elif ind == 1:
                            l = 1
                        elif ind == 2:
                            k = -1
                        elif ind == 3:
                            k = 1
                        back [i+l, j+k] = colors[index]

                # print(green1, gray1, orange1, red1)



            # cv.imshow('c', cropped)
            # cv.waitKey(0)

    # print(front)
    return np.array([back, front])


if __name__ == "__main__":
    image = cv.imread('images/image.jpg')

    print(count_the_types_of_cubes(image, 1))
