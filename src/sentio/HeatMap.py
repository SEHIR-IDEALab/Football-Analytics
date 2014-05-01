import math
import numpy
from src.sentio.Pass import Pass

__author__ = 'doktoray'

class HeatMap:
    def __init__(self, ax):
        self.ax = ax
        self.hm = None
        self.pRisk = Pass()

    def remove(self):
        if self.hm != None:
            self.hm.remove()

    def draw(self, definedPass):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords

        x1, y1 = p1.get_position()
        x2, y2 = p2.get_position()

        x_coord = numpy.linspace(min([x1,x2]),max([x1,x2]),int(math.ceil(math.fabs(x1-x2)*2)))
        y_coord = numpy.linspace(min([y1,y2]),max([y1,y2]),int(math.ceil(math.fabs(y1-y2)*2)))

        q = []
        for y in y_coord:
            w = []
            for x in x_coord:
                current_risk = self.pRisk.risk((x1,y1), (x,y), (x2,y2))
                w.append(current_risk)
            q.append(w)

        self.hm = self.ax.imshow(q, interpolation='bilinear',aspect="auto", extent=[min([x1,x2]),max([x1,x2]),
                                                                                    max([y1,y2]),min([y1,y2])], vmax=12)
        self.ax.set_xlim(-6.5, 111.5)
        self.ax.set_ylim(-1.2, 67.0)
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 115, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))

    def __str__(self):
        pass
