import math
from src.sentio.Time import Time
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'emrullah'


class Player(object):

    def __init__(self, team_name, time, player_coord_info, events_info, game_stop_time_interval):
        self.initial_info = player_coord_info
        self.object_types = {0: "Home Team Player", 1: "Away Team Player", 2: "Referee", 3: "Home Team Goalkeeper",
                             4: "Away Team Goalkeeper", -1: "Unknown object", 6: "The other referees",
                             7: "The other referees", 8: "The other referees", 9: "The other referees"}
        self.player_coord_info = {time.half: {time.minute: {time.second: {time.mili_second:
                                                [float(self.initial_info[3]), float(self.initial_info[4])]}}}}
        self.events_info = events_info
        self.team_name = team_name
        self.game_stop_time_interval = game_stop_time_interval

        self.ball_steal = 0
        self.ball_lose = 0
        self.ball_pass = 0
        self.ball_ownership_time = 0

    def add_ballSteal(self):
        self.ball_steal += 1

    def add_ballLose(self):
        self.ball_lose += 1

    def add_ballPass(self):
        self.ball_pass += 1

    def add_ballOwnershipTime(self, bown_time):
        self.ball_ownership_time += bown_time

    def appendNewCoordInfo(self, new_timeInfo, new_player_coord_info):
        current_player_coord_info = new_player_coord_info
        x_current, y_current = float(current_player_coord_info[3]), float(current_player_coord_info[4])
        half, minute, second, milisecond = new_timeInfo.half, new_timeInfo.minute, new_timeInfo.second, new_timeInfo.mili_second
        try:
            self.player_coord_info[half][minute][second][milisecond] = (x_current, y_current)
        except KeyError:
            try:
                self.player_coord_info[half][minute][second] = {milisecond: (x_current, y_current)}
            except KeyError:
                try:
                    self.player_coord_info[half][minute] = {second: {milisecond: (x_current, y_current)}}
                except KeyError:
                    try:
                        self.player_coord_info[half] = {minute: {second: {milisecond: (x_current, y_current)}}}
                    except KeyError:
                        print "!!!!!!!!!"

    def get_playerCoordInfo(self):
        return self.player_coord_info

    def get_eventsInfo(self):
        return self.events_info

    def get_ballOwnershipTime(self):
        time = Time().int_to_time(self.ball_ownership_time)
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

    def isPlayerInGame(self, half, minute, sec, milisec):
        try:
            if milisec in self.player_coord_info[half][minute][sec]:
                return True
            return False
        except KeyError:
            return False

    def getTimeInterval_played(self):
        a = list()
        for half in self.player_coord_info:
            minutes = self.player_coord_info[half].keys()
            a.append(minutes)
        return a

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

    def get_minMaxOfHalf_forPlayer(self):
        a = {}
        q = self.get_playerCoordInfo()
        for half in q.keys():
            a[half] = []
            minutes = q[half].keys()
            min_minute, max_minute = min(minutes), max(minutes)
            seconds = q[half][min_minute].keys()
            min_second, max_second = min(seconds), max(seconds)
            mili_seconds = q[half][min_minute][min_second].keys()
            min_milisecond, max_milisecond = min(mili_seconds), max(mili_seconds)
            a[half].append([min_minute, min_second, min_milisecond])
            a[half].append([max_minute, max_second, max_milisecond])
        return a

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

    def compute_runningDistance(self):
        x_previous, y_previous = None, None
        total_runningDistance = 0.0
        q = self.get_playerCoordInfo()
        for half in sorted(q.keys()):
            for minute in sorted(q[half].keys()):
                for sec in sorted(q[half][minute].keys()):
                    for mili_sec in sorted(q[half][minute][sec].keys()):
                        x_current, y_current = q[half][minute][sec][mili_sec]
                        if x_previous is not None:
                            #current_events = self.get_eventsInfo()[half][minute][sec]
                            total_runningDistance += math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                        x_previous, y_previous = x_current, y_current
        return total_runningDistance

    def get_averageLocation(self):
        q = self.get_playerCoordInfo()
        x_total, y_total = 0, 0
        count = 0
        for half in q:
            for minute in q[half]:
                for second in q[half][minute]:
                    for milisecond in q[half][minute][second]:
                        x_current, y_current = q[half][minute][second][milisecond]
                        x_total += x_current
                        y_total += y_current
                        count += 1
        x_average, y_average = (x_total/count), (y_total/count)
        return (x_average, y_average)

    def getObjectType(self):
        return int(self.initial_info[0])

    def getObjectName(self):
        return self.object_types[int(self.initial_info[0])]

    def getObjectID(self):
        return int(self.initial_info[1])

    def getJerseyNumber(self):
        return int(self.initial_info[2])

    def getCoordinateXY(self, half, minute, sec, milisec):
        x,y = self.player_coord_info[half][minute][sec][milisec]
        return (x,y)

    def __str__(self):
        return "%s %2s" %(str(self.getObjectName()).ljust(20), self.getJerseyNumber())
