from src.sentio.Player import Player
from src.sentio.Team import Team
from src.sentio.Time import Time
from src.sentio.Visualization import Visualization

__author__ = 'emrullah'

class Match(object):

    def __init__(self, sentio):

        self.sentio = sentio

        self.homeTeamPlayers = dict()
        self.awayTeamPlayers = dict()
        self.referees = dict()
        self.unknownObjects = dict()

        self.teamNames = self.getTeamNames()

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
        d = dict()
        e = self.sentio.getEventData_byTime()
        done = False
        for half in sorted(e.keys()):
            for minute in sorted(e[half].keys()):
                for second in sorted(e[half][minute].keys()):
                    events = e[half][minute][second]
                    for event in events:
                        teamName_current, js_current, eventID_current = event
                        if teamName_current != "": d.setdefault(teamName_current, 0)
                        if eventID_current in range(112, 218): d[teamName_current] += 1
                    half_, minute_, second_ = self.getValidEventDataTime_forGivenTime(half_, minute_, second_, milisec_)
                    if half==half_ and minute==minute_ and second==second_:
                        done = True; break
                if done: break
            if done: break
        return d


    def getTeamNames(self):
        eventData_raw = self.sentio.getEventData()
        homeTeam, awayTeam = None, None
        initial_coordInfo = self.sentio.getCoordinateData_byTime()[1][0][0][0]
        initial_eventInfo = eventData_raw[0]
        teamName1, jerseyNumber = initial_eventInfo[3], int(initial_eventInfo[4])
        for player in initial_coordInfo:
            playerTeamID, playerJS, coordX, coordY = int(player[0]), int(player[2]), float(player[3]), float(player[4])
            if 50<coordX<55 and 30<coordY<35 and jerseyNumber==playerJS:
                if playerTeamID==0: homeTeam = teamName1
                elif playerTeamID==1: awayTeam = teamName1
        for line in eventData_raw:
            teamName2 = line[3]
            if teamName2 != teamName1 and teamName2 != "":
                if homeTeam == None: homeTeam = teamName2
                else: awayTeam = teamName2
                break
        return (homeTeam, awayTeam)

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
        homeTeamName = self.teamNames[0]
        team = Team(homeTeamName, self.homeTeamPlayers)
        return team

    def getAwayTeam(self):
        awayTeamName = self.teamNames[1]
        team = Team(awayTeamName, self.awayTeamPlayers)
        return team

    def get_referees(self):
        return self.referees

    def get_unknownObjects(self):
        return self.unknownObjects

    def get_ID_Explanation(self):
        a = dict()
        for line in self.sentio.getEventData():
            id, explanation = int(line[5]), line[6]
            a[id] = explanation
        return a

    def get_minMaxOfHalf(self):
        a, index, q = dict(), 0, self.sentio.getCoordinateData()
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
                                    if teamName_previous == self.teamNames[0]:
                                        self.homeTeamPlayers[js_previous].add_ballOwnershipTime(bown_time)
                                    elif teamName_previous == self.teamNames[1]:
                                        self.awayTeamPlayers[js_previous].add_ballOwnershipTime(bown_time)
                                if teamName_current != teamName_previous and teamName_previous != "":
                                    if teamName_current == self.teamNames[0]:
                                        self.homeTeamPlayers[js_current].add_ballSteal()
                                        self.awayTeamPlayers[js_previous].add_ballLose()
                                    elif teamName_current == self.teamNames[1]:
                                        self.awayTeamPlayers[js_current].add_ballSteal()
                                        self.homeTeamPlayers[js_previous].add_ballLose()
                                elif teamName_current == teamName_previous and teamName_previous != "" and js_current != js_previous:
                                    if teamName_current == self.teamNames[0]:
                                        self.homeTeamPlayers[js_previous].add_ballPass()
                                    elif teamName_current == self.teamNames[1]:
                                        self.awayTeamPlayers[js_previous].add_ballPass()
                            except KeyError:
                                pass
                        teamName_previous, js_previous, eventID_previous = teamName_current, js_current, eventID_current
                        time_previous_miliseconds = time_current_miliseconds

    def get_timeInterval_ofGameStop(self):
        game_stop_time_intervals = dict()
        time = Time()
        time.set_minMaxOfHalf(self.get_minMaxOfHalf())
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
            back_half, back_minute, back_second, back_milisec = back_time.half, back_time.minute, back_time.second, back_time.mili_second
            try:
                checkIfInside = game_stop_time_intervals[back_half][back_minute][back_second][back_milisec]
                current_time = time.next()
                game_stop_time_intervals = self.append_newEventTimeIntervals(game_stop_time_intervals, current_time)
            except KeyError:
                pass
        return game_stop_time_intervals


    def append_newEventTimeIntervals(self, myDict, new_time_info):
        half, minute, second, mili_second = new_time_info.half, new_time_info.minute, new_time_info.second, new_time_info.mili_second
        myDict.setdefault(half, {})
        myDict[half].setdefault(minute, {})
        myDict[half][minute].setdefault(second, {})
        myDict[half][minute][second][mili_second] = None
        return myDict

    def identifyObjects(self):
        gameStop = self.get_timeInterval_ofGameStop()
        events_info = self.sentio.getEventData_byTime()
        time = Time()
        time.set_minMaxOfHalf(self.get_minMaxOfHalf())
        q = self.sentio.getCoordinateData_byTime()
        players_coord_info = q[time.half][time.minute][time.second][time.mili_second]
        self.makeClassification(time, players_coord_info, events_info, gameStop)
        while True:
            try:
                next_time = time.next()
                try:
                    players_coord_info = q[next_time.half][next_time.minute][next_time.second][next_time.mili_second]
                    self.makeClassification(time, players_coord_info, events_info, gameStop)
                except KeyError:
                    #print half, minute, second, mili_second
                    pass
            except KeyError:
                break

    def makeClassification(self, time_info, objects_coord_info, events_info, gameStop):
        types = [[0,3], [1,4], [2,6,7,8,9], [-1]]
        for player_coord_info in objects_coord_info:
            object_type, jersey_number = int(player_coord_info[0]), int(player_coord_info[2])
            for index, object_class in enumerate([self.homeTeamPlayers, self.awayTeamPlayers, self.referees, self.unknownObjects]):
                if object_type in types[index]:
                    if jersey_number in object_class:
                        object_class[jersey_number].appendNewCoordInfo(time_info, player_coord_info)
                    else:
                        teamName = None
                        if object_type in [0, 3]: teamName = self.teamNames[0]
                        elif object_type in [1, 4]: teamName = self.teamNames[1]
                        object_class[jersey_number] = Player(teamName, time_info, player_coord_info, events_info, gameStop)

    def visualizeMatch(self):
        visualization = Visualization(self.sentio.getCoordinateData_byTime(),self.sentio.getEventData_byTime(),
                                      self.getTeamNames(), self.get_minMaxOfHalf(), self.get_ID_Explanation())


    def __str__(self):
        pass
