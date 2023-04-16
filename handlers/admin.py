from ast import Delete
from os import name
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data_base import sqlite_db
from keyboards import client_kb, Bot, admin_kb
# from handlers.client import Seseeons 
from config import password, blok
from datetime import datetime, date
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from google_sheet import sheet





Seseeons_admin = {}
Seseeons = {}
ALL_time = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "Ніч"]
Name_key_add = dict() #dict
Dinamic_dl_time = dict()

#ONE
Sum_for_one_and_red = 90
Sum_for_one_and_blue = 130
Sum_for_one_and_black = 140

#GROUP
Sum_for_group_and_red = 100
Sum_for_group_and_blue = 150
Sum_for_group_and_black = 160

#NIGHT
Night_red = 700
Night_blue = 1000
Night_black = 1200



class Admin(StatesGroup):
    password = State()

class Add_admin(StatesGroup):
    start = State()
    month = State()
    day = State()  
    room = State()
    time = State()
    gruop_or_one = State()
    name = State()
    number = State()
    check = State()

class Delete_admin(StatesGroup):
    select_date = State()
    delet_time = State()

class Blok(StatesGroup):
    man = State()

class advert(StatesGroup):
    advert = State()

class Advert(StatesGroup):
    advert = State()

#------------------------------------------------ Check Admin --------------------------------------------------------#

async def admin_id(message: types.Message):
    
    if message.from_user.id not in Seseeons_admin.keys():
        Seseeons_admin[message.from_user.id] = {
                "password" : 0,
                "data": 0,
                "firts_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "user_name": message.from_user.username
            }
    
        await Admin.password.set()
    elif Seseeons_admin[message.from_user.id]["password"] == password: 
        # sti = open("handlers/stikers/Wait.tgs", "rb")
        # await bot.send_sticker(message.from_user.id, sticker = sti)
        await message.answer("Да слушаю ...", reply_markup= admin_kb.admin_Menu)
    
async def check_admin(message: types.Message, state: FSMContext):
    
    
    if message.text == password:
        Seseeons_admin[message.from_user.id]["password"] = message.text
        await bot.delete_message(message.chat.id, message.message_id)
        
        await state.finish()
        await message.answer("Да сулшаю ...", reply_markup = admin_kb.admin_Menu)
        # sti = open("handlers/stikers/What.tgs", "rb")
        # await bot.send_sticker(message.from_user.id, sticker = sti)
    
    else:
        await bot.delete_message(message.chat.id, message.message_id)
        await state.finish()
        del Seseeons_admin[message.from_user.id]

#-----------------------------------     Check    -------------------------------------------#

async def Check_month_invalid_int(message: types.Message):
    
    if message.text == "Щось інше" or message.text == "Січень":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"/stop\"")
    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"/stop\"")

async def Check_day_invalid_int(message: types.Message):
    if message.text == "Не існуючий місяць день місяця":
        await message.reply("Провірь правильність відповіді і впиши ще раз, те що ти хотів. Якщо хочеш скасувати реєстрацією введи \"/stop\"")
    elif message.text == "Більше двох місяців":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"/stop\"")
    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"/stop\"")

async def Check_number_invalid_int(message: types.Message):
    await message.reply("Проблема з номером, перевірть ще раз його. Якщо хочеш скасувати реєстрацією введи \"st\"")

async def last_check(message: types.Message, state: FSMContext):
    if message.text == "Зайнятий час":
        await state.finish()
        await message.reply("Пробач, але ти трішки не встигла хтось уже зареєструвався на цей час. Введи команду \"/start\", щоб спробувати ще раз")
    else :
        Bot.ctb.write_config("logging/finish.log", Seseeons)
        # current_state = await state.get_state()
        # if current_state is None:
        #     return
        await state.finish()
        del Seseeons[message.from_user.id]
        await message.answer("Всі ведені дані були видаленні. Введи команду \"/start\", щоб спробувати ще раз")

async def check_my_Data(message: types.Message):
    pass
 


#------------------------------------------------ Menu admin --------------------------------------------------------#

