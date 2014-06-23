import numpy
from src.sentio.Pass import Pass
from src.sentio.Player_base import Player_base
import matplotlib.pyplot as plt

__author__ = 'emrullah'

class HeatMap:
    def __init__(self, ax, coordOfObjects):
        self.ax = ax
        self.hm = None
        self.cbar = None
        self.allObjects = self.convertTextsToPlayers(coordOfObjects)
        self.clt_pass = Pass()

        self.totalEffectiveness_withComponents_byCoordinates = {}


    def get_totalEffectiveness_withComponents_byCoordinates(self, x, y):
        return self.totalEffectiveness_withComponents_byCoordinates[(x,y)]


    def convertTextsToPlayers(self, coordinateDataOfObjects):
        if coordinateDataOfObjects == None: return None
        q = []
        for p in coordinateDataOfObjects:
            p = p.point
            object_type, object_id, js, (x, y) = p.object_type, p.object_id, p.get_text(), p.get_position()
            player_base = Player_base([object_type, object_id, js, x, y])
            q.append(player_base)
        return q


    def remove(self):
        if self.hm != None:
            self.hm.remove()
        self.totalEffectiveness_withComponents_byCoordinates = {}


    def draw(self, givenComponent, canvas):
        q = givenComponent
        self.hm = self.ax.imshow(q, interpolation='bilinear',aspect="auto",
                                 extent=[-5.0, 110.0, 65.0, 0], vmax=12, alpha=0.8)
        self.ax.set_xlim(-5.0, 110.0)
        self.ax.set_ylim(0, 65.0)
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 115, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))
        canvas.draw()


    def heatmap_base(self, definedPass, p_accordingTo, number_of_points):
        p1, p2 = definedPass
        p_initial_pos = p_accordingTo.get_position()

        x_points, y_points = number_of_points
        x_coord = numpy.linspace(0, 105, x_points)
        y_coord = numpy.linspace(0, 65, y_points)

        totalEffectiveness_withComponents = {"effectiveness":[], "gain":[], "passAdvantage":[], "goalChance":[], "overallRisk":[]}
        for y in y_coord:
            temp_effect, temp_gain, temp_passAdv, temp_goalChange, temp_overRisk = [], [], [], [], []
            for x in x_coord:
                p_accordingTo.set_position((x,y))
                self.clt_pass.coordinateDataOfObjects = self.allObjects
                currentEffectiveness_withComponents = self.clt_pass.effectiveness_withComponents(p1, p2)
                self.totalEffectiveness_withComponents_byCoordinates[(x,y)] = currentEffectiveness_withComponents
                #(effectiveness, gain, passAdvantage, goalChance) = currentEffectiveness_withComponents
                for index, component in enumerate([temp_effect, temp_gain, temp_passAdv, temp_goalChange, temp_overRisk]):
                    component.append(currentEffectiveness_withComponents[index])
                #print x,y
            totalEffectiveness_withComponents["effectiveness"].append(temp_effect)
            totalEffectiveness_withComponents["gain"].append(temp_gain)
            totalEffectiveness_withComponents["passAdvantage"].append(temp_passAdv)
            totalEffectiveness_withComponents["goalChance"].append(temp_goalChange)
            totalEffectiveness_withComponents["overallRisk"].append(temp_goalChange)

        p_accordingTo.set_position(p_initial_pos)
        q = totalEffectiveness_withComponents["effectiveness"]
        self.hm = self.ax.imshow(q, interpolation='bilinear',aspect="auto", extent=[-5.0, 110.0, 65.0, 0], vmax=12, alpha=0.8)
        if self.cbar == None: self.cbar = plt.colorbar(self.hm)
        self.ax.set_xlim(-5.0, 110.0)
        self.ax.set_ylim(0, 65.0)
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 115, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))
        return totalEffectiveness_withComponents


    def draw_defencePositionTaking(self, definedPass, chosenObject, number_of_points=(105,65)):
        p1, p2 = definedPass
        p_chosen = None

        p1_team = p1.getTypeName()
        for obj in self.allObjects:
            temp_obj_js = obj.getJerseyNumber()
            temp_obj_team = obj.getTypeName()
            if (temp_obj_js == chosenObject) and (temp_obj_team not in [p1_team, "referee", "unknown"]):
                p_chosen = obj

        return self.heatmap_base(definedPass, p_chosen, number_of_points)


    def draw_positionOfTargetOfPass(self, definedPass, number_of_points=(105,65)):
        p1, p2 = definedPass
        return self.heatmap_base(definedPass, p2, number_of_points)


    def draw_positionOfSourceOfPass(self, definedPass, number_of_points=(105,65)):
        p1, p2 = definedPass
        return self.heatmap_base(definedPass, p1, number_of_points)


    def __str__(self):
        pass
