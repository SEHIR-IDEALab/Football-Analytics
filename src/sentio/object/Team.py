__author__ = 'emrullah'


class Team(object):

    def __init__(self, team_name, team_players):
        self.team_name = team_name
        self.team_players = team_players


    def getTeamName(self):
        return self.team_name


    def getTeamPlayersWithJS(self):
        return self.team_players


    def getJerseyNumbersOfPlayers(self):
        return self.team_players.keys()


    def getTeamPlayers(self):
        return self.team_players.values()


    def getGoalKeeper(self):
        goal_keeper = None
        for player in self.getTeamPlayers():
            if player.isGoalKeeper():
                goal_keeper = player
        return goal_keeper


    def __str__(self):
        a = ""
        for player in self.getTeamPlayers():
            a += "%s\n" %(player)
        return a
