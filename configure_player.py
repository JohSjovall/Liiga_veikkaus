import datetime
import sqlite3
import Consol

conn = sqlite3.connect('Database_liiga_game.db')
c = conn.cursor()
team_list = "HPK, HIFK, ILVES, JUKURIT, JYP, KALPA, KOOKOO, KARPAT, LUKKO, PELICANS, SAIPA, SPORT, TAPPARA, TPS, ASSAT"

def create_tables():
    c.execute("CREATE TABLE IF NOT EXISTS PLAYERS(Player_ID INTEGER PRIMARY KEY, First_Name TEXT NOT NULL, Last_Name TEXT NOT NULL, Mail TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS GAMES(Game_ID INTEGER PRIMARY KEY, Game_Name TEXT NOT NULL UNIQUE)")
    c.execute("CREATE TABLE IF NOT EXISTS PLAYERS_GUESSES(Player_ID REFERENCES PLAYERS(Player_ID) ON UPDATE CASCADE ON DELETE CASCADE, Game_ID REFERENCES GAMES(Game_ID) ON UPDATE CASCADE ON DELETE CASCADE, HPK INT NOT NULL, HIFK INT NOT NULL, ILVES INT NOT NULL, JUKURIT INT NOT NULL, JYP INT NOT NULL, KALPA INT NOT NULL, KOOKOO INT NOT NULL, KARPAT INT NOT NULL, LUKKO INT NOT NULL, PELICANS INT NOT NULL, SAIPA INT NOT NULL, SPORT INT NOT NULL, TAPPARA INT NOT NULL, TPS INT NOT NULL, ASSAT INT NOT NULL, CONSTRAINT PlayerGame_PK PRIMARY KEY(Player_ID, Game_ID))")
    c.execute("CREATE TABLE IF NOT EXISTS PLAYERS_POINTS(Day_ID DATE NOT NULL, Player_ID REFERENCES PLAYERS(Player_ID) ON UPDATE CASCADE ON DELETE CASCADE , Game_ID REFERENCES GAMES(Game_ID) ON UPDATE CASCADE ON DELETE CASCADE, HPK INT NOT NULL, HIFK INT NOT NULL, ILVES INT NOT NULL, JUKURIT INT NOT NULL, JYP INT NOT NULL, KALPA INT NOT NULL, KOOKOO INT NOT NULL, KARPAT INT NOT NULL, LUKKO INT NOT NULL, PELICANS INT NOT NULL, SAIPA INT NOT NULL, SPORT INT NOT NULL, TAPPARA INT NOT NULL, TPS INT NOT NULL, ASSAT INT NOT NULL, Six_Correct_Point INT, Points INT, CONSTRAINT DayPlayerGame_PK PRIMARY KEY(Day_ID, Player_ID, Game_ID))")

def create_games_tables():
    c.execute("SELECT Game_Name FROM GAMES")
    gamesList = c.fetchall()
    for game in gamesList:
        c.execute("CREATE TABLE IF NOT EXISTS "+game[0]+" (Day_ID DATE, Place INT, Shared_Place INT, Player_ID REFERENCES PLAYERS(Player_ID) ON UPDATE CASCADE ON DELETE CASCADE, First_Name, Last_Name, Points INT, CONSTRAINT DayPlayer_PK PRIMARY KEY(Day_ID, Player_ID))")

def update_game_data(day, name, data): #data = [Place, Player_ID, First_Name, Last_Name, Points] name = game_name
    c.execute("UPDATE "+name+" SET Day_ID = ?, Player_ID = ?, First_Name = ?, Last_Name = ?, Points = ?, Place = ?, Shared_Place = ? WHERE Day_ID = "+str(day)+" AND Player_ID = "+str(data[1])+"",(day,data[1],data[2],data[3],data[4],data[5],data[6]))
    conn.commit()

def make_game_data(day, name, data): #data = [Place, Player_ID, First_Name, Last_Name, Points] name = game_name day = Day_ID
    c.execute("INSERT INTO "+name+" (Day_ID, Player_ID, First_Name, Last_Name, Points, Place, Shared_Place) VALUES (?,?,?,?,?,?,?)",(day,data[1],data[2],data[3],data[4],data[5],data[6]))
    conn.commit()

