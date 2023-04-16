from aiogram.utils import executor
from create_bot import dp, bot
from data_base import sqlite_db
from aiogram import types
from config import blok, URL_APP
import os


async def on_startup(_):
    print('Бот зарущений')
    sqlite_db.sql_start()
    
# async def on_startup(dp):
#     await bot.set_webhook(URL_APP)
#    # insert code here to run it after start

# async def on_shutdown(dp):
#     await bot.delete_webhook()



from handlers import client, other, admin


@dp.message_handler(lambda message: message.from_user.id in blok.keys())
async def user_blok(message: types.Message):
    print("user_blok!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    id = message.from_user.id
    if blok[id] == []:
        blok[id] = "Не визначенна"
    await message.answer("Тебе заблоковано.\nПричина:\n{}".format(blok[id]) )


admin.register_hendlers_client(dp)
client.register_hendlers_client(dp)


executor.start_polling(dp, skip_updates = True, on_startup = on_startup)
# executor.start_webhook(
#         dispatcher=dp,
#         webhook_path='',
#         on_startup=on_startup,
#         on_shutdown=on_shutdown,
#         skip_updates=True,
#         host="0.0.0.0",
#         port=int(os.environ.get("PORT", 5000)),
# )