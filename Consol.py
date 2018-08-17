import datetime
import time
import sqlite3

connConsol = sqlite3.connect('Database_liiga_consol.db')
consol = connConsol.cursor()
consol.execute("CREATE TABLE IF NOT EXISTS MESSAGES (Date DATE, Time TEXT, Message TEXT)")

def Message(message):
    timeNow = time.strftime('%H:%M:%S')
    dayNow = datetime.date.today()
    consol.execute("INSERT INTO MESSAGES(Date, Time, Message) VALUES (?,?,?)",(dayNow, timeNow, message))
    connConsol.commit()
    print(dayNow,timeNow+": "+message)