async def Client_used_bot(message: types.Message):
    if Seseeons_admin[message.from_user.id]["password"] == password:
        tmp, key = sqlite_db.all_id_name()
        if key == []:
            await message.answer("Зараз ще немає зареєстрованих людей")
        else:
            i = 1
            for id in key:
                name = tmp[id]
                admin_kb.client_user(id)
                await message.answer(f"#{i}")
                await message.answer("id: {},\nІм'я: {} ".format(id, name), reply_markup = admin_kb.admin_data)
                i += 1

async def All_data(message: types.Message):
    if Seseeons_admin[message.from_user.id]["password"] == password:
        vale, key= sqlite_db.all_data()
        for id in key:
            i = 0
            # print(name, room, time, id, date, number)
            tmp = vale[id]
            # print(tmp)
            await message.answer("#############{}#############".format(id))
            for name in tmp.keys():
                # print(type(name))
                admin_kb.add_del_block(id, name)
                # print("I went")
                # print(name)
                await message.answer(
                    "Ім'я: {}\n".format(name) + "date: {}\n".format(tmp[name]["date"])+ "time: {}\n".format(tmp[name]["time"]) + "room: {}\n".format(tmp[name]["room"]) + "number: {}".format(tmp[name]["number"]), reply_markup = admin_kb.admin_data)
            
async def advertisement(message: types.Message):
    await advert.advert.set()
    await message.answer("Що оголосити всім?:", reply_markup = ReplyKeyboardRemove())

async def exit(message: types.Message):
    del Seseeons_admin[message.from_user.id]
    await message.answer("Хорошо только тссс..", reply_markup = ReplyKeyboardRemove())
    # sti = open("handlers/stikers/TSSSS.tgs", "rb")
    # await bot.send_sticker(message.from_user.id, sticker = sti)

#------------------------------------------------ ADD User --------------------------------------------------------#

async def ADD_admin(cb: types.CallbackQuery): 
    
    data = cb.data.split("/")


    await add_time_to_sql(data, cb)
    await cb.answer()

async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    del Seseeons[message.from_user.id]
    await bot.send_message(message.from_user.id, "Ok, регистрация отменена.", reply_markup = admin_kb.admin_Menu)   
        
async def add_time_to_sql(data, cb):
    time = datetime.now()
    Seseeons[cb.from_user.id]= { 
                                    "id": int(data[1]),
                                    "time_user_regist": time,
                                    "data" : {
                                                "day": 0, 
                                                "month": 0, 
                                                "year": 0
                                                            },
                                    "room" : 0,
                                    "time" : [],
                                    "number": 0,
                                    "user_write_name": '',
                                    "Group_or_one": '',
                                    "sum_order" : 0,
                                    "Name":{
                                                "firts_name": cb.from_user.first_name,
                                                "last_name": cb.from_user.last_name,
                                                "user_name" : cb.from_user.username
                                                                                                }
                                    }
    await Add_admin.month.set()
    await bot.send_message(cb.from_user.id, "Выбери месяц?", reply_markup = client_kb.client_month)

async def add_month(message: types.Message, state: FSMContext):
    if await Bot.ctb.Check_month(message, Seseeons[message.from_user.id]):
        await Add_admin.next()
        await bot.send_message(message.from_user.id, "Выберите День:", reply_markup=client_kb.client_day_kb)

    elif message.text == "Щось інше" or message.text == "Січень":
        await message.reply("Выбирай то что снизу. Если хочешь отменить регистрацией введи \"st\"")

    else:
        await message.reply("Если хочешь отменить регистрацией введи \"st\"")

async def add_day(message: types.Message, state: FSMContext):

    if await Bot.ctb.Check_day(message, Seseeons[message.from_user.id]):
        await Add_admin.next()
        await bot.send_message(message.from_user.id, "Выбери комнату:", reply_markup = client_kb.client_rkb)

    elif message.text == "Не існуючий місяць день місяця":
        await message.reply("Проверь правильность ответа и впиши еще раз то, что ты хотел. Если хочешь отменить регистрацией введи \"st\"")
    elif message.text == "Більше двох місяців":
        await message.reply("Выбирай то что снизу. Если хочешь отменить регистрацией введи \"st\"")
    else:
        await message.reply("Если хочешь отменить регистрацией введи \"st\"")

