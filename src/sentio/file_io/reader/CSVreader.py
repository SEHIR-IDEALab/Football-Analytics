import csv
import os
from nltk import OrderedDict
from src.sentio.Parameters import DATA_BASE_DIR
from src.sentio.Time import Time
from src.sentio.file_io.reader.ReaderBase import ReaderBase
import xml.etree.cElementTree as ET
from src.sentio.object.GameEvent import GameEvent
from src.sentio.object.PassEvent import PassEvent
from src.sentio.object.PlayerBase import PlayerBase


__author__ = 'emrullah'


class CSVreader(ReaderBase):

    def __init__(self, file_path):
        ReaderBase.__init__(self, file_path)

        self.coordinate_data = {}
        self.event_data = {}

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
            current_teams = ReaderBase.divideIntoTeams(coordinate_data.get((half, minute, second, 4)))
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
                    n_teams = ReaderBase.divideIntoTeams(coordinate_data.get((n_half, n_minute, n_second, 4)))
                    n_player = self.convertEventPlayerToCoordinatePlayer(n_player, n_teams)
                    n_game_event = GameEvent(n_player, n_event_id, n_event_name)
                    if current_player is not None and n_player is not None:
                        current_player = ReaderBase.getPlayerIn(current_player, n_teams)
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
            a[(half, minute, second, millisecond)] = ReaderBase.divideIntoTeams(coord_data)
        return a


    def getCombinedEventData(self):
        event_data = self.getEventData()
        coordinate_data = self.getRawCoordinateData()
        for time in event_data:
            current_event_data = event_data[time]
            current_teams = ReaderBase.divideIntoTeams(coordinate_data[time + (4,)])
            current_event_data.player = self.convertEventPlayerToCoordinatePlayer(current_event_data.player,
                                                                                  current_teams)
        return event_data


    def parseSentioData(self, coordinate_data, event_data):
        with open(coordinate_data) as md, open(event_data) as ed:
            coordinate_dt, event_dt = csv.reader(md, delimiter="\t"), csv.reader(ed, delimiter="\t")
            for line in coordinate_dt: self.coordinate_data += [line]
            for line in event_dt: self.event_data += [line]


    #####################################
    ############ Converters #############
    #####################################

    def convertToXML(self):
        root = ET.Element("data")
        ET.SubElement(root, "TimeUnit").text = "millisecond"

        halfs = [1, 2]
        limit = Time.toMilliseconds((45, 0, 0))

        for temp_half in halfs:
            half_root = ET.SubElement(root, "Half", number=str(temp_half))
            ### coord_data
            position_data = ET.SubElement(half_root, "PositionData")
            for coord_data in self.coordinate_data:
                half, minute, second, millisecond = coord_data

                if half == temp_half:
                    time_in_mils = Time.toMilliseconds((minute, second, millisecond))
                    if half == 2:
                        time_in_mils -= limit

                    time_point = ET.SubElement(position_data, "TimePoint", val=str(time_in_mils))
                    teams = self.coordinate_data.get((half, minute, second, millisecond))
                    for index, team in enumerate((teams.home_team, teams.away_team, teams.referees, teams.unknowns)):
                        for player in team.getTeamPlayers():

                            ET.SubElement(
                                time_point, "Player",
                                type = str(player.object_type),
                                id = str(player.object_id),
                                js = str(player.jersey_number),
                                x = str(player.position_x),
                                y = str(player.position_y)
                            )

            ### event_data
            evnt_data = ET.SubElement(half_root, "EventData")
            for event_data in self.event_data:
                half, minute, second, millisecond = event_data
                game_event = self.event_data.get((half, minute, second, millisecond))

                if half == temp_half:
                    time_in_mils = Time.toMilliseconds((minute, second, millisecond))
                    if half == 2:
                        time_in_mils -= limit

                    try:
                        ET.SubElement(
                            evnt_data, "Event",
                            time = str(time_in_mils),
                            type_id = str(game_event.event_id),
                            type = game_event.event_name,
                            player_id = str(game_event.player.object_id)
                        )
                    except:
                        pass

        tree = ET.ElementTree(root)
        tree.write(os.path.join(DATA_BASE_DIR, 'output/sentio_data.xml'))


    def __str__(self):
        pass