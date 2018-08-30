import csv
import sqlite3
import configure_player as con_player
import Consol

conn = sqlite3.connect('Database_liiga_game.db')
c = conn.cursor()

def csv_read_test(dokument_name):
    print("---------------------------------------------")
    with open("Game_CSV_files/"+dokument_name+'.csv', 'r') as file:
        csv_reader_1 = csv.reader(file)
        next(csv_reader_1)
        continue_reder = True
        for line in csv_reader_1:
            teamList=[]
            miss = False
            tooMuch = []
            missTemas = ['HPK', 'HIFK', 'ILVES', 'JUKURIT', 'JYP', 'KALPA', 'KARPAT', 'LUKKO', 'PELICANS', 'SAIPA', 'SPORT', 'TAPPARA', 'TPS', 'ASSAT', 'KOOKOO']
            for x in range(5,20):
                if line[x] in teamList:
                    tooMuch.append(line[x])
                    miss = True
                    continue_reder = False
                else:
                    teamList.append(line[x])
            if miss:
                print(line[3].upper(),line[4].upper(),line[1])
                print("TO MANY TIME: "+str(tooMuch))
                for x in teamList:
                    if x in missTemas:
                        missTemas.remove(x)
                    else:
                        pass
                print("NO NAME ON LIST: "+str(missTemas))
                print("---------------------------------------------")
        if continue_reder:
            read_csv_dokument(dokument_name)
            pass
def read_csv_dokument(dokument_name):
    c.execute("SELECT Game_Name FROM GAMES WHERE Game_Name = '"+str(dokument_name.upper())+"'")
    IsNone = c.fetchone() == None
    if IsNone:
        c.execute("SELECT MAX(Player_ID) FROM PLAYERS")
        maxPID = c.fetchone()[0]
        if maxPID is None:
            maxPID = 1
        else:
            maxPID += 1
        c.execute("SELECT MAX(Game_ID) FROM GAMES")
        maxGID = c.fetchone()[0]
        if maxGID is None:
            maxGID = 1
        else:
            maxGID += 1
        new_game(maxGID,dokument_name)
        with open("Game_CSV_files/"+dokument_name+'.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader:
                guesses = ""
                if line[2] != "Ei":
                    mail=line[1]
                else:
                    mail=None
                for x in range(5,20):
                    guesses += ","+line[x]
                maxPID = make_player_and_guess(maxPID, maxGID, guesses, line[3:5],mail)
        print("---------------------------------------------")
        Consol.Message("NEW PLAYER DATA ADD")
        con_player.create_games_tables()
        con_player.make_updates()
        print("---------------------------------------------")
    else:
        print("GAME NAME IS ON USE!")
        print("---------------------------------------------")
        pass
def new_player_guess(pID, gID, data):
    c.execute("INSERT INTO PLAYERS_GUESSES (Player_ID, Game_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pID,gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
    conn.commit()
    print("NEW PLAYER GUESS PLAYER:"+str(pID)+" GAME:"+str(gID)+" IS DONE")
    print("---------------------------------------------")
def new_player(pID,name,mail):
    c.execute("INSERT INTO PLAYERS(Player_ID, First_Name, Last_Name, Mail) VALUES (?,?,?,?)",(pID,name[0].upper(),name[1].upper(),mail))
    conn.commit()
    print("NEW PLAYER: "+name[0].upper()+" "+name[1].upper()+" ID NUMBER: "+str(pID)+" IS DONE")
def new_game(gID, name):
    c.execute("INSERT INTO GAMES(Game_ID, Game_Name) VALUES (?,?)",(gID,name.upper()))
    conn.commit()
    print("NEW GAME: "+name.upper()+" ID NUMBER: "+str(gID)+" IS DONE")
    print("---------------------------------------------")
def make_player_and_guess(pID, gID, data,pName,mail):
    if mail is None:
        c.execute("SELECT Player_ID FROM PLAYERS WHERE First_Name = ? AND Last_Name = ? AND Mail IS NULL",(pName[0].upper(),pName[1].upper()))
    else:
        c.execute("SELECT Player_ID FROM PLAYERS WHERE First_Name = ? AND Last_Name = ? AND Mail = ?",(pName[0].upper(),pName[1].upper(),mail))
    playerID = c.fetchone()
    if playerID is None:
        c.execute("INSERT INTO PLAYERS (Player_ID, First_Name, Last_Name, Mail) VALUES (?,?,?,?)",(pID,pName[0].upper(),pName[1].upper(),mail))
        conn.commit()
        print("NEW PLAYER: "+pName[0].upper()+" "+pName[1].upper()+" ID NUMBER: "+str(pID)+" IS DONE")
        c.execute("INSERT INTO PLAYERS_GUESSES (Player_ID, Game_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pID,gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
        conn.commit()
        print("NEW PLAYER GUESS PLAYER:"+str(pID)+" GAME:"+str(gID)+" IS DONE")
        return(pID+1)
    else:
        c.execute("SELECT Game_ID FROM PLAYERS_GUESSES WHERE Player_ID = ?",(playerID[0],))
        if gID in c.fetchall():
            print("PLAYER "+pName[0].upper()+" "+pName[1].upper()+" IS REDEY IN THE GAME")
        else:
            print("PLAYER: "+pName[0].upper()+" "+pName[1].upper()+" IS REDY")
            c.execute("INSERT INTO PLAYERS_GUESSES (Player_ID, Game_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(playerID[0],gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
            conn.commit()
            print("NEW PLAYER GUESS PLAYER:"+str(pID)+" GAME: "+str(gID)+" IS DONE")
        return(pID)

while True:
    try:
        csv_read_test(str(input("CSV FILE NAME: ")))
    except Exception as e:
        print(e)