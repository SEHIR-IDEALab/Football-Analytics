from Tkconstants import END
import numpy
from src.sentio.HeatMap import HeatMap
from src.sentio.Pass import Pass
from matplotlib import pylab as p
from matplotlib.text import Text
from src.sentio.Player_base import Player_base

__author__ = 'doktoray'


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
        self.heatMap = HeatMap(ax, coordinateDataOfObjects)

        self.effectiveness_withComp_byTime = None


    def connect(self):
        self.cidpick = self.figure.canvas.mpl_connect("pick_event", self.on_pick_event)
        self.cidmotion = self.figure.canvas.mpl_connect("motion_notify_event", self.on_motion_event)
        self.cidpress = self.figure.canvas.mpl_connect('button_press_event', self.on_press_event)


    def set_passDisplayer(self, passDisplayer):
        self.passDisplayer = passDisplayer


    def set_variables(self, heatMap, resolution, components):
        self.chosenHeatMap = heatMap
        self.chosenResolution = resolution
        self.chosenComponent = components

        self.chosenComponent.trace("w", self.draw_withChosenComponent)


    def resolutionToNumberOfPoints(self):
        chosenResolution = self.chosenResolution.get()
        q = {"10":(10,6), "5":(20,12), "4":(27,17), "3":(40,25), "2":(53,33), "1":(105,65), "0.5":(210,130)}
        return q[chosenResolution]


    def draw_withChosenComponent(self, *args):
        chosenComponent = self.chosenComponent.get()
        print chosenComponent
        if chosenComponent == "effectiveness":
            q = self.effectiveness_withComp["effectiveness"]
            return self.heatMap.draw(q, self.figure.canvas)
        elif chosenComponent == "gain":
            q = self.effectiveness_withComp["gain"]
            return self.heatMap.draw(q, self.figure.canvas)
        elif chosenComponent == "pass advantage":
            q = self.effectiveness_withComp["passAdvantage"]
            return self.heatMap.draw(q, self.figure.canvas)
        elif chosenComponent == "goal chance":
            q = self.effectiveness_withComp["goalChance"]
            return self.heatMap.draw(q, self.figure.canvas)
        elif chosenComponent == "overall risk":
            q = self.effectiveness_withComp["overallRisk"]
            return self.heatMap.draw(q, self.figure.canvas)


    def draw_heatMapChosen(self):
        self.heatMap.remove()
        chosenHeatMap = self.chosenHeatMap.get()

        p1 = self.passAnnotation.textcoords
        p2 = self.passAnnotation.xycoords
        object_type1, object_id1, js1, (x1, y1) = p1.object_type, p1.object_id, p1.get_text(), p1.get_position()
        object_type2, object_id2, js2, (x2, y2) = p2.object_type, p2.object_id, p2.get_text(), p2.get_position()

        p1 = Player_base([object_type1, object_id1,js1, x1, y1])
        p2 = Player_base([object_type2, object_id2,js2, x2, y2])

        if chosenHeatMap == "defence position taking":
            self.effectiveness_withComp = self.heatMap.draw_defencePositionTaking((p1,p2), 16,
                                                           number_of_points=self.resolutionToNumberOfPoints())
        elif chosenHeatMap == "position of target of pass":
            self.effectiveness_withComp = self.heatMap.draw_positionOfTargetOfPass((p1,p2),
                                                            number_of_points=self.resolutionToNumberOfPoints())
        elif chosenHeatMap == "position of source of pass":
            self.effectiveness_withComp = self.heatMap.draw_positionOfSourceOfPass((p1,p2),
                                                            number_of_points=self.resolutionToNumberOfPoints())


    def on_pick_event(self, event):
        if isinstance(event.artist, Text):
            if self.dragged != None:
                self.dragged2 = event.artist

                self.passAnnotation.xy = (.5,.5)
                self.passAnnotation.xycoords = self.dragged2
                self.passAnnotation.arrowprops["patchB"] = self.dragged2.get_bbox_patch()

                self.draw_heatMapChosen()

                self.figure.canvas.draw()
                self.definedPasses.append(self.passAnnotation)
                self.displayDefinedPasses()

                self.dragged, self.dragged2, self.passAnnotation = None, None, None
            else:
                self.dragged = event.artist
                xBall, yBall = (event.mouseevent.xdata, event.mouseevent.ydata)

                self.passAnnotation = self.ax.annotate('', xy=(xBall, yBall), xycoords='data', xytext=(.5,.5), va="center",
                    ha="center", picker=True, textcoords=(self.dragged), size=20, arrowprops=dict(
                        patchA=self.dragged.get_bbox_patch(), arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))

                self.figure.canvas.draw()


    def on_motion_event(self, event):
        if self.dragged != None:
            xBall, yBall = (event.xdata, event.ydata)
            try:
                self.passAnnotation.xy = (xBall, yBall)
                self.figure.canvas.draw()
            except TypeError:
                pass


    def on_press_event(self, event):
        if event.button == 3:
            x_points, y_points = self.resolutionToNumberOfPoints()
            x_coords = numpy.linspace(0, 105, x_points)
            y_coords = numpy.linspace(0, 65, y_points)
            givenCoordinate_x, givenCoordinate_y = event.xdata, event.ydata
            coord_x = min(x_coords, key=lambda x:abs(x-givenCoordinate_x))
            coord_y = min(y_coords, key=lambda y:abs(y-givenCoordinate_y))
            print self.heatMap.get_totalEffectiveness_withComponents_byCoordinates(coord_x, coord_y)


    def displayDefinedPasses(self):
        self.passDisplayer.delete("1.0", END)
        for dPass in self.definedPasses:
            self.displayDefinedPass(dPass, self.passDisplayer)


    def disconnect(self):
        try:
            self.figure.canvas.mpl_disconnect(self.cidpick)
            #self.figure.canvas.mpl_disconnect(self.cidmotion)
        except AttributeError:
            pass

