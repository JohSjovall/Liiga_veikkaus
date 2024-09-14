class Team:
    position = 0
    def __init__(self, position: int, guess: int):
        self.position = position
        self.guess = guess
        self.points = 0

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


class Points:

    def __init__(self, player_value, game_value):
        self.teams = []
        self.six_correct = 0
        self.top4_correct = 0
        self.player = -1
        self.game = -1
        self.total_points = 0
        self.player = player_value
        self.game = game_value

    def get_position_poits(self, team: Team):
        return 4 - abs(team.get_guess - team.get_position)

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

    def set_extra_poitns(self, team: Team):
        if team.get_guess() < 5 and team.isCorrect(): # top4
            self.top4_correct += 1
        if team.isCorrect():
            self.six_correct += 1
    
    def cout_points(self, guess_lis: list, position_list: list):
        for index in range(len(guess_lis)):
            self.set_points_at_team(position_list[index] ,guess_lis[index])

    def set_points_at_team(self, position, guess):
        team = Team(position, guess)
        team.add_points(self.get_position_poits(team))
        team.add_points(self.get_location_poits(team))
        self.set_extra_poitns(team)
        self.total_points += team.get_points()
        self.teams.append(team)


    def get_player(self):
        return self.player

    def get_game(self):
        return self.game

    def get_team_points(self, index):
        global teams
        team: Team = teams[index]
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