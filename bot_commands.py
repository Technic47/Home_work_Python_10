import csv

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
import config
import os
import logger
import database as db

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Database(StatesGroup):
    name = State()
    col1 = State()
    col2 = State()
    col3 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hello! Let`s start!')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    with open('READ_ME.txt', 'r') as file:
        read_me = file.readlines()
        for line in read_me:
            await bot.send_message(message.from_user.id, line)


@dp.message_handler(commands=['new'])
async def new(message: types.Message):
    database1 = db.create_new()
    await bot.send_message(message.from_user.id, f'New database created: {database1}')
    await bot.send_message(message.from_user.id, f'First col name:')
    await Database.col1.set()


@dp.message_handler(state=Database.col1)
async def col1_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['col1'] = message.text
    await Database.next()
    await message.reply('Second col name:')
    await Database.col2.set()


@dp.message_handler(state=Database.col2)
async def col2_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['col2'] = message.text
    await Database.next()
    await message.reply('Third col name:')
    await Database.col3.set()


@dp.message_handler(state=Database.col3)
async def col3_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['col3'] = message.text
        print(Database.col1)
        await bot.send_message(
            message.from_user.id,
            md.text(
                md.text(f'Col1:', data['col1']),
                md.text(f'Col2:', data['col2']),
                md.text(f'Col3:', data['col3']),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN)
    cols = [data['col1'], data['col2'], data['col3']]
    db.set_cols(cols)


@dp.message_handler(commands=['show_dir'])
async def show_dir(message: types.Message):
    dirname = 'database'
    for filename in os.listdir(dirname):
        await bot.send_message(message.from_user.id, filename)


@dp.message_handler(commands=['show_current'])
async def show_current(message: types.Message):
    await bot.send_message(message.from_user.id, db.show_current())


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    data = message.text.replace(' ', ',').replace(';', ',').replace('.', ',').split(',')
    db.save_data(data[1:])
    data_text = ' '.join(data[1:])
    await bot.send_message(message.from_user.id, f'Line added: {data_text}')


@dp.message_handler(commands=['show_base'])
async def show_base(message: types.Message):
    rows = db.get_cols()
    with open(db.show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            await bot.send_message(message.from_user.id, f'{row[rows[0]]}, {row[rows[1]]}, {row[rows[2]]}')


@dp.message_handler(commands=['select'])
async def select(message: types.Message):
    data = message.text.replace(' ', ',').replace(';', ',').replace('.', ',').split(',')
    db.select_base(data[1])
    await bot.send_message(message.from_user.id, f'Database {data[1]}.db selected and set as current')


@dp.message_handler(commands=['merge'])
async def merge(message: types.Message):
    data = message.text.replace(' ', ',').replace(';', ',').replace('.', ',').split(',')
    db.merge(data[1])
    await bot.send_message(message.from_user.id, f'Database {data[1]}.db was merged with current')


@dp.message_handler(commands=['export_json'])
async def export_json(message: types.Message):
    db.export_json()
    await bot.send_message(message.from_user.id, f'Database {db.show_current()} was exported as .json')


@dp.message_handler(commands=['export_xml'])
async def export_xml(message: types.Message):
    db.export_xml()
    await bot.send_message(message.from_user.id, f'Database {db.show_current()} was exported as .xml')


@dp.message_handler(commands=['search'])
async def import_json(message: types.Message):
    data = message.text.replace(' ', ',').replace(';', ',').replace('.', ',').split(',')
    db.search(data[1:])
    requested_data = db.show_indexed()
    indexes = requested_data[0]
    results = requested_data[1]
    for item in range(len(results)):
        await bot.send_message(message.from_user.id, f'{indexes[item]}: {results[item]}')
    await bot.send_message(message.from_user.id, 'For deleting these lines use "/del indexes" command.')


@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.from_user.id, message.text)
    # await message.answer(message.text)  # просто ответ
    # await message.reply(message.text)  # ответ с цитированием собщения пользователя
    # await bot.send_message(message.from_user.id, message.text) #ответ в личку
