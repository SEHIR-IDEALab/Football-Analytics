__author__ = 'emrullah'


class GameInstance:

    def __init__(self, time, players, event=None):
        self.time = time
        self.players = players
        self.event = event

        self.game_stop_status = False


    def setPlayers(self, players):
        self.players = players


    def setEvent(self, event):
        self.event = event


    def setGameStopStatus(self, status):
        self.game_stop_status = status


    def isGameStop(self):
        return self.game_stop_status


    def __str__(self):
        return "%s" %(self.event)