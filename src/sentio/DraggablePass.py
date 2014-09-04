import numpy
from src.sentio import Dialogs
from src.sentio.HeatMap import HeatMap
from src.sentio.Parameters import *
from src.sentio.Pass import Pass
from matplotlib import pylab as p
from matplotlib.text import Text
from src.sentio.Player_base import Player_base
import wx

__author__ = 'emrullah'


class DraggablePass(Pass):

    def __init__(self, ax, coordinateDataOfObjects, figure=None):
        Pass.__init__(self, coordinateDataOfObjects)
        if figure is None: figure = p.gcf()
        self.dragged = None
        self.dragged2 = None
        self.passAnnotation = None
        self.definedPasses = []
        self.ax = ax
        self.figure = figure
        self.heatMap = HeatMap(ax, coordinateDataOfObjects, figure)

        self.effectiveness_withComp_byTime = None


    def set_defined_passes(self, passes):
        self.definedPasses = passes


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


    def draw_heatMapChosen(self):
        chosenHeatMap = self.chosenHeatMap.GetSelection()
        self.chosenComponent.SetSelection(4)

        p1 = self.passAnnotation.textcoords
        p2 = self.passAnnotation.xycoords
        object_type1, object_id1, js1, (x1, y1) = p1.object_type, p1.object_id, p1.get_text(), p1.get_position()
        object_type2, object_id2, js2, (x2, y2) = p2.object_type, p2.object_id, p2.get_text(), p2.get_position()

        p1 = Player_base([object_type1, object_id1,js1, x1, y1])
        p2 = Player_base([object_type2, object_id2,js2, x2, y2])

        self.heatMap.totalEffectiveness_withComponents_byCoordinates = {}
        if chosenHeatMap == 1:
            chosenNumber = Dialogs.ask(message='Enter the jersey number of a player from the opponent team')
            print chosenNumber

            if chosenNumber is not None:
                chosenNumber = int(chosenNumber)
                app = wx.App()
                self.effectiveness_withComp = self.heatMap.draw_defencePositionTaking((p1,p2), chosenNumber,
                                                           number_of_points=self.resolutionToNumberOfPoints())
                app.MainLoop()
        elif chosenHeatMap == 2:
            self.effectiveness_withComp = self.heatMap.draw_positionOfTargetOfPass((p1,p2),
                                                            number_of_points=self.resolutionToNumberOfPoints())
        elif chosenHeatMap == 3:
            self.effectiveness_withComp = self.heatMap.draw_positionOfSourceOfPass((p1,p2),
                                                            number_of_points=self.resolutionToNumberOfPoints())
        else:
            self.heatMap.clear()


    def on_pick_event(self, event):
        if isinstance(event.artist, Text):
            if self.dragged != None:

                self.dragged2 = event.artist
                if self.dragged != self.dragged2:
                    self.passAnnotation.xy = (.5,.5)
                    self.passAnnotation.xycoords = self.dragged2

                    self.definedPasses.append(self.passAnnotation)
                    self.displayDefinedPasses()

                    self.draw_heatMapChosen()
                else:
                    self.dragged2 = None
            else:
                self.dragged = event.artist
                xBall, yBall = (event.mouseevent.xdata, event.mouseevent.ydata)

                self.passAnnotation = self.ax.annotate('', xy=(xBall, yBall), xytext=(.5,.5), picker=True,
                        textcoords=(self.dragged), size=20, arrowprops=dict(patchA=self.dragged.get_bbox_patch(),
                        arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))

            self.figure.canvas.draw()


    def on_motion_event(self, event):
        if self.dragged is not None and self.dragged2 is None:
            xBall, yBall = (event.xdata, event.ydata)
            try:
                self.passAnnotation.xy = (xBall, yBall)
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
        if self.dragged is not None and self.dragged2 is not None:
            self.dragged, self.dragged2, self.passAnnotation = None, None, None


    def displayDefinedPasses(self):
        self.logger.Clear()
        for dPass in self.definedPasses:
            self.displayDefinedPass(dPass, self.logger)


    def disconnect(self):
        try:
            self.figure.canvas.mpl_disconnect(self.cidpick)
            #self.figure.canvas.mpl_disconnect(self.cidmotion)
            self.figure.canvas.mpl_disconnect(self.cidpress)
        except AttributeError:
            pass

