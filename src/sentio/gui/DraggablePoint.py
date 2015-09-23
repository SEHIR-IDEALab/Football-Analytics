from src.sentio.file_io import Parser
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.pass_evaluate.Pass import Pass


class DraggablePoint:
    lock = None #only one can be animated at a time

    def __init__(self, point):
        self.point = point
        self.press = None
        self.background = None


    def setPlayer(self, player):
        self.player = player


    def getPlayer(self):
        return self.player


    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)


    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = (self.point.get_position()), event.xdata, event.ydata
        DraggablePoint.lock = self

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
        if DraggablePoint.lock is not self:
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
        if DraggablePoint.lock is not self:
            return

        self.press = None
        DraggablePoint.lock = None

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()

        self.displayDefinedPasses()


    def setPassLogger(self, pass_logger):
        self.pass_logger = pass_logger


    def setDefinedPasses(self, passes_defined):
        self.passes_defined = passes_defined


    def setVisualPlayers(self, visual_idToPlayers):
        self.visual_idToPlayers = visual_idToPlayers


    def convertVisualPlayerToPlayer(self, visual_player):
        visual_player = self.visual_idToPlayers[visual_player.object_id]
        player = visual_player.player
        player.set_position(visual_player.get_position())
        return player


    def displayDefinedPasses(self):
        self.pass_logger.Clear()

        passes = Pass()
        for defined_pass in self.passes_defined:
            defined_pass.pass_source = self.convertVisualPlayerToPlayer(defined_pass.pass_source)
            defined_pass.pass_target = self.convertVisualPlayerToPlayer(defined_pass.pass_target)
            defined_pass.teams = ReaderBase.divideIntoTeams(self.visual_idToPlayers.values(), visual=True)
            passes.displayDefinedPass(defined_pass, self.pass_logger, dragged=True)


    def disconnect(self):
        'disconnect all the stored connection ids'
        try:
            self.point.figure.canvas.mpl_disconnect(self.cidpress)
            #self.point.figure.canvas.mpl_disconnect(self.cidrelease)
            self.point.figure.canvas.mpl_disconnect(self.cidmotion)
        except AttributeError:
            pass