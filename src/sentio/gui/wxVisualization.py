# coding=utf-8


import wx
import matplotlib
matplotlib.use('WXAgg')   # The recommended way to use wx with mpl is with the WXAgg backend.

from src.sentio.Parameters import GUI_TITLE
from src.sentio.gui.RiskRange import RiskRange


from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.gui.VisualPlayer import VisualPlayer
from src.sentio.gui.wxListeners import wxListeners
from src.sentio.gui.wxLayouts import wxLayouts

from src.sentio import Parameters
from src.sentio.gui.DraggablePass import DraggablePass
from src.sentio.Time import Time



__author__ = 'emrullah'


class wxVisualization(wx.Frame):

    def __init__(self, sentio):
        display_size = wx.DisplaySize()
        padding = 50
        screen_perc = 3/4.
        wx.Frame.__init__(self, None, wx.ID_ANY, GUI_TITLE,
                          pos=(padding, padding),
                          size=(display_size[0]*screen_perc, display_size[1]*screen_perc))

        self.sentio = sentio

        self.paused = True

        #-------------------
        self.listeners = wxListeners(self)

        self.layouts = wxLayouts(self)
        self.layouts.layout_controls()

        self.listeners.layouts = self.layouts
        self.listeners.activate()
        #-------------------

        self.risk_range = RiskRange(self.layouts.ax)

        self.govern_passes = None
        self.defined_passes_forSnapShot = list()

        self.trail_annotations, self.event_annotation, self.pass_event_annotations, self.effectiveness_annotation = \
            [], None, [], None

        self.pass_event = None

        self.effectiveness_count = 0
        self.play_speed = 2

        self.current_time = Time()
        game_instance = self.sentio.game_instances.getGameInstance(self.current_time)
        self.setPositions(game_instance.players)

        self.draw_figure()


    def draw_figure(self):
        self.layouts.canvas.draw()


    def refresh_ui(self):
        self.remove_allDefinedPassesForSnapShot()
        # self.remove_directionSpeedOfObjects()

        # self.pass_info_page.logger.Clear()
        self.govern_passes.heatMap.clear()


    def visualizePositionsFor(self, time):
        self.updatePositions(time)
        self.annotateGameEventsFor(time)
        self.layouts.canvas.draw()


    def annotateGameEventsFor(self, time):
        game_instance  = self.sentio.game_instances.getGameInstance(time)
        current_teams = ReaderBase.divideIntoTeams(game_instance.players)

        if self.effectiveness_count < 5: self.effectiveness_count += 1
        if self.effectiveness_count == 5: self.removeEffectivenessAnnotation()

        current_event = game_instance.event
        if current_event:
            self.removeEventAnnotation()

            self.p_event = current_event
            if current_event.event_id != 1:
                self.removePassEventAnnotations()
                self.removeTrailAnnotations()
                self.event_annotation = self.layouts.ax.annotate(current_event.event_name, xy=(52.5,32.5),  xycoords='data',
                                        va="center", ha="center", xytext=(0, 0), textcoords='offset points', size=20,
                                        bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5), alpha=0.5))
            else:
                if current_event.isPassEvent():
                    pass_event = current_event.getPassEvent()
                    print pass_event

                    p_visual_player = self.convertPlayerToVisualPlayer(pass_event.pass_source)
                    p_visual_player.clearBallHolder()
                    p_visual_player.clearDirectionWithSpeed()

                    c_visual_player = self.convertPlayerToVisualPlayer(pass_event.pass_target)
                    c_visual_player.setAsBallHolder()
                    c_visual_player.drawDirectionWithSpeed()

                    pass_event_annotation = self.layouts.ax.annotate('', xy=pass_event.pass_target.get_position(),
                                                             xytext=pass_event.pass_source.get_position(), size=20,
                                                             arrowprops=dict(arrowstyle="->", fc=pass_event.pass_source.getObjectColor(),
                                                                          ec=pass_event.pass_source.getObjectColor(), alpha=1.0))

                    effectiveness = self.govern_passes.displayDefinedPass(pass_event, self.layouts.pass_info_page.logger)
                    self.pass_event_annotations.append(pass_event_annotation)
                    self.updatePassEventAnnotations()

                    if Parameters.IS_DEBUG_MODE_ON:
                        self.risk_range.drawRangeFor(pass_event)

                    ultX = ((pass_event.pass_target.getX() + pass_event.pass_source.getX()) / 2.)
                    ultY = ((pass_event.pass_target.getY() + pass_event.pass_source.getY()) / 2.)

                    self.effectiveness_annotation = self.layouts.ax.annotate(("effectiveness %.2f"%(effectiveness)),
                        xy=(ultX-10, ultY), xycoords="data", va="center", ha="center", xytext=(ultX-10, ultY),
                        textcoords="offset points", size=10, bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7),
                                                                           ec=(1., .5, .5), alpha=0.5))
                    self.effectiveness_count = 0

                    c_visual_player.startTrail()
                    self.trail_annotations.append(c_visual_player.trail_annotation)
                    self.updateTrailAnnotations()
        else:
            try:
                if self.p_event.event_id == 1:
                    c_visual_player = self.convertPlayerToVisualPlayer(self.p_event.player)
                    c_visual_player.updateTrail()
            except:
                pass


    def convertPlayerToVisualPlayer(self, player):
        if player.object_id in self.visual_idToPlayers:
            return self.visual_idToPlayers[player.object_id]
        return None


    def remove_visual_players(self):
        for visual_player in self.visual_idToPlayers.values():
            visual_player.remove()


    def setPositions(self, players):
        self.visual_idToPlayers = {}
        for player in players:
            visual_player = VisualPlayer(self.layouts.ax, player, self.current_time, self.sentio.game_instances)
            self.visual_idToPlayers[player.object_id] = visual_player

        self.govern_passes = DraggablePass(self.layouts.ax, self.visual_idToPlayers, self.layouts.fig)
        self.govern_passes.set_defined_passes(self.defined_passes_forSnapShot)
        self.govern_passes.set_passDisplayer(self.layouts.pass_info_page.logger)
        self.govern_passes.set_variables(self.layouts.heatmap_setup_page.heat_map,
                                         self.layouts.heatmap_setup_page.resolution,
                                        self.layouts.heatmap_setup_page.effectiveness)
        self.govern_passes.heatMap.set_color_bar(self.layouts.heatmap_setup_page.color_bar,
                                                self.layouts.heatmap_setup_page.colorbar_canvas)
        self.govern_passes.heatMap.set_color_bar_listeners((self.layouts.heatmap_setup_page.vmin_auto_rbutton,
                                                           self.layouts.heatmap_setup_page.vmin_custom_rbutton,
                                                           self.layouts.heatmap_setup_page.vmin_custom_entry),
                                                          (self.layouts.heatmap_setup_page.vmax_auto_rbutton,
                                                           self.layouts.heatmap_setup_page.vmax_custom_rbutton,
                                                           self.layouts.heatmap_setup_page.vmax_custom_entry),
                                                          self.layouts.heatmap_setup_page.colorbar_refresh_button)
        for visual_player in self.visual_idToPlayers.values():
            visual_player.draggable.setPassLogger(self.layouts.pass_info_page.logger)
            visual_player.draggable.setDefinedPasses(self.govern_passes.passes_defined)
            visual_player.draggable.setVisualPlayers(self.visual_idToPlayers)


    def updatePositions(self, time):
        game_instance = self.sentio.game_instances.getGameInstance(time)
        for player in game_instance.players:
            if player.object_id in self.visual_idToPlayers:
                visual_player = self.visual_idToPlayers[player.object_id]
                if not visual_player.update_position(time):
                    visual_player.remove()
                    del self.visual_idToPlayers[player.object_id]
            else:
                visual_player = VisualPlayer(self.layouts.ax, player, time, self.sentio.game_instances)
                self.visual_idToPlayers[player.object_id] = visual_player



    def remove_defined_passes(self):
        if self.govern_passes.passes_defined:
            for i in self.govern_passes.passes_defined: i.remove()
            del self.govern_passes.passes_defined[:]


    def remove_allDefinedPassesForSnapShot(self):
        if self.defined_passes_forSnapShot:
            for pass_event in self.defined_passes_forSnapShot:
                pass_event.remove()
            del self.defined_passes_forSnapShot[:]
            self.layouts.canvas.draw()


    def removeEventAnnotation(self):
        if self.event_annotation != None:
            self.event_annotation.remove(); del self.event_annotation; self.event_annotation = None


    def removePassEventAnnotations(self):
        if self.pass_event_annotations != []:
            for pass_event_annotation in self.pass_event_annotations:
                pass_event_annotation.remove()
            del self.pass_event_annotations[:]


    def updatePassEventAnnotations(self):
        if self.pass_event_annotations != []:
            temp_pass_event_annotations = []
            for pass_event_annotation in self.pass_event_annotations[-3:-1]:
                temp_pass_event_annotation = self.layouts.ax.annotate('', xy=pass_event_annotation.xy, xytext=pass_event_annotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=pass_event_annotation.arrowprops["fc"],
                                                  ec=pass_event_annotation.arrowprops["ec"], alpha=0.5))
                temp_pass_event_annotations.append(temp_pass_event_annotation)

            c_pass_annotation = self.pass_event_annotations[-1]
            temp_pass_event_annotations.append(self.layouts.ax.annotate('', xy=c_pass_annotation.xy, xytext=c_pass_annotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=c_pass_annotation.arrowprops["fc"],
                                                  ec=c_pass_annotation.arrowprops["ec"], alpha=1.0)))

            for passAnnotation in self.pass_event_annotations: passAnnotation.remove()
            self.pass_event_annotations = temp_pass_event_annotations


    def updateTrailAnnotations(self):
        if self.trail_annotations != []:

            while len(self.trail_annotations) > 3:
                self.trail_annotations[0].remove()
                del self.trail_annotations[0]

            for trail_annotation in self.trail_annotations[-3:-1]:
                trail_annotation.set_alpha(0.5)
                trail_annotation.set_color(trail_annotation.color)


    def removeTrailAnnotations(self):
        if self.trail_annotations !=[]:
            for trail_annotation in self.trail_annotations:
                trail_annotation.remove()
            del self.trail_annotations[:]


    def removeEffectivenessAnnotation(self):
        if self.effectiveness_annotation != None:
            self.effectiveness_annotation.remove(); del self.effectiveness_annotation
            self.effectiveness_annotation = None


    def removeAllAnnotations(self):
        # self.remove_directionSpeedOfObjects()
        self.remove_allDefinedPassesForSnapShot()
        self.removeEventAnnotation()
        self.removePassEventAnnotations()
        self.removeTrailAnnotations()
        self.removeEffectivenessAnnotation()
        self.layouts.pass_info_page.logger.Clear()








