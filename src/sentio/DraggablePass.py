from Tkconstants import END
from src.sentio.HeatMap import HeatMap
from src.sentio.Pass import Pass
from matplotlib import pylab as p
from matplotlib.text import Text

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
        self.heatMap = HeatMap(self.ax)


    def connect(self):
        self.cidpick = self.figure.canvas.mpl_connect("pick_event", self.on_pick_event)
        self.cidmotion = self.figure.canvas.mpl_connect("motion_notify_event", self.on_motion_event)


    def set_passDisplayer(self, passDisplayer):
        self.passDisplayer = passDisplayer


    def on_pick_event(self, event):
        if isinstance(event.artist, Text):
            if self.dragged != None:
                self.dragged2 = event.artist

                self.passAnnotation.xy = (.5,.5)
                self.passAnnotation.xycoords = self.dragged2
                self.passAnnotation.arrowprops["patchB"] = self.dragged2.get_bbox_patch()

                self.heatMap.remove()
                self.heatMap.draw(self.passAnnotation)

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

