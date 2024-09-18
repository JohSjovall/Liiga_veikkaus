import datetime
import time
import sqlite3
import logging
from configure import DB_CONSOLE

connConsolStart = sqlite3.connect(DB_CONSOLE)
consolStart = connConsolStart.cursor()
consolStart.execute("CREATE TABLE IF NOT EXISTS MESSAGES (Date DATE, Time TEXT, Message TEXT)")
connConsolStart.close()
logging.basicConfig(filename='liiga.log',
                        filemode='a',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')

def MessageToDB(message):
    connConsol = sqlite3.connect(DB_CONSOLE)
    consol = connConsol.cursor()
    timeNow = time.strftime('%H:%M:%S')
    dayNow = datetime.date.today()
    consol.execute("INSERT INTO MESSAGES(Date, Time, Message) VALUES (?,?,?)",(dayNow, timeNow, message))
    connConsol.commit()
    connConsol.close()

def ErroMessage(message):
    MessageToDB(message)
    logging.error(message)

def Message(message):
    MessageToDB(message)
    logging.info(message)