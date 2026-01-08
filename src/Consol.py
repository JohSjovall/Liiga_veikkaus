import datetime
import time
import sqlite3
import logging
from configure import DB_CONSOLE, LOGIN_FILE

connConsolStart = sqlite3.connect(DB_CONSOLE)
consolStart = connConsolStart.cursor()
consolStart.execute("CREATE TABLE IF NOT EXISTS MESSAGES (Date DATE, Time TEXT, Message TEXT)")
connConsolStart.close()

logger = logging.getLogger('liiga-app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=LOGIN_FILE+'/liiga.log', mode='a')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S' )
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


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
    logger.error(message)

def Message(message):
    MessageToDB(message)
    logger.info(message)