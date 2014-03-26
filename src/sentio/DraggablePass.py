from Tkconstants import INSERT, END
from src.sentio.Pass import Pass

__author__ = 'doktoray'

from matplotlib import pylab as p
from matplotlib.text import Text, Annotation

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

                self.figure.canvas.draw()
                self.definedPasses.append(self.passAnnotation)
                self.displayDefinedPasses()

                self.dragged, self.dragged2, self.passAnnotation = None, None, None
            else:
                self.dragged = event.artist
                xBall, yBall = (event.mouseevent.xdata, event.mouseevent.ydata)

                self.passAnnotation = self.ax.annotate('', xy=(xBall, yBall), xycoords='data', xytext=(.5,.5), va="center",
                    ha="center", textcoords=(self.dragged), size=20, arrowprops=dict(patchA = self.dragged.get_bbox_patch(),
                        arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))

                self.figure.canvas.draw()
        if isinstance(event.artist, Annotation):
            print "adasdasd"

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
        for i in self.definedPasses:
            p1 = i.textcoords
            p2 = i.xycoords

            self.passDisplayer.insert(INSERT, "\n%s --> %s" %(p1.get_text(), p2.get_text()))
            self.passDisplayer.insert(END, "\noverall_risk = %s" %self.overallRisk(p1, p2))
            self.passDisplayer.insert(END, "\ngain = %s" %self.gain(p1, p2))
            self.passDisplayer.insert(END, "\npass_advantage = %s (%s)" %self.passAdvantage(p2))
            self.passDisplayer.insert(END, "\neffectiveness = %s" %self.effectiveness(p1, p2))
            self.passDisplayer.insert(END, "\ngoal_chance = %s\n" %self.goalChance(p2))

    def disconnect(self):
        try:
            self.figure.canvas.mpl_disconnect(self.cidpick)
            #self.figure.canvas.mpl_disconnect(self.cidmotion)
        except AttributeError:
            pass

