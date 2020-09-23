import os
import sys
import time
import traceback
from functools import wraps
from os.path import dirname
from socketIO_client_nexus import SocketIO
import json
from collections import OrderedDict

# ファイル読み込みインターバル
#READ_INTERVAL = 200 / 1000
READ_INTERVAL = 500 / 1000

# WebSocket サーバ
socketIO = SocketIO('localhost', 8080)
socket = 'current_data'


def wrapper(func):
    @wraps(func)
    def _func(*args, **keywords):
        try:
            func(*args, **keywords)
        except Exception:
            traceback.print_exc()

    return _func


def send_data(data):
    # print(json.dumps(data))
    socketIO.emit(socket, json.dumps(data))


def MakeTrajectoryData(columns):
    data = OrderedDict()
    data["unixtime"] = float(columns[0])
    data["id"] = columns[1]
    data["x"] = float(columns[2])
    data["y"] = float(columns[3])
    data["z"] = float(columns[4])
    data["velocity"] = float(columns[5])
    data["direction"] = float(columns[6])
    data["acceleration"] = float(columns[7])
    data["ang_velocity"] = float(columns[8])
    data["category"] = int(columns[9])
    data["grid_id"] = columns[10]
    data["area_id"] = columns[11]
    data["size"] = int(columns[12])
    return data


def tail_like(path):
    current_path = path

    # TODO: なくなったら次のファイルに行く処理
    current_file = open(path, 'r')
    try:
        buffer = []
        old_unix_time = 0

        data = ''

        for row in current_file:
            columns = row.split(',')
            unix_time = columns[0]
            if int(columns[9]) != 2:
                continue
            print("ID: %s, X: %f, Y: %f" % (columns[1], float(columns[2]), float(columns[3])))

            if row == '':
                pass
            elif unix_time != '' and old_unix_time == 0:
                pass
            elif float(unix_time) > old_unix_time:
                send_data(buffer)
                old_unix_time = float(unix_time)
                # print(buffer)
                buffer = []
                buffer.append(MakeTrajectoryData(columns))
                print("sleeping : %f" % READ_INTERVAL)
                time.sleep(READ_INTERVAL)
            else:
                buffer.append(MakeTrajectoryData(columns))

            if unix_time != '':
                old_unix_time = float(unix_time)

    finally:
        current_file.close()

@wrapper
def main():
    global web_socket_wrapper
    if len(sys.argv) < 2:
        print('invalid arguments. specified csv full path.')
        return
    path = sys.argv[1]
    if not os.path.exists(path):
        print("No such file exist.")
        return

    tail_like(path)


if __name__ in '__main__':
    main()
