from aiogram.dispatcher.filters.builtin import Command
from create_bot import dp, bot
from aiogram import types, Dispatcher
from data_base import sqlite_db
from data_base.ORM import Time
from keyboards import client_kb, Bot
#from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime, time
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from google_sheet import sheet
import os







ALL_time = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "Ніч"]
Dinamic_dl_time = dict()

Seseeons = dict() #dict
Name_key_add = dict() #dict
# Name_key_delet = dict()
# Id_key = dict()
# Room = dict()

#ONE
Sum_for_one_and_red = 100
Sum_for_one_and_blue = 130
Sum_for_one_and_black = 140

#GROUP
Sum_for_group_and_red = 120
Sum_for_group_and_blue = 150
Sum_for_group_and_black = 160

#NIGHT
Night_red = 700
Night_blue = 1000
Night_black = 1200



class FSMClient(StatesGroup):
    month = State()
    day = State()  
    # downloan = State()
    room = State()
    time = State()
    gruop_or_one = State()
    name = State()
    number = State()
    check = State()

class FSMClient_add_time(StatesGroup):
    start = State()
    month = State()
    day = State()  
    room = State()
    time = State()
    gruop_or_one = State()
    check = State()

class FSMClient_delet(StatesGroup):
    select_data = State()
    select_id = State()
    delet_time = State()

#-----------------------------------     MENU    -------------------------------------------#


"""START"""
#@dp.message_handler(commands=['start'])
async def Start(message : types.Message):
    await bot.send_message(message.from_user.id, "Привітик я бот Repka. Якщо ти зі мною і Базовими правилами ще не знайомий, вибери в меню команду \"/Познайомитись\"\n\n" +
                                                    "Якщо виникають якісь проблеми з реєструванням, ти можеш зв'язатися з підтримкою ( \"/help\" )", reply_markup = client_kb.client_Menu ) 
    
    await message.answer("Ціни(за годину):\n" +
                        "$$$$$-САМ-$$$$$\n"+
                        "Червона -> 100\n" +
                        "Синя -> 130\n"+
                        "Чорна -> 140\n\n"
                        "$$$$$-Група-$$$$$\n" +
                        "Червона -> 120\n" +
                        "Синя -> 150\n"+
                        "Чорна -> 160\n\n"+
                        "^***Нічний час***^\n" +
                        "Червона -> 700\n" +
                        "Синя -> 1000\n" +
                        "Чорна -> 1200")


'''Help'''
#@dp.message_handler(commands=['help'])
async def Help(messege : types.Message): 
    await bot.send_message(messege.from_user.id, "Зв'язок з aдміністрацією\n" +
                                            "Telegram: @sybercore\n"+
                                            "Номер адміністрації: +380633681696\n"+
                                            "Номер для скарг: +380634405747\n" +
                                            "Telegram служба підтримки БОТА: @CS_Gnom")

'''Geolocation'''
#@dp.message_handler(commads=['Геолокація'])
async def Geolocation(message : types.Message):
    await bot.send_photo( message.from_user.id, open('handlers/client_img/Geolocation.png', 'rb'), 'Google Maps:\nhttps://goo.gl/maps/qT9EVhR3TrBmEkAE8')

#dp.message_handler( lambda message: not Bot.ctb.check_this_user(message) )
async def check_my_Data(message: types.Message):
    pass

'''Show_myData'''
#@dp.message_hamdler(commans=['Мої_дані'])
async def My_Data(message: types.Message):
    
    sqlite_db.sql_del_every_day()

    tmp_volue_nm_tm_dt_nmb, key = sqlite_db.get_data_fromSQL(message.from_user.id)
    

    Name_key_add[message.from_user.id] = key
    
    for name in key:
        
        id = tmp_volue_nm_tm_dt_nmb[name]["id"]
        date = tmp_volue_nm_tm_dt_nmb[name]["date"]
        time = tmp_volue_nm_tm_dt_nmb[name]["time"]
        room = tmp_volue_nm_tm_dt_nmb[name]["room"]
        if type(room) == list:

            for i in range(len(id)):
                
                    await bot.send_message(message.from_user.id,    "#_#_#_#_#_#_#_#_#{}#_#_#_#_#_#_#_#_#\n".format(id[i] + 1) +
                                                                    "{}:\n".format(name) + 
                                                                    "{} кімната:\n".format(room[i]) +
                                                                    "Записаний на {} такий час:\n".format(date[i]) +
                                                                    "{}".format(time[i]), reply_markup = client_kb.client_upgrad)

