import UI
import cache
import logger
import database
import os


def start():
    """main console loop"""
    print('System started')
    logger.start_logger()
    while True:
        match input('Enter command: '):
            case 'exit':
                cache.delete()
                logger.log('cache', 'cleared')
                logger.stop_logger()
                quit()
            case 'help':
                print('READ_ME file may help you.')
            case 'new':
                database1 = logger.log(database.create_new(), 'created')
                print(f'New database created: {database1}')
                print("Set a new database as current?\nY/N:")
                answer = UI.get_data()
                if answer == 'Y' or answer == 'y' or answer == 'yes':
                    database.set_current(database1)
                    logger.log(database.show_current(), 'set as current')
            case 'show dir':
                dirname = 'database'
                for filename in os.listdir(dirname):
                    print(filename)
                logger.log('databases', 'shown')
            case 'show current':
                print(database.show_current())
                logger.log('current_database', 'shown')
            case 'add':
                logger.log(database.save_data(database.collect_data()), 'added')
            case 'show base':
                database.show_base()
                logger.log('current database', 'shown')
            case 'select':
                name = input("Enter name of database: ")
                database.select_base(name)
                logger.log(name, 'selected')
                logger.log(database.show_current(), ' set as current')
            case 'merge':
                print("Enter name of database: ")

                database.merge(name)
                logger.log(path, 'merged with current db')
            case 'export json':
                database.export_json()
                logger.log('current database', 'exported as .json')
            case 'export xml':
                database.export_xml()
                logger.log('current database', 'exported as .xml')
            case 'import xml':
                database.import_xml()
                logger.log('xmlfile', 'imported')
            case 'import json':
                database.import_json()
                logger.log('jsonfile', 'imported')
            case 'search':
                logger.log(database.search(), 'searched')
            case 'clear log':
                logger.clear()
            case 'delete logs':
                logger.delete()
            case 'delete':
                logger.log(database.custom_delete(), 'deleted')
            case _:
                print('Wrong command')
