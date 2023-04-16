from datetime import datetime, date
from os import name
from re import escape
import sqlite3 as sq
import json
from data_base import ORM
from handlers.admin import Seseeons
# from handlers.admin import Seseeons
from keyboards import client_kb
from .ORM import *
from create_bot import bot
from keyboards import Bot

#, seseeons[message.from_user.id]["user_write_name"], seseeons[message.from_user.id]["data"]["year"]), seseeons[message.from_user.id]["room"], seseeons[message.from_user.id]["time"][0])


# def sql_start():
#     create_table = """
#     CREATE TABLE Person(
#         id INT PRIMARY KEY, 
#         Name VARCHAR(100), 
#         Date YEAR(4), 
#         Number INT, 
#         Numder_regist INT
#         )"""

#     # base = connect(
#     # host="localhost",
#     # user="root",
#     #     password="Halloillyahaus&1&2"
#     # )


#     # cur = base.cursor()
#     # cur.execute("CREATE DATABASE Regist_person")

#     # try:
#     #     with connect(
#     #         host="localhost",
#     #         user="root",
#     #         password="Halloillyahaus&1&2"
#     #     ) as connection:
#     #         create_db_query = "CREATE DATABASE Regist_person;"
#     #         with connection.cursor() as cursor:
#     #             cursor.execute(create_db_query)
#     # except Error as e:
    
#     with connect(
#             host="localhost",
#             user="root",
#             password="Halloillyahaus&1&2",
#             database = "Regist_person"
#         ) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(create_table)
#         connection.commit()
        



def sql_start():
    
    if db:
        print("База даних запущена")
        with db:
            db.create_tables([Names, Id, Time, Id_c, All_regist, All_regist_copy, Blok_user])

def check_id(user_id):
    try:
        with db:
            id = Id.get(Id.id_tl == user_id)    
            
    except:
        id = None
        
    if id == None:
        client_kb.Dinamic_kb_regist(False)
        return False

    elif user_id == id.id_tl :
        client_kb.Dinamic_kb_regist(True)
        return True
      
def sql_add_command(seseeons):
    
    #data = json.loads(seseeons)
    # with open("data_base/data_file.json", "w") as write_file:
    #     json.dump(seseeons, write_file, indent= 2)
    time = seseeons["data"]
    
    
    id = seseeons["id"]
    names = seseeons["user_write_name"]
    data = date.today()
    data_regist = date(time["year"], time["month"], time["day"])
    room = seseeons["room"]
    time = seseeons['time'] #time_tulp(seseeons[message.from_user.id]['time']) #time = tuple(seseeons[message.from_user.id]["time_user_regist"])
    number = seseeons["number"]
    group = seseeons["Group_or_one"]
    user_pay = seseeons["sum_order"]
    


    with db:
        person_name = Names.create(name = names)

    with db:
        person_id = Id.create(id_tl = id)
        
    with db:
        
        try:
        
            c_id = Id_c.get(Id_c.id_tl == id)    
            name = c_id.name.split(", ")
            if names not in name:
                tmp = ""
                for i in name:
                    tmp += i + ", "
                    
                name = tmp + names
                Id_c.update( {Id_c.name : name} ).where(Id_c.id_tl == id).execute()
            
        except:
            Id_c(id_tl = id, name = names).save()

    with db:

        person = All_regist.create(id_tlbot = person_id, name = person_name.name, datetime = data, room = room, day_regist = data_regist, oneORgroup = group, pay_for_time = user_pay, number = number)
        All_regist_copy.create(id_tlbot = person_id.id_tl, name = person_name.name, datetime = data, room = room, day_regist = data_regist, oneORgroup = group, pay_for_time = user_pay, number = number)
    
    with db:
        for i in time:
            
            Time.create(time = i, person = person)

def get_data_fromSQL(user_id, name = None):
    tmp = dict()
    names_key = []
    with db:
        get_all_ID = Id.select().where(Id.id_tl == user_id)
        
        for get in get_all_ID:

            if name != None:
                names = get_all_data_All_regist = All_regist.select().where(All_regist.id_tlbot_id == get.id, All_regist.name_id == name)
            else:
                get_all_data_All_regist = All_regist.select().where(All_regist.id_tlbot_id == get.id)
        
            
            
            
            for get_All_regist in get_all_data_All_regist:
                
                time = []
                
                get_all_data = Time.select().where(Time.person_id == get_All_regist.id)
                for get_Time in get_all_data:
                        time.append(get_Time.time)
            
            
                if get_All_regist.name_id not in names_key:
                    names_key.append(get_All_regist.name_id)
                   
                    i = 0
            
                

                    tmp[get_All_regist.name_id]= {
                            "id" : [i],
                            "room":[get_All_regist.room],
                            "time":[time],
                            "date": [get_All_regist.day_regist],
                            "group": [get_All_regist.oneORgroup],
                            "number": get_All_regist.number
                                                                }
                elif get_All_regist.day_regist in tmp[get_All_regist.name_id]["date"] and get_All_regist.room in tmp[get_All_regist.name_id]["room"]:

                    index = tmp[get_All_regist.name_id]["date"].index(get_All_regist.day_regist)
                    if get_All_regist.room in tmp[get_All_regist.name_id]["room"][index]:
                        for tm in time:
                            tmp[get_All_regist.name_id]["time"][ index ].append(tm)
                        tmp[get_All_regist.name_id]["time"][ index ] = Bot.numbering(tmp[get_All_regist.name_id]["time"][ index ]) 
            
                    else:
                        tmp_time = tmp[get_All_regist.name_id]["date"][1 : len(tmp[get_All_regist.name_id]["date"])]
                        index = tmp_time.index(get_All_regist.day_regist) + 1
                        for tm in time:
                            tmp[get_All_regist.name_id]["time"][ index ].append(tm)
                        tmp[get_All_regist.name_id]["time"][ index ] = Bot.numbering(tmp[get_All_regist.name_id]["time"][ index ])   
                
                else:
                    id = tmp[get_All_regist.name_id]["id"]
                    id.append(id[len(id) - 1] + 1)
                    tmp[get_All_regist.name_id]["room"].append(get_All_regist.room)
                    # tmp_mass.append(tmp[get_All_regist.name_id]["room"]) 
                    # tmp_mass.append(get_All_regist.room)
                    # tmp[get_All_regist.name_id]["room"] = tmp_mass
                    tmp[get_All_regist.name_id]["group"].append(get_All_regist.oneORgroup)
                    tmp[get_All_regist.name_id]["date"].append(get_All_regist.day_regist)
                    tmp[get_All_regist.name_id]["time"].append(time)

    #[get_name, get_time, get_date, get_number]
    
    return tmp, names_key

