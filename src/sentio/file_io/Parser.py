
from collections import OrderedDict, deque
import csv
from src.sentio import Parameters
from src.sentio.Time import Time
from src.sentio.object.GameEvent import GameEvent
from src.sentio.object.GameInstance import GameInstance
from src.sentio.object.PassEvent import PassEvent
from src.sentio.object.PlayerBase import PlayerBase
from src.sentio.object.Team import Team
from src.sentio.object.Teams import Teams

import xml.etree.cElementTree as ET






__author__ = 'emrullah'


class Parser(object):

    def __init__(self):
        self.coordinate_data = list()
        self.event_data = list()


    def getGameEvents(self):
        coordinate_data = self.getRawCoordinateData()
        a = OrderedDict()
        index = 0
        while index < len(self.event_data)-1:
            line = self.event_data[index]
            half, minute, second, team_name, js, event_id, event_name = int(line[0]), int(line[1]), int(line[2]), \
                                                                        line[3], int(line[4]), int(line[5]), line[6]
            current_player = PlayerBase((0, 0, js, 0, 0))
            current_player.setTeamName(team_name)
            current_teams = Parser.divideIntoTeams(coordinate_data.get((half, minute, second, 4)))
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
                    n_teams = Parser.divideIntoTeams(coordinate_data.get((n_half, n_minute, n_second, 4)))
                    n_player = self.convertEventPlayerToCoordinatePlayer(n_player, n_teams)
                    n_game_event = GameEvent(n_player, n_event_id, n_event_name)
                    if current_player is not None and n_player is not None:
                        current_player = Parser.getPlayerIn(current_player, n_teams)
                        n_game_event.setPassEvent(PassEvent(current_player, n_player, n_teams))
                    a[(n_half, n_minute, n_second, 4)] = n_game_event
            index += 1
        return a


    def eventDataParser(self, event_data):
        line = event_data
        team_name, js, event_id, event_name = line[3], int(line[4]), int(line[5]), line[6]
        player = PlayerBase((0, 0, js, 0, 0))
        player.setTeamName(team_name)

        return GameEvent(player, event_id, event_name)


    def getEventData(self):
        a = OrderedDict()
        for line in self.event_data:
            half, minute, second = int(line[0]), int(line[1]), int(line[2])
            a[(half, minute, second)] = self.eventDataParser(line)
        return a


    def getRawCoordinateData(self):
        a = OrderedDict()
        for line in self.coordinate_data:
            half, minute, second, millisecond, coord_data = int(line[3]), int(line[4]), int(line[5]), int(line[2][-3]),\
                                                        [playerInfo.split(",") for playerInfo in line[6].split("+")[:-1]]
            a[(half, minute, second, millisecond)] = coord_data
        return a


    def getRevisedCoordinateData(self):
        a = OrderedDict()
        for line in self.coordinate_data:
            half, minute, second, millisecond, coord_data = int(line[3]), int(line[4]), int(line[5]), int(line[2][-3]),\
                                                        [playerInfo.split(",") for playerInfo in line[6].split("+")[:-1]]
            a[(half, minute, second, millisecond)] = Parser.divideIntoTeams(coord_data)
        return a


    def getCombinedEventData(self):
        event_data = self.getEventData()
        coordinate_data = self.getRawCoordinateData()
        for time in event_data:
            current_event_data = event_data[time]
            current_teams = Parser.divideIntoTeams(coordinate_data[time + (4,)])
            current_event_data.player = self.convertEventPlayerToCoordinatePlayer(current_event_data.player,
                                                                                  current_teams)
        return event_data


    def parseSentioData(self, coordinate_data, event_data):
        with open(coordinate_data) as md, open(event_data) as ed:
            coordinate_dt, event_dt = csv.reader(md, delimiter="\t"), csv.reader(ed, delimiter="\t")
            for line in coordinate_dt: self.coordinate_data += [line]
            for line in event_dt: self.event_data += [line]


    def __str__(self):
        pass
