from src.sentio.file_io import Parser
from src.sentio.file_io.reader import ReaderBase
from src.sentio.pass_evaluate.Pass import Pass


class DraggablePlayer:
    lock = None #only one can be animated at a time

    def __init__(self, point):
        self.visual_player = point
        self.press = None
        self.background = None


    def setPlayer(self, player):
        self.player = player


    def getPlayer(self):
        return self.player


    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.visual_player.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.visual_player.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.visual_player.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)


    def on_press(self, event):
        if event.inaxes != self.visual_player.axes: return
        if DraggablePlayer.lock is not None: return
        contains, attrd = self.visual_player.contains(event)
        if not contains: return
        self.press = (self.visual_player.get_position()), event.xdata, event.ydata
        DraggablePlayer.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.visual_player.figure.canvas
        axes = self.visual_player.axes
        self.visual_player.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.visual_player.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.visual_player)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)


    def on_motion(self, event):
        if DraggablePlayer.lock is not self:
            return
        if event.inaxes != self.visual_player.axes: return
        center_of_text, xpress, ypress = self.press
        self.visual_player.set_position(center_of_text)
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        new_dx, new_dy = self.visual_player.get_position()
        self.visual_player.set_position((new_dx+dx, new_dy+dy))
        
        canvas = self.visual_player.figure.canvas
        axes = self.visual_player.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.visual_player)

        # blit just the redrawn area
        canvas.blit(axes.bbox)


    def on_release(self, event):
        'on release we reset the press data'
        if DraggablePlayer.lock is not self:
            return

        self.press = None
        DraggablePlayer.lock = None

        # turn off the rect animation property and reset the background
        self.visual_player.set_animated(False)
        self.background = None

        # redraw the full figure
        self.visual_player.figure.canvas.draw()

        self.displayDefinedPasses()


    def setPassLogger(self, pass_logger):
        self.pass_logger = pass_logger


    def setDefinedPasses(self, passes_defined):
        self.passes_defined = passes_defined


    def setDraggableVisualTeams(self, draggable_visual_teams):
        self.draggable_visual_teams = draggable_visual_teams


    def displayDefinedPasses(self):
        self.pass_logger.Clear()

        teams = ReaderBase.convertDraggableToTeams(self.draggable_visual_teams)
        passes = Pass()
        passes.teams=teams
        for defined_pass in self.passes_defined:
            passes.displayDefinedPass(defined_pass, self.pass_logger, visual=True)


    def disconnect(self):
        'disconnect all the stored connection ids'
        try:
            self.visual_player.figure.canvas.mpl_disconnect(self.cidpress)
            #self.point.figure.canvas.mpl_disconnect(self.cidrelease)
            self.visual_player.figure.canvas.mpl_disconnect(self.cidmotion)
        except AttributeError:
            pass