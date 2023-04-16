import httplib2
from pprint import pprint
#import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime, date

import google_sheet
from .funSheet import *
import gspread
import send_app_script
import json



gc = gspread.service_account(filename = "creds.json")


basedir = os.path.abspath(os.path.dirname(__file__))
#basedir + "\\" + "creds.json" WINDOWS
#basedir + "/" + "creds.json"  LINUX
scredentials_FILE = basedir + "/" + "creds.json"
# scredentials_FILE = basedir + "\\" + 'creds.json'



#1dUAg-BIJXM0zmw1jEojlgznD0Vpl9GgF6JyWFUaBytM
spreadsheet_id = '1eD8X0i6sZ9U3AKHDMOrJZIxjtysft2hApfl9GnDfGeg'
spreadsheet_id_help = '1b8Z8QdE7Lmsb8rh4W9sNh9qt3k1I1MPBg9YkD303vBg'
spreadsheet_id_schedule = '14TTe8vZRzl63rJ2r91m8VOnV0aoL8yMdF4dqSIQ8PEg'

credentials = ServiceAccountCredentials.from_json_keyfile_name(scredentials_FILE,
                                        ['https://www.googleapis.com/auth/drive',
                                         'https://www.googleapis.com/auth/spreadsheets'])

httpAuth = credentials.authorize(httplib2.Http())
service = build('sheets', 'v4', http = httpAuth)
'''
values = service.spreadsheets().values().get(
    spreadsheetId = spreadsheet_id,
    range =  'S25'
    ).execute()

    try:
        a = values["values"]
    except:

print(values)
exit()
'''
'''
values_add = service.spreadsheets().values().batchUpdate(
    spreadsheetId = spreadsheet_id,
    
  body = {"valueInputOption": "USER_ENTERED",
  "data": [
    {"range":"B4:B11",
    "majorDimension":"ROWS",
     "values":[[mas_name_namber[0]], []]}] 
          }).execute()

values_clear = service.spreadsheets().values().clear(
    spreadsheetId = spreadsheet_id,
    range = "B5:B6"
    ).execute()
'''


def create_sheet(month_year, seseeons):
    print("create_sheet")
    spreadsheet = service.spreadsheets().create(
        body = {'properties':{'title':'Admin', 'locale':'ru_RU'},
                'sheets':[{'properties':{'sheetType':'GRID',
                                         'sheetId': 0,
                                         'title':'Лист номер один',
                                         'gridProperties':{'rowCount': 90, 'columnCount': 33}
                                         }
                           }]
                }).execute()
    spreadsheetId = spreadsheet['spreadsheetId']
    

    driveService = build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'illya2033@gmail.com',
                                              'emailAddress': 'illvauser8@gmail.com',
                                              'emailAddress': "mtohym@gmail.com"},  # Открываем доступ на редактирование
    fields = 'id'
    ).execute()
    
    
    check_m = check_month(seseeons)
   
    
    
        
    name_sheet = month_year

    results = service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
      body ={
        "requests": [
          {
            "addSheet": {
              "properties": {
                "title": name_sheet,
                "gridProperties": {
                    "rowCount": 90,
                    "columnCount": 33
                  }
              }
        }
          }
        ]}).execute()
   

    ##with open('test.txt', 'w') as f:
      #  f.write(sheetList)
    
    spreadsheet_copy = service.spreadsheets().sheets().copyTo(
        spreadsheetId = spreadsheet_id_help,
        sheetId = 0,
        body = {
            "destinationSpreadsheetId": spreadsheet_id
        }).execute()

    spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheet_id).execute()
    sheetList = spreadsheet.get('sheets')
    # sheetId = sheetList[0]['properties']['sheetId']
    
    results = service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
    body ={
     "requests": [
        {
        
      "copyPaste": {
        "source":{
            "sheetId": sheetList[len(sheetList)-1]['properties']['sheetId'],
            "startRowIndex": check_m[0],
            "endRowIndex": check_m[1],
            "startColumnIndex": 0,
            "endColumnIndex": 33
        },
        "destination": {
            "sheetId": sheetList[len(sheetList)-2]['properties']['sheetId'],
            "startRowIndex": 0,
            "endRowIndex": 90,
            "startColumnIndex": 0,
            "endColumnIndex": 33}
     }}
      ]
         }
           ).execute()



    results = service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body ={
     "requests": [
        {
      "deleteSheet": {
            "sheetId": sheetList[len(sheetList)-1]['properties']['sheetId']
            }
          }
        ]
         }
           ).execute()

    
    # Получаем список листов, их Id и название
    
    day = []
    for i in range(4):
        day.append(i+1)
    spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheet_id).execute()


    sheetList = spreadsheet.get('sheets')
    sheet = sheetList[len(sheetList)-1]
    
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet_id, body = {
    "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": 
        {"range": sheet['properties']['title'] +"!"+ "A1",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [["hall0"]] }
    
  }).execute()
    
