import os
import json
USER = os.getenv("USER")
SETUP = os.getenv("SETUP")
CONNECT = os.getenv("CONNECT")
DB_PATH = os.getenv('DB_PATH')
WORK_PATH = os.getenv("WORK_PATH")
BACKUP_PATH = os.getenv("BACKUP_PATH")
DB = DB_PATH + os.getenv("DB")
DB_CONSOLE = DB_PATH +os.getenv("DB_CONSOLE")
SCOPE = [os.getenv("SCOPE_APP"), os.getenv("SCOPE_AUTH")]
URL = os.getenv("URL")
TEAMS_DATA = str(os.getenv("TEAMS_DATA"))
TEAMS_LIST_STRING = "HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KESPOO, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT"
TEAMS_LIST = ["HPK", "HIFK", "ILVES", "JUKURIT", "JYP", "KALPA", "KESPOO", "KOOKOO", "KARPAT", "LUKKO", "PELICANS", "SAIPA", "SPORT", "TAPPARA", "TPS", "ASSAT"]
LOGIN_FILE = os.getenv("LOG_PATH")
f = open(TEAMS_DATA)
TEAMS = json.load(f)

def SAVE():
    try:
        os.system("cp "+DB+" "+BACKUP_PATH)
        os.system("cp "+DB_CONSOLE+" "+BACKUP_PATH)
    except:
        print('SAVE_FAILL')