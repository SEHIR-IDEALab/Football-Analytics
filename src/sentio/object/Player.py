from src.sentio.Parameters import SPEED_THRESHOLD
from src.sentio.file_io.reader import tree
import math

from src.sentio.Time import Time
from src.sentio.object.PlayerBase import PlayerBase


__author__ = 'emrullah'


class Player(PlayerBase):

    def __init__(self, time, object_info):
        PlayerBase.__init__(self, object_info)
        self.coord_info = tree()
        self.coord_info[time.half][time.milliseconds] = self.get_position()

        self.ball_steal = 0
        self.ball_lose = 0
        self.ball_pass = 0
        self.ball_ownership_time = 0

        self.dominant_region = 0
        self.total_area_for_dominant_regions = 0
        self.total_number_of_instances = 0


    def calculateAverageDRPerInstance(self):
        return self.dominant_region / float(self.total_number_of_instances)


    def calculateDRPercentageInTotal(self):
        return self.calculateAverageDRPerInstance() / float(self.total_area_for_dominant_regions)


    def printStats(self):
        return "ball_steal: %s\nball_lose: %s\nball_pass: %s\nball_ownership_time: %s" \
                %(self.ball_steal, self.ball_lose, self.ball_pass, Time.milliseconds_to_time(self.ball_ownership_time))


    def appendNewCoordInfo(self, time, coord_info):
        self.coord_info[time.half][time.milliseconds] = coord_info


    def set_gameStopTimeInterval(self, game_stop_time_interval):
        self.game_stop_time_interval = game_stop_time_interval


    def add_ballSteal(self):
        self.ball_steal += 1


    def add_ballLose(self):
        self.ball_lose += 1


    def add_ballPass(self):
        self.ball_pass += 1


    def add_ballOwnershipTime(self, bown_time):
        self.ball_ownership_time += bown_time


    def get_playerCoordInfo(self):
        return self.coord_info


    def get_ballOwnershipTime(self):
        time = Time.milliseconds_to_time(self.ball_ownership_time)
        minute, second = time.minute, time.second
        q = "%s.%s" % (minute, second)
        return float(q)


    def get_totalBallSteal(self):
        return self.ball_steal


    def get_totalBallLose(self):
        return self.ball_lose


    def get_totalBallPass(self):
        return self.ball_pass


    def isPlayerInGame(self, time):
        if self.coord_info[time.half][time.milliseconds]:
            return True
        return False


    ## it may include same minutes for multiple times
    def getTimeIntervalPlayed(self):
        a = list()
        for half in self.coord_info:
            for milliseconds in self.coord_info[half]:
                minute, second, millisecond = Time.milliseconds_to_time(milliseconds)
                a.append(minute)
        return a


    def calculateSpeed(self, time):
        return PlayerBase.calculateSpeedFor(time, self.coord_info, visual=False)


    def calculateSpeedAtAllPoints(self):
        speeds = tree()
        for half in self.coord_info:
            for milliseconds in self.coord_info[half].keys():
                speeds[half][milliseconds] = self.calculateSpeed(Time(half, milliseconds))
        return speeds


    def calculateDirection(self, time):
        return PlayerBase.calculateDirectionFor(time, self.coord_info, visual=False)


    def calculateDirectionAtAllPoints(self):
        directions = tree()
        for half in self.coord_info:
            for milliseconds in self.coord_info[half].keys():
                directions[half][milliseconds] = self.calculateDirection(Time(half, milliseconds))
        return directions


    def computeRunningDistance(self):
        pre_x, pre_y = None, None
        total = 0.0
        for half in self.coord_info:
            for position in self.coord_info[half].values():
                if pre_x is not None:
                    total += math.sqrt(pow(position[0]-pre_x, 2) + pow(position[1]-pre_y, 2))
                pre_x, pre_y = position
        return total


    def computeRunningDistanceWithGameStopFilter(self):
        pre_x, pre_y = None, None
        total = 0.0
        for half in self.coord_info:
            for milliseconds in self.coord_info[half]:
                position = self.coord_info[half][milliseconds]
                if pre_x is not None and self.game_stop_time_interval[half][milliseconds] != True:
                    total += math.sqrt(pow(position[0]-pre_x, 2) + pow(position[1]-pre_y, 2))
                pre_x, pre_y = position
        return total


    def computeRunningDistanceWithSpeedFilter(self):
        pre_x, pre_y = None, None
        total = 0.0
        for half in self.coord_info:
            for position in self.coord_info[half].values():
                if pre_x is not None:
                    local_rd = math.sqrt(pow(position[0]-pre_x, 2) + pow(position[1]-pre_y, 2))
                    if local_rd <= SPEED_THRESHOLD:
                        total += local_rd
                pre_x, pre_y = position
        return total


    def computeRunningDistanceWithGameStopAndSpeedFilter(self):
        pre_x, pre_y = None, None
        total = 0.0
        for half in self.coord_info:
            for milliseconds in self.coord_info[half]:
                position = self.coord_info[half][milliseconds]
                if pre_x is not None and self.game_stop_time_interval[half][milliseconds] != True:
                    local_rd = math.sqrt(pow(position[0]-pre_x, 2) + pow(position[1]-pre_y, 2))
                    if local_rd <= SPEED_THRESHOLD:
                        total += local_rd
                pre_x, pre_y = position
        return total


    def getHalfIntervalsPlayed(self):
        q = {}
        for half in self.coord_info:
            milliseconds = self.coord_info[half].keys()
            min_of_half, max_of_half = milliseconds[0], milliseconds[-1]
            q[half] = Time.milliseconds_to_time(min_of_half), Time.milliseconds_to_time(max_of_half)
        return q


    def computeAverageLocation(self):
        total_x, total_y = 0.0, 0.0
        count = 0
        for half in self.coord_info:
            for position in self.coord_info[half].values():
                total_x += position[0]
                total_y += position[1]
                count += 1
        return (total_x/count), (total_y/count)


    def getCoordinateXY(self, time):
        return self.coord_info[time.half][time.milliseconds]


    def __str__(self):
        return "%s %2s" %(str(self.getObjectTypeName()).ljust(20), self.getJerseyNumber())
