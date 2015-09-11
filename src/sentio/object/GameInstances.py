__author__ = 'emrullah'

class GameInstances:

    def __init__(self, game_instances):
        self.game_instances = game_instances


    def getTotalNumber(self):
        total = 0
        for half in self.game_instances:
            total += len(self.game_instances[half].keys())
        return total


    def getFirstHalfInstances(self):
        try:
            return self.game_instances[1].values()
        except:
            return None


    def getSecondHalfInstances(self):
        try:
            return self.game_instances[2].values()
        except:
            return None


    def __str__(self):
        pass
