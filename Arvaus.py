import datetime
import time
import urllib.request
import sqlite3
import os
from html.parser import HTMLParser

conn = sqlite3.connect('LiigaData.db')
c = conn.cursor()
conn2 = sqlite3.connect('PelaajaData.db')
c2 = conn2.cursor()
tilanne = []

def create_gamers_list():
    c2.execute("CREATE TABLE IF NOT EXISTS PELAAJAT(PLAYER_ID INTEGER PRIMARY KEY, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL, MAIL TEXT)")
def create_games_list():
    c2.execute("CREATE TABLE IF NOT EXISTS PELIT(GAME_ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL UNIQUE)")
def create_players_guess(): #name on PLAYER_ID numero
    c2.execute("CREATE TABLE IF NOT EXISTS PELAAJIEN_ARVAUKSET(PLAYER_ID REFERENCES PELAAJAT(PLAYER_ID) ON UPDATE CASCADE ON DELETE CASCADE, GAME_ID REFERENCES PELIT(GAME_ID) ON UPDATE CASCADE ON DELETE CASCADE, HPK INT NOT NULL, HIFK INT NOT NULL, ILVES INT NOT NULL, JUKURIT INT NOT NULL, JYP INT NOT NULL, KALPA INT NOT NULL, KOOKOO INT NOT NULL, KARPAT INT NOT NULL, LUKKO INT NOT NULL, PELICANS INT NOT NULL, SAIPA INT NOT NULL, SPORT INT NOT NULL, TAPPARA INT NOT NULL, TPS INT NOT NULL, ASSAT INT NOT NULL, CONSTRAINT PG_PK PRIMARY KEY(PLAYER_ID, GAME_ID))")
def create_players_points ():
    c2.execute("CREATE TABLE IF NOT EXISTS PELAAJIEN_PISTEET(DAY_ID DATE NOT NULL, PLAYER_ID REFERENCES PELAAJAT(PLAYER_ID) ON UPDATE CASCADE ON DELETE CASCADE , GAME_ID REFERENCES PELIT(GAME_ID) ON UPDATE CASCADE ON DELETE CASCADE, HPK INT NOT NULL, HIFK INT NOT NULL, ILVES INT NOT NULL, JUKURIT INT NOT NULL, JYP INT NOT NULL, KALPA INT NOT NULL, KOOKOO INT NOT NULL, KARPAT INT NOT NULL, LUKKO INT NOT NULL, PELICANS INT NOT NULL, SAIPA INT NOT NULL, SPORT INT NOT NULL, TAPPARA INT NOT NULL, TPS INT NOT NULL, ASSAT INT NOT NULL, KUUSI_OIKEIN INT, KOKONAISPISTEET INT, CONSTRAINT DPG_PK PRIMARY KEY(DAY_ID, PLAYER_ID, GAME_ID))")
