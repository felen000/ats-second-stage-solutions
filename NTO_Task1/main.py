# -*- coding: utf-8 -*-
"""
Файл служит для определения точности вашего алгоритма

Для получения оценки точности, запустите файл на исполнение
"""

import eval as submission
import cv2
import pandas as pd


def main():
    csv_file = "annotations.csv"
    data = pd.read_csv(csv_file, sep=',')  # TODO: check for , or ;
    data = data.sample(frac=1)

    models = submission.load_models()

    correct = 0
    for i, row in enumerate(data.itertuples()):
        row_id, video_filename, real_answer = row

        video = cv2.VideoCapture(video_filename)

        user_answer = submission.count_vehicles(video, models)

        if real_answer == user_answer:
            correct += 1
            print(video_filename, '- верно')
        else:
            print(video_filename, '- неверно')

    total_object = len(data.index)
    print(f"Из {total_object} объектов верно определены {correct}.")

    score = correct / total_object
    print(f"Точность: {score:.2f}")


if __name__ == '__main__':
    main()
