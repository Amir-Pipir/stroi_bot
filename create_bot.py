from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

storage = MemoryStorage

bot = Bot(os.getenv('TOKEN'))

dp = Dispatcher(bot, storage=MemoryStorage())
