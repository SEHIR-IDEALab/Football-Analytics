import csv

from src.sentio.Parameters import *
from src.sentio.object.PassEvent import PassEvent
from src.sentio.object.PlayerBase import PlayerBase
from src.sentio.object.Team import Team
from src.sentio.object.Teams import Teams
from src.sentio.file_io import Parser
from src.sentio.pass_evaluate.Pass import Pass


__author__ = 'emrullah'


def adjust_arrow_size(current_position, next_position, speed):
    current_x, current_y = current_position
    next_x, next_y = next_position

    length_x = (next_x - current_x) * speed
    next_x = length_x + current_x
    length_y = (next_y - current_y) * speed
    next_y = length_y + current_y

    if length_x >= 0: next_x += INITIAL_ARROW_SIZE
    else: next_x -= INITIAL_ARROW_SIZE
    if length_y >= 0: next_y += INITIAL_ARROW_SIZE
    else: next_y -= INITIAL_ARROW_SIZE

    return next_x, next_y


class SnapShot:

    def __init__(self, file_name):
        self.file_name = file_name


    def saveSnapShot(self, draggable_visual_teams, defined_passes, directions, speeds):
        out = csv.writer(open(self.file_name,"w"), delimiter='\t', quoting=csv.QUOTE_NONE)
        out.writerow(["object_type", "object_id", "team_name", "jersey_number",
                      "x1", "y1", "x2", "y2", "speed", "pass_to"])
        teams = Parser.convertDraggableToTeams(draggable_visual_teams)
        for index, team in enumerate((teams.home_team, teams.away_team, teams.referees, teams.unknowns)):
            a = team.getTeamPlayersWithJS()
            for js in a:
                player = a[js]
                teamName = (HOME_TEAM_NAME if index == 0 else (AWAY_TEAM_NAME if index == 1
                                                         else ("referee" if index == 2 else "unknown")))
                nextX, nextY = directions[index][js]
                speed = speeds[index][js]
                js2 = ""
                for defined_pass in defined_passes:
                    if player.getObjectID() == defined_pass.pass_source.player.getObjectID():
                        p2 = defined_pass.pass_target.player
                        js2 += str(p2.getObjectID()) + "@"
                passTo = ("None" if js2=="" else js2[:-1])
                out.writerow([player.getObjectType(), player.getObjectID(), teamName, player.getJerseyNumber(),
                          player.getPositionX(), player.getPositionY(), nextX, nextY, speed, passTo])


    def loadSnapShot(self, ax):
        home_team, away_team, referees, unknowns = {}, {}, {}, {}
        list_of_directions = []
        with open(self.file_name) as fname:
            fname.readline()
            snapshot_data= csv.reader(fname, delimiter="\t")
            for line in snapshot_data:
                object_type, object_id, team_name, jersey_number, current_x, current_y, next_x, next_y, speed, pass_to = \
                    int(line[0]), int(line[1]), line[2], int(line[3]), float(line[4]), float(line[5]), float(line[6]), \
                    float(line[7]), float(line[8]), line[9]

                next_x, next_y = adjust_arrow_size((current_x, current_y), (next_x, next_y), speed)
                directionAnnotation = ax.annotate('', xy=(next_x,next_y), xycoords='data', xytext=(current_x,current_y),
                                            textcoords='data',size=20, va="center", ha="center",zorder=2, arrowprops=dict(
                                            arrowstyle="simple", connectionstyle="arc3",fc="cyan", ec="b", lw=2))
                list_of_directions.append(directionAnnotation)

                player = PlayerBase((object_type, object_id, jersey_number, current_x, current_y))
                if player.isHomeTeamPlayer(): home_team[player.getJerseyNumber()] = player
                elif player.isAwayTeamPlayer(): away_team[player.getJerseyNumber()] = player
                elif player.isReferee(): referees[player.getJerseyNumber()] = player
                else: unknowns[player.getJerseyNumber()] = player

        teams = Teams(Team("home", home_team), Team("away", away_team),
                     Team("referee", referees), Team("unknown", unknowns))
        return teams, list_of_directions


    def displayAllPasses(self, file_path, ax, draggable_visual_teams, pass_logger):
        all_defined_passes = []
        drag_pass = Pass()
        drag_pass.teams = Parser.convertDraggableToTeams(draggable_visual_teams)
        with open(file_path) as fname:
            fname.readline()
            snapshot_data= csv.reader(fname, delimiter="\t")
            for line in snapshot_data:
                object_type, object_id, team_name, jersey_number, current_x, current_y, next_x, next_y, speed, pass_to = \
                    int(line[0]), int(line[1]), line[2], int(line[3]), float(line[4]), float(line[5]), float(line[6]), \
                    float(line[7]), float(line[8]), line[9]
                defined_passes = self.displayPasses_perPlayer(draggable_visual_teams, ax, drag_pass, pass_logger,
                                                              pass_to, object_id)
                all_defined_passes.extend(defined_passes)
        return all_defined_passes


    def displayPasses_perPlayer(self, draggable_visual_teams, ax, drag_pass, pass_display,
                                passTo, object_id):
        defined_passes = []
        if passTo != "None":
            p1, p2_s = None, []
            passTo = [int(pto) for pto in passTo.split("@")]
            for id_to in passTo:
                for draggable_visual_team in draggable_visual_teams:
                    for draggable_visual_player in draggable_visual_team.values():
                        visual_player = draggable_visual_player.visual_player
                        if  visual_player.player.getObjectID() == object_id:
                            p1 = visual_player
                        elif visual_player.player.getObjectID() == id_to:
                            p2_s.append(visual_player)
            for p2 in p2_s:
                pass_annotation = ax.annotate('', xy=(.5, .5), xytext=(.5, .5), xycoords=(p2), textcoords=(p1), size=20,
                                    picker = True, arrowprops=dict(patchA=p1.get_bbox_patch(), arrowstyle="fancy",
                                    fc="0.6", ec="none", connectionstyle="arc3"))
                pass_event = PassEvent(pass_annotation.textcoords, pass_annotation.xycoords, drag_pass.teams)
                pass_event.root = pass_annotation
                defined_passes.append(pass_event)
                drag_pass.displayDefinedPass(pass_event, pass_display, visual=True)
        return defined_passes


    def loadTeams(self):
        home_team_players, away_team_players, referees, unknowns = {}, {}, {}, {}
        with open(self.file_name) as fname:
            fname.readline()
            snapshot_data= csv.reader(fname, delimiter="\t")
            for line in snapshot_data:
                object_type, object_id, team_name, jersey_number, current_x, current_y, next_x, next_y, speed, pass_to = \
                    int(line[0]), int(line[1]), line[2], int(line[3]), float(line[4]), float(line[5]), float(line[6]), \
                    float(line[7]), float(line[8]), line[9]
                player = PlayerBase((object_type, object_id, jersey_number, current_x, current_y))
                if player.isHomeTeamPlayer(): home_team_players[player.getJerseyNumber()] = player
                elif player.isAwayTeamPlayer(): away_team_players[player.getJerseyNumber()] = player
                elif player.isReferee(): referees[player.getJerseyNumber()] = player
                else: unknowns[player.getJerseyNumber()] = player

        teams = Teams(Team("home", home_team_players), Team("away", away_team_players),
                     Team("referee", referees), Team("unknown", unknowns))
        return teams


    def getLoadedPassesFor(self, teams):
        all_defined_passes = []
        with open(self.file_name) as fname:
            fname.readline()
            snapshot_data= csv.reader(fname, delimiter="\t")
            for line in snapshot_data:
                object_type, object_id, team_name, jersey_number, current_x, current_y, next_x, next_y, speed, pass_to = \
                    int(line[0]), int(line[1]), line[2], int(line[3]), float(line[4]), float(line[5]), float(line[6]), \
                    float(line[7]), float(line[8]), line[9]
                defined_passes = self.getLoadedPassPerPlayer(teams, object_id, pass_to)
                all_defined_passes.extend(defined_passes)
        return all_defined_passes


    def getLoadedPassPerPlayer(self, teams, object_id, passTo):
        defined_passes = []
        if passTo != "None":
            p1, p2_s = None, []
            passTo = [int(pto) for pto in passTo.split("@")]
            for id_to in passTo:
                for team in (teams.home_team, teams.away_team, teams.referees, teams.unknowns):
                    for player in team.getTeamPlayers():
                        if p1 == None:
                            if player.getObjectID() == object_id:
                                p1 = player
                        if player.getObjectID() == id_to:
                            p2_s.append(player)
            for p2 in p2_s:
                pass_event = PassEvent(p1, p2, None)
                defined_passes.append(pass_event)
        return defined_passes


    def __str__(self):
        pass
