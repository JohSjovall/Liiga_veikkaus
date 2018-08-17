import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configure
import Consol

conn = sqlite3.connect('Database_liiga_game.db')
c = conn.cursor()
teams_list = "HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT"
team_list = ["HPK", "HIFK", "ILVES", "JUKURIT", "JYP", "KALPA", "KOOKOO", "KARPAT", "LUKKO", "PELICANS", "SAIPA", "SPORT", "TAPPARA", "TPS", "ASSAT"]

def send_mail(to, subject, html):    
    try:
        me = configure.USER
        setup = configure.SETUP
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
        Consol.Message('EMAIL TO: '+to+' SUCCEED')
    except:
        Consol.Message('EMAIL TO: '+to+' FAILL')
def make_liiga_league_table_order():
    order = ["","","","","","","","","","","","","","",""]
    counter = 0
    try:
        c.execute("SELECT "+teams_list+" FROM LIIGA_LEAGUE_TABLE WHERE Day_ID = (SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE)")
        for team in c.fetchone():
            order[team-1] = team_list[counter]
            counter += 1
        return order
    except:
        return None
def make_players_list():
    c.execute("SELECT PLAYERS_GUESSES.Player_ID, PLAYERS_GUESSES.Game_ID, PLAYERS.Mail FROM PLAYERS_GUESSES, PLAYERS WHERE PLAYERS_GUESSES.Player_ID = PLAYERS.Player_ID AND Mail IS NOT NULL")
    return c.fetchall()

def make_players_guesses_table_order(PlayerGame):
    order = ["","","","","","","","","","","","","","","","",""]
    counter = 0
    c.execute("SELECT "+teams_list+", Six_Correct_Point, Points FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ? AND Day_ID = (SELECT MAX(Day_ID) FROM PLAYERS_POINTS)",(PlayerGame[0],PlayerGame[1]))
    points = c.fetchone()
    try:
        c.execute("SELECT "+teams_list+" FROM PLAYERS_GUESSES WHERE Player_ID = ? AND Game_ID = ?",(PlayerGame[0],PlayerGame[1]))
        for team in c.fetchone():
            order[team-1] = (team_list[counter],points[counter])
            counter += 1
        order[15] = ("Six_Correct_Point",points[15])
        order[16] = ("Points",points[16])
        return order
    except:
        return None
def make_Player_statistics(PlayerGame):
    c.execute("SELECT Day_ID, "+teams_list+", Six_Correct_Point, Points FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ? ORDER BY Day_ID DESC",(PlayerGame[0],PlayerGame[1]))
    return(c.fetchall())
def make_game_table_order(name):
    c.execute("SELECT Place, Points, First_Name, Last_Name, Day_ID FROM "+name+" WHERE Day_ID = (SELECT MAX(Day_ID) FROM "+name+") ORDER BY Points DESC")
    return c.fetchall()
def get_player_Shared_Place_and_Place_and_Day_ID(name,player_id):
    c.execute("SELECT Shared_Place, Place, Day_ID FROM "+str(name)+" WHERE Day_ID = (SELECT MAX(Day_ID) FROM "+str(name)+" ) AND Player_ID = "+str(player_id))
    return c.fetchone()
def get_game_name(game_id):
    c.execute("SELECT Game_Name FROM GAMES WHERE Game_ID = ?",(game_id,))
    return c.fetchone()[0]
def get_player_name(player_id):
    c.execute("SELECT First_Name, Last_Name FROM PLAYERS WHERE Player_ID = ?",(player_id,))
    return c.fetchone()
