from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_REPKA, TOKEN_TEST

storage = MemoryStorage()

bot = Bot( token = TOKEN_REPKA )
dp = Dispatcher(bot, storage = storage)