import csv
from src.sentio import Parameters
from src.sentio.Time import Time
from src.sentio.object.GameEvent import GameEvent
from src.sentio.object.PassEvent import PassEvent
from src.sentio.object.PlayerBase import PlayerBase
from src.sentio.object.Team import Team
from src.sentio.object.Teams import Teams


__author__ = 'emrullah'


def convertDraggableToTeams(draggable_visual_teams):
    q = ({},{},{},{})
    for index, team in enumerate(draggable_visual_teams):
        for draggable_visual_player in team.values():
            player = draggable_visual_player.visual_player.player
            player.set_position(draggable_visual_player.visual_player.get_position())
            q[index][player.getJerseyNumber()] = player
    return Teams(Team("home", q[0]), Team("away", q[1]),
                 Team("referee", q[2]), Team("unknown", q[3]))


class Parser(object):

    def __init__(self):
        self.coordinate_data = list()
        self.event_data = list()


    def eventDataParser(self, event_data):
        line = event_data
        team_name, js, event_id, event_name = line[3], int(line[4]), int(line[5]), line[6]
        player = PlayerBase((0, 0, js, 0, 0))
        player.setTeamName(team_name)

        return GameEvent(player, event_id, event_name)


    def getEventData(self):
        a = dict()
        for line in self.event_data:
            half, minute, second = int(line[0]), int(line[1]), int(line[2])
            a[(half, minute, second)] = self.eventDataParser(line)
        return a


    def coordinateDataParser(self, coordinate_data):
        home_team_players, away_team_players, referees, unknowns = {}, {}, {}, {}

        for object_info in coordinate_data:
            player = PlayerBase(object_info)
            if player.isHomeTeamPlayer(): home_team_players[player.getJerseyNumber()] = player
            elif player.isAwayTeamPlayer(): away_team_players[player.getJerseyNumber()] = player
            elif player.isReferee(): referees[player.getJerseyNumber()] = player
            else: unknowns[player.getJerseyNumber()] = player

        return Teams(Team("home", home_team_players), Team("away", away_team_players),
                     Team("referee", referees), Team("unknown", unknowns))


    def getRawCoordinateData(self):
        a = dict()
        for line in self.coordinate_data:
            half, minute, second, millisecond, coord_data = int(line[3]), int(line[4]), int(line[5]), int(line[2][-3]),\
                                                        [playerInfo.split(",") for playerInfo in line[6].split("+")[:-1]]
            a[(half, minute, second, millisecond)] = coord_data
        return a


    def getRevisedCoordinateData(self):
        a = dict()
        for line in self.coordinate_data:
            half, minute, second, millisecond, coord_data = int(line[3]), int(line[4]), int(line[5]), int(line[2][-3]),\
                                                        [playerInfo.split(",") for playerInfo in line[6].split("+")[:-1]]
            a[(half, minute, second, millisecond)] = self.coordinateDataParser(coord_data)
        return a


    def getGameEvents(self):
        coordinate_data = self.getRawCoordinateData()
        a = dict()
        index = 0
        while index < len(self.event_data)-1:
            line = self.event_data[index]
            half, minute, second, team_name, js, event_id, event_name = int(line[0]), int(line[1]), int(line[2]), \
                                                                        line[3], int(line[4]), int(line[5]), line[6]
            current_player = PlayerBase((0, 0, js, 0, 0))
            current_player.setTeamName(team_name)
            current_teams = self.coordinateDataParser(coordinate_data.get((half, minute, second, 4)))
            current_player = self.convertEventPlayerToCoordinatePlayer(current_player, current_teams)
            if (half, minute, second, 4) in a:
                temp_game_event = a.get((half, minute, second, 4))
                if temp_game_event.event_id != 1:
                    a[(half, minute, second, 4)] = GameEvent(current_player, event_id, event_name)
            else:
                a[(half, minute, second, 4)] = GameEvent(current_player, event_id, event_name)
            if event_id == 1:
                n_line = self.event_data[index+1]
                n_half, n_minute, n_second, n_team_name, n_js, n_event_id, n_event_name = \
                    int(n_line[0]), int(n_line[1]), int(n_line[2]), n_line[3], int(n_line[4]), int(n_line[5]), n_line[6]
                if n_event_id == 1:
                    n_player = PlayerBase((0, 0, n_js, 0, 0))
                    n_player.setTeamName(n_team_name)
                    n_teams = self.coordinateDataParser(coordinate_data.get((n_half, n_minute, n_second, 4)))
                    n_player = self.convertEventPlayerToCoordinatePlayer(n_player, n_teams)
                    n_game_event = GameEvent(n_player, n_event_id, n_event_name)
                    if current_player is not None and n_player is not None:
                        current_player = Parser.getPlayerIn(current_player, n_teams)
                        n_game_event.setPassEvent(PassEvent(current_player, n_player, n_teams))
                    a[(n_half, n_minute, n_second, 4)] = n_game_event
            index += 1
        return a


    @staticmethod
    def getPlayerIn(p_player, teams):
        own_team = None
        if p_player.isHomeTeamPlayer(): own_team = teams.home_team
        elif p_player.isAwayTeamPlayer(): own_team = teams.away_team
        return own_team.getTeamPlayersWithJS().get(p_player.getJerseyNumber())


    def convertEventPlayerToCoordinatePlayer(self, event_player, teams):
        if event_player.getTeamName() == Parameters.HOME_TEAM_NAME: own_team = teams.home_team
        else: own_team = teams.away_team

        for player in own_team.getTeamPlayers():
            if player.getJerseyNumber() == event_player.getJerseyNumber():
                return player


    def getCombinedEventData(self):
        event_data = self.getEventData()
        coordinate_data = self.getRawCoordinateData()
        for time in event_data:
            current_event_data = event_data[time]
            current_teams = self.coordinateDataParser(coordinate_data[time + (4,)])
            current_event_data.player = self.convertEventPlayerToCoordinatePlayer(current_event_data.player,
                                                                                  current_teams)
        return event_data


    def parseSentioData(self, coordinate_data="parser/data/GS_FB_Sentio.txt", event_data="parser/data/GS_FB_Event.txt"):
        with open(coordinate_data) as md, open(event_data) as ed:
            coordinate_dt, event_dt = csv.reader(md, delimiter="\t"), csv.reader(ed, delimiter="\t")
            for line in coordinate_dt: self.coordinate_data += [line]
            for line in event_dt: self.event_data += [line]


    def get_ID_Explanation(self):
        a = dict()
        for line in self.event_data:
            id, explanation = int(line[5]), line[6]
            a[id] = explanation
        return a


    def checkTimeValid_forEvent(self, time, eventData_byTime):
        try:
            eventData_current = eventData_byTime[time.half][time.minute][time.second]
            return eventData_current
        except KeyError:
            current_time = time
            back_time = current_time.back()
            return self.checkTimeValid_forEvent(back_time, eventData_byTime)


    def get_currentEventData(self, time):
        current_time = time
        current_time.set_minMaxOfHalf(Parameters.HALF_MIN_MAX)
        eventData_byTime = self.getEventData()
        return self.checkTimeValid_forEvent(current_time, eventData_byTime)


    def get_previousEventData(self, time, chosenSkip):
        if chosenSkip == None: chosenSkip = 0
        half, minute, second, millisecond = time
        current_time = Time(half, minute, second, millisecond)
        current_time.set_minMaxOfHalf(Parameters.HALF_MIN_MAX)
        back_time = current_time
        for skipTimes in range(chosenSkip+1):
            back_time = current_time.back()
        eventData_previous = self.get_currentEventData(back_time)
        return eventData_previous


    def __str__(self):
        pass
