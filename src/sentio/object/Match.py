import wx
from src.sentio import Parameters

from src.sentio.Time import Time
from src.sentio.gui.wxVisualization import wxVisualization
from src.sentio.object.Player import Player
from src.sentio.object.Team import Team


__author__ = 'emrullah'

class Match(object):

    def __init__(self, sentio):

        self.sentio = sentio

        self.homeTeamPlayers = dict()
        self.awayTeamPlayers = dict()
        self.referees = dict()
        self.unknownObjects = dict()


    def getMatchID(self):
        return self.sentio.getCoordinateData()[0][1]


    def getValidEventDataTime_forGivenTime(self, half, minute, second, milisec):
        try:
            eventData_current = self.sentio.getEventData_byTime()[half][minute][second]
            return half, minute, second
        except KeyError:
            time = Time(half, minute, second, milisec)
            time.set_minMaxOfHalf(self.get_minMaxOfHalf())   ####### may be removed!
            back_time = time.back()
            #print back_time.half, back_time.minute, back_time.second, back_time.mili_second
            return self.getValidEventDataTime_forGivenTime(back_time.half, back_time.minute, back_time.second, back_time.mili_second)


    def getMatchScore_forGivenTime(self, half_, minute_, second_, milisec_):
        d = {team_name:0 for team_name in (Parameters.HOME_TEAM_NAME, Parameters.AWAY_TEAM_NAME)}
        e = self.sentio.getEventData_byTime()
        done = False
        for half in sorted(e.keys()):
            for minute in sorted(e[half].keys()):
                for second in sorted(e[half][minute].keys()):
                    events = e[half][minute][second]
                    for event in events:
                        teamName_current, js_current, eventID_current = event
                        if eventID_current in range(112, 218): d[teamName_current] += 1
                    half_, minute_, second_ = self.getValidEventDataTime_forGivenTime(half_, minute_, second_, milisec_)
                    if half==half_ and minute==minute_ and second==second_:
                        done = True; break
                if done: break
            if done: break
        return d


    def getPlayersOfTeams(self):
        teams_players = dict()
        for line in self.sentio.getEventData():
            if line[3]:
                teamName, player_jerseyNumber = line[3], int(line[4])
                if teamName not in teams_players:
                    teams_players[teamName] = [player_jerseyNumber]
                else:
                    if player_jerseyNumber not in teams_players[teamName]:
                        teams_players[teamName] += [player_jerseyNumber]
        return teams_players


    def getHomeTeam(self):
        team = Team(Parameters.HOME_TEAM_NAME, self.homeTeamPlayers)
        return team


    def getAwayTeam(self):
        team = Team(Parameters.AWAY_TEAM_NAME, self.awayTeamPlayers)
        return team


    def get_referees(self):
        return self.referees


    def get_unknownObjects(self):
        return self.unknownObjects


    @staticmethod
    def get_minMaxOfHalf(coordinate_data):
        a, index, q = dict(), 0, coordinate_data
        min_half, min_minute, min_second, min_mili_second = int(q[index][3]), int(q[index][4]),\
                                                         int(q[index][5]), int(q[index][2][-3])
        a[min_half] = []
        a[min_half].append([min_minute, min_second, min_mili_second])
        while index < len(q)-1:
            current_half, next_half = q[index][3], q[index+1][3]
            if current_half != next_half:
                current_max_half, current_max_minute, current_max_second, current_max_mili_second = int(q[index][3]), \
                            int(q[index][4]), int(q[index][5]), int(q[index][2][-3])
                a[current_max_half].append([current_max_minute, current_max_second, current_max_mili_second])
                next_min_half, next_min_minute, next_min_second, next_min_mili_second = int(q[index+1][3]), \
                            int(q[index+1][4]), int(q[index+1][5]), int(q[index+1][2][-3])
                a[next_min_half] = []
                a[next_min_half].append([next_min_minute, next_min_second, next_min_mili_second])
            index += 1
        max_half, max_minute, max_second, max_mili_second = int(q[index][3]), int(q[index][4]), \
                                                    int(q[index][5]), int(q[index][2][-3])
        a[max_half].append([max_minute, max_second, max_mili_second])
        return a


    def compute_someEvents(self):
        teamName_previous, js_previous, eventID_previous = None, None, None
        time_previous_miliseconds = None
        e = self.sentio.getEventData_byTime()
        for half in sorted(e.keys()):
            for minute in sorted(e[half].keys()):
                for second in sorted(e[half][minute].keys()):
                    events = e[half][minute][second]
                    for event in events:
                        teamName_current, js_current, eventID_current = event
                        time_current = Time(half, minute, second)
                        time_current_miliseconds = time_current.time_to_int(time_current)
                        if teamName_previous is not None:
                            try:
                                if teamName_current != teamName_previous or js_current != js_previous or eventID_previous == 1:
                                    bown_time = time_current_miliseconds - time_previous_miliseconds
                                    if teamName_previous == Parameters.HOME_TEAM_NAME:
                                        self.homeTeamPlayers[js_previous].add_ballOwnershipTime(bown_time)
                                    elif teamName_previous == Parameters.AWAY_TEAM_NAME:
                                        self.awayTeamPlayers[js_previous].add_ballOwnershipTime(bown_time)
                                if teamName_current != teamName_previous and teamName_previous != "":
                                    if teamName_current == Parameters.HOME_TEAM_NAME:
                                        self.homeTeamPlayers[js_current].add_ballSteal()
                                        self.awayTeamPlayers[js_previous].add_ballLose()
                                    elif teamName_current == Parameters.AWAY_TEAM_NAME:
                                        self.awayTeamPlayers[js_current].add_ballSteal()
                                        self.homeTeamPlayers[js_previous].add_ballLose()
                                elif teamName_current == teamName_previous and teamName_previous != "" and js_current != js_previous:
                                    if teamName_current == Parameters.HOME_TEAM_NAME:
                                        self.homeTeamPlayers[js_previous].add_ballPass()
                                    elif teamName_current == Parameters.AWAY_TEAM_NAME:
                                        self.awayTeamPlayers[js_previous].add_ballPass()
                            except KeyError:
                                pass
                        teamName_previous, js_previous, eventID_previous = teamName_current, js_current, eventID_current
                        time_previous_miliseconds = time_current_miliseconds


    def get_timeInterval_ofGameStop(self):
        game_stop_time_intervals = dict()
        time = Time()
        time.set_minMaxOfHalf(self.get_minMaxOfHalf(self.sentio.getCoordinateData()))
        q = self.sentio.getEventData_byTime()
        game_stop_time_intervals = self.checkForGameStopEvent(time, game_stop_time_intervals, q)
        while True:
            try:
                next_time = time.next()
                #print next_time.half, next_time.minute, next_time.second, next_time.mili_second
                game_stop_time_intervals = self.checkForGameStopEvent(next_time, game_stop_time_intervals, q)
            except KeyError:
                break
        return game_stop_time_intervals


    def checkForGameStopEvent(self, time, game_stop_time_intervals, q):
        try:
            instant_events = q[time.half][time.minute][time.second]
            for instant_event in instant_events:
                teamName, js, eventID = instant_event
                if eventID == 2:
                    game_stop_time_intervals = self.append_newEventTimeIntervals(game_stop_time_intervals, time)
        except KeyError:
            back_time = time.back()
            back_half, back_minute, back_second, back_millisec = back_time.half, back_time.minute, back_time.second, back_time.millisecond
            try:
                checkIfInside = game_stop_time_intervals[back_half][back_minute][back_second][back_millisec]
                current_time = time.next()
                game_stop_time_intervals = self.append_newEventTimeIntervals(game_stop_time_intervals, current_time)
            except KeyError:
                pass
        return game_stop_time_intervals


    def append_newEventTimeIntervals(self, myDict, new_time_info):
        half, minute, second, mili_second = new_time_info.half, new_time_info.minute, new_time_info.second, new_time_info.millisecond
        myDict.setdefault(half, {})
        myDict[half].setdefault(minute, {})
        myDict[half][minute].setdefault(second, {})
        myDict[half][minute][second][mili_second] = None

        return myDict


    def identifyObjects(self):
        event_data = self.sentio.getEventData_byTime()
        game_stop = self.get_timeInterval_ofGameStop()
        time = Time()
        time.set_minMaxOfHalf(self.get_minMaxOfHalf(self.sentio.getCoordinateData()))
        q = self.sentio.getCoordinateData_byTime()
        players_coord_info = q[time.half][time.minute][time.second][time.millisecond]
        self.makeClassification(time, players_coord_info, event_data, game_stop)
        while True:
            try:
                next_time = time.next()
                try:
                    players_coord_info = q[next_time.half][next_time.minute][next_time.second][next_time.mili_second]
                    self.makeClassification(time, players_coord_info, event_data, game_stop)
                except KeyError:
                    #print half, minute, second, mili_second
                    pass
            except KeyError:
                break


    def makeClassification(self, time_info, objects_coord_info, event_data, game_stop):
        types = [[0,3], [1,4], [2,6,7,8,9], [-1]]
        for player_coord_info in objects_coord_info:
            object_type, jersey_number = int(player_coord_info[0]), int(player_coord_info[2])
            for index, object_class in enumerate([self.homeTeamPlayers, self.awayTeamPlayers, self.referees, self.unknownObjects]):
                if object_type in types[index]:
                    if jersey_number in object_class:
                        object_class[jersey_number].appendNewCoordInfo(time_info, player_coord_info)
                    else:
                        teamName = None
                        if object_type in [0, 3]: teamName = Parameters.HOME_TEAM_NAME
                        elif object_type in [1, 4]: teamName = Parameters.AWAY_TEAM_NAME
                        object_class[jersey_number] = Player(teamName, time_info, player_coord_info)
                        player = object_class[jersey_number]
                        player.set_eventsInfo(event_data)
                        player.set_gameStopTimeInterval(game_stop)


    def visualizeMatch(self):
        app = wx.App()
        app.frame = wxVisualization(self.sentio.game_instances)
        app.frame.Show()
        app.MainLoop()


    def __str__(self):
        pass
