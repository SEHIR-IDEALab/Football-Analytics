import math
import numpy
import wx
from src.sentio.Pass import Pass
import matplotlib.pyplot as plt
from src.sentio.Player_base import Player_base

__author__ = 'emrullah'


class HeatMap:
    def __init__(self, ax, coordOfObjects, figure=None):
        self.allObjects = coordOfObjects
        self.ax = ax
        self.hm = None
        self.cbar = None
        self.figure = figure
        self.clt_pass = Pass()

        self.totalEffectiveness_withComponents_byCoordinates = {}


    def get_totalEffectiveness_withComponents_byCoordinates(self, x, y):
        return self.totalEffectiveness_withComponents_byCoordinates[(x, y)]


    def remove(self):
        self.totalEffectiveness_withComponents_byCoordinates = {}


    @staticmethod
    def compute_mean(data):
        total_value = 0.0
        total_length = 0.0
        for value_list in data:
            total_length += len(value_list)
            for value in value_list:
                total_value += value
        return total_value / total_length


    @staticmethod
    def compute_standard_deviation(data):
        mean = HeatMap.compute_mean(data)
        total = 0.0
        total_length = 0.0
        for value_list in data:
            total_length += len(value_list)
            for value in value_list:
                total += math.pow((value - mean), 2)
        variance = total / (total_length - 1)
        standard_deviation = math.sqrt(variance)
        return mean, standard_deviation


    def set_color_bar_listeners(self, (vmin_custom, vmin_text), (vmax_custom, vmax_text), refresh_button):
        self.vmin_custom = vmin_custom
        self.vmin_text = vmin_text
        self.vmax_custom = vmax_custom
        self.vmax_text = vmax_text
        self.refresh_button = refresh_button

        self.refresh_button.Bind(wx.EVT_BUTTON, self.adjust_color_bar)


    def set_color_bar(self, color_bar, color_bar_canvas):
        self.color_bar = color_bar
        self.color_bar_canvas = color_bar_canvas


    def adjust_color_bar(self, *args):
        if self.vmin_custom.GetValue(): vmin = self.vmin_text.GetValue()
        else: vmin = self.hm.norm.vmin
        if self.vmax_custom.GetValue(): vmax = self.vmax_text.GetValue()
        else: vmax = self.hm.norm.vmax

        print vmin, vmax
        self.color_bar.set_clim(vmin=vmin, vmax=vmax)
        self.hm.set_clim(vmin=vmin, vmax=vmax)
        self.color_bar.draw_all()

        self.color_bar_canvas.draw()
        self.figure.canvas.draw()


    def adjust_heatMap(self, data):
        mean, standard_deviation = HeatMap.compute_standard_deviation(data)
        v_min = mean - 2*standard_deviation
        v_max = mean + 2*standard_deviation
        if self.hm is not None:
            self.hm.set_data(data)
        else:
            self.hm = self.ax.imshow(data, interpolation='bilinear', extent=[0.0, 105.0, 65.0, 0.0],
                                 vmin=v_min, vmax=v_max, alpha=0.8)
        self.color_bar.set_clim(vmin=v_min, vmax=v_max)
        self.color_bar.draw_all()
        self.color_bar_canvas.draw()


    def draw(self, data, canvas=None):
        self.adjust_heatMap(data)
        self.ax.set_xlim(-6.5, 111.5)
        self.ax.set_ylim(66.5, -1.5)
        if canvas is not None: canvas.draw()


    def heatmap_base(self, definedPass, p_accordingTo, number_of_points):
        p1, p2 = definedPass

        x_points, y_points = number_of_points
        x_coord = numpy.linspace(0, 105, x_points)
        y_coord = numpy.linspace(0, 65, y_points)

        totalEffectiveness_withComponents = {"effectiveness": [], "gain": [], "passAdvantage": [], "goalChance": [],
                                             "overallRisk": []}
        pass_ = Pass(self.allObjects)
        for player in pass_.allObjects:
            if player.object_id == p_accordingTo.object_id:
                p_accordingTo = player

        for y in y_coord:
            temp_effect, temp_gain, temp_passAdv, temp_goalChange, temp_overRisk = [], [], [], [], []
            for x in x_coord:
                p_accordingTo.set_position((x, y))
                if p_accordingTo.object_id == p1.object_id:
                    currentEffectiveness_withComponents = pass_.effectiveness_withComponents(p_accordingTo, p2)
                elif p_accordingTo.object_id == p2.object_id:
                    currentEffectiveness_withComponents = pass_.effectiveness_withComponents(p1, p_accordingTo)
                else:
                    currentEffectiveness_withComponents = pass_.effectiveness_withComponents(p1, p2)
                self.totalEffectiveness_withComponents_byCoordinates[(x, y)] = currentEffectiveness_withComponents
                for index, component in enumerate(
                        [temp_effect, temp_gain, temp_passAdv, temp_goalChange, temp_overRisk]):
                    component.append(currentEffectiveness_withComponents[index])
                    # print x,y
            totalEffectiveness_withComponents["effectiveness"].append(temp_effect)
            totalEffectiveness_withComponents["gain"].append(temp_gain)
            totalEffectiveness_withComponents["passAdvantage"].append(temp_passAdv)
            totalEffectiveness_withComponents["goalChance"].append(temp_goalChange)
            totalEffectiveness_withComponents["overallRisk"].append(temp_overRisk)

        data = totalEffectiveness_withComponents["effectiveness"]
        self.draw(data)
        return totalEffectiveness_withComponents


    def draw_defencePositionTaking(self, definedPass, chosenObject, number_of_points=(105, 65)):
        p1, p2 = definedPass
        p_chosen = None

        p1_team = p1.getTypeName()
        for obj in Player_base.convertTextsToPlayers(self.allObjects):
            temp_obj_js = obj.getJerseyNumber()
            temp_obj_team = obj.getTypeName()
            if (temp_obj_js == chosenObject) and (temp_obj_team not in [p1_team, "referee", "unknown"]):
                p_chosen = obj

        return self.heatmap_base(definedPass, p_chosen, number_of_points)


    def draw_positionOfTargetOfPass(self, definedPass, number_of_points=(105, 65)):
        p1, p2 = definedPass
        return self.heatmap_base(definedPass, p2, number_of_points)


    def draw_positionOfSourceOfPass(self, definedPass, number_of_points=(105, 65)):
        p1, p2 = definedPass
        return self.heatmap_base(definedPass, p1, number_of_points)


    def __str__(self):
        pass
