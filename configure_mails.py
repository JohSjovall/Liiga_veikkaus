import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configure
import Consol

teams_list = "HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT"
team_list = ["HPK", "HIFK", "ILVES", "JUKURIT", "JYP", "KALPA", "KOOKOO", "KARPAT", "LUKKO", "PELICANS", "SAIPA", "SPORT", "TAPPARA", "TPS", "ASSAT"]

def send_mail(to, subject, html):    
    try:
        me = configure.USER
        setup = configure.SETUP
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = to
        part = MIMEText(html, 'html')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(me, setup)
        server.sendmail(me, to, msg.as_string())
        server.quit
        Consol.Message('EMAIL TO: '+to+' SUCCEED')
    except:
        Consol.Message('EMAIL TO: '+to+' FAILL')
def make_liiga_league_table_order(c):
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
def make_players_list(c):
    c.execute("SELECT PLAYERS_GUESSES.Player_ID, PLAYERS_GUESSES.Game_ID, PLAYERS.Mail FROM PLAYERS_GUESSES, PLAYERS WHERE PLAYERS_GUESSES.Player_ID = PLAYERS.Player_ID AND Mail IS NOT NULL")
    return c.fetchall()

def make_admin_list(c):
    c.execute("SELECT Mail, Games_ID FROM ADMINS WHERE Mail IS NOT NULL")
    return c.fetchall()

def make_players_guesses_table_order(PlayerGame,c):
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
def make_Player_statistics(PlayerGame,c):
    c.execute("SELECT Day_ID, "+teams_list+", Six_Correct_Point, Points FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ? ORDER BY Day_ID DESC",(PlayerGame[0],PlayerGame[1]))
    return(c.fetchall())
def make_game_table_order(name,c):
    c.execute("SELECT Place, Points, First_Name, Last_Name, Day_ID, Player_ID FROM "+name+" WHERE Day_ID = (SELECT MAX(Day_ID) FROM "+name+") ORDER BY Points DESC")
    return c.fetchall()
def points_change(name, player_id,c):
    c.execute("SELECT Points FROM "+name+" WHERE Player_ID = "+str(player_id)+" ORDER BY Day_ID DESC")
    first = c.fetchone()[0]
    try:
        second = c.fetchone()[0]
    except:
        second = first
    if first >= second:
        return '+'+str(first-second)
    else:
        return str(first-second)
def place_change(name, player_id,c):
    c.execute("SELECT Place FROM "+name+" WHERE Player_ID = "+str(player_id)+" ORDER BY Day_ID DESC")
    first = c.fetchone()[0]
    try:
        second = c.fetchone()[0]
    except:
        second = first
    if first < second:
        return '&nbsp;&#8896; '+str(abs(first-second))#arrow up
    elif first > second:
        return '&nbsp;&#8897; '+str(abs(first-second))#arrow down
    else:
        return '&nbsp;&#9472;&nbsp;'
def get_player_Shared_Place_and_Place_and_Day_ID(name,player_id,c):
    c.execute("SELECT Shared_Place, Place, Day_ID FROM "+str(name)+" WHERE Day_ID = (SELECT MAX(Day_ID) FROM "+str(name)+" ) AND Player_ID = "+str(player_id))
    return c.fetchone()
def get_game_name(game_id,c):
    c.execute("SELECT Game_Name FROM GAMES WHERE Game_ID = ?",(game_id,))
    return c.fetchone()[0]
def get_player_name(player_id,c):
    c.execute("SELECT First_Name, Last_Name FROM PLAYERS WHERE Player_ID = ?",(player_id,))
    return c.fetchone()
