import datetime
import time
import urllib.request
import sqlite3
from html.parser import HTMLParser

conn = sqlite3.connect('LiigaData.db')
c = conn.cursor()
tilanne = []

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS LIIGATILANNE(datestamp TEXT, HPK INT, HIFK INT, ILVES INT, JUKURIT INT, JYP INT, KALPA INT, KOOKOO INT, KARPAT INT, LUKKO INT, PELICANS INT, SAIPA INT, SPORT INT, TAPPARA INT, TPS INT, ASSAT INT)")
def liiga_data(day, data):
    c.execute("INSERT INTO LIIGATILANNE ("+data+") VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(day ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
    conn.commit()
def joukkue_tabel(data):
    c.execute("CREATE TABLE IF NOT EXISTS "+ data + "(datestamp TEXT, OTTELUT INT, VOITOT INT, TASAPELIT INT, LISA_PISTE INT, TEHDYT_MAALIT INT, PAASTETYT_MAALIT INT, PISTEET INT)")
def joukkue_data(day, data):
    c.execute("INSERT INTO "+data[0]+"(datestamp , OTTELUT, VOITOT, TASAPELIT, LISA_PISTE, TEHDYT_MAALIT, PAASTETYT_MAALIT, PISTEET) VALUES ( ?,?,?,?,?,?,?,?)", (day, data[1] , data[2] , data[3] , data[4] , data[5] , data[6] , data[7]))
    conn.commit()
def joukkue_OTTELU_chek(data):
    update = False
    for x in range(len(data)):
        joukkue_tabel(str(data[x][0]))
        c.execute("SELECT OTTELUT FROM "+str(data[x][0])+"")
        joukkue_data = c.fetchall()
        if (len(joukkue_data)-1) >= 0:
            #print("Kannasta: ",joukkue_data[len(joukkue_data)-1][0])
            #print("verkosta: ",data[x][1])
            if joukkue_data[len(joukkue_data)-1][0] == data[x][1]:
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
    else:
        print("NO UPDATE: "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        pass
def joukkue_data_updaet():
    TIME = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    data = "datestamp "
    for x in range(len(tilanne)):
        data = data+", "+tilanne[x][0]
        joukkue_data(TIME, tilanne[x])
    liiga_data(TIME, data)
    print("UPDATE DONE: "+TIME)
    
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        joukkueet = ["Lukko","K\\xc3\\xa4rp\\xc3\\xa4t","TPS","Tappara","Sport","Pelicans","KalPa","\\xc3\\x84ss\\xc3\\xa4t","KooKoo","SaiPa","HIFK","HPK","Ilves","Jukurit","JYP"]
        if data in joukkueet:
            if data == joukkueet[1]:
                tilanne.append(["KARPAT"])
                #print("\n", "KARPAT")
            if data == joukkueet[7]:
                tilanne.append(["ASSAT"])
                #print("\n", "ASSAT")
            if data != joukkueet[1] and data != joukkueet[7]:
                tilanne.append([str(data.upper())])
                #print("\n", data.upper())
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

    
c.close()
conn.close()