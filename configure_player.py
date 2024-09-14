import datetime
import sqlite3
import Consol
import helpper
from player_data import Player_Points
from configure import TEAMS_LIST_STRING as team_list

def create_games_tables():
    c = helpper.connectDB()
    c.execute("SELECT Game_Name FROM GAMES")
    gamesList = c.fetchall()
    helpper.disconnectDB()
    for game in gamesList:
        c = helpper.connectDB()
        c.execute("CREATE TABLE IF NOT EXISTS "+game[0]+" (Day_ID DATE, Place INT, Shared_Place INT, Player_ID REFERENCES PLAYERS(Player_ID) ON UPDATE CASCADE ON DELETE CASCADE, First_Name, Last_Name, Points INT, CONSTRAINT DayPlayer_PK PRIMARY KEY(Day_ID, Player_ID))")
        helpper.disconnectDB()

def update_game_data(day, name, data,c,conn): #data = [Place, Player_ID, First_Name, Last_Name, Points] name = game_name
    c.execute("UPDATE "+str(name)+" SET Day_ID = ?, Player_ID = ?, First_Name = ?, Last_Name = ?, Points = ?, Place = ?, Shared_Place = ? WHERE Day_ID = ? AND Player_ID = ?", (day,data[1],data[2],data[3],data[4],data[5],data[6],day,data[1]))
    conn.commit()

def make_game_data(day, name, data,c,conn): #data = [Place, Player_ID, First_Name, Last_Name, Points] name = game_name day = Day_ID
    c.execute("INSERT INTO "+name+" (Day_ID, Player_ID, First_Name, Last_Name, Points, Place, Shared_Place) VALUES (?,?,?,?,?,?,?)",(day,data[1],data[2],data[3],data[4],data[5],data[6]))
    conn.commit()

