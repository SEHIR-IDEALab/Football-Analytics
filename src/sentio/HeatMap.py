import math
import numpy
from src.sentio.Pass import Pass

__author__ = 'doktoray'

class HeatMap:
    def __init__(self, ax, coordOfObjects):
        self.ax = ax
        self.hm = None
        self.allObjects = coordOfObjects
        self.clt_pass = Pass()


    def remove(self):
        if self.hm != None:
            self.hm.remove()


    def draw_defencePositionTaking(self, definedPass, chosenObject):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords
        p_chosen = None
        p_chosen_initialPosition = None

        x_coord = numpy.linspace(0, 105, 52)
        y_coord = numpy.linspace(0, 65, 32)

        p1_team = Pass.teams[p1.get_bbox_patch().get_facecolor()]
        for obj in self.allObjects:
            temp_obj_js = obj.point.get_text()
            temp_obj_team = Pass.teams[obj.point.get_bbox_patch().get_facecolor()]
            if (temp_obj_js == chosenObject) and (temp_obj_team not in [p1_team, "referee", "unknown"]):
                p_chosen = obj.point
                p_chosen_initialPosition = p_chosen.get_position()

        q = []
        for y in y_coord:
            w = []
            for x in x_coord:
                p_chosen.set_position((x,y))
                self.clt_pass.coordinateDataOfObjects = self.allObjects
                current_effectiveness = self.clt_pass.effectiveness(p1, p2)
                w.append(current_effectiveness)
                print x,y
            q.append(w)

        p_chosen.set_position(p_chosen_initialPosition)
        self.hm = self.ax.imshow(q, interpolation='bilinear',aspect="auto", extent=[-5.0, 110.0, 65.0, 0], vmax=12, alpha=0.8)
        self.ax.set_xlim(-5.0, 110.0)
        self.ax.set_ylim(0, 65.0)
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 115, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))


    def draw_positionOfTargetOfPass(self, definedPass):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords
        p_target_initialPosition = p2.get_position()

        x_coord = numpy.linspace(0, 105, 52)
        y_coord = numpy.linspace(0, 65, 32)

        q = []
        for y in y_coord:
            w = []
            for x in x_coord:
                p2.set_position((x,y))
                self.clt_pass.coordinateDataOfObjects = self.allObjects
                current_effectiveness = self.clt_pass.effectiveness(p1, p2)
                w.append(current_effectiveness)
                #print x,y, current_effectiveness
            q.append(w)

        p2.set_position(p_target_initialPosition)
        self.hm = self.ax.imshow(q, interpolation='bilinear',aspect="auto", extent=[-5.0, 110.0, 65.0, 0], vmax=12, alpha=0.8)
        self.ax.set_xlim(-5.0, 110.0)
        self.ax.set_ylim(0, 65.0)
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 115, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))


    def draw_positionOfSourceOfPass(self, definedPass):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords
        p_source_initialPosition = p1.get_position()

        x_coord = numpy.linspace(0, 105, 52)
        y_coord = numpy.linspace(0, 65, 32)

        q = []
        for y in y_coord:
            w = []
            for x in x_coord:
                p1.set_position((x,y))
                self.clt_pass.coordinateDataOfObjects = self.allObjects
                current_effectiveness = self.clt_pass.effectiveness(p1, p2)
                w.append(current_effectiveness)
                print x,y
            q.append(w)

        p1.set_position(p_source_initialPosition)
        self.hm = self.ax.imshow(q, interpolation='bilinear',aspect="auto", extent=[-5.0, 110.0, 65.0, 0], vmax=12, alpha=0.8)
        self.ax.set_xlim(-5.0, 110.0)
        self.ax.set_ylim(0, 65.0)
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 115, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))


    def __str__(self):
        pass
