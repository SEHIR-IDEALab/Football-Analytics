import xml.etree.cElementTree as ET


__author__ = 'emrullah'


class SnapShot:

    def __init__(self):
        pass


    @staticmethod
    def save(file_path, time, visual_players, pass_events):
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
                          speed = str(visual_player.calculateSpeed()),
                          direction = str(visual_player.calculateDirection())
            )

        defined_passes = ET.SubElement(root, "Passes")
        for pass_event in pass_events:
            ET.SubElement(defined_passes, "Pass",
                          source_id = str(pass_event.pass_source.object_id),
                          target_id = str(pass_event.pass_target.object_id),
            )

        tree = ET.ElementTree(root)
        tree.write(file_path)


    def load(self):
        pass


    def __str__(self):
        pass
