from collections import deque
import xml.etree.cElementTree as ET
from src.sentio.Time import Time
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.object.GameEvent import GameEvent
from src.sentio.object.GameInstance import GameInstance
from src.sentio.object.GameInstances import GameInstances
from src.sentio.object.PassEvent import PassEvent
from src.sentio.object.PlayerBase import PlayerBase

__author__ = 'emrullah'


class XMLreader(ReaderBase):

    def __init__(self, file_path):
        ReaderBase.__init__(self, file_path)


    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        mapping_index = 0
        for child in root:
            if child.tag == "Half":
                temp_half = int(child.attrib["number"])
                for grandchild in child:
                    if grandchild.tag == "PositionData":
                        for time_point in grandchild:
                            time_in_millisec = int(time_point.attrib["val"])
                            players = deque()
                            for plyr in time_point:
                                players.append(
                                    [
                                        plyr.attrib["type"],
                                        plyr.attrib["id"],
                                        plyr.attrib["js"],
                                        plyr.attrib["x"],
                                        plyr.attrib["y"]
                                    ]
                                )
                            temp_time = Time(int(temp_half), time_in_millisec)
                            self.game_instances[temp_half][time_in_millisec] = GameInstance(temp_time, players)

                            self.slider_mapping[mapping_index] = temp_time
                            mapping_index += 1

                    elif grandchild.tag == "EventData":
                        index = 0
                        while index < len(grandchild)-1:
                            c_event = grandchild[index]
                            c_time_in_millisec = int(c_event.attrib["time"])
                            c_player_id = int(c_event.attrib["player_id"])
                            c_event_type = c_event.attrib["type"]
                            c_event_id = int(c_event.attrib["type_id"])

                            temp_game_instance = self.game_instances[temp_half][c_time_in_millisec]
                            teams = ReaderBase.divideIntoTeams(temp_game_instance.players)
                            c_player = self.idToPlayer(c_player_id, teams)
                            if temp_game_instance.event is not None:
                                if c_event_id != 1:
                                    temp_game_instance.setEvent(GameEvent(c_player, c_event_id, c_event_type))
                            else:
                                temp_game_instance.setEvent(GameEvent(c_player, c_event_id, c_event_type))

                            if c_event_id == 1:
                                if index != 0:
                                    p_event = grandchild[index-1]
                                    p_time_in_millisec = int(p_event.attrib["time"])
                                    p_event_type = p_event.attrib["type"]
                                    p_event_id = int(p_event.attrib["type_id"])
                                    p_player_id = int(p_event.attrib["player_id"])

                                    p_temp_game_instance = self.game_instances[temp_half][p_time_in_millisec]
                                    p_teams = ReaderBase.divideIntoTeams(p_temp_game_instance.players)
                                    p_player = self.idToPlayer(p_player_id, p_teams)
                                    p_game_event = GameEvent(p_player, p_event_id, p_event_type)

                                    if p_event_id == 1:
                                        p_player = self.idToPlayer(p_player_id, teams)
                                        if p_player is not None and c_player is not None:
                                            temp_game_instance.event.setPassEvent(PassEvent(p_player, c_player, teams))
                            index += 1

        self.game_instances = GameInstances(self.game_instances)
        return self.game_instances, self.slider_mapping


    def __str__(self):
        pass