def make_players_points(): #piste systemi eroteltava omiin metodeihin
    day = datetime.date.today()
    c = helpper.connectDB()
    c.execute("SELECT "+team_list+" FROM LIIGA_LEAGUE_TABLE WHERE Day_ID = (SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE)")
    helpper.disconnectDB()
    league_table = c.fetchone()
    c = helpper.connectDB()
    c.execute("SELECT Player_ID, Game_ID, "+team_list+" FROM PLAYERS_GUESSES")
    players_guesses = c.fetchall()
    helpper.disconnectDB()
    for player in players_guesses:
        player_points = Player_Points(player[0], player[1])
        player_points.cout_points(player[2:], league_table)
        try:
            c = helpper.connectDB()
            c.execute("SELECT MAX(Day_ID) FROM PLAYERS_POINTS WHERE Player_ID = ? AND Game_ID = ?",(player_points.get_player(), player_points.get_game()))
            maxDay = c.fetchone()
            helpper.disconnectDB()
            if maxDay is not None and "('"+str(day)+"',)" == str(maxDay):
                c = helpper.connectDB()
                c.execute("UPDATE PLAYERS_POINTS SET HPK = ?, HIFK= ?, ILVES = ?, JUKURIT = ?, JYP = ?, KALPA = ?, KESPOO = ?, KOOKOO = ?, KARPAT = ?, LUKKO = ?, PELICANS = ?, SAIPA = ?, SPORT = ?, TAPPARA = ?, TPS = ?, ASSAT = ?, Six_Correct_Point = ?, top4_Correct_Point = ? , Points = ? WHERE Day_ID = ? AND Player_ID = ? AND Game_ID = ?", (player_points[0] , player_points[1] , player_points[2] , player_points[3] , player_points[4] , player_points[5] , player_points[6] , player_points[7] , player_points[8] , player_points[9] , player_points[10] , player_points[11] , player_points[12] , player_points[13] , player_points[14] , player_points[15], player_points[16], player_points[17] , day, player[15], player[16], player_points[18]))
                helpper.connect().commit()
                helpper.disconnectDB()
                Consol.Message("UPDATE POINTS DONE PALYER "+str(player_points.get_player())+" GAME "+str(player_points.get_game()))
            else:
                c = helpper.connectDB()
                c.execute("INSERT INTO PLAYERS_POINTS(Day_ID, Player_ID, Game_ID, "+team_list+", top4_Correct_Point ,Six_Correct_Point, Points) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (day, player_points.get_player(), player_points.get_game(), player_points.get_team_points(0), player_points.get_team_points(1), player_points.get_team_points(2), player_points.get_team_points(3), player_points.get_team_points(4), player_points.get_team_points(5), player_points.get_team_points(6), player_points.get_team_points(7), player_points.get_team_points(8), player_points.get_team_points(9), player_points.get_team_points(10), player_points.get_team_points(11), player_points.get_team_points(12), player_points.get_team_points(13), player_points.get_team_points(14), player_points.get_team_points(15), player_points.get_top4_poits(), player_points.get_sex_correct_poits(), player_points.get_total_points()))
                helpper.connect().commit()
                helpper.disconnectDB()
                Consol.Message("NEW POINTS DATA DONE PALYER "+str(player_points.get_player())+" GAME "+str(player_points.get_game()))
        except:
            Consol.Message("FAILL POINTS UPDATE PALYER "+str(player_points.get_player())+" GAME "+str(player_points.get_game()))

def make_game_tabel_data():
    day = datetime.date.today()
    c = helpper.connectDB()
    c.execute("SELECT Game_ID, Game_Name FROM GAMES")
    data = c.fetchall()
    helpper.disconnectDB()
    for game in data:
        c = helpper.connectDB()
        c.execute("SELECT PLAYERS_POINTS.Day_ID, PLAYERS_POINTS.Player_ID, PLAYERS.First_Name, PLAYERS.Last_Name, PLAYERS_POINTS.Points FROM PLAYERS_POINTS, PLAYERS WHERE PLAYERS_POINTS.Day_ID = (SELECT MAX(Day_ID) FROM PLAYERS_POINTS WHERE Game_ID = "+str(game[0])+") AND PLAYERS_POINTS.Game_ID = "+str(game[0])+" AND PLAYERS_POINTS.Player_ID IS PLAYERS.Player_ID ORDER BY PLAYERS_POINTS.Points DESC")
        playersData = c.fetchall()
        helpper.disconnectDB()
        place = 1
        placeMember = 1
        try:
            if len(playersData)>=2:
                pointMember = playersData[1][4]
                c.execute("SELECT MAX(Day_ID) FROM "+str(game[1]))
                maxDay = str(c.fetchone()) == "('"+str(day)+"',)"
                counter = 0
                for player in playersData:
                    if player[4] == pointMember:
                        player += (placeMember,)
                        player += (1,)
                        place += 1
                    if player[4] != pointMember:
                        placeMember = place
                        player += (placeMember,)
                        try:
                            if int(player[4]) == int(playersData[counter+1][4]):
                                player += (1,)

                            else:
                                player += (0,)
                        except:
                            player += (0,)
                        place += 1
                        pointMember = player[4]
                    if maxDay == True:
                        update_game_data(day,game[1],player,c,conn)
                        Consol.Message("GAME "+str(game[1])+" UPDATE PLAYER "+str(player[1])+" DATA")
                    if maxDay == False:
                        make_game_data(day,game[1],player,c,conn)
                        Consol.Message("GAME "+str(game[1])+" ADD PLAYER "+str(player[1])+" DATA")
                    counter += 1
                Consol.Message("GAME "+game[1]+" TABEL IS UPDATED")
            else:
                playersData[0] += (1,)
                playersData[0] += (0,)
                c.execute("SELECT MAX(Day_ID) FROM "+str(game[1]))
                maxDay = str(c.fetchone()) == "('"+str(day)+"',)"
                if maxDay:
                    update_game_data(day,game[1],player,c,conn)
                else:
                    make_game_data(day,game[1],player,c,conn)
                Consol.Message("GAME "+str(game[1])+" TABEL IS UPDATED")
        except:
            Consol.Message("GAME "+str(game[1])+" TABEL UPDATED FAILL")
            pass
def make_updates():
    make_players_points()
    make_game_tabel_data()

helpper.make_player_and_team_tabels
create_games_tables()