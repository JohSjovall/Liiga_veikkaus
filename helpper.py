import sqlite3
from configure import DB, TEAMS_LIST

conn = None
c = None

def connectDB():
    global conn, c
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    return c

def connect():
    global conn
    return conn

def disconnectDB():
    global conn
    if conn != None:
        conn.close()
    c = None

def make_player_and_team_tabels():
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS PLAYERS(Player_ID INTEGER PRIMARY KEY, First_Name TEXT NOT NULL, Last_Name TEXT NOT NULL, Mail TEXT)")
    disconnectDB()
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS GAMES(Game_ID INTEGER PRIMARY KEY, Game_Name TEXT NOT NULL UNIQUE)")
    disconnectDB()
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS SHEET(Game_ID INTEGER REFERENCES GAMES(Game_ID) ON UPDATE CASCADE ON DELETE CASCADE, Game_staus TEXT NOT NULL UNIQUE , Game_history TEXT NOT NULL UNIQUE, List_Order INTEGER DEFAULT 1 NOT NULL CHECK (List_Order IN (0, 1)), CONSTRAINT GameSheet_PK PRIMARY KEY(Game_ID, Game_staus, Game_history))")
    disconnectDB()
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS PLAYERS_GUESSES(Player_ID INTEGER REFERENCES PLAYERS(Player_ID) ON UPDATE CASCADE ON DELETE CASCADE, Game_ID INTEGER REFERENCES GAMES(Game_ID) ON UPDATE CASCADE ON DELETE CASCADE, HPK INT NOT NULL, HIFK INT NOT NULL, ILVES INT NOT NULL, JUKURIT INT NOT NULL, JYP INT NOT NULL, KALPA INT NOT NULL, KESPOO INT NOT NULL, KOOKOO INT NOT NULL, KARPAT INT NOT NULL, LUKKO INT NOT NULL, PELICANS INT NOT NULL, SAIPA INT NOT NULL, SPORT INT NOT NULL, TAPPARA INT NOT NULL, TPS INT NOT NULL, ASSAT INT NOT NULL, CONSTRAINT PlayerGame_PK PRIMARY KEY(Player_ID, Game_ID))")
    disconnectDB()
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS PLAYERS_POINTS(Day_ID DATE NOT NULL, Player_ID INTEGER REFERENCES PLAYERS(Player_ID) ON UPDATE CASCADE ON DELETE CASCADE , Game_ID INTEGER REFERENCES GAMES(Game_ID) ON UPDATE CASCADE ON DELETE CASCADE, HPK INT NOT NULL, HIFK INT NOT NULL, ILVES INT NOT NULL, JUKURIT INT NOT NULL, JYP INT NOT NULL, KALPA INT NOT NULL, KESPOO INT NOT NULL,  KOOKOO INT NOT NULL, KARPAT INT NOT NULL, LUKKO INT NOT NULL, PELICANS INT NOT NULL, SAIPA INT NOT NULL, SPORT INT NOT NULL, TAPPARA INT NOT NULL, TPS INT NOT NULL, ASSAT INT NOT NULL, top4_Correct_Point INT ,Six_Correct_Point INT, Points INT, CONSTRAINT DayPlayerGame_PK PRIMARY KEY(Day_ID, Player_ID, Game_ID))")
    disconnectDB()
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS ADMINS(Admin_ID INTEGER PRIMARY KEY, First_Name TEXT NOT NULL, Last_Name TEXT NOT NULL, Mail TEXT NOT NULL, Games_ID TEXT)")
    disconnectDB()

def make_liiga_table():
    c = connectDB()
    c.execute("CREATE TABLE IF NOT EXISTS LIIGA_LEAGUE_TABLE(Day_ID DATE PRIMARY KEY, HPK INT, HIFK INT, ILVES INT, JUKURIT INT, JYP INT, KALPA INT, KESPOO INT, KOOKOO INT, KARPAT INT, LUKKO INT, PELICANS INT, SAIPA INT, SPORT INT, TAPPARA INT, TPS INT, ASSAT INT)")
    disconnectDB()

def make_teams_tables():
    for team in TEAMS_LIST:
        c = connectDB()
        c.execute("CREATE TABLE IF NOT EXISTS "+team+" (Day_ID DATE, Games_Played INTEGER PRIMARY KEY, Wins INT, Draw INT, Losses INT, Overtime_Wins INT, Goals_For INT, Goals_Against INT, Points INT)")
        disconnectDB()