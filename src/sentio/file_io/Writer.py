import json
import os
import xml.etree.cElementTree as ET
from src.sentio.Parameters import DATA_BASE_DIR
from src.sentio.Time import Time
from src.sentio.object.PlayerBase import PlayerBase

__author__ = 'emrullah'


class Writer:

    def __init__(self, game_instances, slider_mapping):
        self.game_instances = game_instances
        self.slider_mapping = slider_mapping

        self.sample_size = 2


    def createFileAsXML(self):
        root = ET.Element("data")
        ET.SubElement(root, "TimeUnit").text = "millisecond"

        q = self.game_instances.items()
        halfs = range(1, q[-1][0][0] - q[0][0][0] + 2)

        for temp_half in halfs:
            range_index = 0  ###
            
            half_root = ET.SubElement(root, "Half", number=str(temp_half))
            position_data = ET.SubElement(half_root, "PositionData")
            for game_instance in self.game_instances:
                half, milliseconds = game_instance
                game_instance = self.game_instances.get((half, milliseconds))
                if half == temp_half:
                    if range_index == self.sample_size:  ###
                            break  ###

                    time_point = ET.SubElement(position_data, "TimePoint", val=str(milliseconds))
                    for player in game_instance.players:
                        player = PlayerBase(player)
                        ET.SubElement(
                            time_point, "Player",
                            type = str(player.object_type),
                            id = str(player.object_id),
                            js = str(player.jersey_number),
                            x = str(player.position_x),
                            y = str(player.position_y)
                        )
                    range_index += 1

            range_index = 0  ###
            evnt_data = ET.SubElement(half_root, "EventData")
            for game_instance in self.game_instances:
                half, milliseconds = game_instance
                game_instance = self.game_instances.get((half, milliseconds))
                if half == temp_half:
                    if game_instance.event:
                        if range_index == self.sample_size:  ###
                            break  ###
                        try:
                            ET.SubElement(
                                evnt_data, "Event",
                                time = str(milliseconds),
                                type_id = str(game_instance.event.event_id),
                                type = game_instance.event.event_name,
                                player_id = str(game_instance.event.player.object_id)
                            )
                        except:
                            pass
                        range_index += 1

        tree = ET.ElementTree(root)
        tree.write(os.path.join(DATA_BASE_DIR, 'output/sample_sentio_data.xml'))


    def createFileAsJSON(self):
        q = self.game_instances.items()
        halfs = range(1, q[-1][0][0] - q[0][0][0] + 2)

        with open(os.path.join(DATA_BASE_DIR, "output/sample_sentio_data.json"), "w") as outfile:
            root = {"data":
                        {
                            "TimeUnit": "millisecond",
                            "Half": {}
                        }
                    }

            for temp_half in halfs:
                root["data"]["Half"][temp_half] = {}
                position_data = []
                range_index = 0  ###
                for game_instance in self.game_instances:
                    half, milliseconds = game_instance
                    if half == temp_half:
                        if range_index == self.sample_size:  ###
                            break  ###
                        game_instance = self.game_instances.get((half, milliseconds))
                        temp_players = []
                        for player in game_instance.players:
                            player = PlayerBase(player)
                            player = {
                                "type": player.object_type,
                                "id": player.object_id,
                                "js": player.jersey_number,
                                "x": player.position_x,
                                "y": player.position_y
                            }
                            temp_players.append(player)
                        time_point = {
                            "val": milliseconds,
                            "players": temp_players
                        }
                        position_data.append(time_point)
                        range_index += 1  ###
                root["data"]["Half"][temp_half]["PositionData"] = position_data

                event_data = []
                range_index = 0  ###
                for game_instance in self.game_instances:
                    half, milliseconds = game_instance
                    if half == temp_half:
                        game_instance = self.game_instances.get((half, milliseconds))
                        if game_instance.event:
                            if range_index == self.sample_size:  ###
                                break  ###
                            try:
                                event = {
                                    "time": milliseconds,
                                    "type_id": game_instance.event.event_id,
                                    "type": game_instance.event.event_name,
                                    "player_id": game_instance.event.player.object_id
                                }
                                event_data.append(event)
                            except:
                                pass
                            range_index += 1  ###
                root["data"]["Half"][temp_half]["EventData"] = event_data

            json.dump(root, outfile)


    def createFileAsCSV(self):
        pass



    def __str__(self):
        pass