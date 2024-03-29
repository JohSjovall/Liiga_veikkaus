import datetime
import time
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import Consol
import configure

#Day_ID, Player_ID, First_Name, Last_Name, Points
class SheetGame:
    def __init__(self, id, staus, history, order):
        self.id = id
        self.staus = staus
        self.history = history
        self.order = order
    def getOrder(self):
        if(self.order == 1):
            return "Last_Name, First_Name"
        else:
            return "First_Name, Last_Name"

def Sheet_Table_List():
    gamesSheetList = []
    conn = sqlite3.connect('Database_liiga_game.db')
    c = conn.cursor()
    c.execute('SELECT Game_ID, Game_staus, Game_history, List_Order FROM SHEET')
    for data in c.fetchall():
        gamesSheetList.append(SheetGame(data[0], data[1], data[2], data[3]))
    return gamesSheetList

def Sheet_Run_List():
    conn = sqlite3.connect('Database_liiga_game.db')
    gamesSheetList = Sheet_Table_List()
    for sheetData in gamesSheetList:
        Sheet_Update(sheetData, conn)
        Sheet_Player_History(sheetData, conn)
    conn.close()


def Sheet_Update(sheetData: SheetGame, conn: sqlite3.Connection):
    c = conn.cursor()
    gameName = getGameName(sheetData, c)
    service = ServiceAccountCredentials.from_json_keyfile_name(configure.CONNECT, configure.SCOPE)
    gc = gspread.authorize(service)
    Consol.Message('SHEET STATUS '+gameName+': START')
    try:
        wks = gc.open(sheetData.staus).sheet1
        c.execute('SELECT '+sheetData.getOrder()+', Points FROM '+gameName+' WHERE Day_ID = (SELECT MAX(Day_ID) FROM '+gameName+') ORDER BY '+sheetData.getOrder())
        row = 2
        for x in c.fetchall():
            #print(x)
            wks.update_cell(row,1,x[0]+' '+x[1])
            wks.update_cell(row,2,x[2])
            row += 1
        c.execute('SELECT MAX(Day_ID) FROM '+gameName)
        wks.update_cell(1,2,c.fetchone()[0])
        Consol.Message('SHEET STATUS '+gameName+': DONE')
    except Exception as e:
        Consol.Message('SHEET STATUS '+gameName+': ERROR (' + str(e) +')')

def getGameName(sheetData: SheetGame, c: sqlite3.Cursor):
    c.execute('SELECT Game_Name FROM GAMES WHERE Game_ID = ?',(str(sheetData.id)))
    gameName = c.fetchone()[0]
    return gameName

def Sheet_Player_History(sheetData: SheetGame, conn: sqlite3.Connection):
    c = conn.cursor()
    gameName = getGameName(sheetData, c)
    service = ServiceAccountCredentials.from_json_keyfile_name(configure.CONNECT, configure.SCOPE)
    gc = gspread.authorize(service)
    Consol.Message('START SHEET HISTORY '+gameName+': START')
    try:
        wks = gc.open(sheetData.history).sheet1
        c.execute('SELECT MAX(Day_ID) FROM '+gameName)
        Day = c.fetchone()[0]
        Line = [Day]
        c.execute('SELECT Points FROM '+gameName+' WHERE Day_ID = (SELECT MAX(Day_ID) FROM '+gameName+') ORDER BY Last_Name, First_Name')
        for x in c.fetchall():
            Line += [x[0]]
        #print(Line)
        wks.append_row(Line)
        Consol.Message('SHEET HISTORY '+gameName+': DONE')
    except Exception as e:
        Consol.Message('SHEET HISTORY '+gameName+': ERROR('+str(e)+')')
def Sheet_Server_run():
    try:
        Consol.Message('SHEET SERVER: ON')
        configure.SAVE()
        while True:
            time.sleep(900)
            timeHouer = int(datetime.datetime.fromtimestamp(time.time()).strftime('%H'))
            if timeHouer==8:
                Sheet_Run_List()
                time.sleep(3600)
                configure.SAVE()
    except Exception as e:
        Consol.Message('SHEET SERVER: ERROR ('+str(e)+')')
        configure.SAVE()
