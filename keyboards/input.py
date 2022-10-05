from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

show_base = KeyboardButton('/show_base')
show_current = KeyboardButton('/show_current')
new = KeyboardButton('/new')
select = KeyboardButton('/select')
add = KeyboardButton('/add')
delete = KeyboardButton('/del')
search = KeyboardButton('/search')
merge = KeyboardButton('/merge')
export_json = KeyboardButton('/export_json')
import_json = KeyboardButton('/import_json')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# kb_client.add(b1).insert(b2) # add - с новой строки, insert - добавляет к строке

kb_client.row(show_base, show_current, new)  # всё в строку
kb_client.row(add, delete, search, select)
kb_client.add(merge, export_json, import_json)