async def Check_batle(seseeons, month_year):
  print("Check_batle")
  day = day_in_nomber_exl(seseeons["data"]["day"])#room_day
  room = room_exl(seseeons["room"])#room_day

  name_sheet = month_year
  data = {
    "title": name_sheet,
    "day": day,
    "room": room,
  }

  time = send_app_script.send_apps_script(data)
  return time
  
  
#name_namber, time, room_day
def Exele_sheet_write(Seseeons, name_title_m_y, Check_defor_write = False):
  time = []
  tmp_get_check = []

  tmp = Seseeons["time_user_regist"]
  now_time = date(tmp.year, tmp.month, 1)
  tmp = Seseeons["data"]
  select_time_user = date(tmp["year"], tmp["month"], 1)
  
  day = day_in_nomber_exl(Seseeons["data"]["day"])#room_day
  time = time_exl(Seseeons["time"])#time
  room = room_exl(Seseeons["room"])#room_day
  group = Seseeons["Group_or_one"]
  text = Seseeons["user_write_name"]+" "+Seseeons["number"]
  name_sheet = name_title_m_y

  data = {"title": name_sheet, 
          "day": day,
          "time": time, 
          "room": room,
          "group": group,
          "text": text,
          }

  if Check_defor_write == False:
    jsonw = json.dumps(data)
    data = {"data": jsonw}
    send_app_script.write_apps_script(data)
    if now_time == select_time_user:
      send_app_script.write_group_apps_script(data)
      

  elif Check_defor_write == True:
    get_time = send_app_script.send_apps_script(data)
    for i in range(len(time)):
      y = time[i]
      if get_time[y] != 0:
        return False
    return True

async def check_existence_Month(name_title_m_y, seseeons):
  
  spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheet_id).execute()
  sheetList = spreadsheet.get('sheets')
  for i in range(len(sheetList)):
    if sheetList[i]["properties"]["title"] == name_title_m_y:
       return True
    
  create_sheet(name_title_m_y, seseeons)

def delet_from_basedate(Seseeons, id):
  tmp = datetime.now()
  now_time = date(tmp.year, tmp.month, 1)
  tmp = Seseeons["date"][id]
  select_time_user = date(tmp.year, tmp.month, 1)

  tmp = Seseeons["date"][id]
  day = day_in_nomber_exl(tmp.day)
  time = time_exl(Seseeons["time"])
  room = room_exl(Seseeons["room"][id])
  room_w = Seseeons["room"][id]
  name_sheet = str(tmp.month) + "." + str(tmp.year)

  data = {"title": name_sheet, 
          "day": day,
          "time": time, 
          "room": room,
          "room_w": room_w,
          }

  jsonw = json.dumps(data)
  data = {"data": jsonw}
  send_app_script.delete_apps_script(data)
  if now_time == select_time_user:
    send_app_script.delete_group_apps_script(data)


