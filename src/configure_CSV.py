import csv
import sqlite3
import configure_player as con_player
import Consol
from configure import DB


def csv_read_test(dokument_name):
    print("---------------------------------------------")
    with open("./Game_CSV_files/"+dokument_name+'.csv', 'r') as file:
        csv_reader_1 = csv.reader(file)
        next(csv_reader_1)
        continue_reder = True
        for line in csv_reader_1:
            teamList=[]
            miss = False
            tooMuch = []
            missTemas = ["HPK", "HIFK", "ILVES", "JUKURIT", "JYP", "KALPA", "KIEKKO-ESPOO", "KOOKOO", "KARPAT", "LUKKO", "PELICANS", "SAIPA", "SPORT", "TAPPARA", "TPS", "ASSAT"]
            for x in range(5,21):
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
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT Game_Name FROM GAMES WHERE Game_Name = ?", [str(dokument_name.upper())])
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
        new_game(maxGID,dokument_name,c,conn)
        with open("Game_CSV_files/"+dokument_name+'.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader:
                guesses = ""
                if line[2] != "Ei":
                    mail=line[1]
                else:
                    mail=None
                for x in range(5,21):
                    #fix team naming
                    if line[x] == "KIEKKO-ESPOO":
                        guesses += ",KESPOO"
                    else:
                        guesses += ","+line[x]
                maxPID = make_player_and_guess(maxPID, maxGID, guesses, line[3:5],mail,c,conn)
        print("---------------------------------------------")
        Consol.Message("NEW PLAYER DATA ADD")
        con_player.create_games_tables()
        #con_player.make_updates()
        print("---------------------------------------------")
        sheet_options(maxGID, c, conn)
    else:
        print("GAME NAME IS ON USE!")
        print("---------------------------------------------")
        pass
    conn.close()
def new_player_guess(pID, gID, data,c: sqlite3.Cursor,conn: sqlite3.Connection):
    c.execute("INSERT INTO PLAYERS_GUESSES (Player_ID, Game_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pID,gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15, 16))
    conn.commit()
    print("NEW PLAYER GUESS PLAYER:"+str(pID)+" GAME:"+str(gID)+" IS DONE")
    print("---------------------------------------------")
def new_player(pID,name,mail,c: sqlite3.Cursor,conn: sqlite3.Connection):
    c.execute("INSERT INTO PLAYERS(Player_ID, First_Name, Last_Name, Mail) VALUES (?,?,?,?)",(pID,name[0].upper(),name[1].upper(),mail))
    conn.commit()
    print("NEW PLAYER: "+name[0].upper()+" "+name[1].upper()+" ID NUMBER: "+str(pID)+" IS DONE")
def new_game(gID, name,c: sqlite3.Cursor,conn: sqlite3.Connection):
    c.execute("INSERT INTO GAMES(Game_ID, Game_Name) VALUES (?,?)",(gID,name.upper()))
    conn.commit()
    print("NEW GAME: "+name.upper()+" ID NUMBER: "+str(gID)+" IS DONE")
    print("---------------------------------------------")
def make_player_and_guess(pID, gID, data,pName,mail,c: sqlite3.Cursor,conn: sqlite3.Connection):
    if mail is None:
        c.execute("SELECT Player_ID FROM PLAYERS WHERE First_Name = ? AND Last_Name = ? AND Mail IS NULL",(pName[0].upper(),pName[1].upper()))
    else:
        c.execute("SELECT Player_ID FROM PLAYERS WHERE First_Name = ? AND Last_Name = ? AND Mail = ?",(pName[0].upper(),pName[1].upper(),mail))
    playerID = c.fetchone()
    if playerID is None:
        c.execute("INSERT INTO PLAYERS (Player_ID, First_Name, Last_Name, Mail) VALUES (?,?,?,?)",(pID,pName[0].upper(),pName[1].upper(),mail))
        conn.commit()
        print("NEW PLAYER: "+pName[0].upper()+" "+pName[1].upper()+" ID NUMBER: "+str(pID)+" IS DONE")
        c.execute("INSERT INTO PLAYERS_GUESSES (Player_ID, Game_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pID,gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15, 16))
        conn.commit()
        print("NEW PLAYER GUESS PLAYER:"+str(pID)+" GAME:"+str(gID)+" IS DONE")
        return(pID+1)
    else:
        c.execute("SELECT Game_ID FROM PLAYERS_GUESSES WHERE Player_ID = ?",(playerID[0],))
        if gID in c.fetchall():
            print("PLAYER "+pName[0].upper()+" "+pName[1].upper()+" IS REDEY IN THE GAME")
        else:
            print("PLAYER: "+pName[0].upper()+" "+pName[1].upper()+" IS REDY")
            c.execute("INSERT INTO PLAYERS_GUESSES (Player_ID, Game_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(playerID[0],gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15, 16))
            conn.commit()
            print("NEW PLAYER GUESS PLAYER:"+str(pID)+" GAME: "+str(gID)+" IS DONE")
        return(pID)
def sheet_options(game_id: int, c: sqlite3.Cursor, conn: sqlite3.Connection):
    print("--------------SHEET CONFIGURE START--------------")
    while True:
        inputValaue = str(input("SET SHEET CONFIGURES (yes/no): "))
        if inputValaue.upper() == 'YES':
            sheet_configure(game_id, c, conn)
            break
        if inputValaue.upper() == 'NO':
            break
        else:
            print('not validation value!')
    print("--------------SHEET CONFIGURE END--------------")

def sheet_configure(game_id: int, c: sqlite3.Cursor, conn: sqlite3.Connection):
    state = str(input("GAME SHEET STATE NAME: "))
    history = str(input("GAME SHEET HISTORY NAME: "))
    print('ORDERS | 0 = First Name Last Name | 1 = Last Name First Name |')
    order = 1
    while True:
        inputValaue = str(input("GAME SHEET ORDER: "))
        if inputValaue == '1':
            order = 1
            break
        if inputValaue == '0':
            order = 0
            break
        else:
            print('not validation value!')
    c.execute('INSERT INTO SHEET(Game_ID, Game_staus, Game_history, List_Order) VALUES (?,?,?,?)',(game_id, state, history, order))
    conn.commit()

while True:
    try:
        csv_read_test(str(input("CSV FILE NAME: ")))
    except Exception as e:
        print(e)