def make_messages(c):
    league_table = make_liiga_league_table_order(c)
    c.execute("SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE")
    day = c.fetchone()[0]
    for x in make_players_list(c):
        pName = get_player_name(x[0],c)
        gName = get_game_name(x[1],c)
        sp_pl_di = get_player_Shared_Place_and_Place_and_Day_ID(gName, x[0],c)
        pPoints = make_players_guesses_table_order(x,c)
        head = '<p>Hei <b>'+pName[0]+'</b></p>'
        if sp_pl_di[0]==1:
            head += '\n<p>Olet <b>'+gName+'</b> pelissa jaetulla sijalla <b>'+str(sp_pl_di[1])+'</b></p>'
        else:
            head += '\n<p>Olet <b>'+gName+'</b> pelissa sijalla <b>'+str(sp_pl_di[1])+'</b></p>'
        table2 = ''
        table3 = ''
        h4 = '\n<p>KUUSI OIKEIN PISTE: '+str(pPoints[15][1])+'</p>'
        h2 = '\n<p>KOKONAISPISTEET: <b>'+str(pPoints[16][1])+'</b></p>'
        h3 = '<h3>RUNKOSARJA JA VEIKKAUKSESI: '+str(day)+'</h3>'
        for z in range(15):
            table2 += '\n<tr>\n<td>'+str(z+1)+'.</td>\n<td>'+league_table[z]+'</td>\n<td>'+pPoints[z][0]+'</td>\n<td>'+str(pPoints[z][1])+'</td>\n</tr>'
        for row in make_Player_statistics(x,c):
            table3 += '\n<tr>\n<td>'+str(row[0])+'</td>\n<td align:"center">'+str(row[1])+'</td>\n<td>'+str(row[2])+'</td>\n<td>'+str(row[3])+'</td>\n<td>'+str(row[4])+'</td>\n<td>'+str(row[5])+'</td>\n<td>'+str(row[6])+'</td>\n<td>'+str(row[7])+'</td>\n<td>'+str(row[8])+'</td>\n<td>'+str(row[9])+'</td>\n<td>'+str(row[10])+'</td>\n<td>'+str(row[11])+'</td>\n<td>'+str(row[12])+'</td>\n<td>'+str(row[13])+'</td>\n<td>'+str(row[14])+'</td>\n<td>'+str(row[15])+'</td>\n<td>'+str(row[16])+'</td>\n<td>'+str(row[17])+'</td>\n</tr>'
        message = '''
<html>
<body>
<style>
table, th, td {
border: 1px solid black;
border-collapse: collapse;
}
th {
text-align: left;
}
</style>
<font face="Arial">'''+head+'''
<p> </p>
'''+h3+'''<table style="width:25%">
<tr align="left">
<th>SIJOITUS</th>
<th>RUNKOSARJA</th>
<th>VEIKKAUKSESI</th>
<th>PISTEET</th>
</tr>'''+table2+'''</table>
'''+h4+h2+'''
<p> </p>
<h3>HISTORIASI</h3>
<table table style="width:80%">
<tr align="left">
<th>PAIVAMAARA</th>
<th>HPK</th>
<th>HIFK</th>
<th>ILVES</th>
<th>JUKURIT</th>
<th>JYP</th>
<th>KALPA</th>
<th>KOOKOO</th>
<th>KARPAT</th>
<th>LUKKO</th>
<th>PELICANS</th>
<th>SAIPA</th>
<th>SPORT</th>
<th>TAPPARA</th>
<th>TPS</th>
<th>ASSAT</th>
<th>KUUSI_OIKEIN</th>
<th>KOKONAISPISTEET</th>
</tr>'''+table3+'''
</table>
</font>
</body>
</html>'''
        subject = "LIIGAVEIKKAUS PELI "+gName+" "+day
        send_mail(x[2],subject,message)
def make_admin_messages(c):
    c.execute("SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE")
    day = c.fetchone()[0]
    for x in make_admin_list(c):
        for game_id in x[1]:
            gName = get_game_name(int(game_id),c)
            h1 = '<h3>'+gName+' RUNKOSARJA '+str(day)+'</h3>'
            table1 = ''
            gTable = make_game_table_order(gName,c)
            for y in gTable:
                table1 +='\n<tr>\n<td>'+str(y[0])+'.</td>\n<td>'+y[2]+' '+y[3]+'</td>\n<td>'+str(y[1])+'</td>\n<td>'+points_change(gName,y[5],c)+'</td>\n<td>'+place_change(gName,y[5],c)+'</td>\n</tr>'
            message ='''
<html>
<body>
<style>
table, th, td {
border: 1px solid black;
border-collapse: collapse;
}
th {
text-align: left;
}
</style>
<font face="Arial">'''+h1+'''
<table style="width:50%">
<tr align="left">
<th>SIJOITUS</th>
<th>PELAAJA</th>
<th>PISTEET</th>
<th>PISTE MUUTOS</th>
<th>SIJOITUS MUUTOS</th>
</tr>'''+table1+'''
</table>
<p> </p>
</font>
</body>
</html>
'''
            subject = gName+" RUNKOSARJA "+day
            send_mail(x[0],subject,message)
def send_mail_players_and_admin():
    conn = sqlite3.connect('Database_liiga_game.db')
    c = conn.cursor()
    Consol.Message('PLAYERS MAILS SENDIN')
    try:
        make_messages(c)
    except:
        Consol.Message('ERROR: PLAYERS MAILS SENDIN FAILL')
    Consol.Message('ADMIN MAILS SENDIN')
    try:
        make_admin_messages(c)
    except:
        Consol.Message('ERROR: ADMINS MAILS SENDIN FAILL')