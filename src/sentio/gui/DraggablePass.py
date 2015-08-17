import numpy
from matplotlib import pylab as p
from matplotlib.text import Text
import wx
from src.sentio import Parameters

from src.sentio.Parameters import *
from src.sentio.file_io.reader import ReaderBase
from src.sentio.gui import Dialogs
from src.sentio.gui.HeatMap import HeatMap
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.object.PassEvent import PassEvent
from src.sentio.file_io import Parser
from src.sentio.pass_evaluate.Pass import Pass


__author__ = 'emrullah'


class DraggablePass(Pass):

    def __init__(self, ax, draggable_visual_teams, figure=None):
        Pass.__init__(self)
        if figure is None: figure = p.gcf()
        self.pass_source = None
        self.pass_target = None
        self.pass_event = None
        self.passes_defined = []
        self.ax = ax
        self.figure = figure
        self.heatMap = HeatMap(ax, draggable_visual_teams, figure)
        self.effectiveness_withComp_byTime = None
        self.risk_range = RiskRange(self.ax)
        self.draggable_visual_teams = draggable_visual_teams


    def set_defined_passes(self, passes):
        self.passes_defined = passes


    def connect(self):
        self.cidpick = self.figure.canvas.mpl_connect("pick_event", self.on_pick_event)
        self.cidmotion = self.figure.canvas.mpl_connect("motion_notify_event", self.on_motion_event)
        self.cidpress = self.figure.canvas.mpl_connect('button_press_event', self.on_press_event)
        self.cidrelease = self.figure.canvas.mpl_connect('button_release_event', self.on_release_event)


    def set_passDisplayer(self, logger):
        self.logger = logger


    def set_variables(self, heatMap, resolution, components):
        self.chosenHeatMap = heatMap
        self.chosenResolution = resolution
        self.chosenComponent = components

        self.chosenComponent.Bind(wx.EVT_COMBOBOX, self.draw_withChosenComponent)


    def resolutionToNumberOfPoints(self):
        chosenResolution = self.chosenResolution.GetValue()
        q = {1:(11,7), 2:(21,13), 3:(35,22), 4:(105,65), 5:(210,130)}
        """
        5 ---> 0.5m
        4 --> 1m
        3 -> 3m
        2 --> 5m
        1 --> 10m
        """
        return q[chosenResolution]


    def draw_withChosenComponent(self, *args):
        chosenComponent = self.chosenComponent.GetSelection()
        if chosenComponent == 0: q = self.effectiveness_withComp["overallRisk"]
        elif chosenComponent == 1: q = self.effectiveness_withComp["gain"]
        elif chosenComponent == 2: q = self.effectiveness_withComp["passAdvantage"]
        elif chosenComponent == 3: q = self.effectiveness_withComp["goalChance"]
        else: q = self.effectiveness_withComp["effectiveness"]
        return self.heatMap.draw(q)


    def isHeatMapChosen(self):
        chosen_heat_map = self.chosenHeatMap.GetSelection()
        if chosen_heat_map not in (1,2,3):
            self.heatMap.clear()
            return False
        return True


    def drawHeatMapFor(self, pass_event):
        chosen_heat_map = self.chosenHeatMap.GetSelection()
        self.chosenComponent.SetSelection(4)

        p1 = pass_event.pass_source.player
        p2 = pass_event.pass_target.player

        self.heatMap.totalEffectiveness_withComponents_byCoordinates = {}
        if chosen_heat_map == 1:
            chosenNumber = Dialogs.ask(message='Enter the jersey number of a player from the opponent team')
            print chosenNumber

            if chosenNumber is not None:
                chosenNumber = int(chosenNumber)
                app = wx.App()
                self.effectiveness_withComp = self.heatMap.draw_defencePositionTaking((p1,p2), chosenNumber,
                                                           number_of_points=self.resolutionToNumberOfPoints())
                app.MainLoop()
        elif chosen_heat_map == 2:
            self.effectiveness_withComp = self.heatMap.draw_positionOfTargetOfPass((p1,p2),
                                                            number_of_points=self.resolutionToNumberOfPoints())
        elif chosen_heat_map == 3:
            self.effectiveness_withComp = self.heatMap.draw_positionOfSourceOfPass((p1,p2),
                                                            number_of_points=self.resolutionToNumberOfPoints())


    def on_pick_event(self, event):
        if isinstance(event.artist, Text):
            if self.pass_source is not None:

                self.pass_target = event.artist
                if self.pass_source != self.pass_target:
                    self.pass_event.xy = (.5,.5)
                    self.pass_event.xycoords = self.pass_target

                    current_pass_event = PassEvent(self.pass_event.textcoords, self.pass_event.xycoords,
                                                   ReaderBase.convertDraggableToTeams(self.draggable_visual_teams))
                    if Parameters.IS_DEBUG_MODE_ON:
                        self.risk_range.drawRangeFor(current_pass_event)
                    self.displayDefinedPass(current_pass_event, self.logger, draggable=False, visual=True)
                    if self.isHeatMapChosen():
                        self.drawHeatMapFor(current_pass_event)
                    self.passes_defined.append(current_pass_event)
                else:
                    self.pass_target = None
            else:
                self.pass_source = event.artist
                xBall, yBall = (event.mouseevent.xdata, event.mouseevent.ydata)

                self.pass_event = self.ax.annotate('', xy=(xBall, yBall), xytext=(.5,.5), picker=True,
                        textcoords=(self.pass_source), size=20, arrowprops=dict(patchA=self.pass_source.get_bbox_patch(),
                        arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))

            self.figure.canvas.draw()


    def on_motion_event(self, event):
        if self.pass_source is not None and self.pass_target is None:
            xBall, yBall = (event.xdata, event.ydata)
            try:
                self.pass_event.xy = (xBall, yBall)
                self.figure.canvas.draw()
            except TypeError:
                pass


    def on_press_event(self, event):
        if event.button == 3:
            if self.heatMap.totalEffectiveness_withComponents_byCoordinates != {}:
                x_points, y_points = self.resolutionToNumberOfPoints()
                x_coords = numpy.linspace(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X, x_points)
                y_coords = numpy.linspace(FOOTBALL_FIELD_MIN_Y, FOOTBALL_FIELD_MAX_Y, y_points)
                givenCoordinate_x, givenCoordinate_y = event.xdata, event.ydata
                coord_x = min(x_coords, key=lambda x:abs(x-givenCoordinate_x))
                coord_y = min(y_coords, key=lambda y:abs(y-givenCoordinate_y))
                components = self.heatMap.get_totalEffectiveness_withComponents_byCoordinates(coord_x, coord_y)
                Pass.display_effectiveness((coord_x, coord_y), components, self.logger)


    def on_release_event(self, event):
        if self.pass_source is not None and self.pass_target is not None:
            self.pass_source, self.pass_target, self.pass_event = None, None, None


    def disconnect(self):
        try:
            self.figure.canvas.mpl_disconnect(self.cidpick)
            #self.figure.canvas.mpl_disconnect(self.cidmotion)
            self.figure.canvas.mpl_disconnect(self.cidpress)
        except AttributeError:
            pass