def make_messages():
    league_table = make_liiga_league_table_order()
    for x in make_players_list():
        pName = get_player_name(x[0])
        gName = get_game_name(x[1])
        sp_pl_di = get_player_Shared_Place_and_Place_and_Day_ID(gName, x[0])
        pPoints = make_players_guesses_table_order(x)
        gTable = make_game_table_order(gName)
        day = gTable[0][4]
        head = '<p>Hei <b>'+pName[0]+'</b></p>'
        if sp_pl_di[0]==1:
            head += '\n<p>Olet <b>'+gName+'</b> pelissa jaetulla sijalla <b>'+str(sp_pl_di[1])+'</b></p>'
        else:
            head += '\n<p>Olet <b>'+gName+'</b> pelissa sijalla <b>'+str(sp_pl_di[1])+'</b></p>'
        table1 = ''
        table2 = ''
        table3 = ''
        h4 = '<p>KUUSI OIKEIN PISTE: '+str(pPoints[15][1])+'</p>'
        h2 = '<p>KOKONAISPISTEET: <b>'+str(pPoints[16][1])+'</b></p>'
        h1 = '<h3>'+gName+' RUNKOSARJA</h3>'
        h3 = '<h3>RUNKOSARJA JA VEIKKAUKSESI: '+day+'</h3>'
        for y in gTable:
            table1 +='\n<tr>\n<td>'+str(y[0])+'.</td>\n<td>'+str(y[1])+'</td>\n<td>'+y[2]+' '+y[3]+'</td>\n</tr>'
        for z in range(15):
            table2 += '\n<tr>\n<td>'+str(z+1)+'.</td>\n<td>'+league_table[z]+'</td>\n<td>'+pPoints[z][0]+'</td>\n<td>'+str(pPoints[z][1])+'</td>\n</tr>'
        for row in make_Player_statistics(x):
            table3 += '\n<tr>\n<td>'+str(row[0])+'</td>\n<td align:"center">'+str(row[1])+'</td>\n<td>'+str(row[2])+'</td>\n<td>'+str(row[3])+'</td>\n<td>'+str(row[4])+'</td>\n<td>'+str(row[5])+'</td>\n<td>'+str(row[6])+'</td>\n<td>'+str(row[7])+'</td>\n<td>'+str(row[8])+'</td>\n<td>'+str(row[9])+'</td>\n<td>'+str(row[10])+'</td>\n<td>'+str(row[11])+'</td>\n<td>'+str(row[12])+'</td>\n<td>'+str(row[13])+'</td>\n<td>'+str(row[14])+'</td>\n<td>'+str(row[15])+'</td>\n<td>'+str(row[16])+'</td>\n<td>'+str(row[17])+'</td>\n</tr>'
        message = '<html>\n<body>\n<style>\ntable, th, td {\nborder: 1px solid black;\nborder-collapse: collapse;\n}\nth {\ntext-align: left;\n}\n</style>\n<font face="Arial">\n'+head+'\n<p> </p>\n'+h1+'\n<table style="width:25%">\n<tr align="left">\n<th>SIJOITUS</th>\n<th>PISTEET</th>\n<th>PELAAJA</th>\n</tr>\n'+table1+'\n</table>\n<p> </p>\n'+h3+'<table style="width:25%">\n<tr align="left">\n<th>SIJOITUS</th>\n<th>RUNKOSARJA</th>\n<th>VEIKKAUKSESI</th>\n<th>PISTEET</th>\n</tr>\n'+table2+'\n</table>\n'+h4+'\n'+h2+'\n<p> </p>\n<h3>HISTORIASI</h3>\n<table table style="width:80%">\n<tr align="left">\n<th>PAIVAMAARA</th>\n<th>HPK</th>\n<th>HIFK</th>\n<th>ILVES</th>\n<th>JUKURIT</th>\n<th>JYP</th>\n<th>KALPA</th>\n<th>KOOKOO</th>\n<th>KARPAT</th>\n<th>LUKKO</th>\n<th>PELICANS</th>\n<th>SAIPA</th>\n<th>SPORT</th>\n<th>TAPPARA</th>\n<th>TPS</th>\n<th>ASSAT</th>\n<th>KUUSI_OIKEIN</th>\n<th>KOKONAISPISTEET</th>\n</tr>\n'+table3+'\n</table>\n</font>\n</body>\n</html>'
        subject = "LIIGAVEIKKAUS PELI "+gName+" "+day
        send_mail(x[2],subject,message)