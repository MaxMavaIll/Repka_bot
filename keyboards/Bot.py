import math
from re import T
from aiogram import types
from pyasn1_modules.rfc2459 import Name
from google_sheet import sheet, funSheet
from keyboards import client_kb
from datetime import datetime, date
from create_bot import bot
from data_base import sqlite_db
import phonenumbers as ch_number
import asyncio
from random import randint
from config import blok, admin

year_now = datetime.now().year
month_now = datetime.now().month
day_now = datetime.now().day

First_day_registration = date(year_now, month_now, day_now)
# Last_day_registration = date(year_now + 2, month_now, day_now)
# duration_day = (Last_day_registration-First_day_registration).day
print()

def check_free_time(time):
    for i in range(len(time)):
        if time[i] == 0:
            return True
    return False





class My_Telegram_Bot:

    def start_check_modul(self, message):
        global month_now

        client_kb.month_kb(month_now)
        sqlite_db.check_id(message.from_user.id)
        sqlite_db.sql_del_every_day()
        sqlite_db.downloand_blok(blok)
        return True

    #_______________________________________________Функії для різних провірок___________________________________________________#

    async def Check_month(self, message, seseeons):

        def conv_month_to_gital(name_month):

            tmp_month = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
                         "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
            for i in range(len(tmp_month)):
                if name_month == tmp_month[i]:
                    return i+1

        global year_now, month_now, day_now

        seseeons["data"]["month"] = conv_month_to_gital(message.text)

        Konst_Day = 63  # константа вказує на кількість днів для зареєстрування

        for i in range(12):  # провірка місяця, чи існує даний користувачем місяць
            if seseeons["data"]["month"] == i+1:

                tmp_year = year_now

                if month_now == 11 and seseeons["data"]["month"] == 1:
                    tmp_year += 1
                elif month_now == 12 and (seseeons["data"]["month"] == 1 or seseeons["data"]["month"] == 2):
                    tmp_year += 1

                seseeons["data"]["year"] = tmp_year

                tmp = {
                    "year": seseeons["data"]["year"],
                    "month": seseeons["data"]["month"]
                }
                day_on_month = funSheet.check_month(tmp, False)

                if day_on_month < day_now:
                    day_now = day_on_month

                user_days = date(tmp_year, seseeons["data"]["month"], day_now)
                # кількість днів "сьогодні - вибраний день"
                user_month = (user_days-First_day_registration).days

                client_kb.day_kb(
                    day_on_month, seseeons["data"]["month"], month_now, day_now, Konst_Day-62)

                if (user_month >= 0) and (user_month <= Konst_Day):
                    return True
        message.text == "Щось інше"
        return False

    async def Check_day(self, message, seseeons):

        def conv_month_to_gital(number_month, name_month):
            tmp = []
            for i in range(number_month):
                tmp.append(str(i+1))
                if tmp[i] == name_month:
                    return i+1

        tmp = {
            "year": seseeons["data"]["year"],
            "month": seseeons["data"]["month"]
        }

        number_month = funSheet.check_month(tmp, False)

        global year_now, month_now, day_now
        seseeons["data"]["day"] = conv_month_to_gital(
            number_month, message.text)
        Konst_Day = 63

        tmp_year = year_now

        if month_now == 11 and seseeons["data"]["month"] == 1:
            tmp_year += 1

        elif month_now == 12 and (seseeons["data"]["month"] == 1 or seseeons["data"]["month"] == 2):
            tmp_year += 1

        if number_month >= seseeons["data"]["day"]:

            user_days = date(
                tmp_year, seseeons["data"]["month"], seseeons["data"]["day"])
            user_month = (user_days-First_day_registration).days

            if (user_month >= 0) and (user_month <= Konst_Day):
                return True
            # else:
            #     message.text = "Не існуючий місяць день місяця"
            #     return False
        message.text = "Більше двох місяців"
        return False

    async def Check_room(self, message, seseeons):
        seseeons['room'] = message.text
        day = seseeons["data"]["day"]

        if seseeons["room"] == "Червона":
            return True

        elif seseeons["room"] == "Синя":
            return True


        elif seseeons["room"] == "Чорна":
            return True
        else:
            return False

    async def Check_time(self, message, Seseeons):
        print("Check_time")
        dice = ["🎲", "🎳", "🎯"]

        day = Seseeons["data"]["day"]
        month = Seseeons["data"]["month"]
        year = Seseeons["data"]["year"]

        month_year = str(month) + "." + str(year)
       # Seseeons["time_user_regist"] = date(year, month, day) #заведення часу в timestamp
        await message.answer_dice(emoji=dice[randint(0, 2)])
        await sheet.check_existence_Month(month_year, Seseeons)
        await message.answer("Зачекай ще трішки. Перевіряю час)")
        time = await sheet.Check_batle(Seseeons, month_year)
        check = check_free_time(time)
        
        if check == True:
            client_kb.Dinamic_kb(time, Seseeons)
            return True
        else:
            message.text = "Зайнто весь день"
            return False

    def Check_NoRepeat(self, message, seseeons):

        for i in range(len(seseeons["time"])):
            if message.text == seseeons["time"][i]:
                return False
        return True

    def Check_numberDigts(self, message):

        try:
            x = ch_number.parse(message.text, "UA")

            if ch_number.is_valid_number(x) and ch_number.is_possible_number(x):

                return True
            else:
                return False

        except:
            return False

    async def Last_check(self, message, Seseeons):
        dice = ["📝"]
        day = Seseeons["data"]["day"]
        month = Seseeons["data"]["month"]
        year = Seseeons["data"]["year"]
        name_title_m_y = str(month) + "." + str(year)
        day_regist = date(year, month, day)
        day_now = date.today()
        sum = day_regist - day_now

        # await message.answer_dice(emoji=dice[0])
        if message.text == "Так":
            await message.answer("Ок. Записую ...")
            if sheet.Exele_sheet_write(Seseeons, name_title_m_y, True):
                await message.answer("Зачекай ще трішки майже записав")
                sheet.Exele_sheet_write(Seseeons, name_title_m_y)
                sqlite_db.sql_add_command(Seseeons)
                if sum.days <= 2:
                    await send_admin(Seseeons)
                ctb.start_check_modul(message)
                return True

            else:
                message.text = "Зайнятий час"
                return False

        elif message.text == "Ні":
            return False

    ##########################################################################################################################################

    def KeyboardButton(self, add_row=False, cols=1, one_time_kb=False, *arg):

        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=one_time_kb, resize_keyboard=True)

        maxArg = len(arg)
        countLoop = math.ceil(maxArg / cols)
        tasks = []
        lastPoiner = 0
        # Цикл для внесення кнопок в двохвимірний масив з вказаними колонками ****
        for i in range(countLoop):  # 0                                        ****
            tmp = []
            for j in range(lastPoiner, lastPoiner + cols):  # прибрати lastPoiner
                if j >= maxArg:
                    break
                tmp.append(types.KeyboardButton(arg[j]))
            lastPoiner = lastPoiner + cols
            tasks.append(tmp)
        # Додавання до об'єкту клавіатури вибраним способом і повернення об'єкту
        if add_row == 0:
            for i in range(len(tasks)):
                markup.add(*tasks[i])
            return markup
        elif add_row == 1:
            for i in range(len(tasks)):

                markup.row(*tasks[i])
            return markup

    def InlineKeyboardButton(self, add_row=False, cols=1, **kwarg):

        markup = types.InlineKeyboardMarkup()

        keyFromkwarg = []
        for key in kwarg.keys():
            keyFromkwarg.append(key)

        maxArg = len(kwarg)
        countLoop = math.ceil(maxArg / cols)
        tasks = []
        lastPoiner = 0
        # Цикл для внесення кнопок в двохвимірний масив з вказаними колонками ****
        for i in range(countLoop):  # 0                                        ****
            tmp = []
            for j in range(lastPoiner, lastPoiner + cols):  # прибрати lastPoiner
                if j >= maxArg:
                    break
                tmp2 = keyFromkwarg[j]
                tmp.append(types.InlineKeyboardButton(
                    tmp2, callback_data=kwarg[tmp2]))
            lastPoiner = lastPoiner + cols
            tasks.append(tmp)
        # Додавання до об'єкту клавіатури вибраним способом і повернення об'єкту
        if add_row == 0:
            for i in range(len(tasks)):
                markup.add(*tasks[i])
            return markup
        elif add_row == 1:
            for i in range(len(tasks)):

                markup.row(*tasks[i])
            return markup

    def write_config(self, name_file, arg):
        file = open(str(name_file), "a+", encoding="utf-8")
        file.write(str(arg))
        file.write("\n\n")
        file.close()