async def add_room(message: types.Message, state: FSMContext):
    room = await Bot.ctb.Check_room(message, Seseeons[message.from_user.id])
    check_room = await Bot.ctb.Check_time(message, Seseeons[message.from_user.id])

    if room and check_room:
        await Add_admin.next()
        await bot.send_message(message.from_user.id, "Выбери время:", reply_markup = client_kb.client_tkb)

    elif not check_room:
        await message.answer("К сожалению, этот день занят на это число. Если хочешь отменить регистрацией введи \"st\"")

    else:
        await message.reply("Проверь правильность ответа и впиши еще раз то, что ты хотел. Если хочешь отменить регистрацией введи \"st\"")

async def add_get_to_user_time(message: types.Message, state: FSMContext):
    
    time =  Seseeons[message.from_user.id]

    if message.text == "Далі👉" and time["time"] != []:

        tmp = ["Група", "Сам"]
        client_kb.registed_name(tmp)

        await Add_admin.next()
        await bot.send_message(message.from_user.id, "Ты будешь заниматься с группой или сам?", reply_markup= client_kb.client_NAME)
        
    elif message.text == "Очистити все":
        Seseeons[message.from_user.id]["time"] = []
        await bot.send_message(message.from_user.id, "Все время стерто, ты можешь выбрать другое время", reply_markup = client_kb.client_tkb)
        
    elif message.text in ALL_time:
        if Bot.ctb.Check_NoRepeat(message, Seseeons[message.from_user.id]):
            time["time"].append(  message.text )
        time["time"] = Bot.numbering(time["time"])

        await bot.delete_message(message.from_user.id, message.message_id)
        # await bot.delete_message(message.from_user.id, bot.message_id)
        await message.answer(time["time"])
        
        #await bot.send_message(message.from_user.id, "Можливо ще якийсь чвс?\nЯкщо ні тисни \"Далі\" ", reply_markup = client_kb.client_tkb)

    else:
        await bot.send_message(message.from_user.id, "Выбери то время, которое находится в низу. Если хочешь отменить регистрацией введи \"st\"", reply_markup = client_kb.client_tkb)

async def add_group(message: types.Message, state: FSMContext):
    tmp = ["Група", "Сам"]
    time = Seseeons[message.from_user.id]["time"]
    room = Seseeons[message.from_user.id]["room"] 

    if message.text in tmp:
        if message.text == "Група":
            if room == "Синя":
                sum = Sum_for_group_and_blue
                for i in time:
                    if i == "Ніч":
                        all_sum += Night_blue                  
                    else:    
                        all_sum += sum

            if room == "Червона":
                sum = Sum_for_group_and_red
                for i in time:
                    if i == "Ніч":
                        all_sum += Night_red
                    else:
                        all_sum += sum

            if room == "Чорна":
                sum = Sum_for_group_and_black
                for i in time:
                    if i == "Ніч":
                        all_sum += Night_black
                    else:
                        all_sum += sum



        elif message.text == "Сам":   
            if room == "Синя":
                sum = Sum_for_one_and_blue
                for i in time:
                    if i == "Ніч":
                        all_sum += Night_blue  
                    else:    
                        all_sum += sum

            if room == "Червона":
                sum = Sum_for_one_and_red
                for i in time:
                    if i == "Ніч":
                        all_sum += Night_red
                    else:    
                        all_sum += sum

            if room == "Чорна":
                sum = Sum_for_one_and_black
                for i in time:
                    if i == "Ніч":
                        all_sum += Night_black
                    else:    
                        all_sum += sum
                        
        Seseeons[message.from_user.id]["sum_order"] = all_sum


        Seseeons[message.from_user.id]["sum_order"] = all_sum
        
    else:
        await message.answer("Выбери то, что находится в низу. Если хочешь отменить регистрацией введи \"st\"")
        return

    await Add_admin.next()
    await bot.send_message(message.from_user.id, "Введи имя или название группы, на кого записать это время", reply_markup = ReplyKeyboardRemove())

