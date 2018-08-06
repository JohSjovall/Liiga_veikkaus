import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

conn = sqlite3.connect('LiigaData.db')
c = conn.cursor()
conn2 = sqlite3.connect('PelaajaData.db')
c2 = conn2.cursor()
teams = ['HPK', 'HIFK', 'ILVES', 'JUKURIT', 'JYP', 'KALPA', 'KOOKOO', 'KARPAT', 'LUKKO', 'PELICANS', 'SAIPA', 'SPORT', 'TAPPARA', 'TPS', 'ASSAT']
def send_mail(to, subject, html):    
    try:
        me = config.USER
        setup = config.SETUP
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = to
        part = MIMEText(html, 'html')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(me, setup)
        server.sendmail(me, to, msg.as_string())
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
    c2.execute("SELECT HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, KOKONAISPISTEET, KUUSI_OIKEIN FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+" AND PLAYER_ID = "+str(Player_ID)+" AND DAY_ID = (SELECT MAX(DAY_ID) FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+")")
    row = c2.fetchone()
    points = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '','','']
    #print(arvausrow)
    #print(row)
    for x in range(0,15):
        points[arvausrow[x]-1] = row[x]
        #print(points)
    points[15] = row[15]
    points[16] = row[16]
    return(points)
def make_Player_order(Game_ID):
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
    c2.execute("SELECT DAY_ID, HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT, KUUSI_OIKEIN, KOKONAISPISTEET FROM PELAAJIEN_PISTEET WHERE GAME_ID = "+str(Game_ID)+" AND PLAYER_ID = "+str(Player_ID)+" ORDER BY DAY_ID DESC")
    return(c2.fetchall())


def make_Player_list():
    c2.execute("SELECT PELAAJIEN_ARVAUKSET.PLAYER_ID, FIRST_NAME, LAST_NAME, PELAAJIEN_ARVAUKSET.GAME_ID, NAME, MAIL FROM PELAAJAT, PELAAJIEN_ARVAUKSET, PELIT WHERE MAIL IS NOT NULL AND PELAAJAT.PLAYER_ID IS PELAAJIEN_ARVAUKSET.PLAYER_ID AND PELIT.GAME_ID IS PELAAJIEN_ARVAUKSET.GAME_ID  ORDER BY PELAAJAT.PLAYER_ID ASC")
    return(c2.fetchall())

def make_Message():
    c.execute("SELECT MAX(DAY_ID) FROM LIIGATILANNE")
    day = c.fetchone()[0]
    for x in make_Player_list():
        #print('Player:',x[0],'Game:',x[3])
        Runkosarja = make_liiga_order()
        Arvaus = make_Player_guess(x[0],x[3])
        Points = make_Player_point(x[0],x[3])
        head = '<p>Hei <b>'+x[1]+'</b></p>'
        table1 = ''
        table2 = ''
        table3 = ''
        h4 = '<p>KUUSI OIKEIN PISTE: '+str(Points[16])+'</p>'
        h2 = '<p>KOKONAISPISTEET: <b>'+str(Points[15])+'</b></p>'
        h1 = '<h3>'+str(x[4])+' RUNKOSARJA</h3>'
        h3 = '<h3>RUNKOSARJA JA VEIKKAUKSESI: '+day+'</h3>'
        for y in make_Player_order(x[3]):
            if int(y[5]) == int(x[0]):
                if y[1]:
                    head = head + '\n<p>Olet <b>'+str(x[4])+'</b> pelissa jaetulla sijalla <b>'+str(y[0])+'</b></p>'
                else:
                    head = head + '\n<p>Olet <b>'+str(x[4])+'</b> pelissa sijalla <b>'+str(y[0])+'</b></p>'
            table1 = table1 + '\n<tr>\n<td>'+str(y[0])+'.</td>\n<td>'+str(y[2])+'</td>\n<td>'+y[3]+' '+y[4]+'</td>\n</tr>'
        for z in range(len(Runkosarja)):
            table2 = table2+'\n<tr>\n<td>'+str(z+1)+'.</td>\n<td>'+Runkosarja[z]+'</td>\n<td>'+Arvaus[z]+'</td>\n<td>'+str(Points[z])+'</td>\n</tr>'
        for row in make_Player_statistics(x[0],x[3]):
            table3 = table3+'\n<tr>\n<td>'+str(row[0])+'</td>\n<td align:"center">'+str(row[1])+'</td>\n<td>'+str(row[2])+'</td>\n<td>'+str(row[3])+'</td>\n<td>'+str(row[4])+'</td>\n<td>'+str(row[5])+'</td>\n<td>'+str(row[6])+'</td>\n<td>'+str(row[7])+'</td>\n<td>'+str(row[8])+'</td>\n<td>'+str(row[9])+'</td>\n<td>'+str(row[10])+'</td>\n<td>'+str(row[11])+'</td>\n<td>'+str(row[12])+'</td>\n<td>'+str(row[13])+'</td>\n<td>'+str(row[14])+'</td>\n<td>'+str(row[15])+'</td>\n<td>'+str(row[16])+'</td>\n<td>'+str(row[17])+'</td>\n</tr>'
        message = '<html>\n<body>\n<font face="Arial">\n'+head+'\n<p> </p>\n'+h1+'\n<table style="width:50%">\n<tr>\n<th align='"'left'"'>SIJOITUS</th>\n<th align="left">PISTEET</th>\n<th align="left">PELAAJA</th>\n</tr>\n'+table1+'\n</table>\n<p> </p>\n'+h3+'<table style="width:50%">\n<tr>\n<th align="left">SIJOITUS</th>\n<th align="left">RUNKOSARJA</th>\n<th align="left">VEIKKAUKSESI</th>\n<th align="left">PISTEET</th>\n</tr>\n'+table2+'\n</table>\n'+h4+'\n'+h2+'\n<p> </p>\n<h3>HISTORIASI</h3>\n<table style="width:100%">\n<tr>\n<th align="left">PAIVAMAARA</th>\n<th align="left">HPK</th>\n<th align="left">HIFK</th>\n<th align="left">ILVES</th>\n<th align="left">JUKURIT</th>\n<th align="left">JYP</th>\n<th align="left">KALPA</th>\n<th align="left">KOOKOO</th>\n<th align="left">KARPAT</th>\n<th align="left">LUKKO</th>\n<th align="left">PELICANS</th>\n<th align="left">SAIPA</th>\n<th align="left">SPORT</th>\n<th align="left">TAPPARA</th>\n<th align="left">TPS</th>\n<th align="left">ASSAT</th>\n<th align="left">KUUSI_OIKEIN</th>\n<th align="left">KOKONAISPISTEET</th>\n</tr>\n'+table3+'\n</table>\n</font>\n</body>\n</html>'
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