ctb = My_Telegram_Bot()


def numbering(time):
    tmp_time = []
    for i in range(9, 24):
        t = str(i)+":00"
        if t == "9:00":
            t = "09:00"
        elif t == "23:00":
            t = "Ніч"

        for j in time:

            if j == t:
                tmp_time.append(t)

    return tmp_time


def filter(name, date, time, room, number):

    tmp = {}
    tmp_name = []
    id = 0

    for nm in name:
        if nm not in tmp_name:
            tmp[nm] = {
                "date": [date[id].strftime("%d-%m-%Y ")],
                "time": [time[id]],
                "room": [room[id]],
                "number": [number[id]],
                "id": [id]
            }
            tmp_name.append(nm)
        else:
            tmp[nm]["date"].append(date[id].strftime("%d-%m-%Y "))
            tmp[nm]["time"].append(time[id])
            tmp[nm]["room"].append(room[id])
            if number[id] not in tmp[nm]["number"]:
                tmp[nm]["number"].append(number[id])
            tmp[nm]["id"].append(id)
        id += 1
    return tmp


async def send_admin(Seseeons):
    time = Seseeons["data"]

    names = Seseeons["user_write_name"]
    data_regist = date(time["year"], time["month"], time["day"])
    room = Seseeons["room"]
    # time_tulp(seseeons[message.from_user.id]['time']) #time = tuple(seseeons[message.from_user.id]["time_user_regist"])
    time = Seseeons['time']
    number = Seseeons["number"]
    user_name = Seseeons["Name"]["user_name"]

    for id_admin in admin:
        await bot.send_message(id_admin, "Ім'я: {}\nUser_name: @{}\n".format(names, user_name) +
                               "{} кімната:\n".format(room) +
                                         "Записаний на {} такий час:\n".format(data_regist) +
                                         "час: {}\n".format(time) +
                                         "Номер: {}\n".format(number))


def change_of_time(time):
    ALL_time = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "Ніч"]
    tmp = []
    tmp1_first = ALL_time.index(time[0])
    tmp1_last = ALL_time.index(time[len(time)-1])
    for i in ALL_time[tmp1_first: tmp1_last]:
        tmp.append(i)


def trans_list_in_str(time):
    ALL_time = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "Ніч"]
    tmp1 = time[0]
    tmp2 = ALL_time.index(time[len(time) - 1])
    tmp2 = ALL_time[tmp2 + 1]
    return "з " + tmp1 + " до " + tmp2
