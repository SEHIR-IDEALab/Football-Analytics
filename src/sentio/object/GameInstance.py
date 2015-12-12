from src.sentio.file_io.reader.ReaderBase import ReaderBase

__author__ = 'emrullah'


class GameInstance:

    def __init__(self, time, players, event=None):
        self.time = time
        self.players = players
        self.event = event


    def getPlayer(self, player_id):
        for player in self.players:
            if player.object_id == player_id:
                return player
        return None


    def isHomeGoalKeeperLocationLeft(self):
        teams = ReaderBase.divideIntoTeams(self.players)
        return teams.home_team.getGoalKeeper().getX() < teams.away_team.getGoalKeeper().getX()


    def setPlayers(self, players):
        self.players = players


    def setEvent(self, event):
        self.event = event


    def __str__(self):
        return "%s\n%s\n%s" %(self.time, self.players, self.event)