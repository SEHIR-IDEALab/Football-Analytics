import math

import numpy
import wx

from src.sentio.Parameters import *
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.pass_evaluate.Pass import Pass


__author__ = 'emrullah'


class HeatMap:
    def __init__(self, ax, draggable_visual_teams, figure=None):
        self.draggable_visual_teams = draggable_visual_teams
        self.ax = ax
        self.hm = None
        self.cbar = None
        self.figure = figure
        self.pass_evaluate = Pass()

        self.effectivenessByPosition = {}


    def clear(self):
        if self.hm is not None:
            self.hm.remove(); self.hm = None
            self.figure.canvas.draw()


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


    def set_color_bar(self, color_bar, color_bar_canvas):
        self.color_bar = color_bar
        self.color_bar_canvas = color_bar_canvas


    def set_color_bar_listeners(self, colorbar_listeners):
        self.vmin_auto, self.vmin_custom, self.vmin_text, \
        self.vmax_auto, self.vmax_custom, self.vmax_text, \
        self.refresh_button = colorbar_listeners

        self.refresh_button.Bind(wx.EVT_BUTTON, self.adjust_color_bar)
        self.vmax_auto.Bind(wx.EVT_RADIOBUTTON, self.on_vmax_auto)
        self.vmin_auto.Bind(wx.EVT_RADIOBUTTON, self.on_vmin_auto)


    def on_vmax_auto(self, event):
        try:
            self.vmax_text.Disable()
            print self.v_max

            self.color_bar.set_clim(vmax=self.v_max)
            self.hm.set_clim(vmax=self.v_max)
            self.color_bar.draw_all()

            self.color_bar_canvas.draw()
            self.figure.canvas.draw()
        except AttributeError:
            pass


    def on_vmin_auto(self, event):
        try:
            self.vmin_text.Disable()
            print self.v_min

            self.color_bar.set_clim(vmin=self.v_min)
            self.hm.set_clim(vmin=self.v_min)
            self.color_bar.draw_all()

            self.color_bar_canvas.draw()
            self.figure.canvas.draw()
        except AttributeError:
            pass


    def refresh_colorbar_setup(self):
        self.vmin_auto.SetValue(True)
        self.vmax_auto.SetValue(True)
        self.vmin_text.Disable()
        self.vmax_text.Disable()


    def adjust_color_bar(self, *args):
        if self.vmin_custom.GetValue(): vmin = self.vmin_text.GetValue()
        else: vmin = self.hm.norm.vmin
        if self.vmax_custom.GetValue(): vmax = self.vmax_text.GetValue()
        else: vmax = self.hm.norm.vmax

        self.color_bar.set_clim(vmin=vmin, vmax=vmax)
        self.hm.set_clim(vmin=vmin, vmax=vmax)
        self.color_bar.draw_all()

        self.color_bar_canvas.draw()
        self.figure.canvas.draw()


    def adjust_heatMap(self, data):
        mean, standard_deviation = HeatMap.compute_standard_deviation(data)
        self.v_min = mean - 3*standard_deviation
        self.v_max = mean + 3*standard_deviation
        print self.v_min, self.v_max
        if self.hm is not None:
            self.hm.set_data(data)
            self.hm.set_clim(vmin=self.v_min, vmax=self.v_max)
        else:
            self.hm = self.ax.imshow(data, interpolation='bilinear', vmin=self.v_min, vmax=self.v_max, alpha=0.8,
                                     extent=[FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X,
                                             FOOTBALL_FIELD_MAX_Y, FOOTBALL_FIELD_MIN_Y])

        self.color_bar.set_clim(vmin=self.v_min, vmax=self.v_max)
        self.color_bar.draw_all()
        self.color_bar_canvas.draw()
        self.figure.canvas.draw()

        self.refresh_colorbar_setup()


    def draw(self, data):
        self.adjust_heatMap(data)


    def evaluate(self, definedPass, p_accordingTo, resolution):
        p1 = definedPass.pass_source
        p2 = definedPass.pass_target

        x_coord = numpy.linspace(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X, resolution[0])
        y_coord = numpy.linspace(FOOTBALL_FIELD_MIN_Y, FOOTBALL_FIELD_MAX_Y, resolution[1])

        self.effectivenessByComponent = {"overallRisk": [], "gain": [], "passAdvantage": [],
                                    "goalChance": [],"effectiveness": []}

        self.pass_evaluate.teams = ReaderBase.divideIntoTeams(self.draggable_visual_teams.values(), visual=True)

        for y in y_coord:
            temp_overRisk, temp_gain, temp_passAdv, temp_goalChange, temp_effect = [], [], [], [], []
            for x in x_coord:
                p_accordingTo.set_position((x, y))
                if p_accordingTo.object_id == p1.object_id:
                    currentEffectiveness_withComponents = self.pass_evaluate.effectiveness_withComponents(p_accordingTo, p2)
                elif p_accordingTo.object_id == p2.object_id:
                    currentEffectiveness_withComponents = self.pass_evaluate.effectiveness_withComponents(p1, p_accordingTo)
                else:
                    currentEffectiveness_withComponents = self.pass_evaluate.effectiveness_withComponents(p1, p2)
                self.effectivenessByPosition[(x, y)] = currentEffectiveness_withComponents
                for index, component in enumerate(
                        [temp_overRisk, temp_gain, temp_passAdv, temp_goalChange, temp_effect]):
                    component.append(currentEffectiveness_withComponents[index])
                    # print x,y
            self.effectivenessByComponent["overallRisk"].append(temp_overRisk)
            self.effectivenessByComponent["gain"].append(temp_gain)
            self.effectivenessByComponent["passAdvantage"].append(temp_passAdv)
            self.effectivenessByComponent["goalChance"].append(temp_goalChange)
            self.effectivenessByComponent["effectiveness"].append(temp_effect)

        self.draw(self.effectivenessByComponent["overallRisk"])


    def draw_defencePositionTaking(self, definedPass, chosen_js, number_of_points=(105, 65)):
        teams = ReaderBase.divideIntoTeams(self.draggable_visual_teams, visual=True)
        if definedPass.pass_source.isHomeTeamPlayer(): opponent_team = teams.away_team
        else: opponent_team = teams.home_team

        p_chosen = opponent_team.getTeamPlayersWithJS().get(chosen_js)
        return self.evaluate(definedPass, p_chosen, number_of_points)


    def draw_positionOfTargetOfPass(self, definedPass, number_of_points=(105, 65)):
        return self.evaluate(definedPass, definedPass.pass_target, number_of_points)


    def draw_positionOfSourceOfPass(self, definedPass, number_of_points=(105, 65)):
        return self.evaluate(definedPass, definedPass.pass_source, number_of_points)


    def __str__(self):
        pass
