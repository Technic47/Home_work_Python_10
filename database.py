from typing import List, Any
from xml.etree import ElementTree
import pandas
import csv
import datetime
import json
import UI


def create_new() -> str:
    """Create a new database"""
    now = datetime.datetime.now()
    now = now.strftime("%d%m%Y")
    name = f'/{now}.csv'
    path = data_path + name
    # set_cols(path)
    with open(setup, 'w') as file:
        file.write(path)
    return path


def set_cols(cols) -> None:
    """
    set names of cols in db from path
    :param path: db path
    """
    data = dict.fromkeys(cols)
    print(data)
    path = show_current()
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(data)


def show_current() -> str:
    """shows current db from setup file"""
    with open(setup, 'r') as file:
        current_database = file.read()
    return current_database


def set_current(data) -> None:
    """change current db to data in setup file"""
    with open(setup, 'w') as file:
        file.write(data)


def get_cols() -> []:
    """shows header of db"""
    with open(show_current(), 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        cols = reader.fieldnames
        return cols


def save_data(data) -> {}:
    """adds line to current db"""
    cols = get_cols()
    with open(show_current(), 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=cols)
        writer.writerow({cols[0]: data[0], cols[1]: data[1], cols[2]: data[2]})
    return data


def show_base() -> None:
    """shows all records in current db"""
    rows = get_cols()
    print(rows)
    with open(show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            print(f'{row[rows[0]]}, {row[rows[1]]}, {row[rows[2]]}')


def select_base(name: str) -> None:
    """selects db and place it to current position"""
    try:
        open(data_path + '/' + name + '.csv', 'r')
    except IOError:
        print('File not found!')
    else:
        data = data_path + '/' + name + '.csv'
        set_current(data)


def search(col, data):
    """Search function in current db"""
    global indexes
    j = 0
    cols = get_cols()
    key = col
    for i in range(len(cols)):
        if key == cols[i]:
            request = data
            csvfile = csv.reader(open(show_current(), 'r'), delimiter=",")
            for row in csvfile:
                j += 1
                if request in row[i]:
                    indexes.append(j)


def show_indexed():
    """shows positions with dedicated numbers in current db"""
    j = 1
    item_list = []
    with open(show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            j += 1
            if j in indexes:
                item_list.append(row)
    return indexes, item_list


def delete(numbers) -> None:
    """removal procedure. Uses cached_base for re-writing current db"""
    j = 1
    with open(show_current(), 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        with open('cache/cached_base.csv', 'w', newline='') as cache_file:
            writer = csv.writer(cache_file, delimiter=",")
            for row in reader:
                if j not in numbers:
                    writer.writerow(row)
                j += 1
    with open(show_current(), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        with open('cache/cached_base.csv', 'r', encoding='utf-8') as cache_file:
            reader = csv.reader(cache_file, delimiter=",")
            for row in reader:
                writer.writerow(row)


def merge(name: str) -> None:
    """Merge selected db to current"""
    path = data_path + '/' + name + '.csv'
    try:
        open(path)
    except FileNotFoundError:
        print('File not found!')
    else:
        cols = get_cols()
        with open(path, newline='') as csvfile:
            data = csv.DictReader(csvfile)
            with open(show_current(), 'a', newline='') as csvfile2:
                writer = csv.DictWriter(csvfile2, delimiter=",", fieldnames=cols)
                for row in data:
                    writer.writerow({cols[0]: row[cols[0]], cols[1]: row[cols[1]], cols[2]: row[cols[2]]})


def export_json() -> None:
    """export current db to .json file"""
    json_array = []
    with open(show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            json_array.append(row)
    json_path = show_current().replace('.csv', '.json')
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        jsonstr = json.dumps(json_array, indent=4)
        jsonfile.write(jsonstr)


def convert_xml(headers, row) -> str:
    """preparation for convertion to xml"""
    s = f'<row>\n'
    for header, item in zip(headers, row):
        s += f'    <{header}>' + f'{item}' + f'</{header}>\n'
    return s + '</row>'


def export_xml() -> None:
    """export current db to .xml file"""
    with open(show_current(), 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        xml = '<data>\n'
        for row in reader:
            xml += convert_xml(headers, row) + '\n'
        xml += '</data>'
    xml_path = show_current().replace('.csv', '.xml')
    with open(xml_path, 'w', encoding='utf-8') as xmlfile:
        xmlfile.write(xml)


setup = 'setup.txt'
data_path = r'database'
indexes = []
setup = 'setup.txt'