def make_players_points():
    day = datetime.date.today()
    c.execute("SELECT "+team_list+" FROM LIIGA_LEAGUE_TABLE WHERE Day_ID = (SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE)")
    league_table = c.fetchone()
    c.execute("SELECT "+team_list+", Player_ID, Game_ID FROM PLAYERS_GUESSES")
    players_guesses = c.fetchall()
    for player in players_guesses:
        player_points = []
        points = 0
        total_points = 0
        correct_counter = 0
        for x in range(15):
            if player[x] == league_table[x]:
                total_points += 3
                points += 3
                correct_counter += 1
            if player[x] > league_table[x]:
                total_points += 3-player[x]+league_table[x]
                points += 3-player[x]+league_table[x]
            if player[x] < league_table[x]:
                total_points += 3-league_table[x]+player[x]
                points += 3-league_table[x]+player[x]
            if player[x] <= 6 and league_table[x] <= 6:
                total_points += 1
                points += 1
            if player[x] <= 10 and league_table[x] <= 10:
                total_points += 1
                points += 1
            player_points.append(points)
            points = 0
        if correct_counter >= 6:
            player_points.append(1)
            total_points += 1
        else:
            player_points.append(0)
        player_points.append(total_points)
        try:
            c.execute("SELECT MAX(Day_ID) FROM PLAYERS_POINTS WHERE Player_ID = "+str(player[15])+" AND Game_ID = "+str(player[16]))
            maxDay = c.fetchone()
            if maxDay is not None and "('"+str(day)+"',)" == str(maxDay):
                c.execute("UPDATE PLAYERS_POINTS SET HPK = ?, HIFK= ?, ILVES = ?, JUKURIT = ?, JYP = ?, KALPA = ?, KOOKOO = ?, KARPAT = ?, LUKKO = ?, PELICANS = ?, SAIPA = ?, SPORT = ?, TAPPARA = ?, TPS = ?, ASSAT = ?, Six_Correct_Point = ?, Points = ? WHERE Day_ID = ? AND Player_ID = ? AND Game_ID = ?", (player_points[0] , player_points[1] , player_points[2] , player_points[3] , player_points[4] , player_points[5] , player_points[6] , player_points[7] , player_points[8] , player_points[9] , player_points[10] , player_points[11] , player_points[12] , player_points[13] , player_points[14] , player_points[15], player_points[16], day, player[15], player[16]))
                conn.commit()
                Consol.Message("UPDATE POINTS DONE PALYER "+str(player[15])+" GAME "+str(player[16]))
            else:
                c.execute("INSERT INTO PLAYERS_POINTS(Day_ID, Player_ID, Game_ID, "+team_list+", Six_Correct_Point, Points) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (day, player[15], player[16], player_points[0] , player_points[1] , player_points[2] , player_points[3] , player_points[4] , player_points[5] , player_points[6] , player_points[7] , player_points[8] , player_points[9] , player_points[10] , player_points[11] , player_points[12] , player_points[13] , player_points[14] , player_points[15], player_points[16]))
                conn.commit()
                Consol.Message("NEW POINTS DATA DONE PALYER "+str(player[15])+" GAME "+str(player[16]))
        except:
            Consol.Message("FAILL POINTS UPDATE PALYER "+str(player[15])+" GAME "+str(player[16]))

def make_game_tabel_data():
    day = datetime.date.today()
    c.execute("SELECT Game_ID, Game_Name FROM GAMES")
    for game in c.fetchall():
        c.execute("SELECT PLAYERS_POINTS.Day_ID, PLAYERS_POINTS.Player_ID, PLAYERS.First_Name, PLAYERS.Last_Name, PLAYERS_POINTS.Points FROM PLAYERS_POINTS, PLAYERS WHERE PLAYERS_POINTS.Day_ID = (SELECT MAX(Day_ID) FROM PLAYERS_POINTS WHERE Game_ID = "+str(game[0])+") AND PLAYERS_POINTS.Game_ID = "+str(game[0])+" AND PLAYERS_POINTS.Player_ID IS PLAYERS.Player_ID ORDER BY PLAYERS_POINTS.Points DESC")
        playersData = c.fetchall()
        place = 1
        placeMember = 1
        try:
            if len(playersData)>=2:
                pointMember = playersData[1][4]
                c.execute("SELECT MAX(Day_ID) FROM "+str(game[1]))
                maxDay = str(c.fetchone()) == "('"+str(day)+"',)"
                for player in playersData:
                    if player[4] == pointMember:
                        player += (placeMember,)
                        player += (1,)
                        place += 1
                    if player[4] != pointMember:
                        placeMember = place
                        player += (placeMember,)
                        player += (0,)
                        place += 1
                        pointMember = player[4]
                    if maxDay == True:
                        update_game_data(day,game[1],player)
                        Consol.Message("GAME "+str(game[1])+" UPDATE PLAYER "+str(player[1])+" DATA")
                    if maxDay == False:
                        make_game_data(day,game[1],player)
                        Consol.Message("GAME "+str(game[1])+" ADD PLAYER "+str(player[1])+" DATA")
                Consol.Message("GAME "+game[1]+" TABEL IS UPDATED")
            else:
                playersData[0] += (1,)
                playersData[0] += (0,)
                c.execute("SELECT MAX(Day_ID) FROM "+str(game[1]))
                maxDay = str(c.fetchone()) == "('"+str(day)+"',)"
                if maxDay:
                    update_game_data(day,game[1],player)
                else:
                    make_game_data(day,game[1],player)
                Consol.Message("GAME "+str(game[1])+" TABEL IS UPDATED")
        except:
            Consol.Message("GAME "+str(game[1])+" TABEL UPDATED FAILL")
            pass
def make_updates():
    make_players_points()
    make_game_tabel_data()
create_tables()
create_games_tables()