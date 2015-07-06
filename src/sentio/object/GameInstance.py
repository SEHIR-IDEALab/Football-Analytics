__author__ = 'emrullah'


class GameInstance:

    def __init__(self, players, event=None):
        self.players = players
        self.event = event


    def setPlayers(self, players):
        self.players = players


    def setEvent(self, event):
        self.event = event


    def __str__(self):
        return "%s" %(self.event)