async def add_name(message: types.Message, state: FSMContext):
    for i in message.text:
        try:
            if int == type(int(i)):
                await message.answer("Веди имя без цифр;)")
                return
        except:
            if i == "/" and len(message.text) <= 12:
                await message.answer("Веди имя без цифр;)")
                return
    async with state.proxy() as data:
        Seseeons[message.from_user.id]["user_write_name"] = message.text
        data['name'] = message.text
    await Add_admin.next()
    await bot.send_message(message.from_user.id, "Введи номер телефона (Пример 066*****03 или 38066*****03)")

async def load_number(message: types.Message, state: FSMContext):
    Seseeons[message.from_user.id]["number"] = message.text
    day = Seseeons[message.from_user.id]["data"]['day']
    month = Seseeons[message.from_user.id]["data"]['month']
    for i in range(10):
        if i == day:
            day = "0" + str(i)
        if i == month:
            month = "0" + str(i)
    
        
    await bot.send_message( message.chat.id, 
            md.text(
                md.text( 'Проверь свои данные:' ),
                md.text( md.bold(Seseeons[message.from_user.id]["Group_or_one"]) ),
                md.text( "Имя:", md.bold(Seseeons[message.from_user.id]["user_write_name"]) ),
                md.text( 'Номер:', md.code(Seseeons[message.from_user.id]["number"]) ),
                md.text( 'Дата:', md.bold(str(day)), ".", md.bold(str(month)) ),
                md.text( "Комната:", md.bold(Seseeons[message.from_user.id]['room']) ),
                md.text( "Время:", md.bold(*Seseeons[message.from_user.id]['time'] ) ),
                md.text( "Сумма оплаты:", md.bold( Seseeons[message.from_user.id]["sum_order"] ) ),
                sep='\n',
            ), 
            reply_markup=client_kb.client_yn_kb,
            parse_mode=ParseMode.MARKDOWN
        )    
        
        
    
    await Add_admin.next()

async def Add_check_for_registration(message: types.Message, state: FSMContext):
    Menu_id = ["Всe клиенты", "Все данные об клиентах"]
    if await Bot.ctb.Last_check(message, Seseeons[message.from_user.id]):
            
        Bot.ctb.write_config("logging/finish.log", Seseeons)
        # async with state.proxy() as data:
        #     await message.reply( str(data) )
        # await sqlite_db.sql_add_command(Seseeons, message)
        client_kb.registed_name(Menu_id)
        await bot.send_message( message.from_user.id, 
                md.text(
                    md.text("Клиент успешно зарегистрирован."),
                    sep='\n'),
                    reply_markup =  admin_kb.admin_Menu, parse_mode=ParseMode.MARKDOWN )
        del Seseeons[message.from_user.id]
        await state.finish()

    elif message.text == "Зайнятий час":
        await state.finish()
        await message.reply("Прости, но ты немного не успела кто-то уже зарегистрировался на это время. Введи команду \"/start\", чтобы попробовать еще раз")

    else :
        Bot.ctb.write_config("logging/finish.log", Seseeons)
        # current_state = await state.get_state()
        # if current_state is None:
        #     return
        await state.finish()
        del Seseeons[message.from_user.id]
        await message.answer("Все ведомые данные были удалены.")



#------------------------------------------------ Close user time -----------------------------------------------------------#

#@dp.callback_query_handler(Text(contains="Скавати"))
async def DELETE_admin(cb: types.CallbackQuery):
    print(cb.data)
    data = cb.data.split("/")
    await search_for_del_time(cb, data)
    await cb.answer()
    
