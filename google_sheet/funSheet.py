


from datetime import datetime
from datetime import date


def room_exl(room):
    if room == "Синя":
        room = 0
        return room

    elif room == "Червона":
        room = 19
        return room

    elif room == "Чорна":
        room = 38
        return room

def time_exl(seseeon_time):
    table_time = 0
    time = []

    for i in range(9, 24):
        t = str(i)+":00"
        if t == "9:00":
            t = "09:00"
        elif t == "23:00":
            t = "Ніч"

        for j in seseeon_time:
        
            if j == t:
                time.append(table_time)
        table_time += 1
    return time



def day_in_nomber_exl(day):
    mas_day = [ "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                "AA", "AB", "AC", "AD", "AE", "AF"]
    
    day = mas_day[day-1]
    return day




def check_month(a = 0, exel = True):
    current_date = datetime.now()
    month = [1, -1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

    for i in range(12):
        if exel == True:
            if i+1 == a["data"]["month"]:
                if month[i] == 1:
                    return [65, 127]
                elif month[i] == 0:
                    return [0, 80]
                else: 
                    return [129, 191]

        elif exel == False:
            if a["month"] == 12:
                a["month"] = 1
            first = date( a["year"], a["month"], 1)
            last = date( a["year"], a["month"] + 1, 1)
            a = (last - first).days
            return a
            
def nomber_day(day):
    

    first_day_weekday = date.today().weekday()
    
    
   