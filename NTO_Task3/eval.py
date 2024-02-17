# -*- coding: utf-8 -*-
import cv2
import numpy as np
# TODO: Допишите импорт библиотек, которые собираетесь использовать


def load_tools():
    """
        Функция осуществляет загрузку модели(ей) нейросети(ей) из файла(ов).
        Выходные параметры: загруженный(е) модели(и)

        Если вы не собираетесь использовать эту функцию, пусть возвращает пустой список []
        Если вы используете несколько моделей, возвращайте их список [tool1, tool2]

        То, что вы вернёте из этой функции, будет передано вторым аргументом в функцию track_movement
    """

    # TODO: Отредактируйте функцию по своему усмотрению.
    # Модель нейронной сети, загрузите на онайн-платформу вместе с eval.py.

    # Пример загрузки моделей из файлов
    # Yolo-модели
    # net = cv2.dnn.readNetFromDarknet('yolo.cfg', 'yolo.weights')
    # yolo_model = cv2.dnn_DetectionModel(net)
    # yolo_model.setInputParams(scale=1/255, size=(416, 416), swapRB=True)
    # tools = [yolo_model]

    # Пример загрузки модели TensorFlow (не забудьте импортировать библиотеку tensorflow)
    # tf_model = tf.keras.models.load_model('model.h5')
    # tools.append(tf_model)

    tools = []
    return tools


def track_movement(video, tools) -> int:
    """
        Функция для трекинга автомобился.

        Входные данные: видео-объект (cv2.VideoCapture)
        Выходные данные: матрицу смежности графа в виде numpy массива (dtype=np.uint8)


        Примеры вывода:
            [[0, 0, 0, 1, 0],
             [0, 0, 1, 0, 0],
             [1, 0, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0]]
    """

    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки один раз вызовет функцию load_tools
    # и для каждого тестового изображения будет вызывать функцию track_movement
    # Все остальные функции должны вызываться из вышеперечисленных.

    result = np.array([[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]], dtype=np.uint8)

    way = []
    last = -1
    while True:
        status, frame = video.read()
        if status == False:
            print("Have't frame1")
            break
        else:
            frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            binary = cv2.inRange(hsv, (0, 5, 20), (255, 255, 255))
            c1 = binary[19:121, 119:317]
            c2 = binary[96:312, 0:120]
            c3 = binary[120:296, 120:312]
            c4 = binary[120:296, 312:428]
            c5 = binary[296:408, 120:319]
            crops = [c1, c2, c3, c4, c5]

            for i in range(len(crops)):
                if crops[i].sum() > 50000:
                    if last != i:
                        way.append(i)
                        last = i

    way = way[1:]
    for i in range(len(way) - 1):
        result[way[i], way[i+1]] = result[way[i], way[i+1]] + 1

    return result