async def search_for_del_time(cb, data):
    tmp_volue_nm_rm_tm_dt_nmb, key = sqlite_db.get_data_fromSQL( int(data[1]) )
    name = data[2]


    Seseeons[cb.from_user.id] = { name: { 
                "id_user": 0,
                "date": [],
                "room": [],
                "time": [],
                "index": 0
                            }
                                }


    tmp_date = []
    tmp = []
    for index in range( len(tmp_volue_nm_rm_tm_dt_nmb[name]["date"] ) ):
        if tmp_volue_nm_rm_tm_dt_nmb[name]["date"][index] not in tmp:
            tmp_date.append( str(tmp_volue_nm_rm_tm_dt_nmb[name]["date"][index]) )
            tmp.append(tmp_volue_nm_rm_tm_dt_nmb[name]["date"][index])
        else:
            tmp_date.append(str(tmp_volue_nm_rm_tm_dt_nmb[name]["date"][index]) + "-" + tmp_volue_nm_rm_tm_dt_nmb[name]["room"][index])
   
    Seseeons[cb.from_user.id][name]["id_user"] = int(data[1])
    Seseeons[cb.from_user.id][name]["date"] = tmp_volue_nm_rm_tm_dt_nmb[name]["date"] 
    Seseeons[cb.from_user.id][name]["room"] = tmp_volue_nm_rm_tm_dt_nmb[name]["room"] 
    Seseeons[cb.from_user.id][name]["time"] = tmp_volue_nm_rm_tm_dt_nmb[name]["time"]


    

    client_kb.registed_name(tmp_date)
    await Delete_admin.select_date.set()
    await bot.send_message(cb.from_user.id, "Вибери дату!", reply_markup = client_kb.client_NAME)

async def select_data(message: types.Message):
    print("select")
    for i in Seseeons[message.from_user.id].keys():
        name = i
    tmp = message.text.split("-")

    time = date(int (tmp[0]), int(tmp[1]), int(tmp[2]))
    index = Seseeons[message.from_user.id][name]["date"].index( time )
    try:
        if tmp[3] not in Seseeons[message.from_user.id][name]["room"][index]:
            tmp_time = Seseeons[message.from_user.id][name]["date"][1:len(Seseeons[message.from_user.id][name]["date"]) ]
            index = tmp_time.index(time) + 1
        
    except:
        pass

    Seseeons[message.from_user.id][name]["index"] = index
    tmp = Dinamic_dl_time[message.from_user.id] = Seseeons[message.from_user.id][name]["time"][index]
    Seseeons[message.from_user.id][name]["time"] = []

    # print(tmp, index, Seseeons[message.from_user.id][name]["id"])
    client_kb.Dinamic_dl_kb(tmp)

    await Delete_admin.next()

    await bot.send_message(message.from_user.id, "Вибери час який ти хочеш видалити!", reply_markup = client_kb.client_tkb)
    
async def delet_user(message: types.Message, state: FSMContext):
    dice = ["🗂"]


    for i in Seseeons[message.from_user.id].keys():
        name = i
    index = Seseeons[message.from_user.id][name]["index"]
    ID_USER = Seseeons[message.from_user.id][name]["id_user"]

    
    
    if message.text == "Далі👉" and Seseeons[message.from_user.id][name]["time"] != []:
        
        time = Seseeons[message.from_user.id][name]["time"]
        print(Seseeons[message.from_user.id][name]["date"], Seseeons[message.from_user.id][name]["room"], name)
        date = Seseeons[message.from_user.id][name]["date"][index]
        room = Seseeons[message.from_user.id][name]["room"][index]

        # await message.answer_dice(emoji="🗂")
        sqlite_db.sql_del(ID_USER, time, date, name, room)
        await message.answer("Зачикай ще трішки. Майже видалив)")
        sheet.delet_from_basedate(Seseeons[message.from_user.id][name], index)
        Bot.ctb.start_check_modul(message)
        

        await bot.send_message(message.from_user.id, "Час {} був видаленний успішно!".format(Seseeons[message.from_user.id][name]["time"]), reply_markup = admin_kb.admin_Menu)
        del Seseeons[message.from_user.id]
        await state.finish()
        
        
    elif message.text == "Очистити все":
        Seseeons[message.from_user.id][name]["time"] = []
        await bot.send_message(message.from_user.id, "Весь час стерто, ти можеш вибрати інший час", reply_markup = client_kb.client_tkb)
        
    elif message.text in Dinamic_dl_time[message.from_user.id]:
        print( Dinamic_dl_time[message.from_user.id] )
        if Bot.ctb.Check_NoRepeat(message, Seseeons[message.from_user.id][name]):
            Seseeons[message.from_user.id][name]["time"].append(message.text)
        await bot.delete_message(message.from_user.id, message.message_id)
        await message.answer(Seseeons[message.from_user.id][name]["time"])

    else:
        await bot.send_message(message.from_user.id, "Вибири той час який знаходиться є знизу", reply_markup = client_kb.client_tkb)


