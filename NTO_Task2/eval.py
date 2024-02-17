# -*- coding: utf-8 -*-
import socket
# TODO: Допишите импорт библиотек, которые собираетесь использовать
import math

def setup_socket(ip_address, port):
    """ Функция инициализирует сокет.
        Входные параметры: ip-адрес и порт сервера
        Выходные параметры: инициализированный сокет

        Если вы не собираетесь использовать эту функцию, пусть возвращает None

        То, что вы вернёте из этой функции, будет передано первым аргументом в функцию communication_cycle
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip_address, port))
    return server

def get_dist(x1, y1, x2, y2):
   return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def communication_cycle(conn: socket.socket, start_pos, start_equipment):
    """ Эта функция отвечает за обмен данными с информационным и сервисным центрами..
        Входные параметры:
            conn - сокет из функции setup_socket,
            start_pos - стартовая позиция беспилотного автомобиля (x, y),
            start_equipment - начальное снаряжение

    """
    # conn.send('hello! World'.encode())
    # answer = conn.recv(1024).decode()
    equips = {'fire': 'bransboit', 'medic_aid': 'medical_kit', 'crash': 'repair_tools'}
    equip_ids = {'bransboit': 1, 'medical_kit': 2, 'repair_tools': 3}
    conn.send('server,give_tasks|'.encode())
    msg = ''
    while True:
      symbol = conn.recv(1).decode()
      if symbol in ('|', ''): break
      msg += symbol

    tasks = [task.split('.') for task in msg.split(',')]
    nearest_task = []
    nearest_task_id = 0
    min_dist = 10000000
    start_x, start_y = start_pos
    if len(tasks) == 0:
      nearest_task_id = 0
    else:
      for task in tasks:
        dist = get_dist(start_x, start_y, int(task[1]), int(task[2]))
        if dist < min_dist:
          min_dist = dist
          nearest_task = task
      nearest_task_id = tasks.index(nearest_task)

    conn.send(f'server,reserve_task,{nearest_task_id}|'.encode())
    msg = ''
    while True:
        symbol = conn.recv(1).decode()
        if symbol in ('|', ''): break
        msg += symbol
    needed_equipment = equips[tasks[nearest_task_id][0]]
    if needed_equipment != start_equipment:
      if start_equipment != 'no_equipment':
        conn.send('hub,offload|'.encode())
        msg = ''
        while True:
            symbol = conn.recv(1).decode()
            if symbol in ('|', ''): break
            msg += symbol

      conn.send(f'hub,give,{equip_ids[needed_equipment]}|'.encode())
      while True:
          symbol = conn.recv(1).decode()
          if symbol in ('|', ''): break
          msg += symbol
    conn.send('equip_ready|'.encode())
    while True:
        symbol = conn.recv(1).decode()
        if symbol in ('|', ''): break
        msg += symbol
    conn.close()
    return 0