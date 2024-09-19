import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configure
import helpper
import Consol
from configure import TEAMS_LIST_STRING as teams_list
from configure import TEAMS_LIST as team_list
from configure import DB
from player_data import Player_Data
from player_data import Team
from player_data import Player_history_round
from player_data import History_Team
from player_data import Admin_Contacts
from player_data import Player_Game_Status

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
    except:
        Consol.ErroMessage('EMAIL TO: '+to+' FAILL')
def make_liiga_league_table_order():
    c = helpper.connectDB()
    order = []
    try:
        c.execute("SELECT Day_ID, "+teams_list+" FROM LIIGA_LEAGUE_TABLE WHERE Day_ID = (SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE)")
        for position in c.fetchone():
            order.append(position)
        helpper.disconnectDB()
        return order
    except:
        helpper.disconnectDB()
        return None
def make_players_list():
    c = helpper.connectDB()
    c.execute("SELECT PLAYERS_GUESSES.Player_ID, PLAYERS_GUESSES.Game_ID, PLAYERS.Mail FROM PLAYERS_GUESSES, PLAYERS WHERE PLAYERS_GUESSES.Player_ID = PLAYERS.Player_ID AND Mail IS NOT NULL")
    data = c.fetchall()
    c.close()
    return data

def make_admin_list():
    admin_data = []
    c = helpper.connectDB()
    c.execute("SELECT Admin_ID, Mail FROM ADMINS WHERE Mail IS NOT NULL")
    data = c.fetchall()
    helpper.disconnectDB()
    for row in data:
        admin = Admin_Contacts(row[0], row[1])
        c = helpper.connectDB()
        c.execute("SELECT GAMES.Game_Name FROM ADMINS_GAMES LEFT JOIN GAMES ON GAMES.Game_ID = ADMINS_GAMES.Game_ID WHERE Admin_ID = ?",(admin.admin_id,))
        gamesdata = c.fetchall()
        helpper.disconnectDB()
        for row in gamesdata:
            admin.add_game_name(row[0])
        admin_data.append(admin)
    return admin_data

def make_players_guesses_table_order(PlayerGame):
    c = helpper.connectDB()
    order = ["" for _ in range(len(team_list)+3)]
    counter = 0
    c.execute("SELECT "+teams_list+", top4_Correct_Point ,Six_Correct_Point, Points FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ? AND Day_ID = (SELECT MAX(Day_ID) FROM PLAYERS_POINTS)",(PlayerGame[0],PlayerGame[1]))
    points = c.fetchone()
    try:
        c.execute("SELECT "+teams_list+" FROM PLAYERS_GUESSES WHERE Player_ID = ? AND Game_ID = ?",(PlayerGame[0],PlayerGame[1]))
        for team in c.fetchone():
            order[team-1] = (team_list[counter],points[counter])
            counter += 1
        order[15] = ("Six_Correct_Point",points[15])
        order[16] = ("Points",points[16])
        helpper.disconnectDB()
        return order
    except:
        helpper.disconnectDB()
        return None
def get_player_guesses_list(PlayerId, GameId):
    c = helpper.connectDB()
    c.execute("SELECT "+teams_list+" FROM PLAYERS_GUESSES WHERE Player_ID = ? AND Game_ID = ?",(PlayerId, GameId))
    data = c.fetchone()
    helpper.disconnectDB()
    return data
def get_player_guesses_points(PlayerId, GameId):
    c = helpper.connectDB()
    c.execute("SELECT Points, Six_Correct_Point, top4_Correct_Point, "+teams_list+" FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ? AND Day_ID = (SELECT MAX(Day_ID) FROM PLAYERS_POINTS)",(PlayerId, GameId))
    data = c.fetchone()
    helpper.disconnectDB()
    return data
def make_Player_statistics(player_id, game_id):
    c = helpper.connectDB()
    c.execute("SELECT Day_ID, Points, Six_Correct_Point, top4_Correct_Point, "+teams_list+" FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ? ORDER BY Day_ID DESC",(player_id, game_id))
    data = c.fetchall()
    helpper.disconnectDB()
    return(data)
