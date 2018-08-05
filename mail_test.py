import smtplib
import config
import sqlite3

conn = sqlite3.connect('LiigaData.db')
c = conn.cursor()
conn2 = sqlite3.connect('PelaajaData.db')
c2 = conn2.cursor()
teams = ['HPK', 'HIFK', 'ILVES', 'JUKURIT', 'JYP', 'KALPA', 'KOOKOO', 'KARPAT', 'LUKKO', 'PELICANS', 'SAIPA', 'SPORT', 'TAPPARA', 'TPS', 'ASSAT']
def send_mail(to, subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.USER, config.SETUP)
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(config.USER, to, message)
        server.send
        server.quit
        print('EMAIL TO:',to,' SUCCEED')
    except:
        print('EMAIL TO:',to,' FAILL')
    
#send_mail(to,"testataas","Toimii")
def make_liiga_order():
    c.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, DAY_ID FROM LIIGATILANNE WHERE DAY_ID = (SELECT MAX(DAY_ID) FROM LIIGATILANNE)")
    row = c.fetchone()
    oder = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    for x in range(0,15):
        oder[row[x]-1] = teams[x]
    return(oder)

def make_Player_guess(Player_ID, Game_ID):
    c2.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT FROM PELAAJIEN_ARVAUKSET WHERE PELAAJIEN_ARVAUKSET.PLAYER_ID = "+str(Player_ID)+" AND PELAAJIEN_ARVAUKSET.GAME_ID = "+str(Game_ID))
    row = c2.fetchone()
    Poder = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    for x in range(0,15):
        Poder[int(row[x])-1] = teams[x]
        pass
    return(Poder)
def make_Player_point(Player_ID, Game_ID):
    c2.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT FROM PELAAJIEN_ARVAUKSET WHERE GAME_ID = "+str(Game_ID)+" AND PLAYER_ID = "+str(Player_ID))
    arvausrow = c2.fetchone()
    c2.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, KOKONAISPISTEET FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+" AND PLAYER_ID = "+str(Player_ID)+" AND DAY_ID = (SELECT MAX(DAY_ID) FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+")")
    row = c2.fetchone()
    points = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '','']
    #print(arvausrow)
    #print(row)
    for x in range(0,15):
        points[arvausrow[x]-1] = row[x]
        #print(points)
    points[15] = row[15]
    return(points)
