from src.sentio.gui.DraggablePoint import DraggablePoint
from src.sentio.object.PlayerBase import PlayerBase

__author__ = 'emrullah'


class VisualPlayer(PlayerBase):

    def __init__(self, ax, player, time, game_instances):
        PlayerBase.__init__(self, player.raw_data)

        self.time = time
        self.game_instances = game_instances

        self.ax =ax

        self.player = player
        self.draggable = DraggablePoint(ax.text(player.getX(), player.getY(), player.getJerseyNumber(),
            horizontalalignment='center',
            verticalalignment='center',
            zorder=1,
            color="w",
            fontsize=10,
            picker=True,
            bbox=dict(
                boxstyle="circle,pad=0.3",
                fc=self.getObjectColor(),
                ec=self.getObjectTypeColor(),
                alpha=0.5,
                linewidth=1
            )
        ))
        self.draggable.point.object_id = self.player.object_id

        self.direction_annotation = None
        self.trail_annotation = None


    def startTrail(self):
        x, y = self.draggable.point.get_position()
        self.trail_x, self.trail_y = [x], [y]
        self.trail_annotation, = self.ax.plot(self.trail_x, self.trail_y,
                                        linestyle="--",
                                        linewidth=2,
                                        color="yellow")
        self.trail_annotation.color = self.getObjectColor()


    def updateTrail(self):
        x, y = self.draggable.point.get_position()
        self.trail_x.append(x), self.trail_y.append(y)
        self.trail_annotation.set_data(self.trail_x, self.trail_y)


    def clearTrail(self):
        self.trail_annotation.remove()


    def setAsBallHolder(self):
        self.draggable.point.set_bbox(dict(boxstyle="circle,pad=0.3",
                                           fc=self.getObjectColor(),
                                           ec="yellow",
                                           linewidth=2))


    def clearBallHolder(self):
        self.draggable.point.set_bbox(dict(boxstyle="circle,pad=0.3",
                                           fc=self.getObjectColor(),
                                           ec=self.getObjectTypeColor(),
                                           alpha=0.5,
                                           linewidth=1))


    def drawDirectionWithSpeed(self):
        speed = self.calculateSpeed()
        direction = self.calculateDirection()

        import math
        def point_pos(x0, y0, d, theta):
            theta_rad = math.pi/4 - math.radians(theta)
            return x0 + d*math.cos(theta_rad), y0 + d*math.sin(theta_rad)

        x, y = self.draggable.point.get_position()
        self.direction_annotation = self.ax.annotate('',
                                          xy=point_pos(x, y, speed, direction),
                                          xycoords='data',
                                          xytext=(x,y),
                                          textcoords='data',
                                          size=20,
                                          va="center",
                                          ha="center",
                                          arrowprops=dict(
                                              arrowstyle="simple",
                                              connectionstyle="arc3",
                                              fc="cyan",
                                              ec="b",
                                              lw=2))


    def clearDirectionWithSpeed(self):
        if self.direction_annotation:
            self.direction_annotation.remove()


    def update_position(self, time):
        self.time = time  ## time should be updated as well!!!
        game_instance = self.game_instances.getGameInstance(time)
        player = game_instance.getPlayer(self.player.object_id)
        if player:
            self.draggable.point.set_position(player.get_position())
            return True
        return False


    def get_position(self):
        return self.draggable.point.get_position()


    def remove(self):
        self.draggable.point.remove()


    def calculateSpeed(self):
        return PlayerBase.calculateSpeedFor(self.time, self.game_instances, visual=True, player_id=self.object_id)


    def calculateDirection(self):
        return PlayerBase.calculateDirectionFor(self.time, self.game_instances, visual=True, player_id=self.object_id)


    def getObjectColor(self):
        if self.object_type in [0,3]: return "blue"
        elif self.object_type in [1,4]: return "red"
        elif self.object_type in [2,6,7,8,9]: return "yellow"
        else: return "black"


    def getObjectTypeColor(self):
        if self.object_type == 0: return "blue"
        elif self.object_type == 1: return "red"
        elif self.object_type in [3,4]: return "black"
        elif self.object_type in [2,6,7,8,9]: return "yellow"
        else: return "black"


    def __str__(self):
        pass