def players_game_table_data(game_name):
    players_list = []
    c = helpper.connectDB()
    c.execute("SELECT First_Name, Last_Name, Place, Shared_Place, Points, Player_ID FROM "+game_name+" WHERE Day_ID = (SELECT MAX(Day_ID) FROM "+game_name+") ORDER BY Points DESC")
    data = c.fetchall()
    helpper.disconnectDB()
    for row in data:
        player = Player_Game_Status(row[0], row[1], row[2], bool(row[3]), row[4])
        c = helpper.connectDB()
        c.execute("SELECT Place, Points FROM "+game_name+" WHERE Player_ID = ? AND Day_ID IS NOT (SELECT MAX(Day_ID) FROM "+game_name+") ORDER BY Day_ID DESC LIMIT 1", (row[5],))
        history = c.fetchone()
        helpper.disconnectDB()
        if history != None:
            player.set_position_change(int(history[0]))
            player.set_points_change(int(history[1]))
        players_list.append(player)
    return sorted(players_list, key=lambda player:player.position)

def points_change(points_change):
    if points_change == 0:
        return ' '
    if points_change > 0:
        return '+'+str(points_change) 
    return str(points_change)

def place_change(place_change):
    if place_change > 0:
        return '&nbsp;&#8896; '+str(place_change)#arrow up
    elif place_change < 0:
        return '&nbsp;&#8897; '+str(place_change)#arrow down
    else:
        return '&nbsp;&#9472;&nbsp;'

def get_player_Shared_Place_and_Place_and_Day_ID(name,player_id):
    c = helpper.connectDB()
    c.execute("SELECT Shared_Place, Place, Day_ID FROM "+str(name)+" WHERE Day_ID = (SELECT MAX(Day_ID) FROM "+str(name)+" ) AND Player_ID = "+str(player_id))
    data = c.fetchone()
    helpper.disconnectDB()
    return(data)

def get_game_name(game_id):
    c = helpper.disconnectDB()
    c.execute("SELECT Game_Name FROM GAMES WHERE Game_ID = ?",(game_id,))
    return c.fetchone()[0]

def get_player_name(player_id):
    c = helpper.connectDB()
    c.execute("SELECT First_Name, Last_Name FROM PLAYERS WHERE Player_ID = ?",(player_id,))
    data = c.fetchall()
    helpper.disconnectDB()
    return(data)

def do_players_subscription_messages():
    league_table = make_liiga_league_table_order()
    c = helpper.connectDB()
    c.execute("SELECT PLAYERS.Player_ID, PLAYERS_GUESSES.Game_ID, PLAYERS.Mail, PLAYERS.First_Name, PLAYERS.Last_Name, GAMES.Game_Name FROM PLAYERS_GUESSES LEFT JOIN PLAYERS ON PLAYERS.Player_ID = PLAYERS_GUESSES.Player_ID LEFT JOIN GAMES ON GAMES.Game_ID = PLAYERS_GUESSES.Game_ID WHERE PLAYERS.Mail IS NOT NULL")
    data = c.fetchall()
    helpper.disconnectDB()
    for playerData in data:
        player = build_player_data(league_table, playerData)
        message = build_player_message(player)
        subject = "LIIGAVEIKKAUS PELI "+player.game_name+" "+player.date
        send_mail(player.player_email,subject,message)

def build_player_data(league_table, playerData):
    player = Player_Data(playerData[0],playerData[1],playerData[2],playerData[3],playerData[4],playerData[5])
    player.set_date(league_table[0])
    pointsData = get_player_guesses_points(player.player_id, player.game_id)
    playerGuessData = get_player_guesses_list(player.player_id, player.game_id)
    playerPositionAnd = get_player_Shared_Place_and_Place_and_Day_ID(player.game_name, player.player_id)
    player.set_shared_place(bool(playerPositionAnd[0]))
    player.set_position(playerPositionAnd[1])
    player.set_total_points(pointsData[0])
    player.set_six_correct(pointsData[1])
    player.set_top4_correct(pointsData[2])
    player.set_teams_data(playerGuessData,league_table[1:],team_list,pointsData[3:])
    return player

