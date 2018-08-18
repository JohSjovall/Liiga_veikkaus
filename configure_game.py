import datetime
import urllib.request
import sqlite3
from html.parser import HTMLParser
import Consol

conn = sqlite3.connect('Database_liiga_game.db')
c = conn.cursor()
league_table = []

#league_table
def create_league_table():
    c.execute("CREATE TABLE IF NOT EXISTS LIIGA_LEAGUE_TABLE(Day_ID DATE PRIMARY KEY, HPK INT, HIFK INT, ILVES INT, JUKURIT INT, JYP INT, KALPA INT, KOOKOO INT, KARPAT INT, LUKKO INT, PELICANS INT, SAIPA INT, SPORT INT, TAPPARA INT, TPS INT, ASSAT INT)")
#Liigakierros
def make_liigakerros_data(day):
    data = "Day_ID"
    for x in range(len(league_table)):
        data = data+", "+league_table[x][0]
    c.execute("INSERT INTO LIIGA_LEAGUE_TABLE ("+data+") VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(day ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
    conn.commit()
def update_liigakierros_data(day):
    data = ""
    for x in range(len(league_table)):
        data = data+str(league_table[x][0])+" = ?"
        if x != 14:
            data=data+" ,"
        else:
            pass
    c.execute("UPDATE LIIGA_LEAGUE_TABLE SET "+data+" WHERE Day_ID = ?",(1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15,day))
    conn.commit()
#Liiga joukkue
def create_Liiga_teams_tables():
    Teams = ["HPK", "HIFK", "ILVES", "JUKURIT", "JYP", "KALPA", "KOOKOO", "KARPAT", "LUKKO", "PELICANS", "SAIPA", "SPORT", "TAPPARA", "TPS", "ASSAT"]
    for x in Teams:
        c.execute("CREATE TABLE IF NOT EXISTS "+x+" (Day_ID DATE, Games_Played INTEGER PRIMARY KEY, Wins INT, Draw INT, Losses INT, Overtime_Wins INT, Goals_For INT, Goals_Against INT, Points INT)")
def make_liiga_team_data(day, data):
    c.execute("INSERT INTO "+data[0]+"(Day_ID , Games_Played, Wins, Draw, Losses, Overtime_Wins, Goals_For, Goals_Against, Points) VALUES ( ?,?,?,?,?,?,?,?,?)", (day, data[1] , data[2] , data[3] , data[4] , data[5] , data[6] , data[7], data[8]))
    conn.commit()
#Update teams and league table
def download_update_liiga(update):
    try:
        response = urllib.request.urlopen('http://liiga.fi/sarjataulukko')
        parser = LiigaHTMLParser()
        parser.feed(str(response.read()))
    except EnvironmentError:
        Consol.Message("ERROR! NO CONNECT!")
    for x in range(len(league_table)):
        c.execute("SELECT MAX(Games_Played) FROM "+str(league_table[x][0]))
        games_data = c.fetchone()
        if games_data is None or games_data[0] == league_table[x][1]:
            pass
        else:
            Consol.Message("NEW UPDATE")
            team_data_updaet()
            league_table.clear()
            return(True)
    Consol.Message("NO UPDATE")
    league_table.clear()
    return(update)

def team_data_updaet():
    TIME = datetime.date.today()
    for x in range(len(league_table)):
        try:
            make_liiga_team_data(TIME, league_table[x])
            Consol.Message("NEW DATA "+league_table[x][0]+" DONE")
        except:
            pass
    c.execute("SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE")
    MaxDay = c.fetchone()[0]
    try:
        if MaxDay is not None and str(MaxDay) == str(TIME):
            update_liigakierros_data(TIME)
            Consol.Message("UPDATE LIIGA LEAGUE TABLE DONE")
        else:
            make_liigakerros_data(TIME)
            Consol.Message("NEW DATA LIIGA LEAGUE TABLE DONE")
    except:
        Consol.Message("ERROR UPDATE LIIGA LEAGUE TABLE")
class LiigaHTMLParser(HTMLParser):
    def handle_data(self, data):
        teams = ["Lukko","K\\xc3\\xa4rp\\xc3\\xa4t","TPS","Tappara","Sport","Pelicans","KalPa","\\xc3\\x84ss\\xc3\\xa4t","KooKoo","SaiPa","HIFK","HPK","Ilves","Jukurit","JYP"]
        if data in teams:
            if data == teams[1]:
                league_table.append(["KARPAT"])
            if data == teams[7]:
                league_table.append(["ASSAT"])
            if data != teams[1] and data != teams[7]:
                league_table.append([str(data.upper())])
            else:
                pass
        else:
            try:
                if data.isdigit():
                    league_table[len(league_table)-1].append(int(data))   
            except:
                pass
        #print(league_table)
create_league_table()
create_Liiga_teams_tables()
#download_update_liiga(False)