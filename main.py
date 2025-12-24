import asyncio
import logging
import threading
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv

import health as hl
from handlers import start, room, game

load_dotenv()

health_thread = threading.Thread(target=hl.start_health_server, daemon=True)
health_thread.start()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(room.router)
dp.include_router(game.router)

async def main():
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="create", description="Создать комнату"),
        BotCommand(command="leave_room", description="Выйти из комнаты"),
        BotCommand(command="start_round", description="Начать раунд")
    ]
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Бот запущен!')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')