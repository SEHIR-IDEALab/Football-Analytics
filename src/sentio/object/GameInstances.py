__author__ = 'emrullah'

class GameInstances:

    def __init__(self, game_instances):
        self.game_instances = game_instances


    def getTotalNumber(self):
        total = 0
        for half in self.game_instances:
            total += len(self.game_instances[half].keys())
        return total


    def getTotalNumberIn(self, half):
        try:
            return len(self.game_instances[half].keys())
        except:
            return None


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


    def getInstancesByInterval(self, interval_min, interval_max):
        return self.getAllInstances()[5*60*interval_min:5*60*interval_max]


    def getAllInstances(self):
        q = []
        for half in self.game_instances:
            half_game_instances = self.game_instances[half].values()
            q.extend(half_game_instances)
        return q


    def getGameInstance(self, time):
        return self.game_instances[time.half][time.milliseconds]


    def __str__(self):
        pass