'''Acquainted'''
async def Acquainted(message: types.Message):
    await message.answer("Привітик я бот Repka. Я бронюю людей до нашої Бази на репетиції. У Бази також є деякі правила які знаходяться за посиланням")
    await message.answer("https://docs.google.com/document/d/1WNQf-t8viJQBMLyelR9C0dOPsP8d_si5/edit")
                        
    
    await message.answer("Зі мною ти можеш Бронювати і Видаляти час самостійно не телефонуючи до адмінів економлячи свій час.\n"+
                        "Команда \"/start\" відкриває головне Меню. Воно має такі кнопки->\n\n"+
                        "<-MENU->\n\n"+
                        "   \"/Забронювати_час\" - Натиснувши на цю кнопку ти можеш забронювати кого завгодно\n"+
                        "       (Коли ти почав бронювання свого часу і хочеш вийти до Меню, ти повинний зупинити реєстрацію командою \"скасувати\")\n"+
                        "   /Геолокація\" - По цій кнопці ти зможеш знайти нас\n"+
                        "   /help\" - Ця кнопка для з'єднання з Адміном.\n\n"+
                        "Після того як ти зареєструвався перший раз у твоє меню додасться нова кнопка \"/Мої_дані\"\n"+
                        "Натиснувши на неї, ти можеш переглядати на який час ти записаний.\n\n "+
                        "<-MENU->\n\n"+
                        "   /Додати\" - Натиснувши на цю кнопку ти можеш додати час на вже заброньованні особи\n"+
                        "   /Видалити\" - Завдяки цій кнопці ти можеш скасувати свій час\n"+
                        "       (Але пам'ятай за 24 години)")
                        

'''Schedule'''
async def Schedule(message: types.Message):
    await message.answer("https://docs.google.com/spreadsheets/d/14TTe8vZRzl63rJ2r91m8VOnV0aoL8yMdF4dqSIQ8PEg/edit#gid=0")
    # os.system("start https://docs.google.com/spreadsheets/d/14TTe8vZRzl63rJ2r91m8VOnV0aoL8yMdF4dqSIQ8PEg/edit#gid=0" )
#-----------------------------------     Check    -------------------------------------------#
"""Month"""
#@dp.message_handler(lambda message: not message.text.isdigit(), state = FSMClient.month)
#@dp.message_handler(lambda message: not Bot.ctb.Check_month(message.text, Seseeone[message.from_user.id]), state = FSMClient.month)
async def Check_month_invalid_int(message: types.Message):
    
    if message.text == "Щось інше" or message.text == "Січень":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

"""Day"""
#@dp.message_handler(lambda message: not message.text.isdigit(), state = FSMClient.month)
#@dp.message_handler(lambda message: not Check_day(message), state = FSMClient.month)
async def Check_day_invalid_int(message: types.Message):
    if message.text == "Не існуючий місяць день місяця":
        await message.reply("Перевірь правильність відповіді і впиши ще раз, те що ти хотів. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    elif message.text == "Більше двох місяців":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"скасувати\"")


