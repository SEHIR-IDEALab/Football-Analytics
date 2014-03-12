__author__ = 'doktoray'

class Team(object):
    def __init__(self, teamName, teamPlayers):
        self.teamName = teamName
        self.teamPlayers = teamPlayers

    def getTeamName(self):
        return self.teamName

    def getTeamPlayers(self):
        return self.teamPlayers

    def __str__(self):
        a = ""
        for player in self.teamPlayers:
            a += "%s\n" %(str(player))
        return a
