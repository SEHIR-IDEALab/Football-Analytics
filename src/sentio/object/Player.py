from src.sentio.file_io.reader import tree
import math

from src.sentio.Time import Time
from src.sentio.object.PlayerBase import PlayerBase


__author__ = 'emrullah'


class Player(PlayerBase):

    coord_info = tree()

    def __init__(self, time, object_info):
        PlayerBase.__init__(self, object_info)
        self.coord_info[time.half][time.milliseconds] = self.get_position()
        self.ball_steal = 0
        self.ball_lose = 0
        self.ball_pass = 0
        self.ball_ownership_time = 0


    def printStats(self):
        return "ball_steal: %s\nball_lose: %s\nball_pass: %s\nball_ownership_time: %s" \
                %(self.ball_steal, self.ball_lose, self.ball_pass, Time.milliseconds_to_time(self.ball_ownership_time))


    def appendNewCoordInfo(self, time, coord_info):
        self.coord_info[time.half][time.milliseconds] = coord_info


    def set_eventsInfo(self, events_info):
        self.events_info = events_info


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


    def get_eventsInfo(self):
        return self.events_info


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


    def getTeamName(self):
        return self.team_name


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


    # def calculateSpeed(self, time):
    #     first_coord = self.coord_info[time.half].itervalues().next()
    #     if self.coord_info[time.half][time.milliseconds] == first_coord:
    #         return 0
    #     else:



    def getSpeedOfPlayer_atAllPoints(self):
        time = Time()
        e = self.get_minMaxOfHalf_forPlayer()
        time.set_minMaxOfHalf(e)
        max_half = max(e.keys())
        while True:
            try:
                w = time.next()
                if [w.minute, w.second, w.mili_second] == e[max_half][1]:
                    break
                q = self.getCoordinateXY(w.half, w.minute, w.second, w.mili_second)
                coordX, coordY= q
                coordinatesXY = ([coordX], [coordY])
                for i in range(5):
                    try:
                        pre_time = w.back()
                        q = self.getCoordinateXY(pre_time.half, pre_time.minute, pre_time.second, pre_time.mili_second)
                        coordX, coordY= q
                        x, y = coordinatesXY[0], coordinatesXY[1]
                        x.append(coordX), y.append(coordY)
                    except KeyError:
                        x, y = coordinatesXY[0], coordinatesXY[1]
                        x.append(coordX), y.append(coordY)
                speed = 0.0
                coordsX, coordsY = coordinatesXY
                for i in range(5):
                    try:
                        x_current, y_current = coordsX[i], coordsY[i]
                        x_previous, y_previous = coordsX[i+1], coordsY[i+1]
                        speed += math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                    except:
                        pass
                print speed
            except KeyError:
                pass


    def getHalfIntervalsPlayed(self):
        q = {}
        for half in self.coord_info:
            milliseconds = self.coord_info[half].keys()
            min_of_half, max_of_half = milliseconds[0], milliseconds[-1]
            q[half] = Time.milliseconds_to_time(min_of_half), Time.milliseconds_to_time(max_of_half)
        return q


    def compute_runningDistance_withGameStopAndSpeedFilter(self):
        gameStop = self.game_stop_time_interval
        x_previous, y_previous = None, None
        total_runningDistance = 0.0
        q = self.get_playerCoordInfo()
        for half in sorted(q.keys()):
            for minute in sorted(q[half].keys()):
                for sec in sorted(q[half][minute].keys()):
                    for mili_sec in sorted(q[half][minute][sec].keys()):
                        x_current, y_current = q[half][minute][sec][mili_sec]
                        if x_previous is not None:
                            try:
                                checkIfInside = gameStop[half][minute][sec][mili_sec]
                            except KeyError:
                                local_runningDistance = math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                                if local_runningDistance <= 2.6: # 13m/s
                                    total_runningDistance += local_runningDistance
                        x_previous, y_previous = x_current, y_current
        return total_runningDistance


    def compute_runningDistance_withGameStopFilter(self):
        gameStop = self.game_stop_time_interval
        x_previous, y_previous = None, None
        total_runningDistance = 0.0
        q = self.get_playerCoordInfo()
        for half in sorted(q.keys()):
            for minute in sorted(q[half].keys()):
                for sec in sorted(q[half][minute].keys()):
                    for mili_sec in sorted(q[half][minute][sec].keys()):
                        x_current, y_current = q[half][minute][sec][mili_sec]
                        if x_previous is not None:
                            try:
                                checkIfInside = gameStop[half][minute][sec][mili_sec]
                            except KeyError:
                                total_runningDistance += math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                        x_previous, y_previous = x_current, y_current
        return total_runningDistance


    def computeRunningDistance(self):
        pre_x, pre_y = None, None
        total = 0.0
        for half in self.coord_info:
            for position in self.coord_info[half].values():
                if pre_x is not None:
                    total += math.sqrt(pow(position[0]-pre_x, 2) + pow(position[1]-pre_y, 2))
                pre_x, pre_y = position
        return total


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