"""Number"""
#@dp.message_handler(lambda message: not message.text.isdigit(), state = FSMClient.month)
#@dp.message_handler(lambda message: not Сheck_number_digits(message), state = FSMClient.month)
async def Check_number_invalid_int(message: types.Message):
    await message.reply("Проблема з номером, перевірть ще раз його. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

"""CHECK"""
#@dp.message_handler(lambda message: not Bot.ctb.Last_check(message, Seseeons[message.from_user.id]), state = FSMClient.check)
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




#---------------------------------      FSMClient     ---------------------------------------------#

'''START'''
#@dp.message_handler(commands = [Зареєстурватися], state = None)
async def cm_start(message : types.Message):
    # Bot.ctb.All_name = [message.from_user.first_name, message.from_user.last_name, message.from_user.username]
    time = datetime.now()
    Seseeons[message.from_user.id]= { 
                                "id": message.from_user.id,
                                "time_user_regist": time,
                                "data" : {
                                            "day": 0, 
                                            "month": 0, 
                                            "year": 0
                                                        },
                                "room" : 0,
                                "time" : [],
                                "number" : 0,
                                "user_write_name": '',
                                "Group_or_one": '',
                                "sum_order" : 0,
                                "Name":{
                                            "firts_name": message.from_user.first_name,
                                            "last_name": message.from_user.last_name,
                                            "user_name" : message.from_user.username
                                                                                            }
                                }
    Bot.ctb.write_config("logging/start.log", Seseeons)
    # if Bot.ctb.ID_user[0] == message.from_user.id:
    #     Bot.ctb.time.clear()

    
    await FSMClient.month.set()
    await bot.send_message(message.from_user.id, "Виберіть Місяць:", reply_markup=client_kb.client_month)

'''STOP'''    
# @dp.message_handler(state='*', commands='stop')
# @dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    del Seseeons[message.from_user.id]
    await bot.send_message(message.from_user.id, "Ok, реєстрація скасована.", reply_markup = client_kb.client_Menu)   
        
#@dp.message_handler(content_types = ['month'], state = FSMClient.month)
async def load_month(message: types.Message, state: FSMContext):
    
    if await Bot.ctb.Check_month(message, Seseeons[message.from_user.id]):
        await FSMClient.next()
        await bot.send_message(message.from_user.id, "Виберіть День:", reply_markup=client_kb.client_day_kb)

    elif message.text == "Щось інше" or message.text == "Січень":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

#@dp.message_handler(state = FSMClient.day)
async def load_day(message: types.Message, state: FSMContext):
    if await Bot.ctb.Check_day(message, Seseeons[message.from_user.id]):
        await FSMClient.next()
        await bot.send_message(message.from_user.id, "Вибери кімнату:", reply_markup = client_kb.client_rkb)

    elif message.text == "Не існуючий місяць день місяця":
        await message.reply("Провірь правильність відповіді і впиши ще раз, те що ти хотів. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    elif message.text == "Більше двох місяців":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    
#@dp.message_handler(state = FSMClient.room)
async def load_room(message: types.Message, state: FSMContext):
    # Seseeons[message.from_user.id]['room'] = message.text
    
    room = await Bot.ctb.Check_room(message, Seseeons[message.from_user.id])

    if room:
        if await Bot.ctb.Check_time(message, Seseeons[message.from_user.id]):
            await FSMClient.next()
            await bot.send_message( message.chat.id,
            md.text( 
                md.text( md.bold("Формат введення") ),
                md.text( "Одна кнопка дорівнює одній годині:\n" + 
                                    "13:00 -> 13:00 - 14:00\n" + 
                                    "Якщо потрібно 3 години:\n" + 
                                    "Натискаємо 13:00, 14:00 і 15:00"),
                                    sep='\n',
                                    ), parse_mode=ParseMode.MARKDOWN 
                                    )
            await bot.send_message(message.from_user.id, "Вибери час:", reply_markup = client_kb.client_tkb)

        else:
            await message.answer("Нажаль цей день зайнятий на це число. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

    else:
        await message.reply("Провірь правильність відповіді і впиши ще раз. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

msg_get_to_user_time = 0

#@dp.message_handler(content_types = ["text"], state = FSMClient.time) 
async def get_to_user_time(message: types.Message, state: FSMContext):
    global msg_get_to_user_time

    time =  Seseeons[message.from_user.id]
    # await bot.delete_message(message.from_user.id, message.from_user.id)
    if len(time["time"]) >= 1:
        await msg_get_to_user_time.delete()
    # if len(time["time"]) == 2:
    #     time["time"].pop(len(time["time"]) - 1)

    if message.text == "Далі👉" and time["time"] != []:

        tmp = ["Група", "Сам"]
        client_kb.registed_name(tmp)
        # Bot.change_of_time(time["time"])
        await FSMClient.next()
        await bot.send_message(message.from_user.id, "Ти будеш займтися з групою чи сам?", reply_markup= client_kb.client_NAME)
        
    elif message.text == "Очистити все":
        Seseeons[message.from_user.id]["time"] = []
        await bot.send_message(message.from_user.id, "Весь час стерто, ти можеш вибрати інший час", reply_markup = client_kb.client_tkb)
        
    elif message.text in ALL_time:
        if Bot.ctb.Check_NoRepeat(message, Seseeons[message.from_user.id]):
            time["time"].append(  message.text )
        time["time"] = Bot.numbering(time["time"])

        await bot.delete_message(message.from_user.id, message.message_id)
        # await bot.delete_message(message.from_user.id, bot.message_id)
        msg_get_to_user_time = await message.answer(time["time"])
        # if len(time["time"]) > 1 and "Ніч" not in time["time"]:
            
        #     msg_get_to_user_time = await message.answer(Bot.trans_list_in_str(time["time"]))
        
        # elif "Ніч" in time["time"]:
        #     time["time"].remove("Ніч")
        #     msg_get_to_user_time = await message.answer(Bot.trans_list_in_str(time["time"]))
        #     await message.answer("І Ніч")
        
        # elif len(time["time"]) == 1:
        #     await message.answer("з {}".format(time["time"][0]))
        #await bot.send_message(message.from_user.id, "Можливо ще якийсь чвс?\nЯкщо ні тисни \"Далі\" ", reply_markup = client_kb.client_tkb)

    else:
        await bot.send_message(message.from_user.id, "Вибири той час який знаходиться в низу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"", reply_markup = client_kb.client_tkb)
        
# @dp.message_handler( state = FSMClient.gruop_or_one)
async def load_group(message: types.Message, state: FSMContext):
    tmp = ["Група", "Сам"]
    time = Seseeons[message.from_user.id]["time"]
    room = Seseeons[message.from_user.id]["room"] 

    if message.text in tmp:
        Seseeons[message.from_user.id]["Group_or_one"] = message.text
        all_sum = 0

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
        
    else:
        await message.answer("Вибири те що знаходиться в низу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
        return

    await FSMClient.next()
    await bot.send_message(message.from_user.id, "Введи ім'я або назву групи на кого записати цей час", reply_markup= ReplyKeyboardRemove())

#@dp.message_handler(state = FSMClient.name)
async def load_name(message: types.Message, state: FSMContext):
    for i in message.text:
        try:
            if int == type(int(i)):
                await message.answer("Веди ім'я без цифр;)")
                return
        except:
            if i == "/" and len(message.text) <= 12:
                await message.answer("Веди ім'я без цифр;)")
                return
    async with state.proxy() as data:
        Seseeons[message.from_user.id]["user_write_name"] = message.text
        data['name'] = message.text
    await FSMClient.next()
    await bot.send_message(message.from_user.id, "Введи номер телефону")

#@dp.message_handler(state = FSMClient.number)
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
                md.text( 'Провірь свої дані:' ),
                md.text( md.bold(Seseeons[message.from_user.id]["Group_or_one"]) ),
                md.text( "Ім'я:", md.bold(Seseeons[message.from_user.id]["user_write_name"]) ),
                md.text( 'Номер:', Seseeons[message.from_user.id]["number"] ),
                md.text( 'Дата:', md.bold(str(day)), ".", md.bold(str(month)) ),
                md.text( "Кімната:", md.bold(Seseeons[message.from_user.id]['room']) ),
                md.text( "Час:", md.bold(*Seseeons[message.from_user.id]['time'] ) ),
                md.text( "Сума оплати:", md.bold( Seseeons[message.from_user.id]["sum_order"] ) ),
                sep='\n',
            ), 
            reply_markup=client_kb.client_yn_kb,
            parse_mode=ParseMode.MARKDOWN
        )    
        
        
    
    await FSMClient.next()

#@dp.message_handler(state = FSMClient)
async def Last_check_for_registration(message: types.Message, state: FSMContext):
    if await Bot.ctb.Last_check(message, Seseeons[message.from_user.id]):
            
        Bot.ctb.write_config("logging/finish.log", Seseeons)
        # async with state.proxy() as data:
        #     await message.reply( str(data) )
        # await sqlite_db.sql_add_command(Seseeons, message)
        
        await bot.send_message( message.from_user.id, 
                md.text(
                    md.text("Тебе успішно зареєстровано."),
                    md.text(  md.bold("Оплата здійснюється на базі"), "!" ),
                    sep='\n'),
                    reply_markup =  client_kb.client_Menu, parse_mode=ParseMode.MARKDOWN )
        await message.answer("Радий, що зміг допомогти тобі;)")
        await message.answer("Обов'язково провірь себе у розкладі\nhttps://docs.google.com/spreadsheets/d/14TTe8vZRzl63rJ2r91m8VOnV0aoL8yMdF4dqSIQ8PEg/edit#gid=0")
        del Seseeons[message.from_user.id]
        await state.finish()

    elif message.text == "Зайнятий час":
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


@dp.callback_query_handler(text = "client_month")
async def all_changes(сlb : types.CallbackQuery):
    print(сlb)




#-------------------------------------------------  Add  -----------------------------------------------#

#@dp.message_handler(commands=['Додати'])
async def select_username(message: types.Message):
    client_kb.registed_name(Name_key_add[message.from_user.id])
    await bot.send_message(message.from_user.id, "Вибери на яке ім'я записувати доданий час", reply_markup = client_kb.client_NAME)
    await FSMClient_add_time.start.set()

#@dp.message_handler(Text(equals=Name_key))
async def add_time_to_sql(message: types.Message):
    if message.text in Name_key_add[message.from_user.id]:
        name = message.text
    else:
        await message.answer("Вибири те що знаходиться в низу.\nЯкщо хочеш скасувати реєстрацією введи \"скасувати\"")
        return
        і
    tmp_volue_nm_tm_dt_nmb, key = sqlite_db.get_data_fromSQL(message.from_user.id)

    date = tmp_volue_nm_tm_dt_nmb[message.text]["date"]
    time = tmp_volue_nm_tm_dt_nmb[message.text]["time"]
    room = tmp_volue_nm_tm_dt_nmb[message.text]["room"]
    number = tmp_volue_nm_tm_dt_nmb[message.text]["number"]
    time = datetime.now()

    Seseeons[message.from_user.id]= { 
                                    "id": message.from_user.id,
                                    "time_user_regist": time,
                                    "time_user_last": date,
                                    "data" : {
                                                "day": 0, 
                                                "month": 0, 
                                                "year": 0
                                                            },
                                    "room" : room,
                                    "time" : [],
                                    "number" : number,
                                    "user_write_name": message.text,
                                    "Group_or_one": '',
                                    "sum_order" : 0,
                                    "Name": {
                                                "firts_name": message.from_user.first_name,
                                                "last_name": message.from_user.last_name,
                                                "user_name" : message.from_user.username
                                                                                                }
                                            
                                    }
    await FSMClient_add_time.next()
    await bot.send_message(message.from_user.id, "Вибери Місяць.", reply_markup = client_kb.client_month)

#@dp.message_handler(content_types = ['month'], state = FSMClient_add_time.month)
async def add_month(message: types.Message, state: FSMContext):
    if await Bot.ctb.Check_month(message, Seseeons[message.from_user.id]):
        await FSMClient_add_time.next()
        await bot.send_message(message.from_user.id, "Виберіть День:", reply_markup=client_kb.client_day_kb)

    elif message.text == "Щось інше" or message.text == "Січень":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

#@dp.message_handler(state = FSMClient_add_time.day)
async def add_day(message: types.Message, state: FSMContext):

    if await Bot.ctb.Check_day(message, Seseeons[message.from_user.id]):
        await FSMClient_add_time.next()
        await bot.send_message(message.from_user.id, "Вибери кімнату:", reply_markup = client_kb.client_rkb)

    elif message.text == "Не існуючий місяць день місяця":
        await message.reply("Провірь правильність відповіді і впиши ще раз, те що ти хотів. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    elif message.text == "Більше двох місяців":
        await message.reply("Вибирай те що знизу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
    else:
        await message.reply("Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

#@dp.message_handler(state = FSMClient_add_time.room)
async def add_room(message: types.Message, state: FSMContext):
    room = await Bot.ctb.Check_room(message, Seseeons[message.from_user.id])
    check_room = await Bot.ctb.Check_time(message, Seseeons[message.from_user.id])

    if room and check_room:
        await FSMClient_add_time.next()
        await bot.send_message(message.from_user.id, "Вибери час:", reply_markup = client_kb.client_tkb)

    elif not check_room:
        await message.answer("Нажаль цей день зайнятий на це число. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

    else:
        await message.reply("Провірь правильність відповіді і впиши ще раз, те що ти хотів. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")

#@dp.message_handler(content_types = ["text"], state = FSMClient_add_time.time) 
async def add_get_to_user_time(message: types.Message, state: FSMContext):
    
    time =  Seseeons[message.from_user.id]

    if message.text == "Далі👉" and time["time"] != []:

        tmp = ["Група", "Сам"]
        client_kb.registed_name(tmp)
        # Bot.change_of_time(time["time"])
        await FSMClient_add_time.next()
        await bot.send_message(message.from_user.id, "Ти будеш займтися з групою чи сам?", reply_markup= client_kb.client_NAME)
        
    elif message.text == "Очистити все":
        Seseeons[message.from_user.id]["time"] = []
        await bot.send_message(message.from_user.id, "Весь час стерто, ти можеш вибрати інший час", reply_markup = client_kb.client_tkb)
        
    elif message.text in ALL_time:
        if Bot.ctb.Check_NoRepeat(message, Seseeons[message.from_user.id]):
            time["time"].append(  message.text )
        time["time"] = Bot.numbering(time["time"])

        await bot.delete_message(message.from_user.id, message.message_id)
        # await bot.delete_message(message.from_user.id, bot.message_id)
        await message.answer(time["time"])
        # if len(time["time"]) > 1 and "Ніч" not in time["time"]:
        #     await message.answer(Bot.trans_list_in_str(time["time"]))
        
        
        # elif "Ніч" in time["time"]:
        #     time["time"].remove("Ніч")
        #     await message.answer(Bot.trans_list_in_str(time["time"]))
        #     await message.answer("І Ніч")
        
        #await bot.send_message(message.from_user.id, "Можливо ще якийсь чвс?\nЯкщо ні тисни \"Далі\" ", reply_markup = client_kb.client_tkb)

    else:
        await bot.send_message(message.from_user.id, "Вибири той час який знаходиться в низу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"", reply_markup = client_kb.client_tkb)

# @dp.message_handler( state = FSMClient_add_time.gruop_or_one)
async def add_group(message: types.Message, state: FSMContext):
    tmp = ["Група", "Сам"]
    time = Seseeons[message.from_user.id]["time"]
    room = Seseeons[message.from_user.id]["room"]
    if message.text in tmp:
        Seseeons[message.from_user.id]["Group_or_one"] = message.text

        if message.text == "Група":

            if room == "Синя":
                sum = Sum_for_group_and_blue
                all_sum = 0  

                for i in time:

                    if i == "Ніч":
                        all_sum += Night_blue
                    
                    else:    
                        all_sum += sum

            if room == "Червона":
                    sum = Sum_for_group_and_red
                    all_sum = 0  

                    for i in time:

                        if i == "Ніч":
                            all_sum += Night_red
                    
                        else:    
                            all_sum += sum

            Seseeons[message.from_user.id]["sum_order"] = all_sum

        elif message.text == "Сам":

            if room == "Синя":
                sum = Sum_for_one_and_blue
                all_sum = 0  

                for i in time:

                    if i == "Ніч":
                        all_sum += Night_blue
                    
                    else:    
                        all_sum += sum

            if room == "Червона":
                    sum = Sum_for_one_and_red
                    all_sum = 0  

                    for i in time:

                        if i == "Ніч":
                            all_sum += Night_red
                    
                        else:    
                            all_sum += sum

            Seseeons[message.from_user.id]["sum_order"] = all_sum
        
    else:
        await message.answer("Вибири те що знаходиться в низу. Якщо хочеш скасувати реєстрацією введи \"скасувати\"")
        return


    day = Seseeons[message.from_user.id]["data"]['day']
    month = Seseeons[message.from_user.id]["data"]['month']
    for i in range(10):
        if i == day:
            day = "0" + str(i)
        if i == month:
            month = "0" + str(i)
    
        

    await FSMClient_add_time.next()
    await bot.send_message( message.chat.id, 
            md.text(
                md.text( 'Провірь свої дані:' ),
                md.text( md.bold(Seseeons[message.from_user.id]["Group_or_one"]) ),
                md.text( "Ім'я:", md.bold(Seseeons[message.from_user.id]["user_write_name"]) ),
                md.text( 'Номер:', Seseeons[message.from_user.id]["number"] ),
                md.text( 'Дата:', md.bold(str(day)), ".", md.bold(str(month)) ),
                md.text( "Кімната:", md.bold(Seseeons[message.from_user.id]["room"]) ),
                md.text( "Час:", md.bold(*Seseeons[message.from_user.id]["time"]) ),
                md.text( "Сума оплати:", md.bold( Seseeons[message.from_user.id]["sum_order"] ) ),
                md.text( "Якщо все правильно натисни \"ТАК\"\n\
                        В іншому випдку \"НІ\"" ),
                sep='\n',
            ), 
            reply_markup=client_kb.client_yn_kb,
            parse_mode=ParseMode.MARKDOWN
        )

#@dp.message_handler(state = FSMClient)
async def Add_check_for_registration(message: types.Message, state: FSMContext):
    if await Bot.ctb.Last_check(message, Seseeons[message.from_user.id]):
            
        Bot.ctb.write_config("logging/finish.log", Seseeons)
        # async with state.proxy() as data:
        #     await message.reply( str(data) )
        # await sqlite_db.sql_add_command(Seseeons, message)
        
        await bot.send_message( message.from_user.id, 
                md.text(
                    md.text("Тебе успішно зареєстровано."),
                    md.text(  md.bold("Оплата здійснюється на базі"), "!" ),
                    sep='\n'),
                    reply_markup =  client_kb.client_Menu, parse_mode=ParseMode.MARKDOWN )
        await message.answer("Радий, що зміг допомогти тобі;)")
        await message.answer("Обов'язково провірь себе у розкладі\nhttps://docs.google.com/spreadsheets/d/14TTe8vZRzl63rJ2r91m8VOnV0aoL8yMdF4dqSIQ8PEg/edit#gid=0")
        del Seseeons[message.from_user.id]
        await state.finish()

    elif message.text == "Зайнятий час":
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


#-------------------------------------------------   Delete  -----------------------------------------------#


#@dp.message_handler(commands = ["Скасувати"])    
async def search_for_del_time(message: types.Message):
    tmp_volue_nm_rm_tm_dt_nmb, key = sqlite_db.get_data_fromSQL(message.from_user.id)

    Seseeon = dict()
    Seseeons[message.from_user.id] = {}


    tmp = []
    
    for name in key:
        Seseeon[name]= { 
                "time_user_regist": datetime.now(),                           
                "id" : [],
                "date": [],
                "room": [],
                "time": [],
                "group": []
                            }
        Seseeons[message.from_user.id].update(Seseeon)


    for name in key:
        i = 0
        id = []
        for time1 in tmp_volue_nm_rm_tm_dt_nmb[name]["time"]:
            date_user = tmp_volue_nm_rm_tm_dt_nmb[name]["date"][i]
            date_now = datetime.now()
            tm = []

            for time2 in time1:
                if time2 == "Ніч":
                    time2 = "23:00"
                    t = time.fromisoformat(time2)
                    time2 = "Ніч"
                else:
                    t = time.fromisoformat(time2)

                
                a = datetime(date_user.year, date_user.month, date_user.day, t.hour)
                zum = a - date_now

                if zum.days >= 1:
                    tm.append(time2)

                    if name not in tmp:
                        tmp.append(name)
                    
                    if i+1 not in Seseeons[message.from_user.id][name]["id"]:
                        Seseeons[message.from_user.id][name]["date"].append(tmp_volue_nm_rm_tm_dt_nmb[name]["date"][i])
                        Seseeons[message.from_user.id][name]["room"].append(tmp_volue_nm_rm_tm_dt_nmb[name]["room"][i])
                        Seseeons[message.from_user.id][name]["group"].append(tmp_volue_nm_rm_tm_dt_nmb[name]["group"][i])
                        Seseeons[message.from_user.id][name]["id"].append(tmp_volue_nm_rm_tm_dt_nmb[name]["id"][i] + 1)
                    
                    if time2 == time1[len(time1) - 1]:
                        Seseeons[message.from_user.id][name]["time"].append( tm )  
                    
                    
            i += 1

    if tmp != []:
        client_kb.registed_name(tmp)
        await FSMClient_delet.select_data.set()
        await bot.send_message(message.from_user.id, "Вибери на яке ім'я у яких ти зможеш скасувати запис", reply_markup = client_kb.client_NAME)
    else:
        await message.answer("Пробач, але ти не можеш скасувати свій час, томущо до твого часу залишилося менше доби. Натисни \"/start\", щоб повернутися до головного меню")

#@dp.message_handler(lambda message: Text(equals = Name_key[message.from_user.id]["name"]))
async def select_id_delet(message: types.Message, state: FSMContext):
    if message.text in Name_key_add[message.from_user.id]:
        name = message.text
    else:
        await message.answer("Вибири те що знаходиться в низу.\nЯкщо хочеш скасувати реєстрацією введи \"скасувати\"")
        return
        
    
    name = message.text
    client_kb.registed_name(Seseeons[message.from_user.id][name]["id"])
    Name_key_add[message.from_user.id] = name
    await FSMClient_delet.next()
    await bot.send_message(message.from_user.id, "Вибери номер для видалення", reply_markup = client_kb.client_NAME)

#@dp.message_handler(lambda message: Text(equals = Id_key[message.from_user.id]))
async def select_id(message: types.Message, state: FSMContext):
    if message.text in Seseeons[message.from_user.id][Name_key_add[message.from_user.id]]["id"]:
        name = message.text
    else:
        await message.answer("Вибири те що знаходиться в низу.\nЯкщо хочеш скасувати реєстрацією введи \"скасувати\"")
        return
    
    name = Name_key_add[message.from_user.id]

    id = Seseeons[message.from_user.id][name]["id"].index(message.text)
    Seseeons[message.from_user.id][name]["id"] = id
    tmp = Dinamic_dl_time[message.from_user.id] = Seseeons[message.from_user.id][name]["time"][id]
    Seseeons[message.from_user.id][name]["time"] = []

    client_kb.Dinamic_dl_kb(tmp)

    await FSMClient_delet.next()

    await bot.send_message(message.from_user.id, "Вибери час який ти хочеш видалити!", reply_markup = client_kb.client_tkb)
    
#@dp.message_handler(lambda message: Text(equals = Id_key[message.from_user.id]))
async def del_time(message: types.Message, state: FSMContext):
    dice = ["🗂"]


    name = Name_key_add[message.from_user.id]
    id = Seseeons[message.from_user.id][name]["id"]
    Dinamic_dl_time[message.from_user.id]

    
    
    if message.text == "Далі👉" and Seseeons[message.from_user.id][name]["time"] != []:
        
        time = Seseeons[message.from_user.id][name]["time"]
        date = Seseeons[message.from_user.id][name]["date"][id]
        room = Seseeons[message.from_user.id][name]["room"][id]

        # await message.answer_dice(emoji="🗂")
        sqlite_db.sql_del(message.from_user.id, time, date, name, room)
        await message.answer("Зачикай ще трішки. Майже видалив)")
        sheet.delet_from_basedate(Seseeons[message.from_user.id][name], id)
        Bot.ctb.start_check_modul(message)
        

        await bot.send_message(message.from_user.id, "Час {} був видаленний успішно!".format(Seseeons[message.from_user.id][name]["time"]), reply_markup = client_kb.client_Menu)
        del Seseeons[message.from_user.id]
        await state.finish()
        
        
    elif message.text == "Очистити все":
        Seseeons[message.from_user.id][name]["time"] = []
        await bot.send_message(message.from_user.id, "Весь час стерто, ти можеш вибрати інший час", reply_markup = client_kb.client_tkb)
        
    elif message.text in Dinamic_dl_time[message.from_user.id]:
        if Bot.ctb.Check_NoRepeat(message, Seseeons[message.from_user.id][name]):
            Seseeons[message.from_user.id][name]["time"].append(message.text)
        await bot.delete_message(message.from_user.id, message.message_id)
        await message.answer(Seseeons[message.from_user.id][name]["time"])

    else:
        await bot.send_message(message.from_user.id, "Вибири той час який знаходиться є знизу", reply_markup = client_kb.client_tkb)



#-------------------------------------------------   Повернення до головного меню  -----------------------------------------------#



async def Сancel(message: types.Message):
    await message.answer('Головне меню', reply_markup = client_kb.client_Menu)
    





#--------------------------------------------------    ALL   --------------------------------------------------------#

# @dp.message_handler()
async def Message(message : types.Message):
    await message.reply("Я не розумію, що ти маєш на увазі, але якщо хочеш зареєструватися введи \"/start\"")





def register_hendlers_client(dp : Dispatcher):
    
    #----------------------------------########################################----------------------------------------------#
    #                                               MENU "/start"
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # dp.register_message_handler(check_my_Data, lambda message: not Bot.ctb.start_check_modul(message))

    dp.register_message_handler(Start, commands = ['start'])
    dp.register_message_handler(cm_start, commands = ['Забронювати_час'], state = None)
    dp.register_message_handler(My_Data, commands = ['Мої_дані'])
    dp.register_message_handler(Help, commands = ['help'])
    dp.register_message_handler(Geolocation, commands = ['Геолокація'])
    dp.register_message_handler(Acquainted, commands = ['Познайомитись'])
    dp.register_message_handler(Schedule, commands = ['Розклад'])


    #----------------------------------########################################----------------------------------------------#
    #                                         FSMClient  "/Зареєструватися"
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    dp.register_message_handler(cancel_handler, text='скасувати', state='*')
    dp.register_message_handler(cancel_handler, Text(equals='скасувати', ignore_case=True), state='*')



    dp.register_message_handler(load_month, state = FSMClient.month)
    dp.register_message_handler(Check_day_invalid_int, lambda message: not message.text.isdigit(), state = FSMClient.day)
    dp.register_message_handler(load_day, state = FSMClient.day)
    dp.register_message_handler(load_room, state = FSMClient.room)
    dp.register_message_handler( get_to_user_time,  state = FSMClient.time)
    dp.register_message_handler( load_group, state = FSMClient.gruop_or_one )
    dp.register_message_handler(load_name, state = FSMClient.name)
    # dp.register_message_handler(Check_number_invalid_int, lambda message: not message.text.isdigit(), state = FSMClient.number)
    dp.register_message_handler(Check_number_invalid_int, lambda message: not Bot.ctb.Check_numberDigts(message), state = FSMClient.number)
    dp.register_message_handler(load_number, state = FSMClient.number)
    # dp.register_message_handler(last_check, lambda message: not Bot.ctb.Last_check(message, Seseeons[message.from_user.id]), state = FSMClient.check)
    dp.register_message_handler(Last_check_for_registration, state = FSMClient.check)

    #______________________________________#####################################_____________________________________________#
    #                                         FSMClient_add_time  "/Додавання"
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    

    dp.register_message_handler(select_username, commands=['Додати'])
    

    dp.register_message_handler(add_time_to_sql, state = FSMClient_add_time.start )
    
    dp.register_message_handler(add_month, state = FSMClient_add_time.month)
    dp.register_message_handler(Check_day_invalid_int, lambda message: not message.text.isdigit(), state = FSMClient_add_time.day)
    dp.register_message_handler(add_day, state = FSMClient_add_time.day)
    dp.register_message_handler(add_room, state = FSMClient_add_time.room)
    dp.register_message_handler( add_get_to_user_time,  state = FSMClient_add_time.time )
    dp.register_message_handler(add_group, state = FSMClient_add_time.gruop_or_one)
    # dp.register_message_handler(last_check, lambda message: not Bot.ctb.Last_check(message, Seseeons[message.from_user.id]), state = FSMClient_add_time.check)
    dp.register_message_handler(Add_check_for_registration, state = FSMClient_add_time.check)


    #______________________________________#####################################_____________________________________________#
    #                                         FSMClient_add_time  "/Видалення"
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    dp.register_message_handler(search_for_del_time, commands = ["Видалити"])


    dp.register_message_handler(select_id_delet, state= FSMClient_delet.select_data)
    dp.register_message_handler(select_id, state= FSMClient_delet.select_id)
    dp.register_message_handler(del_time, state= FSMClient_delet.delet_time) 

    #______________________________________#####################################_____________________________________________#
    #                                         FSMClient_add_time  "/Видалення"
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    dp.register_message_handler(Сancel, commands = ["Головне_Меню"])

    #_____________________________________######################################___________________________________________#
    #                                                     All
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    dp.register_message_handler(Message, content_types=['text'])

    #########################################################################################################################
    

