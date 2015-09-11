__author__ = 'emrullah'

class GameInstances:

    def __init__(self, game_instances):
        self.game_instances = game_instances


    def getTotalNumber(self):
        total = 0
        for half in self.game_instances:
            total += len(self.game_instances[half].keys())
        return total


    def getGameInstance(self, time):
        return self.game_instances[time.half][time.milliseconds]


    def __str__(self):
        pass
