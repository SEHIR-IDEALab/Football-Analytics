import json
import os
import xml.etree.cElementTree as ET
from src.sentio.Parameters import DATA_BASE_DIR
from src.sentio.Time import Time

__author__ = 'emrullah'


class Writer:

    def __init__(self, coord_data, event_data):
        self.coord_data = coord_data
        self.event_data = event_data


    def createFileAsXML(self):
        root = ET.Element("data")
        ET.SubElement(root, "TimeUnit").text = "millisecond"

        halfs = [1, 2]
        limit = Time.toMilliseconds((45, 0, 0))

        for temp_half in halfs:
            half_root = ET.SubElement(root, "Half", number=str(temp_half))
            ### coord_data
            position_data = ET.SubElement(half_root, "PositionData")
            for coord_data in self.coord_data:
                half, minute, second, millisecond = coord_data

                if half == temp_half:
                    time_in_mils = Time.toMilliseconds((minute, second, millisecond))
                    if half == 2:
                        time_in_mils -= limit

                    time_point = ET.SubElement(position_data, "TimePoint", val=str(time_in_mils))
                    teams = self.coord_data.get((half, minute, second, millisecond))
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


    def createFileAsCSV(self):
        pass


    def createFileAsJSON(self):
        with open(os.path.join(DATA_BASE_DIR, "output/coord_data.json"), "w") as outfile:
            data = []
            for coord_data in self.coord_data:
                half, minute, second, millisecond = coord_data

                tms = {}
                team_names = ("home", "away", "referee", "unknown")
                teams = self.coord_data.get((half, minute, second, millisecond))
                for index, team in enumerate((teams.home_team, teams.away_team, teams.referees, teams.unknowns)):
                    temp_team = []
                    for player in team.getTeamPlayers():
                        player = {
                            "object_type": player.object_type,
                            "object_id": player.object_id,
                            "jersey_number": player.jersey_number,
                            "position_x": player.position_x,
                            "position_y": player.position_y
                        }
                        temp_team.append(player)
                    tms[team_names[index]] = {
                        "name": "-",
                        "players": temp_team
                    }

                data.append({
                    "time":
                        {
                            "half": half,
                            "minute": minute,
                            "second": second,
                            "millisecond": millisecond
                        },
                    "teams": tms
                })
            json.dump(data, outfile)


    def __str__(self):
        pass