from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from keyboards import kb_client
from aiogram import Bot, types
from classes import *
import database as db
import config
import os
import csv

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

new = Database()
add = AddInfo()
del_line = DelInfo()
search = SearchInfo()
merge = Merge()
select = Select()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hello! Let`s start!', reply_markup=kb_client)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    with open('READ_ME.txt', 'r') as file:
        read_me = file.readlines()
        for line in read_me:
            await bot.send_message(message.from_user.id, line)


@dp.message_handler(commands=['new'])
async def new_db(message: types.Message):
    database1 = db.create_new()
    await bot.send_message(message.from_user.id, f'New database created: {database1}')
    await bot.send_message(message.from_user.id, f'First col name:')
    await new.state1.set()


@dp.message_handler(state=new.state1)
async def col1_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await new.next()
    await message.reply('Second col name:')
    await new.state2.set()


@dp.message_handler(state=new.state2)
async def col2_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
    await new.next()
    await message.reply('Third col name:')
    await new.state3.set()


@dp.message_handler(state=new.state3)
async def col3_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state3'] = message.text
        await bot.send_message(
            message.from_user.id,
            md.text(
                md.text(f'Col1:', data['state1']),
                md.text(f'Col2:', data['state2']),
                md.text(f'Col3:', data['state3']),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN)
    cols = [data['state1'], data['state2'], data['state3']]
    db.set_cols(cols)
    await state.finish()


@dp.message_handler(commands=['add'])
async def add_line(message: types.Message):
    await bot.send_message(message.from_user.id, f'First col info:')
    await add.state1.set()


@dp.message_handler(state=add.state1)
async def col1_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await add.next()
    await message.reply('Second col info:')
    await add.state2.set()


@dp.message_handler(state=add.state2)
async def col2_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
    await add.next()
    await message.reply('Third col info:')
    await add.state3.set()


@dp.message_handler(state=add.state3)
async def col3_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state3'] = message.text
        await bot.send_message(
            message.from_user.id,
            md.text(
                md.text(f'Col1:', data['state1']),
                md.text(f'Col2:', data['state2']),
                md.text(f'Col3:', data['state3']),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN)
    cols = [data['state1'], data['state2'], data['state3']]
    db.save_data(cols)
    print(cols)
    await state.finish()


@dp.message_handler(commands=['show_dir'])
async def show_dir(message: types.Message):
    dirname = 'database'
    for filename in os.listdir(dirname):
        await bot.send_message(message.from_user.id, filename)


@dp.message_handler(commands=['show_current'])
async def show_current(message: types.Message):
    await bot.send_message(message.from_user.id, db.show_current())


@dp.message_handler(commands=['show_base'])
async def show_base(message: types.Message):
    rows = db.get_cols()
    with open(db.show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            await bot.send_message(message.from_user.id, f'{row[rows[0]]}, {row[rows[1]]}, {row[rows[2]]}')


@dp.message_handler(commands=['select'])
async def select_db(message: types.Message):
    await show_dir(message)
    await bot.send_message(message.from_user.id, f'What DB would you like to chose?')
    await select.state1.set()


@dp.message_handler(state=select.state1)
async def del_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = message.text
        data['state1'] = text
        await bot.send_message(message.from_user.id, f'Database {text}.db selected and set as current')
    db.select_base(data['state1'])
    await state.finish()


@dp.message_handler(commands=['merge'])
async def merge_db(message: types.Message):
    await bot.send_message(message.from_user.id, f'DB for adding to current:')
    await merge.state1.set()


@dp.message_handler(state=merge.state1)
async def del_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = message.text
        data['state1'] = text
        await bot.send_message(message.from_user.id, f'Database {text}.db was merged with current')
    db.merge(data['state1'])
    await state.finish()


@dp.message_handler(commands=['export_json'])
async def export_json(message: types.Message):
    db.export_json()
    await bot.send_message(message.from_user.id, f'Database {db.show_current()} was exported as .json')


@dp.message_handler(commands=['export_xml'])
async def export_xml(message: types.Message):
    db.export_xml()
    await bot.send_message(message.from_user.id, f'Database {db.show_current()} was exported as .xml')


@dp.message_handler(commands=['search'])
async def search_line(message: types.Message):
    await bot.send_message(message.from_user.id, f'Column name for search:')
    await search.state1.set()


@dp.message_handler(state=search.state1)
async def col1_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await search.next()
    await message.reply('Info:')
    await search.state2.set()


@dp.message_handler(state=search.state2)
async def col2_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
    db.search(data['state1'], data['state2'])
    requested_data = db.show_indexed()
    indexes = requested_data[0]
    results = requested_data[1]
    for item in range(len(results)):
        await bot.send_message(message.from_user.id, f'{indexes[item]}: {results[item]}')
    await bot.send_message(message.from_user.id, 'For deleting these lines use "/del indexes" command.')
    await state.finish()


@dp.message_handler(commands=['del'])
async def delete(message: types.Message):
    await bot.send_message(message.from_user.id, f'Indexes to delete:')
    await del_line.state1.set()


@dp.message_handler(state=del_line.state1)
async def del_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        numbers = message.text.replace(' ', ',').replace(';', ',').replace('.', ',').split(',')
        list1 = list(map(int, numbers))
        data['state1'] = list1
        await bot.send_message(message.from_user.id, f'Lines with indexes {list1} were deleted.')
    indexes = data['state1']
    print(indexes)
    db.delete(indexes)
    await state.finish()


@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text)
    # await message.answer(message.text)  # просто ответ
    # await message.reply(message.text)  # ответ с цитированием собщения пользователя
    # await bot.send_message(message.from_user.id, message.text) #ответ в личку
