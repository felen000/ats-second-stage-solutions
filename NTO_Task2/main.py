# -*- coding: utf-8 -*-
"""
Файл служит для определения точности вашего алгоритма

Для получения оценки точности, запустите файл на исполнение
"""
from pathlib import Path
import socket
import threading
import eval as submission
# import cv2
import pandas as pd
import time


equipments = ['no_equipment', 'bransboit', 'medical_kit', 'repair_tools', 'cleaner_kit', 'gardening_tools', 'comfortable_salon']


def server_loop(tasks, start_equipment, nearest_task_id, need_equipment):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 8000))
    sock.listen(1)
    sock.settimeout(5)

    client, address = sock.accept()

    reserved_task = None
    current_equipment = start_equipment
    fail = False

    while True:
        msg = ''
        while True:
            symbol = client.recv(1).decode()
            if symbol in ('|', ''): break
            msg += symbol

        # print("Got in server:", msg)

        if msg == 'server,give_tasks':
            client.send((tasks + '|').encode())

        elif msg.startswith('server,reserve_task'):
            task_id = int(msg.split(',')[-1])

            if not reserved_task:
                client.sendall('ok|'.encode())
                reserved_task = task_id
            else:
                client.sendall('error|'.encode())
                fail = True

        elif msg == 'hub,offload':
            if current_equipment != equipments[0]:
                client.sendall('ok|'.encode())
                current_equipment = equipments[0]
            else:
                client.sendall('error|'.encode())
                fail = True

        elif msg.startswith('hub,give'):
            if current_equipment == equipments[0]:
                eq_id = int(msg.split(',')[-1])
                current_equipment = equipments[eq_id]
                client.sendall('ok|'.encode())
            else:
                client.sendall('error|'.encode())
                fail = True

        elif msg == 'equip_ready':
            sock.close()
            if current_equipment == need_equipment and reserved_task == nearest_task_id and not fail:
                return True
            else:
                return False

        else:
            sock.close()
            return False
    return False


def create_client(start_pos, start_eq):
    user_sock = submission.setup_socket("127.0.0.1", 8000)
    submission.communication_cycle(user_sock, start_pos, start_eq)


def main():
    cur_dir = Path(__file__).parent
    csv_file = cur_dir / "annotations.csv"
    data = pd.read_csv(csv_file, sep=';')
    data = data.sample(frac=1)

    correct = 0
    for i, row in enumerate(data.itertuples()):
        row_id, tasks, start_pos_x, start_pos_y, start_eq, nearest_task_id, needed_equipment = row
        start_pos = (start_pos_x, start_pos_y)

        threading.Thread(target=create_client, args=(start_pos, start_eq), daemon=True).start()

        result = server_loop(tasks, start_eq, nearest_task_id, needed_equipment)

        if result:
            correct += 1

    total_object = len(data.index)
    print(f"Из {total_object} объектов верно определены {correct}.")

    score = correct / total_object
    print(f"Точность: {score:.2f}")


if __name__ == '__main__':
    main()