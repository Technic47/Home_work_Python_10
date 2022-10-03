from aiogram.utils import executor
from bot_commands import dp


async def on_startup(_):
    print('Bot is online')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
