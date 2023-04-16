from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import types
from keyboards import Bot 
from datetime import datetime, date


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                               KeyboardButton
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

client_month = types.ReplyKeyboardMarkup()

def month_kb(tmp_day_first):
    global client_month
    tmp_month = [ "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
    tmp = []
    if tmp_day_first == 11:
        tmp.append(tmp_month[10])
        tmp.append(tmp_month[11])
        tmp.append(tmp_month[0])
        client_month = Bot.ctb.KeyboardButton(True, 3, False, *tmp)
    elif tmp_day_first == 12:
        tmp.append(tmp_month[11])
        tmp.append(tmp_month[0])
        tmp.append(tmp_month[1])
        client_month = Bot.ctb.KeyboardButton(True, 3, False, *tmp)
    else:
        for i in range(tmp_day_first-1, tmp_day_first+2):
            tmp.append(tmp_month[i])
        client_month = Bot.ctb.KeyboardButton(True, 3, False, *tmp)

#------------------------------------------------------------------------------#

client_upgrad = Bot.ctb.KeyboardButton(False, 1, False, "/Додати", "/Видалити", "/Головне_Меню")

#------------------------------------------------------------------------------#

client_rkb = Bot.ctb.KeyboardButton(True, 2, True, "Синя","Червона", "Чорна")

#------------------------------------------------------------------------------#

client_tkb = types.ReplyKeyboardMarkup()

def Dinamic_kb(time, Seseeons):
    print("Dinamic_kb")
    global client_tkb
    OBMe = Seseeons["time_user_regist"]
    hour = OBMe.hour
    date_user = Seseeons["data"]
    a = datetime(date_user["year"], date_user["month"], date_user["day"] )
    b = datetime(OBMe.year, OBMe.month, OBMe.day)


    tmp = [] # Тимчасова зміна
    time_str_for_kb = ["09:00","10:00","11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
    
    for i in range(len(time) - 1):

        if a == b:

            if hour < i + 9:

                if time[i] == 0:
                    tmp.append(time_str_for_kb[i])
                    
        else:

            if time[i] == 0:
                tmp.append(time_str_for_kb[i])

    client_tkb = Bot.ctb.KeyboardButton(True, 6, False, *tmp)
    print(len(time) - 1)
    print(time)
    if time[len(time) - 1] == 0:
        client_tkb.row(KeyboardButton("Ніч"))
    
    client_tkb.row(KeyboardButton("Очистити все"), KeyboardButton("Далі👉"))
    
    
#----------------------------------------------------------------------------#
client_Menu = types.ReplyKeyboardMarkup()

def Dinamic_kb_regist(tmp):
    global client_Menu
    print("Dinamic_kb_regist")
    if tmp == True:
        tmp = [ "/Познайомитись", "/Забронювати_час", "/Мої_дані", "/help", "/Геолокація", "/Розклад"]
        client_Menu = Bot.ctb.KeyboardButton(False, 1, False, *tmp)
    elif tmp == False:
        tmp = ["/Познайомитись", "/Забронювати_час", "/help", "/Геолокація", "/Розклад"]
        client_Menu = Bot.ctb.KeyboardButton(False, 1, False, *tmp)
#----------------------------------------------------------------------------#

client_day_kb = ReplyKeyboardMarkup()

def day_kb(dayOFmonth, month, month_now, day, konst):
    global client_day_kb

    if month_now == 11 and month == 1:
        month_now = -1

    elif month_now == 12 and (month == 1 or month == 2):
        month_now = 0
    
    month = month - month_now
    tmp = []
    
    for i in range(dayOFmonth):
        if month == 0 and i+1 >= day:
            tmp.append(str(i+1))

        elif month == 2 and i+1 <= day + konst:
            tmp.append(str(i+1))
        
        elif month == 1:
            tmp.append(str(i+1))

    client_day_kb = Bot.ctb.KeyboardButton(True, 7, False, *tmp)


#----------------------------------------------------------------------------#


client_yn_kb = Bot.ctb.KeyboardButton(False, 1, True, "Так", "НІ")

#----------------------------------------------------------------------------#

client_NAME = ReplyKeyboardMarkup()

def registed_name(tmp_name):
    for i in range( len(tmp_name) ):
        if type(tmp_name[i]) == int:
            tmp_name[i] = str(tmp_name[i])

    global client_NAME
    client_NAME = Bot.ctb.KeyboardButton(True, 7, False, *tmp_name)



def Dinamic_dl_kb(time):
    global client_tkb
    client_tkb = Bot.ctb.KeyboardButton(True, 6, False, *time)
    
    client_tkb.row(KeyboardButton("Очистити все"), KeyboardButton("Далі👉"))


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                           InlineKeyboardButton
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# client_month = types.InlineKeyboardMarkup()

# def month_kb(tmp_day_first):
#     global client_month
#     tmp_month = [ "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
#     tmp = []
#     tmp2 = dict()
#     if tmp_day_first == 11:
#         tmp.append(tmp_month[10])
#         tmp.append(tmp_month[11])
#         tmp.append(tmp_month[0])
#         client_month = Bot.ctb.KeyboardButton(True, 3, True, *tmp)
#     elif tmp_day_first == 12:
#         tmp.append(tmp_month[11])
#         tmp.append(tmp_month[0])
#         tmp.append(tmp_month[1])
#         for i in tmp:
#             tmp2[i] = "client_month"
#         print(tmp2)
#         client_month = Bot.ctb.InlineKeyboardMarkup(False, 4, *tmp2[0])
#     else:
#         for i in range(tmp_day_first-1, tmp_day_first+2):
#             tmp.append(tmp_month[i])
#         client_month = Bot.ctb.KeyboardButton(True, 3, True, *tmp)
