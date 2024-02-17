# -*- coding: utf-8 -*-
from typing import Tuple
import cv2
import numpy as np
# TODO: Допишите импорт библиотек, которые собираетесь использовать


def load_models():
    net = cv2.dnn.readNetFromDarknet(
        'weigh/yolov4-tiny-obj-test.cfg', 'weigh/yolov4-tiny-obj_best.weights')
    modelsv = cv2.dnn_DetectionModel(net)
    modelsv.setInputParams(scale=1/255, size=(416, 416), swapRB=True)

    models = [modelsv]
    return models


def count_vehicles(video, models) -> int:  # добавить models перед сдачей
    past = []
    count = 0
    first = True
    modelsv = models[0]

    Conf_threshold = 0.5
    NMS_threshold = 0.5

    with open('weigh/obj.names', 'r') as f:
        classes_list = f.read().split('\n')
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        classes, scores, boxes = modelsv.detect(
            frame, Conf_threshold, NMS_threshold)
        if first:
            count = len(boxes)
            # print(count)
            first = False
        else:
            for box in boxes:
                new = True
                x1, y1, width1, height1 = box
                x1 = x1 + width1 // 2
                y1 = y1 + height1 // 2
                for p_box in past:
                    x2, y2, width2, height2 = p_box
                    x2 = x2 + width2 // 2
                    y2 = y2 + height2 // 2
                    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    # dists.append(dist)
                    if dist <= 260:
                        new = False
                        break
                if new:
                    count += 1
                # if count > 4:
                    # print(dists)
            # print(dists)
        if len(boxes) > 0:
          past = boxes


    print(count)
    return count


# if __name__ == '__main__':
#     print(count_vehicles(cv2.VideoCapture(
#         root+'videos/a8ecae93-cc99-4e04-adcb-395a3c33ced7.mp4'), load_models()))
