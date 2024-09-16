class Team:
    def __init__(self, position: int, guess: int):
        self.name: str = ""
        self.position: int = position
        self.guess: int = guess
        self.points: int = 0
    
    def set_team_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_position(self, position):
        self.position = position
    
    def set_guess(self, guess):
        self.guess = guess
    
    def isCorrect(self):
        return self.position == self.guess

    def add_points(self, points):
        self.points = self.points + points
    
    def get_points(self):
        return self.points
    
    def get_position(self):
        return self.position
    
    def get_guess(self):
        return self.guess
    
    def __repr__(self):
        return repr((self.name, self.guess, self.position, self.points))


class Player_Points:

    def __init__(self, player_value, game_value):
        self.teams = []
        self.six_correct: int = 0
        self.top4_correct: int = 0
        self.total_points: int = 0
        self.player: int = player_value
        self.game: int = game_value
    
    def cout_points(self, guess_lis: list, position_list: list):
        for index in range(len(guess_lis)):
            self.set_points_at_team(position_list[index], guess_lis[index])

    def set_points_at_team(self, position, guess):
        team = Team(position, guess)
        team.add_points(self.get_position_poits(team))
        team.add_points(self.get_location_poits(team))
        self.total_points += team.get_points()
        self.teams.append(team)
        if team.get_guess() < 5 and team.isCorrect(): # top4
            self.top4_correct += 1
        if team.isCorrect():
            self.six_correct += 1
    
    def get_position_poits(self, team: Team):
            return 4 - abs(team.get_guess() - team.get_position())

    def get_location_poits(self, team: Team):
        points = 0
        if team.get_guess() == 1 or team.get_guess() == 16: # 1 or 16
            if team.isCorrect():
                points += 1
        if team.get_guess() < 5: # 1-4
            if team.get_position() < 5:
                points += 1
            return 0
        elif team.get_guess() < 13:
            points = 0
            if team.get_position() < 13 and team.get_position() > 4: # 5-12
                points += 1
                if team.get_guess() < 9 and team.get_position() < 9: # 5-8
                    points += 1
        elif team.get_guess() > 14: # 15-16
            if team.get_position() > 14:
                points += 1
        return points


    def get_player(self):
        return self.player

    def get_game(self):
        return self.game

    def get_team_points(self, index):
        team: Team = self.teams[index]
        return team.get_points()

    def get_total_points(self):
        return self.total_points
    
    def get_top4_poits(self):
        if self.top4_correct == 4:
            return 1
        return 0
    def get_sex_correct_poits(self):
        if self.six_correct > 5:
            return 1
        return 0
    
class Player_Data:

    def __init__(self, player_id, game_id, email, first_name, last_name, game_name):
        self.teams = []
        self.six_correct: int = 0
        self.top4_correct: int = 0
        self.total_points: int = 0
        self.player_id: int = player_id
        self.player_email: str = email
        self.player_position: int = 0
        self.player_shared_place: bool = False
        self.player_first_name: str = first_name
        self.player_last_name: str = last_name
        self.game_id: int = game_id
        self.game_name: str = game_name
        self.date: str = ""
    
    def set_teams_data(self, guess_lis: list, position_list: list, name_list: list, points_list: list):
        for index in range(len(guess_lis)):
            self.set_team_data(position_list[index] ,guess_lis[index], name_list[index], points_list[index])

    def set_team_data(self, position ,guess, name, points):
        team = Team(position, guess)
        team.set_team_name(name)
        team.add_points(points)
        self.teams.append(team)
    
    def set_six_correct(self, points):
        self.six_correct = points
    
    def set_top4_correct(self, points):
        self.top4_correct = points
    
    def set_player_name(self, first_name, last_name):
        self.player_first_name = first_name
        self.player_last_name = last_name
    
    def set_game_name(self, game_name):
        self.game_name = game_name
    
    def set_position(self, position):
        self.player_position = position

    def set_shared_place(self, shared_place: bool):
        self.player_shared_place = shared_place
    
    def set_date(self, date):
        self.date = date
    
    def set_total_points(self, points):
        self.total_points = points
    
    def __repr__(self):
        return repr((self.player_id, 
                     self.game_id, 
                     self.player_email,
                     self.player_first_name,
                     self.player_last_name,
                     self.player_position,
                     self.player_shared_place,
                     self.teams,
                     self.top4_correct,
                     self.six_correct,
                     self.total_points,
                     self.date))

class Player_history_round:
    def __init__(self, data: list):
        self.teams = []
        self.six_correct: int = data[2]
        self.top4_correct: int = data[3]
        self.total_points: int = data[1]
        self.date: str = data[0]
        for points in range(4,len(data)):
            self.teams.append(History_Team(data[points]))
class History_Team:
    def __init__(self, points):
        self.points = points

class Admin_Contacts:
    def __init__(self, admin_id: int, email: str,):
        self.admin_id: int = admin_id
        self.email: str = email
        self.game_names: list = []
    
    def add_game_name(self, game_name: str):
        self.game_names.append(game_name)

class Player_Game_Status:
    def __init__(self, first_name: str, last_name: str, position: int, shared_place: bool, points: int):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.points: int = points
        self.position: int = position
        self.shared_place: bool = shared_place
        self.position_change: int = 0
        self.points_change: int = 0
    
    def set_position_change(self, old_position: int):
        self.position_change =  old_position - self.position
    
    def set_points_change(self, old_points: int):
        self.points_change =  self.points - old_points