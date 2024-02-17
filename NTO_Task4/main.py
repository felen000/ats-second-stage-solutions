# -*- coding: utf-8 -*-
"""
Файл служит для определения точности вашего алгоритма

Для получения оценки точности, запустите файл на исполнение
"""

import eval as submission
import cv2
import pandas as pd
import numpy as np


def check_answer(real_answer, user_answer):
    return np.array_equal(real_answer, user_answer)


def main():
    csv_file = "annotations.csv"
    data = pd.read_csv(csv_file, sep=';')
    data = data.sample(frac=1)

    tools = submission.load_tools()

    correct = 0
    for i, row in enumerate(data.itertuples()):
        row_id, image_filename, layers = row
        layers = np.array(eval(layers))

        image = cv2.imread(image_filename)

        user_answer = submission.count_the_types_of_cubes(image, tools)

        if check_answer(layers, user_answer):
            correct += 1
            print(image_filename, '- верно')
        else:
            print(image_filename, '- неверно')

    total_object = len(data.index)
    print(f"Из {total_object} светофоров верно детектированы {correct}")

    score = correct / total_object
    print(f"Точность: {score:.2f}")


if __name__ == '__main__':
    main()