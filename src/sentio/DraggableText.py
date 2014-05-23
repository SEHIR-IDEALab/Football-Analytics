from Tkconstants import END
from src.sentio.Pass import Pass
from src.sentio.Player_base import Player_base


class DraggableText:
    lock = None #only one can be animated at a time
    def __init__(self, point):
        self.point = point
        self.press = None
        self.background = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if DraggableText.lock is not None: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = (self.point.get_position()), event.xdata, event.ydata
        DraggableText.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.point)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        if DraggableText.lock is not self:
            return
        if event.inaxes != self.point.axes: return
        center_of_text, xpress, ypress = self.press
        self.point.set_position(center_of_text)
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        new_dx, new_dy = self.point.get_position()
        self.point.set_position((new_dx+dx, new_dy+dy))
        
        canvas = self.point.figure.canvas
        axes = self.point.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.point)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableText.lock is not self:
            return

        self.press = None
        DraggableText.lock = None

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()

        self.displayDefinedPasses()

    def set_passDisplayer(self, passDisplayer):
        self.passDisplayer = passDisplayer

    def set_definedPasses(self, definedPasses):
        self.definedPasses = definedPasses

    def set_coordinatesOfObjects(self, coord):
        self.coordinatesOfObjects = coord

    def displayDefinedPasses(self):
        self.passDisplayer.delete("1.0", END)
        passes = Pass(self.coordinatesOfObjects)
        for i in self.definedPasses:
            p1 = i.textcoords
            p2 = i.xycoords
            object_type1, object_id1, js1, (x1, y1) = p1.object_type, p1.object_id, p1.get_text(), p1.get_position()
            object_type2, object_id2, js2, (x2, y2) = p2.object_type, p2.object_id, p2.get_text(), p2.get_position()

            p1 = Player_base([object_type1, object_id1,js1, x1, y1])
            p2 = Player_base([object_type2, object_id2,js2, x2, y2])

            self.passDisplayer.insert("1.0", "goal_chance = %.2f\n" %passes.goalChance(p2))
            self.passDisplayer.insert("1.0", "effectiveness = %.2f\n" %passes.effectiveness(p1, p2))
            self.passDisplayer.insert("1.0", "pass_advantage = %.2f (%s)\n" %passes.passAdvantage(p2))
            self.passDisplayer.insert("1.0", "gain = %.2f\n" %passes.gain(p1, p2))
            self.passDisplayer.insert("1.0", "overall_risk(%s->g_Kpr) = %.2f\n" %(p2.getJerseyNumber(), passes.overallRisk(p2, [0.0, 32.75])))
            self.passDisplayer.insert("1.0", "overall_risk(%s->%s) = %.2f\n" %(p1.getJerseyNumber(), p2.getJerseyNumber(), passes.overallRisk(p1, p2)))
            self.passDisplayer.insert("1.0", "\n%s --> %s\n" %(p1.getJerseyNumber(), p2.getJerseyNumber()))

    def disconnect(self):
        'disconnect all the stored connection ids'
        try:
            self.point.figure.canvas.mpl_disconnect(self.cidpress)
            self.point.figure.canvas.mpl_disconnect(self.cidrelease)
            self.point.figure.canvas.mpl_disconnect(self.cidmotion)
        except AttributeError:
            pass