import datetime
import urllib.request
import sqlite3
from html.parser import HTMLParser
import Consol
import configure
import json
import functools
import helpper

#league_table
def create_league_table():
    helpper.make_liiga_table()
#Liigakierros
def make_liigakerros_data(day,c,conn):
    global league_table
    data = "Day_ID"
    for x in range(len(league_table)):
        data = data+", "+league_table[x][0]
    c.execute("INSERT INTO LIIGA_LEAGUE_TABLE ("+data+") VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(day ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15, 16))
    conn.commit()
def update_liigakierros_data(day,c,conn):
    global league_table
    data = ""
    for x in range(len(league_table)):
        data = data+str(league_table[x][0])+" = ?"
        if x != 14:
            data=data+" ,"
        else:
            pass
    c.execute("UPDATE LIIGA_LEAGUE_TABLE SET "+data+" WHERE Day_ID = ?",(1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15, 16 ,day))
    conn.commit()
#Liiga joukkue
def create_Liiga_teams_tables():
    helpper.make_teams_tables()
def make_liiga_team_data(day, data):
    c = helpper.connectDB()
    c.execute("INSERT INTO "+data[0]+"(Day_ID , Games_Played, Wins, Draw, Losses, Overtime_Wins, Goals_For, Goals_Against, Points) VALUES ( ?,?,?,?,?,?,?,?,?)", (day, data[1] , data[2] , data[3] , data[4] , data[5] , data[6] , data[7], data[8]))
    helpper.connect().commit()
    helpper.disconnectDB()
#Update teams and league table
def download_update_liiga(update):
    global league_table
    try:
        response = urllib.request.urlopen(configure.URL)
        data = response.read().decode("utf-8")
        json_data = json.loads(data)
        league_table = update_liiga_data(json_data)
    except EnvironmentError:
        Consol.Message("ERROR! NO CONNECT!")
        return(False)
    except ValueError:
        Consol.Message("ERROR! JSON DATA NOT WORKING!")
        return(False)
    for x in range(len(league_table)):
        c = helpper.connectDB()
        c.execute("SELECT MAX(Games_Played) FROM "+str(league_table[x][0]))
        games_data = c.fetchone()
        helpper.disconnectDB()
        if games_data is None or games_data[0] == league_table[x][1]:
            pass
        else:
            Consol.Message("NEW UPDATE")
            team_data_updaet()
            league_table.clear()
            return(True)
    Consol.Message("NO UPDATE")
    league_table.clear()

    return(update)

def team_data_updaet(c,conn):
    global league_table
    TIME = datetime.date.today()
    for x in range(len(league_table)):
        try:
            make_liiga_team_data(TIME, league_table[x],c,conn)
            Consol.Message("NEW DATA "+league_table[x][0]+" DONE")
        except:
            pass
    c.execute("SELECT MAX(Day_ID) FROM LIIGA_LEAGUE_TABLE")
    MaxDay = c.fetchone()[0]
    try:
        if MaxDay is not None and str(MaxDay) == str(TIME):
            update_liigakierros_data(TIME,c,conn)
            Consol.Message("UPDATE LIIGA LEAGUE TABLE DONE")
        else:
            make_liigakerros_data(TIME,c,conn)
            Consol.Message("NEW DATA LIIGA LEAGUE TABLE DONE")
    except Exception as e:
        Consol.Message("ERROR UPDATE LIIGA LEAGUE TABLE: "+str(e))

def update_liiga_data(data):
    global league_table
    teams = configure.TEAMS
    temp_league_table = [[]] * 15
    season = data['season']
    for i in range(0,16):
        team = season[i]
        temp_league_table[i] = [teams[str(team['teamId'])]] #Team name
        temp_league_table[i].append(int(team['games'])) #Games_Played
        temp_league_table[i].append(int(team['wins'])) #Wins
        temp_league_table[i].append(int(int(team['overtimeWins'])+int(team['overtimeLosses']))) #Draws
        temp_league_table[i].append(int(team['losses'])) #Losses
        temp_league_table[i].append(int(team['overtimeWins'])) #Overtime_Wins
        temp_league_table[i].append(int(team['goals'])) #Goals_for
        temp_league_table[i].append(int(team['goalsAgainst'])) #Goals_Against
        temp_league_table[i].append(int(team['points'])) #Points
    temp_league_table_sort = sorted(temp_league_table, key=functools.cmp_to_key(shortGameTable))
    league_table = temp_league_table_sort
    return league_table

def shortGameTablePoints(table):
    return table['0']


def shortGameTable(teamA, teamB):
    if(teamA[8] != teamB[8]): #points
        return comparing(teamA[8], teamB[8])
    if(teamA[2] != teamB[2]): #wins
        return comparing(teamA[2], teamB[2])
    gdA = teamA[6]-teamA[7]
    gdB = teamB[6]-teamB[7]
    if(gdA != gdB): #goalsDifference
        return goalsDifference(gdA, gdB)
    if(teamA[6] != teamB[6]): #goals
        return comparing(teamA[6], teamB[6])
    return 0

    
def comparing(a,b):
    if(a > b):
        return -1
    else:
        return 1

def goalsDifference(a,b):
    if(a > b):
        return -1
    else:
        return 1

league_table = []
create_league_table()
create_Liiga_teams_tables()