def update_player_points (name, data, day):
    try:
        c2.execute("INSERT INTO PELAAJIEN_PISTEET(PLAYER_ID, GAME_ID, HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, KUUSI_OIKEIN, KOKONAISPISTEET, DAY_ID) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (int(name[0]), int(name[1]), data[0] , data[1] , data[2] , data[3] , data[4] , data[5] , data[6] , data[7] , data[8] , data[9] , data[10] , data[11] , data[12] , data[13] , data[14] , data[15], data[16], day))
        conn2.commit()
        print("PLAYER: ",name[0]," GAME: ",name[1]," POINTS ARE UPDATED ",day)
    except:
        print("NO UPDATED! PLAYER: ",name[0]," GAME: ",name[1]," POINTS HAS UPDATED ",day)
def make_points ():
    day = datetime.date.today()
    c.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT FROM LIIGATILANNE WHERE DAY_ID = (SELECT MAX(DAY_ID) FROM LIIGATILANNE)")
    tilanne = c.fetchall()
    c2.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, PLAYER_ID, GAME_ID FROM PELAAJIEN_ARVAUKSET")
    pelaajat = c2.fetchall()
    for row in range(len(pelaajat)):
        update_player_points(pelaajat[row][15:17], laskenta(tilanne[0], pelaajat[row][0:15]), day)
def laskenta (tilanne, arvaus):
    kuusioikein = 0
    taulukko = []
    total = 0
    totalkuuis = 0
    pisteet = 0
    for x in range(15):
        if arvaus[x] == tilanne[x]:
            total = total + 3
            pisteet = pisteet + 3
            kuusioikein = kuusioikein + 1
        if arvaus[x] > tilanne [x]:
            total = total + 3-arvaus[x]+tilanne[x]
            pisteet = pisteet + 3-arvaus[x]+tilanne[x]
        if arvaus[x] < tilanne[x]:
            total = total + 3-tilanne[x]+arvaus[x]
            pisteet = pisteet + 3-tilanne[x]+arvaus[x]
        if arvaus[x] <= 6 and tilanne[x] <= 6:
            total = total + 1
            pisteet = pisteet + 1
        if (arvaus[x] == 1 and tilanne[x] == 1)or(arvaus[x] == 15 and tilanne[x] == 15):
            total = total + 1
            pisteet = pisteet + 1
            kuusioikein = kuusioikein + 1
        if arvaus[x] <= 10 and tilanne[x] <= 10:
            total = total + 1
            pisteet = pisteet + 1
        taulukko.append(pisteet)
        pisteet = 0
    if kuusioikein >= 6:
        totalkuuis = 1
        total = total + 1
    taulukko.append(totalkuuis)
    taulukko.append(total)
    return taulukko
def make_player ():
    Player_ID = 1
    Game_ID = 1
    Fname = "Tiina"
    Lname = "Kokeilu"
    data = [10,2,3,4,6,7,5,8,12,11,9,13,15,14,1]
    c2.execute("INSERT INTO PELIT(NAME) VALUES (?)",("Testi",))
    conn2.commit()
    c2.execute("INSERT INTO PELAAJAT(FIRST_NAME, LAST_NAME) VALUES (?,?)",(Fname,Lname))
    conn2.commit()
    c2.execute("INSERT INTO PELAAJIEN_ARVAUKSET(PLAYER_ID, GAME_ID, HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (Player_ID, Game_ID, data[0] , data[1] , data[2] , data[3] , data[4] , data[5] , data[6] , data[7] , data[8] , data[9] , data[10] , data[11] , data[12] , data[13] , data[14]))
    conn2.commit()
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS LIIGATILANNE(DAY_ID DATE, HPK INT, HIFK INT, ILVES INT, JUKURIT INT, JYP INT, KALPA INT, KOOKOO INT, KARPAT INT, LUKKO INT, PELICANS INT, SAIPA INT, SPORT INT, TAPPARA INT, TPS INT, ASSAT INT)")
def liiga_data(day, data):
    c.execute("INSERT INTO LIIGATILANNE ("+data+") VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(day ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
    conn.commit()
def joukkue_tabel(data):
    c.execute("CREATE TABLE IF NOT EXISTS "+ data + "(DAY_ID DATE, OTTELUT INTEGER PRIMARY KEY, VOITOT INT, TASAPELIT INT, LISA_PISTE INT, TEHDYT_MAALIT INT, PAASTETYT_MAALIT INT, PISTEET INT)")
def joukkue_data(day, data):
    c.execute("INSERT INTO "+data[0]+"(DAY_ID , OTTELUT, VOITOT, TASAPELIT, LISA_PISTE, TEHDYT_MAALIT, PAASTETYT_MAALIT, PISTEET) VALUES ( ?,?,?,?,?,?,?,?)", (day, data[1] , data[2] , data[3] , data[4] , data[5] , data[6] , data[7]))
    conn.commit()
def joukkue_OTTELU_chek(data):
    update = False
    for x in range(len(data)):
        joukkue_tabel(str(data[x][0]))
        c.execute("SELECT MAX(OTTELUT) FROM "+str(data[x][0]))
        joukkue_data = c.fetchone()
        if joukkue_data is not None:
            #print("Kannasta: ",joukkue_data[0])
            #print("verkosta: ",data[x][1])
            if joukkue_data[0] == data[x][1]:
                pass
                #print('sama') 
            else:
                update = True
                #print('ei sama')
        else:
            update = True
            #print("ei aiempaa dataa")
    if update:
        print("NEW UPDATE: "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        joukkue_data_updaet()
        #os.system('python Pelaajat.py')
    else:
        print("NO UPDATE: "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        pass
def joukkue_data_updaet():
    TIME = datetime.date.today()
    data = "DAY_ID"
    for x in range(len(tilanne)):
        data = data+", "+tilanne[x][0]
        try:
            joukkue_data(TIME, tilanne[x])
            print("UPDATE TEAM: ",tilanne[x][0])
        except:
            #print("NO UPDATE TEAM: ",tilanne[x][0])
            pass
    liiga_data(TIME, data)
    make_points()
    print("UPDATE DONE: "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))   
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        joukkueet = ["Lukko","K\\xc3\\xa4rp\\xc3\\xa4t","TPS","Tappara","Sport","Pelicans","KalPa","\\xc3\\x84ss\\xc3\\xa4t","KooKoo","SaiPa","HIFK","HPK","Ilves","Jukurit","JYP"]
        if data in joukkueet:
            if data == joukkueet[1]:
                tilanne.append(["KARPAT"])
            if data == joukkueet[7]:
                tilanne.append(["ASSAT"])
            if data != joukkueet[1] and data != joukkueet[7]:
                tilanne.append([str(data.upper())])
            else:
                pass
        else:
            try:
                if data.isdigit():
                    tilanne[len(tilanne)-1].append(int(data))   
            except:
                pass
counter = 0
play = True
create_gamers_list()
create_games_list()
create_players_guess()
create_players_points()
#make_player()
while play:
    try:
        response = urllib.request.urlopen('http://liiga.fi/sarjataulukko')
        parser = MyHTMLParser()
        parser.feed(str(response.read()))
    except EnvironmentError:
        print("ERROR! NO CONNECT: "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    create_table()
    joukkue_OTTELU_chek(tilanne)
    tilanne.clear()
    time.sleep(15)
c2.close()
c.close()
conn.close()
conn2.close()