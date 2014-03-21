from Tkconstants import INSERT, END
from src.sentio.Pass import Pass

__author__ = 'doktoray'

from matplotlib import pylab as p
from matplotlib.text import Text

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
        self.cidrelease = self.figure.canvas.mpl_connect('button_release_event', self.on_release_event)

    def set_passDisplayer(self, passDisplayer):
        self.passDisplayer = passDisplayer

    def on_pick_event(self, event):
        " Store which text object was picked and were the pick event occurs."
        if isinstance(event.artist, Text):
            if self.dragged != None:
                self.dragged2 = event.artist
                #xBall, yBall = self.dragged2.get_position()
                #previous_xBall, previous_yBall = self.dragged.get_position()
                passAnnotation = self.ax.annotate('', xy=(.5, .5), xycoords=(self.dragged2), ha="center", va="center",
                    xytext=(.5, .5), textcoords=(self.dragged), size=20, arrowprops=dict(patchA=self.dragged.get_bbox_patch(),
                    patchB=self.dragged2.get_bbox_patch(), arrowstyle="fancy", fc="0.6", ec="none",
                    connectionstyle="arc3"))
                self.definedPasses.append(passAnnotation)
            else:
                self.dragged = event.artist
        else:
            self.dragged = None
            self.dragged2 = None
            if self.passAnnotation != None:
                self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None
            self.figure.canvas.draw()

    def on_motion_event(self, event):
        if self.dragged != None:
            previous_xBall, previous_yBall = self.dragged.get_position()
            xBall, yBall = (event.xdata, event.ydata)
            if self.passAnnotation != None: self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None
            try:
                self.passAnnotation = self.ax.annotate('', xy=(xBall, yBall), xycoords='data', xytext=(previous_xBall, previous_yBall),
                    textcoords='data', size=20, arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                                                connectionstyle="arc3"))
                self.figure.canvas.draw()
            except TypeError:
                pass

    def displayDefinedPasses(self):
        print self.definedPasses
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

    def on_release_event(self, event):
        if self.passAnnotation != None: self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None
        if self.dragged2 != None:
            passAnnotation = self.ax.annotate('', xy=(.5, .5), xycoords=(self.dragged2), ha="center", va="center",
                        xytext=(.5, .5), textcoords=(self.dragged), size=20, arrowprops=dict(patchA=self.dragged.get_bbox_patch(),
                        patchB=self.dragged2.get_bbox_patch(), arrowstyle="fancy", fc="0.6", ec="none",
                        connectionstyle="arc3"))
            self.definedPasses[-1].remove(); del self.definedPasses[-1]
            self.definedPasses.append(passAnnotation)

            self.displayDefinedPasses()

            self.dragged = None
            self.dragged2 = None

        self.figure.canvas.draw()

    def disconnect(self):
        try:
            self.figure.canvas.mpl_disconnect(self.cidpick)
            #self.figure.canvas.mpl_disconnect(self.cidmotion)
            self.figure.canvas.mpl_disconnect(self.cidrelease)
        except AttributeError:
            pass