def make_Player_order(Game_ID):
    c2.execute("SELECT MAX(DAY_ID) FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID))
    day = c2.fetchone()[0]
    c2.execute("SELECT KOKONAISPISTEET, FIRST_NAME, LAST_NAME, PELAAJAT.PLAYER_ID FROM PELAAJAT, PELAAJIEN_PISTEET WHERE PELAAJAT.PLAYER_ID = PELAAJIEN_PISTEET.PLAYER_ID AND PELAAJIEN_PISTEET.GAME_ID = "+str(Game_ID)+" AND DAY_ID = (SELECT MAX(DAY_ID) FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+") ORDER BY KOKONAISPISTEET DESC")
    member = None
    placeMember = 0
    players = c2.fetchall()
    for x in range(len(players)):
        if x != 0 and member == players[x][0]:
            players[x] = (placeMember, True, players[x][0], players[x][1], players[x][2], players[x][3])
        else:
            placeMember = placeMember + 1
            member = players[x][0]
            players[x] = (x+1, False, players[x][0], players[x][1], players[x][2], players[x][3])
        if x == 1 and placeMember == 1:
            players[0] = (players[0][0], True, players[0][2], players[0][3], players[0][4], players[0][5])
        else:
            pass
    return(players)
def make_Player_statistics(Player_ID, Game_ID):
    c2.execute("SELECT DAY_ID, HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, KOKONAISPISTEET FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+" AND PLAYER_ID = "+str(Player_ID)+" ORDER BY DAY_ID DESC")
    return(c2.fetchall())


def make_Player_list():
    c2.execute("SELECT PELAAJIEN_ARVAUKSET.PLAYER_ID, FIRST_NAME, LAST_NAME, PELAAJIEN_ARVAUKSET.GAME_ID, NAME, MAIL FROM PELAAJAT, PELAAJIEN_ARVAUKSET, PELIT WHERE MAIL IS NOT NULL AND PELAAJAT.PLAYER_ID IS PELAAJIEN_ARVAUKSET.PLAYER_ID AND PELIT.GAME_ID IS PELAAJIEN_ARVAUKSET.GAME_ID  ORDER BY PELAAJAT.PLAYER_ID ASC")
    return(c2.fetchall())

def make_Message():
    c.execute("SELECT MAX(DAY_ID) FROM LIIGATILANNE")
    day = c.fetchone()[0]
    for x in make_Player_list():
        #print('Player:',x[0],'Game:',x[3])
        msg = 'Hei '+x[1]
        tilanne = '\nTILANNE\tPISTEE\tPELAAJA'
        RuArPi = '\nRUNKOSARJA JA VEIKKAUS: '+day+'\n\nTILANNE\tRUNKOSARJA\tVEIKKAUS\tP'
        for y in make_Player_order(x[3]):
            if int(y[5]) == int(x[0]):
                if y[1]:
                    msg = msg + '\nOlet '+str(x[4])+' pelissa jaetulla sijalla '+str(y[0])
                else:
                    msg = msg + '\nOlet '+str(x[4])+' pelissa sijalla '+str(y[0])
            tilanne = tilanne + '\n'+str(y[0])+'.\t'+str(y[2])+'\t'+y[3]+' '+y[4]
        Runkosarja = make_liiga_order()
        Arvaus = make_Player_guess(x[0],x[3])
        Points = make_Player_point(x[0],x[3])
        history = '\nHISTORIASI\n\nPAIVAMAARA\tHPK\tHIFK\tILVES\tJUKURIT\tJYP\tKALPA\tKOOKOO\tKARPAT\tLUKKO\tPELICANS SAIPA\tSPORT\tTAPPARA\tTPS\tASSAT\tKOKONAISPISTEET'
        for z in range(len(Runkosarja)):
            bole1 = Runkosarja[z] == "PELICANS" and Arvaus[z] != "PELICANS"
            bole2 = Arvaus[z] == "PELICANS" and Runkosarja[z] != "PELICANS"
            bole3 = Runkosarja[z] == "PELICANS" and Arvaus[z] == "PELICANS"
            bole4 = Runkosarja[z] != "PELICANS" and Arvaus[z] != "PELICANS"            
            if bole1:
                RuArPi = RuArPi+'\n'+str(z+1)+'.\t'+Runkosarja[z]+'\t'+Arvaus[z]+'\t\t'+str(Points[z])
            if bole2:
                RuArPi = RuArPi+'\n'+str(z+1)+'.\t'+Runkosarja[z]+'\t\t'+Arvaus[z]+'\t'+str(Points[z])
            if bole3:
                RuArPi = RuArPi+'\n'+str(z+1)+'.\t'+Runkosarja[z]+'\t'+Arvaus[z]+' \t'+str(Points[z])
            if bole4:
                RuArPi = RuArPi+'\n'+str(z+1)+'.\t'+Runkosarja[z]+'\t\t'+Arvaus[z]+'\t\t'+str(Points[z])
            else:
                pass
        RuArPi = RuArPi+'\nKOKONAISPISTEESI: '+str(Points[15])
        for row in make_Player_statistics(x[0],x[3]):
            history = history +'\n'+str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])+'\t'+str(row[3])+'\t'+str(row[4])+'\t'+str(row[5])+'\t'+str(row[6])+'\t'+str(row[7])+'\t'+str(row[8])+'\t'+str(row[9])+'\t'+str(row[10])+'\t '+str(row[11])+'\t'+str(row[12])+'\t'+str(row[13])+'\t'+str(row[14])+'\t'+str(row[15])+'\t'+str(row[16])
        message = msg+'\n'+tilanne+'\n'+RuArPi+'\n'+history
        subject = 'LIIGAVEIKKAUS_PAIVITYS_'+day
        send_mail(x[5],subject,message)
        #print(message)

#print(make_liiga_order())
#print(make_Player_guess(2,2))
#print(make_Player_order(2))
#print(make_Player_statistics(1,1))
#print(make_Player_list())
#print(make_Player_point(1,1))
make_Message()