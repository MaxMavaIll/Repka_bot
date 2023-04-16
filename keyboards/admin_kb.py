from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import types
from keyboards import Bot 
from datetime import datetime, date
from config import blok






admin_Menu = Bot.ctb.KeyboardButton(False, 3, False, "Всe клиенты", "Все данные об клиентах", "Разослать объявление", "Вийти з адміна")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                           InlineKeyboardButton
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

admin_data = types.InlineKeyboardMarkup()

def add_del_block(id, name):
    global admin_data
    
    if id not in blok.keys():
        
        tmp = [ "Ск", "Все"]
        for i in range(len(tmp)):
            tmp[i] = tmp[i] + "/" + str(id)  + "/" + name
        
        admin_data = Bot.ctb.InlineKeyboardButton(False, 2, Скасувати = tmp[0], Скасувати_все = tmp[1])

    else:
        
        tmp = ["Ск", "Все"]
        for i in range(len(tmp)):
            tmp[i] = tmp[i] + "/" + str(id)  + "/" + name
        
        admin_data = Bot.ctb.InlineKeyboardButton(False, 2, Скасувати = tmp[0], Скасувати_все = tmp[1])

def client_user(id):
    global admin_data
    if id not in blok.keys():
        tmp = ["Ств", "Все", "Блок", "Огол"]
        for i in range(len(tmp)):
            tmp[i] = tmp[i] + "/" + str(id)
        
        admin_data = Bot.ctb.InlineKeyboardButton(False, 3, Створити = tmp[0], Скасувати_все = tmp[1], Заблокувати = tmp[2], Оголошення = tmp[3])

    else:
        tmp = ["Ств", "Все", "Розбл", "Огол"]
        for i in range(len(tmp)):
            tmp[i] = tmp[i] + "/" + str(id)
        
        admin_data = Bot.ctb.InlineKeyboardButton(False, 2, Створити = tmp[0], Скасувати_все = tmp[1], Оголошення = tmp[3], Розблокувати = tmp[2])

