import datetime
import time
import sqlite3

connConsolStart = sqlite3.connect('Database_liiga_consol.db')
consolStart = connConsolStart.cursor()
consolStart.execute("CREATE TABLE IF NOT EXISTS MESSAGES (Date DATE, Time TEXT, Message TEXT)")
connConsolStart.close()

def Message(message):
    connConsol = sqlite3.connect('Database_liiga_consol.db')
    consol = connConsol.cursor()
    timeNow = time.strftime('%H:%M:%S')
    dayNow = datetime.date.today()
    consol.execute("INSERT INTO MESSAGES(Date, Time, Message) VALUES (?,?,?)",(dayNow, timeNow, message))
    connConsol.commit()
    print(dayNow,timeNow+": "+message)
    connConsol.close()