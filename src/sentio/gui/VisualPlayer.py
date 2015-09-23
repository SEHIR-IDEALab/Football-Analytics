from src.sentio.gui.DraggablePoint import DraggablePoint
from src.sentio.object.PlayerBase import PlayerBase

__author__ = 'emrullah'


class VisualPlayer(PlayerBase):

    def __init__(self, ax, player, time, game_instances):
        PlayerBase.__init__(self, player.raw_data)

        self.time = time
        self.game_instances = game_instances

        self.player = player
        self.draggable = DraggablePoint(ax.text(player.getX(), player.getY(), player.getJerseyNumber(),
            zorder=1,
            color="w",
            fontsize=(9 if len(str(player.getJerseyNumber()))==1 else 7),
            picker=True,
            bbox=dict(
                boxstyle="circle,pad=0.3",
                fc=player.getObjectColor(),
                ec=player.getObjectTypeColor(),
                alpha=0.5,
                linewidth=1
            )
        ))
        self.draggable.point.object_id = self.player.object_id


    def setAsBallHolder(self):
        self.draggable.point.set_bbox(dict(boxstyle="circle,pad=0.3",
                                           fc=self.player.getObjectColor(),
                                           ec="yellow",
                                           linewidth=2))


    def clearBallHolder(self):
        self.draggable.point.set_bbox(dict(boxstyle="circle,pad=0.3",
                                           fc=self.player.getObjectColor(),
                                           ec=self.player.getObjectTypeColor(),
                                           alpha=0.5,
                                           linewidth=1))


    def update_position(self, time):
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


    def __str__(self):
        pass
