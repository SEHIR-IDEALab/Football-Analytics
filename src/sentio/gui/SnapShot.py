import xml.etree.cElementTree as ET
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.object.PassEvent import PassEvent
from src.sentio.object.PlayerBase import PlayerBase


__author__ = 'emrullah'


class SnapShot:

    def __init__(self):
        pass


    @staticmethod
    def save(file_path, visual_players, pass_events):
        root = ET.Element("data")

        time_point = ET.SubElement(root, "Players")
        for visual_player in visual_players:
            ET.SubElement(time_point, "Player",
                          type = str(visual_player.player.object_type),
                          team_name = str(visual_player.player.getTypeName()),
                          id = str(visual_player.player.object_id),
                          js = str(visual_player.player.jersey_number),
                          x = str(visual_player.get_position()[0]),
                          y = str(visual_player.get_position()[1]),
                          speed = str(visual_player.speed),
                          direction = str(visual_player.direction)
            )

        defined_passes = ET.SubElement(root, "Passes")
        for pass_event in pass_events:
            ET.SubElement(defined_passes, "Pass",
                          source_id = str(pass_event.pass_source.object_id),
                          target_id = str(pass_event.pass_target.object_id),
            )

        tree = ET.ElementTree(root)
        tree.write(file_path)


    @staticmethod
    def load(file_path):
        idToPlayers = {}
        pass_events = []

        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
            if child.tag == "Players":
                for plyr in child:
                    player_id = plyr.attrib["id"]
                    player = PlayerBase([
                        plyr.attrib["type"],
                        player_id,
                        plyr.attrib["js"],
                        plyr.attrib["x"],
                        plyr.attrib["y"]])
                    player.speed = float(plyr.attrib["speed"])
                    player.direction = float(plyr.attrib["direction"])
                    idToPlayers[player_id] = player
            elif child.tag == "Passes":
                for pass_event in child:
                    pass_events.append(
                        PassEvent(
                            idToPlayers[pass_event.attrib["source_id"]],
                            idToPlayers[pass_event.attrib["target_id"]],
                            ReaderBase.divideIntoTeams(idToPlayers.values())
                        )
                    )
        return idToPlayers.values(), pass_events


    def __str__(self):
        pass
