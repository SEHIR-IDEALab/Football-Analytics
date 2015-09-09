from collections import deque
import json
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.object.GameEvent import GameEvent
from src.sentio.object.GameInstance import GameInstance
from src.sentio.object.PassEvent import PassEvent

__author__ = 'emrullah'


class JSONreader(ReaderBase):

    def __init__(self, file_path):
        ReaderBase.__init__(self, file_path)

    def parse(self):
        with open(self.file_path) as data_file:
            data = json.load(data_file)
            mapping_index = 0
            for temp_half in data["data"]["Half"]:
                positions_data = data["data"]["Half"][temp_half]["PositionData"]
                for position_data in positions_data:
                    time_in_millisec = position_data["val"]
                    players = deque()
                    for plyr in position_data["players"]:
                        players.append(
                            [
                                plyr["type"],
                                plyr["id"],
                                plyr["js"],
                                plyr["x"],
                                plyr["y"]
                            ]
                        )
                    self.game_instances[(int(temp_half), time_in_millisec)] = GameInstance(players)

                    self.slider_mapping[mapping_index] = (int(temp_half), time_in_millisec)
                    mapping_index += 1

                index = 0
                events_data = data["data"]["Half"][temp_half]["EventData"]
                while index < len(events_data)-1:
                    c_event = events_data[index]
                    c_time_in_millisec = int(c_event["time"])
                    c_player_id = int(c_event["player_id"])
                    c_event_type = c_event["type"]
                    c_event_id = int(c_event["type_id"])

                    temp_game_instance = self.game_instances[(int(temp_half), c_time_in_millisec)]
                    teams = ReaderBase.divideIntoTeams(temp_game_instance.players)
                    c_player = self.idToPlayer(c_player_id, teams)
                    if temp_game_instance.event is not None:
                        if c_event_id != 1:
                            temp_game_instance.setEvent(GameEvent(c_player, c_event_id, c_event_type))
                    else:
                        temp_game_instance.setEvent(GameEvent(c_player, c_event_id, c_event_type))

                    if c_event_id == 1:
                        if index != 0:
                            p_event = events_data[index-1]
                            p_time_in_millisec = int(p_event["time"])
                            p_event_type = p_event["type"]
                            p_event_id = int(p_event["type_id"])
                            p_player_id = int(p_event["player_id"])

                            p_temp_game_instance = self.game_instances[(int(temp_half), p_time_in_millisec)]
                            p_teams = ReaderBase.divideIntoTeams(p_temp_game_instance.players)
                            p_player = self.idToPlayer(p_player_id, p_teams)
                            p_game_event = GameEvent(p_player, p_event_id, p_event_type)

                            if p_event_id == 1:
                                p_player = self.idToPlayer(p_player_id, teams)
                                if p_player is not None and c_player is not None:
                                    temp_game_instance.event.setPassEvent(PassEvent(p_player, c_player, teams))
                    index += 1

        return self.game_instances, self.slider_mapping


    def __str__(self):
        pass