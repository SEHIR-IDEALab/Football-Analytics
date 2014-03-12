import math

__author__ = 'doktoray'

from matplotlib import pylab as p
from matplotlib.text import Text

class DraggablePass(object):

    def __init__(self, ax, figure=None):
        if figure is None : figure = p.gcf()
        # simple attibute to store the dragged text object
        self.dragged = None
        self.dragged2 = None
        self.passAnnotation = None

        self.definedPasses = []
        self.coordinateDataOfObjects = None

        self.ax = ax
        self.figure = figure

    def connect(self):
        self.cidpick = self.figure.canvas.mpl_connect("pick_event", self.on_pick_event)
        self.cidmotion = self.figure.canvas.mpl_connect("motion_notify_event", self.on_motion_event)
        self.cidrelease = self.figure.canvas.mpl_connect('button_release_event', self.on_release_event)

    def setCoordinateDataOfObjects(self, coordDataOfObjects):
        self.coordinateDataOfObjects = coordDataOfObjects


    def risk(self, p1, p3, p2):
        teams = {(0.0, 0.0, 1.0, 0.5):"home", (1.0, 0.0, 0.0, 0.5):"away",
                 (1.0, 1.0, 0.0, 0.5):"referee", (0.0, 0.0, 0.0, 0.5):"unknown"}

        x1, y1 = p1.get_position()
        team1 = teams[p1.get_bbox_patch().get_facecolor()]
        js1 = p1.get_text()

        x2, y2 = p2.get_position()
        team2 = teams[p2.get_bbox_patch().get_facecolor()]
        js2 = p2.get_text()

        x3, y3 = p3.get_position()
        js3 = p3.get_text()
        team3 = teams[p3.get_bbox_patch().get_facecolor()]

        risk = 0.0
        if (x1<=x3<=x2 or x2<=x3<=x1) and (y1<=y3<=y2 or y2<=y3<=y1):
            if team3 not in [team1, "referee", "unknown"]:
                slope = (y2-y1) / (x2-x1)
                a = slope
                b = -1
                c = ( ( slope * (-x1) ) + y1 )
                d2 = math.fabs(a*x3 + b*y3 + c) / math.sqrt(math.pow(a,2)+math.pow(b,2))
                hipotenus_1to3 = math.sqrt(math.pow(x3-x1,2) + math.pow(y3-y1,2))
                d1 = math.sqrt(math.pow(hipotenus_1to3,2) - math.pow(d2,2))
                risk = d1 / d2
                print js3, team3, risk
        return risk

    def overallRisk(self, definedPass):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords

        overallRisk = 0.0
        for dragged in self.coordinateDataOfObjects:
            p3 = dragged.point
            overallRisk += self.risk(p1, p3, p2)
        print overallRisk, self.gain(p1,p2)

    def gain(self, p1, p2):
        teams = {(0.0, 0.0, 1.0, 0.5):"home", (1.0, 0.0, 0.0, 0.5):"away",
                 (1.0, 1.0, 0.0, 0.5):"referee", (0.0, 0.0, 0.0, 0.5):"unknown"}

        x1, y1 = p1.get_position()
        team1 = teams[p1.get_bbox_patch().get_facecolor()]
        js1 = p1.get_text()

        x2, y2 = p2.get_position()
        team2 = teams[p2.get_bbox_patch().get_facecolor()]
        js2 = p2.get_text()

        gain = 0
        opponentTeam = []
        sameTeam = []
        for dragged in self.coordinateDataOfObjects:
            p3 = dragged.point

            x3, y3 = p3.get_position()
            js3 = p3.get_text()
            team3 = teams[p3.get_bbox_patch().get_facecolor()]

            if team3 not in [team1, "referee", "unknown"]:
                if x1<=x3<=x2 or x2<=x3<=x1:
                    gain += 1
                opponentTeam.append(x3)
            elif team3 == team1:
                sameTeam.append(x3)

        min_ultimate = min([min(opponentTeam), min(sameTeam)])
        max_ultimate = max([max(opponentTeam), max(sameTeam)])
        if (min_ultimate in sameTeam) and max_ultimate in opponentTeam:
            if x1 < x2: return gain
            else: return -gain
        else:
            if x1 < x2: return -gain
            else: return gain

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

    def on_release_event(self, event):
        if self.passAnnotation != None: self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None
        if self.dragged2 != None:
            passAnnotation = self.ax.annotate('', xy=(.5, .5), xycoords=(self.dragged2), ha="center", va="center",
                        xytext=(.5, .5), textcoords=(self.dragged), size=20, arrowprops=dict(patchA=self.dragged.get_bbox_patch(),
                        patchB=self.dragged2.get_bbox_patch(), arrowstyle="fancy", fc="0.6", ec="none",
                        connectionstyle="arc3"))
            self.definedPasses[-1].remove(); del self.definedPasses[-1]
            self.definedPasses.append(passAnnotation)

            self.dragged = None
            self.dragged2 = None

        self.figure.canvas.draw()

    def disconnect(self):
        try:
            self.figure.canvas.mpl_disconnect(self.cidpick)
            self.figure.canvas.mpl_disconnect(self.cidmotion)
            self.figure.canvas.mpl_disconnect(self.cidrelease)
            print self.definedPasses
            for i in self.definedPasses:
                self.overallRisk(i)
        except AttributeError:
            pass