#------------------------------------------------ Close user all time --------------------------------------------------------#

#@dp.callback_query_handler(Text(contains="Скасувати все"))
async def Delet_all_admin(cb: types.CallbackQuery):
    await cb.message.answer("Починаю видаляти ...")
    try:
        data = cb.data.split("/")
        id = int(data[1])
        name = data[2]
        vale, key = sqlite_db.get_data_fromSQL(id, name)
        for name in key:
            Seseeons[cb.from_user.id] = { 
                "date": vale[name]["date"],
                "time": 0,
                "room": vale[name]["room"],
                
            }
            
            for i in range(len(vale[name]["room"])):
                Seseeons[cb.from_user.id]["time"] = vale[name]["time"][i]
                sheet.delet_from_basedate(Seseeons[cb.from_user.id], i)
                sqlite_db.sql_del(id, vale[name]["time"][i], vale[name]["date"][i], name, vale[name]["room"][i])
            
        await bot.delete_message(cb.message.chat.id, cb.message.message_id)
        await cb.message.answer("Всі дані id : \"{}\" були видалені видаленні!".format(data[1]))
    except:
        
        data = cb.data.split("/")
        id = int(data[1])
        vale, key = sqlite_db.get_data_fromSQL(id)
        for name in key:
            Seseeons[cb.from_user.id] = { 
                "date": vale[name]["date"],
                "time": 0,
                "room": vale[name]["room"],
                
            }
            
            for i in range(len(vale[name]["room"])):
                Seseeons[cb.from_user.id]["time"] = vale[name]["time"][i]
                sheet.delet_from_basedate(Seseeons[cb.from_user.id], i)
                sqlite_db.sql_del(id, vale[name]["time"][i], vale[name]["date"][i], name, vale[name]["room"][i])
            
        await bot.delete_message(cb.message.chat.id, cb.message.message_id)
        await cb.message.answer("Всі дані id : \"{}\" були видалені видаленні!".format(data[1]))

#------------------------------------------------ Block user -----------------------------------------------------------------#

#@dp.callback_query_handler(Text(contains="Заблокувати"))
async def Block_admin(cb: types.CallbackQuery):
    data = cb.data.split("/")
    Seseeons_admin[cb.from_user.id]["data"] = data
    id = int(data[1])
    blok[id] = " "
    admin_kb.client_user(id)
    await bot.edit_message_reply_markup(cb.message.chat.id, cb.message.message_id, cb.inline_message_id, reply_markup=admin_kb.admin_data)
    await Blok.man.set()
    await bot.send_message(cb.from_user.id, "Введи чому ти заболокував цього користувача (Користувач отримуватиме це повідомлення):" )   
    
async def question(message: types.Message, state: FSMContext):
    id_user = int(Seseeons_admin[message.from_user.id]["data"][1])
    blok[id_user] = message.text
    sqlite_db.blok_unblok( int(Seseeons_admin[message.from_user.id]["data"][1]), blok )
    # sti = open("handlers/stikers/Arrested.tgs", "rb")
    # await bot.send_sticker(message.from_user.id, sticker = sti)
    await message.answer("Корестувач з id : \"{}\" був заблокований!!!!😈".format(Seseeons_admin[message.from_user.id]["data"][1]))
    await state.finish()

