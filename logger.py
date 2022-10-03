import datetime
import database
import glob
import os

logs_path = r'logs'
current_log = ''
now = datetime.datetime.now()
now = now.strftime("%d%m%Y_%H%M%S")


def start_logger() -> str:
    """initializing of logger"""
    global current_log
    name = f'/{now}.txt'
    path = logs_path + name
    with open(path, 'w') as text:
        text.write(
            f"Current database - {database.show_current()}\n"
            f"{now} - session started;\n")
    print(f'Logger started. Current log - {name}')
    current_log = path
    return path


def log(data, action: str):
    """
    record new line to current log file
    :param data: object of action
    :param action: action done with object
    :return: data argument
    """
    with open(current_log, 'a') as text:
        text.write('{0} - {1} {2};'.format(now, data, action) + '\n')
    return data


def clear() -> None:
    """clear current log"""
    with open(current_log, 'w') as text:
        text.write(f'{now} - session cleared')
    print('Current log cleared')


def stop_logger() -> None:
    """add closing line to current log"""
    with open(current_log, 'a') as text:
        text.write(f"{now} - session closed;")
    print('Logger stopped.')


def delete() -> None:
    """delete all log files in directory"""
    for file in glob.glob('logs/*'):
        os.remove(file)
        print('All logs deleted')