def blok_unblok(id, blok):
    with db:
        if id in blok.keys():
            Blok_user.create(id_user = id, reason = blok[id])
        
        elif id not in blok.keys():
            Blok_user.delete().where(Blok_user.id_user == id).execute()

def sql_del(user_id, tim, date, nm, room):
    with db:
        # n = All_regist.select().where( All_regist.name_id == nm )#and (All_regist.datetime == date) and (All_regist.room == room) )
        n = All_regist.select().where( All_regist.name_id == nm, All_regist.day_regist == date, All_regist.room == room )

        for nom in n:
            for t in tim:
                Time.delete().where(Time.person_id == nom.id, Time.time == t).execute()          
           
             
            
            try:
                er = Time.get(Time.person_id == nom.id)
            except:
                er = None


            if er == None:
                Id.delete().where(Id.id == nom.id_tlbot_id).execute()
                All_regist.delete().where(All_regist.id_tlbot == nom.id_tlbot_id, All_regist.datetime == date and All_regist.room == room).execute()

def sql_del_every_day():
    with db:
        n = All_regist.select().where(All_regist.day_regist < datetime.now())
        for nom in n:
            Id.delete().where(Id.id == nom.id_tlbot_id).execute()
            Time.delete().where(Time.person_id == nom.id).execute()
        
        All_regist.delete().where(All_regist.day_regist < datetime.now()).execute()

def all_id_name():
    with db:
        Seseeons = {}
        key = []
        rg = Id_c.select()
        
        for all_data in rg:
            id = all_data.id_tl
            name = all_data.name
            Seseeons[id] = name
            key.append(id)
        return Seseeons, key

def all_data():
    tmp = {}
    key = []
    name_keys = []
    with db:
        rg = All_regist.select()
        i = 0
        for all_data in rg:
            id = Id.get(Id.id == all_data.id_tlbot_id)
            name = all_data.name_id
            date = all_data.day_regist.strftime("%d-%m-%Y ")
            room = all_data.room
            time = []
            get_all_data = Time.select().where(Time.person_id == all_data.id)
            for get_Time in get_all_data:
                    time.append(get_Time.time)
            number = all_data.number
            if name not in name_keys:
                if id.id_tl not in tmp.keys():
                    key.append(id.id_tl)
                    tmp[id.id_tl] = {}
                    tmp_id_name = tmp[id.id_tl]

                tmp_id_name[name] = {
                    
                    "date": [date],
                    "time": [time],
                    "room": [room],
                    "number": [number]
                    
                }
                name_keys.append(name)

            elif date in tmp[id.id_tl][name]["date"] and room in tmp[id.id_tl][name]["room"]:
                
                index = tmp[id.id_tl][name]["date"].index(date)
                if all_data.room in tmp[id.id_tl][name]["room"][index]:
                    for tm in time:
                        tmp[id.id_tl][name]["time"][ index ].append(tm)
                    tmp[id.id_tl][name]["time"][ index ] = Bot.numbering(tmp[id.id_tl][name]["time"][ index ]) 
                
                else:
                    tmp_time = tmp[id.id_tl][name]["date"][1: len(tmp[id.id_tl][name]["date"]) ]
                    index = tmp_time.index(date) + 1
                    for tm in time:
                        tmp[id.id_tl][name]["time"][ index ].append(tm)
                    tmp[id.id_tl][name]["time"][ index ] = Bot.numbering(tmp[id.id_tl][name]["time"][ index ])

            else:
                
                tmp[id.id_tl][name]["date"].append(date)
                tmp[id.id_tl][name]["time"].append(time)
                tmp[id.id_tl][name]["room"].append(room)
                tmp[id.id_tl][name]["number"].append(number)
                
                
    return tmp, key

def time_tulp(seseeons):
    time = []
    for i in range(9, 23):
        
        for j in range(len(seseeons)):
            if seseeons[j] == str(i)+":00":
               time.append(i) 
            elif seseeons[j] == "Ніч":
                time.append(i)
    return tuple(time)

def downloand_blok(blok):
    with db:
        blokk = Blok_user.select()
        for all_data in blokk:
            id = all_data.id_user
            reason = all_data.reason
            blok[id] = reason

async def send_users_adver():
    tmp = []
    with db:
        id_key = Id_c.select()

        for id_all in id_key:
            id = id_all.id_tl
            tmp.append(id)
    return tmp