#@dp.callback_query_handler(Text(contains="Заблокувати"))
async def Unblock_admin(cb: types.CallbackQuery):
    data = cb.data.split("/")
    id = int(data[1])
    del blok[id]
    sqlite_db.blok_unblok( id, blok )
    admin_kb.client_user(id)
    
    await bot.edit_message_reply_markup(cb.message.chat.id, cb.message.message_id, cb.inline_message_id, reply_markup=admin_kb.admin_data)
    # sti = open("handlers/stikers/Unblok.tgs", "rb")
    # await bot.send_sticker(cb.from_user.id, sticker = sti)
    







async def send_adver(message: types.Message, state: FSMContext):

    tmp = await sqlite_db.send_users_adver()
    for id in tmp:
        await bot.send_message(id, 
            md.text(
                md.bold( message.text ),
                sep='\n',
            ), 
            parse_mode=ParseMode.MARKDOWN
        )
    
    await state.finish()
    await message.answer("Сообщение разослано!", reply_markup = admin_kb.admin_Menu)

id = 0

async def Adver(cb: types.CallbackQuery):
    global id
    data = cb.data.split("/")
    id = data[1]
    await cb.message.answer("Веди що ти хочеш відправти користувачу з таким іd: {}".format(id))
    await Advert.advert.set()
    

async def send_message(message: types.Message, state: FSMContext):
    global id
    await bot.send_message(id, message.text)
    await state.finish()
    await message.answer("Повідомлення відправленно!")
    id = 0



def register_hendlers_client( dp : Dispatcher):
    
    dp.register_message_handler(check_my_Data, lambda message: not Bot.ctb.start_check_modul(message))

    dp.register_message_handler(admin_id, Text(equals="admin", ignore_case=True))
    dp.register_message_handler(check_admin, state = Admin.password)
    
    dp.register_message_handler( Client_used_bot, Text(equals="Всe клиенты", ignore_case=True))
    dp.register_message_handler( All_data, Text(equals="Все данные об клиентах", ignore_case=True))
    dp.register_message_handler( advertisement, Text(equals="Разослать объявление") ) 
    dp.register_message_handler( send_adver, state = advert.advert)
    dp.register_message_handler( exit, Text(equals="Вийти з адміна", ignore_case=True) )

    dp.register_callback_query_handler(ADD_admin, Text(contains="Ств"))
    dp.register_message_handler(cancel, text='st', state='*')
    dp.register_message_handler(cancel, Text(equals='st', ignore_case=True), state='*')
    dp.register_message_handler(add_month, state = Add_admin.month)
    dp.register_message_handler(Check_day_invalid_int, lambda message: not message.text.isdigit(), state = Add_admin.day)
    dp.register_message_handler(add_day, state = Add_admin.day)
    dp.register_message_handler(add_room, state = Add_admin.room)
    dp.register_message_handler( add_get_to_user_time,  state = Add_admin.time )
    dp.register_message_handler(add_group, state = Add_admin.gruop_or_one)
    dp.register_message_handler(add_name, state = Add_admin.name)
    # dp.register_message_handler(Check_number_invalid_int, lambda message: not message.text.isdigit(), state = FSMClient.number)
    dp.register_message_handler(Check_number_invalid_int, lambda message: not Bot.ctb.Check_numberDigts(message), state = Add_admin.number)
    dp.register_message_handler(load_number, state = Add_admin.number)
    dp.register_message_handler(Add_check_for_registration, state = Add_admin.check)

    dp.register_callback_query_handler(DELETE_admin, Text(contains="Ск"))
    dp.register_message_handler(select_data, state = Delete_admin.select_date)
    dp.register_message_handler(delet_user, state = Delete_admin.delet_time)

    dp.register_callback_query_handler(Delet_all_admin, Text(contains="Все"))


    dp.register_callback_query_handler(Block_admin, Text(contains="Блок"))
    dp.register_message_handler(question, state = Blok.man)


    dp.register_callback_query_handler(Unblock_admin, Text(contains="Розбл"))

    dp.register_callback_query_handler(Adver, Text(contains="Огол"))
    dp.register_message_handler(send_message, state = Advert.advert)