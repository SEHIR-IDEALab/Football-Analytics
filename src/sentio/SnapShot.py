import csv
import tkFileDialog
from src.sentio.Pass import Pass
from src.sentio.Player_base import Player_base

__author__ = 'emrullah'


class SnapShot:

    def __init__(self):
        pass


    def getAllObjects(self, list_of_objects):
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = {}, {}, {}, {}
        for player in Player_base.convertTextsToPlayers(list_of_objects):
            q = player.getObjectType()
            if q in [0,3]: homeTeamPlayers[player.getJerseyNumber()] = player
            elif q in [1,4]: awayTeamPlayers[player.getJerseyNumber()] = player
            elif q in [2,6,7,8,9]: referees[player.getJerseyNumber()] = player
            else: unknownObjects[player.getJerseyNumber()] = player
        return (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)


    def saveSnapShot(self, team_names, all_objects, defined_passes, directions, speeds):
        fileName = tkFileDialog.asksaveasfilename(initialfile=("%s_%s"%team_names), initialdir="../../SampleScenarios")
        if fileName:
            a = list()
            a.extend(["object_type", "object_ID", "team_name", "jersey_no", "x1", "y1", "x2", "y2", "speed", "passTo"])
            homeTeam, awayTeam = team_names
            name_of_file = "%s.csv" %(fileName)
            out = csv.writer(open(name_of_file,"a"), delimiter='\t', quoting=csv.QUOTE_NONE)
            out.writerow(a)
            del a[:]
            homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getAllObjects(all_objects)
            for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for js in team:
                    player = team[js]
                    teamName = (homeTeam if index == 0 else (awayTeam if index == 1
                                                             else ("referee" if index == 2 else "unknownObject")))
                    nextX, nextY = directions[index][js].getPositionX()[1], directions[index][js].getPositionY()[1]
                    speed = speeds[index][js]
                    js2 = ""
                    for i in defined_passes:
                        p1 = i.textcoords
                        x1, y1 = p1.get_position()
                        js1 = p1.get_text()
                        if player.getPositionX()==x1 and player.getPositionY()==y1 and player.getJerseyNumber()==int(js1):
                            p2 = i.xycoords
                            js2 += p2.get_text() + "@"
                    passTo = ("None" if js2=="" else js2[:-1])
                    a.extend([player.getObjectType(), player.getObjectID(), teamName, player.getJerseyNumber(),
                              player.getPositionX(), player.getPositionY(), nextX, nextY, speed, passTo])
                    out.writerow(a)
                    del a[:]


    def loadSnapShot(self, filename, ax):
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = dict(),dict(),dict(),dict()
        list_of_directions = []
        with open(filename) as fname:
            fname.readline()
            snapshot_data= csv.reader(fname, delimiter="\t")
            for line in snapshot_data:
                object_type, object_ID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = line
                object_type, object_ID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = \
                    int(object_type), int(object_ID), teamName, int(jersey_number), float(currentX), float(currentY), \
                    float(nextX), float(nextY), float(speed), passTo

                lengthX = (nextX - currentX) * speed
                nextX = lengthX + currentX

                lengthY = (nextY - currentY) * speed
                nextY = lengthY + currentY

                default_arrow_size = 2
                if lengthX >= 0: nextX += default_arrow_size
                else: nextX -= default_arrow_size
                if lengthY >= 0: nextY += default_arrow_size
                else: nextY -= default_arrow_size

                directionAnnotation = ax.annotate('', xy=(nextX,nextY), xycoords='data', xytext=(currentX,currentY),
                                            textcoords='data',size=20, va="center", ha="center",zorder=2, arrowprops=dict(
                                            arrowstyle="simple", connectionstyle="arc3",fc="cyan", ec="b", lw=2))
                list_of_directions.append(directionAnnotation)

                player = Player_base([object_type, object_ID, jersey_number, currentX, currentY])
                q = player.getObjectType()
                if q in [0,3]: homeTeamPlayers[player.getJerseyNumber()] = player
                elif q in [1,4]: awayTeamPlayers[player.getJerseyNumber()] = player
                elif q in [2,6,7,8,9]: referees[player.getJerseyNumber()] = player
                else: unknownObjects[player.getJerseyNumber()] = player

        return (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects), list_of_directions


    def displayAllPasses(self, filename, ax, list_of_objects, pass_display):
        all_defined_passes = []
        drag_pass = Pass(list_of_objects)
        with open(filename) as fname:
            fname.readline()
            snapshot_data= csv.reader(fname, delimiter="\t")
            for line in snapshot_data:
                object_type, object_ID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = line
                object_type, object_ID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = \
                    int(object_type), int(object_ID), teamName, int(jersey_number), float(currentX), float(currentY), \
                    float(nextX), float(nextY), float(speed), passTo
                defined_passes = self.displayPasses_perPlayer(list_of_objects, ax, drag_pass, pass_display,
                                                              passTo, currentX, currentY, jersey_number, object_type)
                all_defined_passes.extend(defined_passes)
        return all_defined_passes


    def displayPasses_perPlayer(self, list_of_objects, ax, drag_pass, pass_display,
                                passTo, currentX, currentY, jersey_number, object_type):
        defined_passes = []
        if passTo != "None":
            p1, p2_s = None, []
            passTo = [pto for pto in passTo.split("@")]
            for jsTo in passTo:
                for player in list_of_objects:
                    player = player.point
                    player_x, player_y = player.get_position()
                    if p1 == None:
                        if currentX==player_x and currentY==player_y and player.jersey_number==jersey_number:
                            p1 = player
                    if player.jersey_number==int(jsTo):
                        p2_s.append(player)
            for p2 in p2_s:
                passAnnotation = ax.annotate('', xy=(.5, .5), xycoords=(p2), ha="center", va="center",
                    xytext=(.5, .5), textcoords=(p1), size=20, arrowprops=dict(patchA=p1.get_bbox_patch(),
                    patchB=p2.get_bbox_patch(), arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))
                defined_passes.append(passAnnotation)
                drag_pass.displayDefinedPass(passAnnotation, pass_display)
        return defined_passes


    def __str__(self):
        pass
