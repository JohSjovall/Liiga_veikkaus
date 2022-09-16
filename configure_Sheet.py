import datetime
import time
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import Consol
import configure

h1 = 'HEMMINKI'
h2 = 'PERHE'
#Day_ID, Player_ID, First_Name, Last_Name, Points
def Sheet_Update():
    conn = sqlite3.connect('Database_liiga_game.db')
    c = conn.cursor()
    service = ServiceAccountCredentials.from_json_keyfile_name(configure.CONNECT, configure.SCOPE)
    gc = gspread.authorize(service)
    Consol.Message('SHEET UPDATE HEMMINKI: START')
    try: #h1
        wks = gc.open('Hemminki_pisteet').sheet1
        c.execute('SELECT Last_Name, First_Name, Points FROM '+h1+' WHERE Day_ID = (SELECT MAX(Day_ID) FROM '+h1+') ORDER BY Last_Name, First_Name')
        row = 2
        for x in c.fetchall():
            #print(x)
            wks.update_cell(row,1,x[0]+' '+x[1])
            wks.update_cell(row,2,x[2])
            row += 1
        c.execute('SELECT MAX(Day_ID) FROM '+h1)
        wks.update_cell(1,2,c.fetchone()[0])
        Consol.Message('SHEET UPDATE HEMMINKI: DONE')
    except Exception as e:
        Consol.Message('SHEET UPDATE HEMMINKI: ERROR (' + str(e) +')')
    Consol.Message('SHEET UPDATE PERHE: START')
    try: #h2
        wks = gc.open('Perhe_pisteet').sheet1
        c.execute('SELECT Last_Name, First_Name, Points FROM '+h2+' WHERE Day_ID = (SELECT MAX(Day_ID) FROM '+h2+') ORDER BY Last_Name, First_Name')
        row = 2
        for x in c.fetchall():
            #print(x)
            wks.update_cell(row,1,x[0]+' '+x[1])
            wks.update_cell(row,2,x[2])
            row += 1
        c.execute('SELECT MAX(Day_ID) FROM '+h2)
        wks.update_cell(1,2,c.fetchone()[0])
        Consol.Message('SHEET UPDATE DONE: PERHE')
    except Exception as e:
        Consol.Message('SHEET UPDATE PERHE: ERROR ('+ str(e) +')')
    conn.close()

def Sheet_Player_History():
    conn = sqlite3.connect('Database_liiga_game.db')
    c = conn.cursor()
    service = ServiceAccountCredentials.from_json_keyfile_name(configure.CONNECT, configure.SCOPE)
    gc = gspread.authorize(service)
    Consol.Message('START SHEET HISTORY UPDATE: HEMMINKI')
    try: #h1
        wks = gc.open('Hemminki_pistekehitys').sheet1
        c.execute('SELECT MAX(Day_ID) FROM '+h1)
        Day = c.fetchone()[0]
        Line = [Day]
        c.execute('SELECT Points FROM '+h1+' WHERE Day_ID = (SELECT MAX(Day_ID) FROM '+h1+') ORDER BY Last_Name, First_Name')
        for x in c.fetchall():
            Line += [x[0]]
        #print(Line)
        wks.append_row(Line)
        Consol.Message('SHEET HISTORY UPDATE DONE: HEMMINKI')
    except Exception as e:
        Consol.Message('SHEET HISTORY UPDATE HEMMINKI: ERROR('+str(e)+')')
    Consol.Message('START SHEET HISTORY UPDATE: PERHE')
    try: #h2
        wks = gc.open('Perhe_pistekehitys').sheet1
        c.execute('SELECT MAX(Day_ID) FROM '+h2)
        Day = c.fetchone()[0]
        Line = [Day]
        c.execute('SELECT Points FROM '+h2+' WHERE Day_ID = (SELECT MAX(Day_ID) FROM '+h2+') ORDER BY Last_Name, First_Name')
        for x in c.fetchall():
            Line += [x[0]]
        #print(Line)
        wks.append_row(Line)
        Consol.Message('SHEET HISTORY UPDATE DONE: PERHE')
    except Exception as e:
        Consol.Message('SHEET HISTORY UPDATE PERHE: ERROR('+str(e)+')')
    conn.close()
def Sheet_Server_run():
    try:
        Consol.Message('SHEET SERVER: ON')
        configure.SAVE()
        while True:
            time.sleep(900)
            timeHouer = int(datetime.datetime.fromtimestamp(time.time()).strftime('%H'))
            if timeHouer==8:
                Sheet_Update()
                time.sleep(3600)
                configure.SAVE()
    except Exception as e:
        Consol.Message('SHEET SERVER: ERROR ('+str(e)+')')
        configure.SAVE()
