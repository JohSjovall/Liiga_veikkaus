import csv
import sqlite3

conn2 = sqlite3.connect('PelaajaData.db')
c2 = conn2.cursor()

def csv_read_test(dokument_name):
    with open("Game_CSV_files/"+dokument_name+'.csv', 'r') as file:
        csv_reader_1 = csv.reader(file)
        next(csv_reader_1)
        for line in csv_reader_1:
            TeamList=[]
            puutuva = False
            liikaa = []
            joukkue = ['HPK', 'HIFK', 'ILVES', 'JUKURIT', 'JYP', 'KALPA', 'KARPAT', 'LUKKO', 'PELICANS', 'SAIPA', 'SPORT', 'TAPPARA', 'TPS', 'ASSAT', 'KOOKOO']
            for x in range(5,20):
                if line[x] in TeamList:
                    liikaa.append(line[x])
                    puutuva = True
                else:
                    TeamList.append(line[x])
        if puutuva:
            print(line[3].upper(),line[4].upper(),line[1])
            print("LISTASSA ESINTYY USESTI",liikaa)
            for x in TeamList:
                if x in joukkue:
                    joukkue.remove(x)
                else:
                    pass
            print("LISTASTA PUUTTUU:",joukkue)
            print("---------------------------------------------")
        else:
            read_csv_dokument(dokument_name)
            pass
def read_csv_dokument(dokument_name):
    c2.execute("SELECT name FROM PELIT WHERE NAME = "+"'"+dokument_name.upper()+"'")
    IsNone = c2.fetchone()
    if IsNone is None:
        c2.execute("SELECT MAX(PLAYER_ID) FROM PELAAJAT")
        idP = c2.fetchone()[0]
        if idP is None:
            idP = 1
        else:
            idP = idP + 1
        c2.execute("SELECT MAX(GAME_ID) FROM PELIT")
        idG = c2.fetchone()[0]
        if idG is None:
            idG = 1
        else:
            idG = idG + 1
        new_game(idG,dokument_name)
        with open("Game_CSV_files/"+dokument_name+'.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader:
                arvaus = ""
                if line[2] != "Ei":
                    mail=line[1]
                else:
                    mail=None
                new_player(idP,line[3:5],mail)
                for x in range(5,20):
                    arvaus = arvaus+","+line[x]
                new_player_guess(int(idP), idG, arvaus)
                idP = idP + 1
    else:
        print("GAME NAME IS ON USE!")
        print("---------------------------------------------")
        pass
def new_player_guess(pID, gID, data):
    c2.execute("INSERT INTO PELAAJIEN_ARVAUKSET (PLAYER_ID, GAME_ID"+data+") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pID,gID,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15))
    conn2.commit()
    print("NEW PLAYER GUESS PLAYER ID NUMBER:",pID,"GAME ID NUMBER:",gID,"IS DONE")
    print("---------------------------------------------")
def new_player(pID,name,mail):
    c2.execute("INSERT INTO PELAAJAT(PLAYER_ID,FIRST_NAME, LAST_NAME,MAIL) VALUES (?,?,?,?)",(pID,name[0].upper(),name[1].upper(),mail))
    conn2.commit()
    print("NEW PLAYER: ",name[0].upper(),"",name[1].upper(),"ID NUMBER: ",pID," IS DONE")
def new_game(gID, name):
    c2.execute("INSERT INTO PELIT(GAME_ID, NAME) VALUES (?,?)",(gID,name.upper()))
    conn2.commit()
    print("NEW GAME: ",name.upper(),"ID NUMBER: ",gID," IS DONE")
    print("---------------------------------------------")
while True:
    try:
        csv_read_test(str(input("ANNA CSV TIEDOTON NIMI: ")))
    except Exception as e:
        print(e)