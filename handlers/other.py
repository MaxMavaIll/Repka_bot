from aiogram import types, Dispatcher
from create_bot import dp, bot


#@dp.message_handler()
async def welcome(message : types.Message):
    await message.answer(message.text)
    # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)

def register_hendlers_other(dp : Dispatcher):
    dp.register_message_handler( welcome, commands = ['start', 'help'])