def build_player_message(player: Player_Data):
    player_heder = player_header(player)
    palyer_teams = player.teams
    league_list = sorted(palyer_teams, key=lambda team:team.position)
    guess_list = sorted(palyer_teams, key=lambda team:team.guess)
    points_table = player_points_table(team_list, league_list, guess_list, player)
    history_table = player_history_table(player)
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
<font face="Arial">
'''+player_heder+'''
<p></p>
'''+points_table+'''
<p></p>
'''+history_table+'''
</font>
</body>
</html>
'''
    return message

def player_header(player: Player_Data):
    heder = '<p>Hei <b>'+player.player_first_name+'</b></p>'
    share_text = '\n</b> pelissa jaetulla sijalla <b>' if player.player_shared_place else '</b> pelissa sijalla <b>'
    heder += '\n<p>Olet <b>'+player.game_name+share_text+str(player.player_position)+'</b></p>'
    return heder

def player_points_table(teams_list, league_list, guess_list, player: Player_Data):
    points_table = '<h3>RUNKOSARJA JA VEIKKAUKSESI: '+str(player.date)+'</h3>'
    points_table += '\n<table style="width:25%">'
    points_table += '\n<tr align="left">'
    points_table += '\n<th>SIJOITUS</th>'
    points_table += '\n<th>RUNKOSARJA</th>'
    points_table += '\n<th>VEIKKAUKSESI</th>'
    points_table += '\n<th>PISTEET</th>'
    points_table += '\n</tr>'
    for index in range(len(teams_list)):
        guess: Team = guess_list[index]
        position: Team = league_list[index]
        points_table += '\n<tr>'
        points_table += '\n<td>'+str(index+1)+'.</td>'
        points_table += '\n<td>'+position.name+'</td>'
        points_table += '\n<td>'+guess.name+'</td>'
        points_table += '\n<td>'+str(guess.points)+'</td>'
        points_table += '\n</tr>'
    points_table += '\n</table>'
    points_table += '\n<p>TOP 4 OIKEIN PISTE: '+str(player.top4_correct)+'</p>'
    points_table += '\n<p>KUUSI OIKEIN PISTE: '+str(player.six_correct)+'</p>'
    points_table += '\n<p>KOKONAISPISTEET: <b>'+str(player.total_points)+'</b></p>'
    return points_table

def player_history_table(player: Player_Data):
    history_table = '\n<h3>HISTORIASI</h3>'
    history_table += '\n<table style="width:80%">'
    history_table += '\n<tr align="left">'
    history_table += '\n<th>PAIVAMAARA</th>'
    for index in range(len(team_list)):
        history_table += '\n<th>'+team_list[index]+'</th>'
    history_table += '\n<th>KUUSI_OIKEIN</th>'
    history_table += '\n<th>TOP4_OIKEIN</th>'
    history_table += '\n<th>KOKONAISPISTEET</th>'
    history_table += '\n</tr>'
    for data in make_Player_statistics(player.player_id, player.game_id):
        player_history = Player_history_round(data)
        history_table += '\n<tr>'
        history_table += '\n<td>'+player_history.date+'</td>'
        for team in player_history.teams:
           history_table += '\n<td>'+str(team.points)+'</td>'
        history_table += '\n<td>'+str(player_history.six_correct)+'</td>'
        history_table += '\n<td>'+str(player_history.top4_correct)+'</td>'
        history_table += '\n<td>'+str(player_history.total_points)+'</td>'
        history_table += '\n</tr>'
    history_table += '\n</table>'
    return history_table

def make_admin_messages():
    c = helpper.connectDB()
    c.execute("SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE")
    day = c.fetchone()[0]
    helpper.disconnectDB()
    admins = make_admin_list()
    for item in admins:
        admin: Admin_Contacts = item
        for game_name in admin.game_names:
            h1 = '<h3>'+game_name+' RUNKOSARJA '+str(day)+'</h3>'
            playerTabeleData = ''
            players_data = players_game_table_data(game_name)
            for row in players_data:
                player: Player_Game_Status = row
                playerTabeleData +='\n<tr>\n<td>'+str(player.position)+'.</td>\n<td>'+player.first_name+' '+player.last_name+'</td>\n<td>'+str(player.points)+'</td>\n<td>'+points_change(player.points_change)+'</td>\n<td>'+place_change(player.position_change)+'</td>\n</tr>'
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
</tr>'''+playerTabeleData+'''
</table>
<p> </p>
</font>
</body>
</html>
'''
            subject = game_name+" RUNKOSARJA "+day
            send_mail(admin.email,subject,message)
def send_mail_players_and_admin():
    Consol.Message('PLAYERS MAILS SENDIN')
    try:
        do_players_subscription_messages()
        Consol.Message('COMPLITED')
    except:
        Consol.ErroMessage('ERROR: PLAYERS MAILS SENDIN FAILL')
    Consol.Message('ADMIN MAILS SENDIN')
    try:
        make_admin_messages()
        Consol.Message('COMPLITED')
    except:
        Consol.ErroMessage('ERROR: ADMINS MAILS SENDIN FAILL')