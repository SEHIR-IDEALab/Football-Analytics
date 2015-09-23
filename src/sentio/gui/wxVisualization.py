# coding=utf-8



import numpy

import matplotlib
matplotlib.use('WXAgg')   # The recommended way to use wx with mpl is with the WXAgg backend.

from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.gui.VisualPlayer import VisualPlayer
from src.sentio.gui.wxListeners import wxListeners

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

from src.sentio import Parameters
from src.sentio.Parameters import *
from src.sentio.gui.DraggablePass import DraggablePass
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.gui.NoteBook import PageOne, PageTwo
from src.sentio.Time import Time
import os

import wx
import wx.media
from wx.lib.agw.shapedbutton import SBitmapButton



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
        self.directions_of_objects = list()




        self.listeners = wxListeners(self)





        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        self.layout_controls()


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


    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_save = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        m_open = menu_file.Append(wx.ID_OPEN, "&Open"," Open a snapshot to display")
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "&Exit\tCtrl-X", "Exit")

        menu_view = wx.Menu()
        debug_mode = menu_view.Append(-1, "&Debug Mode", kind=wx.ITEM_CHECK)

        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the tool")

        self.Bind(wx.EVT_MENU, self.listeners.on_save_plot, m_save)
        self.Bind(wx.EVT_MENU, self.listeners.on_open_plot, m_open)
        self.Bind(wx.EVT_MENU, self.listeners.on_exit, m_exit)
        self.Bind(wx.EVT_MENU, self.listeners.on_debug_mode, debug_mode)
        self.Bind(wx.EVT_MENU, self.listeners.on_about, m_about)

        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_view, "&View")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)


    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()


    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.listeners.on_flash_status_off, self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)


    def create_main_panel(self):
        self.panel = wx.Panel(self)

        ### main canvas
        self.dpi = 100
        self.fig = Figure((7,5), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.toolbar = NavigationToolbar(self.canvas)

        self.ax = self.fig.add_axes([0.015, 0.03, 0.980, 0.925])

        self.risk_range = RiskRange(self.ax)

        im = plt.imread('gui/source/background.png')
        self.ax.imshow(im, zorder=0, extent=[FOOTBALL_FIELD_MIN_X-4.5, FOOTBALL_FIELD_MAX_X+4.5,
                                             FOOTBALL_FIELD_MIN_Y-1.5, FOOTBALL_FIELD_MAX_Y+1.5])
        self.ax.grid()
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X+5, 5))
        self.ax.set_yticks(numpy.arange(FOOTBALL_FIELD_MIN_Y, FOOTBALL_FIELD_MAX_Y+5, 5))
        self.ax.tick_params(axis="both", labelsize=6)
        self.ax.autoscale(False)

        a,b,c,d, = plt.plot([],[],"bo",[],[],"ro",[],[],"yo",[],[],"ko", markersize=6)
        self.ax.legend([a,b,c,d], [HOME_TEAM_NAME.decode("utf-8"), AWAY_TEAM_NAME.decode("utf-8"), 'Referees',
                                   'Unknown Objects'], numpoints=1, fontsize=6, bbox_to_anchor=(0., 1.0, 1., .102),
                       loc=3, ncol=4, mode="expand", borderaxespad=0.5)

        self.current_time_display = wx.StaticText(self.panel, -1, "Time = 1_00:00:00")

        radioList = ['New Pass', 'Drag Object']
        self.rb = wx.RadioBox(self.panel,label="Mouse Action",choices=radioList, majorDimension=1,
                              style=wx.RA_SPECIFY_COLS)

        self.play_speed_slider = wx.Slider(self.panel, -1, value=2, minValue=1, maxValue=5)
        self.slider = wx.Slider(self.panel, -1, value=0, minValue=0, maxValue=self.sentio.game_instances.getTotalNumber()-1)

        self.upbmp = wx.Bitmap(os.path.join(BITMAP_DIRECTORY, "play.png"), wx.BITMAP_TYPE_PNG)
        self.disbmp = wx.Bitmap(os.path.join(BITMAP_DIRECTORY, "pause.png"), wx.BITMAP_TYPE_PNG)
        self.play_button = SBitmapButton(self.panel, -1, self.upbmp, (48, 48), size=(40,40))

        self.Bind(wx.EVT_RADIOBOX, self.listeners.on_mouse_action, self.rb)
        self.Bind(wx.EVT_BUTTON, self.listeners.on_play_button, self.play_button)
        self.Bind(wx.EVT_UPDATE_UI, self.listeners.on_update_play_button, self.play_button)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.listeners.on_slider_release, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.listeners.on_slider_shift, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.listeners.on_play_speed_slider, self.play_speed_slider)


    def layout_controls(self):
        # Layout with box sizers
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        p = wx.Panel(self.panel)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        self.pass_info_page = PageOne(nb)
        self.heatmap_setup_page = PageTwo(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.pass_info_page, "Info")
        nb.AddPage(self.heatmap_setup_page, "HeatMaps")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        vbox_rb_notebook = wx.BoxSizer(wx.VERTICAL)
        vbox_rb_notebook.Add(self.rb,0, wx.ALIGN_CENTER|wx.EXPAND)
        vbox_rb_notebook.Add(p,1, wx.EXPAND)

        self.play_speed_box = wx.StaticBox(self.panel, wx.ID_ANY, "Speed = 1x")
        play_speed_box_sizer = wx.StaticBoxSizer(self.play_speed_box, wx.VERTICAL)
        play_speed_box_sizer.Add(self.play_speed_slider)
        vbox_rb_notebook.Add(play_speed_box_sizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER)

        self.hbox.Add(vbox_rb_notebook, 0, wx.EXPAND)

        self.vbox_canvas = wx.BoxSizer(wx.VERTICAL)
        self.vbox_canvas.Add(self.canvas, 1, wx.EXPAND)
        self.vbox_canvas.Add(self.toolbar, 0, wx.EXPAND)

        self.hbox.Add(self.vbox_canvas, 1, wx.EXPAND)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.hbox, 1, wx.EXPAND)

        self.hbox_play = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_play.Add(self.play_button, 0, flag=wx.ALIGN_CENTER)
        self.hbox_play.Add(self.slider, 1, wx.EXPAND)
        self.hbox_play.Add(self.current_time_display, 0, flag=flags)
        self.vbox.Add(self.hbox_play, 0, wx.EXPAND)

        self.panel.SetSizer(self.vbox)
        # self.Fit()



    def draw_figure(self):
        self.canvas.draw()


    def refresh_ui(self):
        self.remove_allDefinedPassesForSnapShot()
        self.remove_directionSpeedOfObjects()

        # self.pass_info_page.logger.Clear()
        self.govern_passes.heatMap.clear()


    def visualizePositionsFor(self, time):
        self.updatePositions(time)
        self.annotateGameEventsFor(time)
        self.canvas.draw()


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
                self.event_annotation = self.ax.annotate(current_event.event_name, xy=(52.5,32.5),  xycoords='data',
                                        va="center", ha="center", xytext=(0, 0), textcoords='offset points', size=20,
                                        bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5), alpha=0.5))
            else:
                if current_event.isPassEvent():
                    pass_event = current_event.getPassEvent()
                    print pass_event

                    p_visual_player = self.convertPlayerToVisualPlayer(pass_event.pass_source)
                    p_visual_player.clearBallHolder()

                    c_visual_player = self.convertPlayerToVisualPlayer(pass_event.pass_target)
                    c_visual_player.setAsBallHolder()

                    pass_event_annotation = self.ax.annotate('', xy=pass_event.pass_target.get_position(),
                                                             xytext=pass_event.pass_source.get_position(), size=20,
                                                             arrowprops=dict(arrowstyle="->", fc=pass_event.pass_source.getObjectColor(),
                                                                          ec=pass_event.pass_source.getObjectColor(), alpha=1.0))

                    effectiveness = self.govern_passes.displayDefinedPass(pass_event, self.pass_info_page.logger)
                    self.pass_event_annotations.append(pass_event_annotation)
                    self.updatePassEventAnnotations()

                    if Parameters.IS_DEBUG_MODE_ON:
                        self.risk_range.drawRangeFor(pass_event)

                    ultX = ((pass_event.pass_target.getX() + pass_event.pass_source.getX()) / 2.)
                    ultY = ((pass_event.pass_target.getY() + pass_event.pass_source.getY()) / 2.)

                    self.effectiveness_annotation = self.ax.annotate(("effectiveness %.2f"%(effectiveness)),
                        xy=(ultX-10, ultY), xycoords="data", va="center", ha="center", xytext=(ultX-10, ultY),
                        textcoords="offset points", size=10, bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7),
                                                                           ec=(1., .5, .5), alpha=0.5))
                    self.effectiveness_count = 0

                    self.entire_trailX, self.entire_trailY = [pass_event.pass_target.getX()],[pass_event.pass_target.getY()]
                    trailAnnotation, = self.ax.plot(self.entire_trailX, self.entire_trailY,
                                                    linestyle="--", linewidth=2, color="yellow")
                    trailAnnotation.player = pass_event.pass_target
                    self.trail_annotations.append(trailAnnotation)
                    self.updateTrailAnnotations()
        else:
            try:
                if self.p_event.event_id == 1:
                    c_player = ReaderBase.getPlayerIn(self.p_event.player, current_teams)
                    self.entire_trailX.append(c_player.getX()), self.entire_trailY.append(c_player.getY())
                    c_trailAnnotation = self.trail_annotations[-1]
                    c_trailAnnotation.set_data(self.entire_trailX, self.entire_trailY)
            except:
                pass


    def convertPlayerToVisualPlayer(self, player):
        if player.object_id in self.visual_idToPlayers:
            return self.visual_idToPlayers[player.object_id]
        return None


    # def annotateDirectionSpeedOfObjects_forGivenTime(self, time):
    #     teams_for_direction = self.getDirectionsOfPlayersFor(time)
    #     teams_for_speed = self.getSpeedsOfPlayersFor(time)
    #     for team1, team2 in zip(teams_for_direction, teams_for_speed):
    #         for player1, player2 in zip(team1, team2):
    #             current_x, next_x = player1.getX()
    #             current_y, next_y = player1.getY()
    #             speed = player2.speed
    #
    #             next_x, next_y = adjust_arrow_size((current_x, current_y), (next_x, next_y), speed)
    #             passAnnotation = self.ax.annotate('', xy=(next_x,next_y), xycoords='data', xytext=(current_x,current_y),
    #                                               textcoords='data',size=20, va="center", ha="center", arrowprops=dict(
    #                     arrowstyle="simple", connectionstyle="arc3",
    #                     fc="cyan", ec="b", lw=2))
    #             self.directions_of_objects.append(passAnnotation)
    #     self.canvas.draw()


    def getDirectionsOfPlayers(self, time):
        game_instance = self.sentio.game_instances.getGameInstance(time)
        idToPlayers = ReaderBase.mapIDToPlayers(game_instance.players)


    # def getDirectionsOfPlayersFor(self, time): # should be rewritten
    #     current_time = Time(time.half, time.minute, time.second, time.millisecond)
    #     current_time.set_minMaxOfHalf(HALF_MIN_MAX)
    #     n_time = current_time.next()
    #
    #     temp_teams = ({},{},{},{})
    #     n_teams = self.sentio.game_instances.get(n_time.get_in_milliseconds())
    #     for index, team in enumerate((n_teams.home_team, n_teams.away_team, n_teams.referees, n_teams.unknowns)):
    #         for temp_player in team.getTeamPlayers():
    #             temp_teams[index][temp_player.getJerseyNumber()] = temp_player.get_position()
    #     return temp_teams
    #
    #
    # def getSpeedsOfPlayersFor(self, time): # should be rewritten
    #     current_time = Time(time.half, time.minute, time.second, time.millisecond)
    #     current_time.set_minMaxOfHalf(HALF_MIN_MAX)
    #
    #     temp_teams = ({},{},{},{})
    #
    #     teams = self.coordinate_data.get((time.half, time.minute, time.second, time.millisecond))
    #     for index, team in enumerate((teams.home_team, teams.away_team, teams.referees, teams.unknowns)):
    #         for player in team.getTeamPlayers():
    #             temp_teams[index][player.getJerseyNumber()] = [player.get_position()]
    #     for i in range(5):
    #         p_time = current_time.back()
    #         p_teams = self.coordinate_data.get((p_time.half, p_time.minute, p_time.second, p_time.millisecond))
    #         for index, team in enumerate((p_teams.home_team, p_teams.away_team, p_teams.referees, p_teams.unknowns)):
    #             for temp_player in team.getTeamPlayers():
    #                 temp_positions = temp_teams[index][temp_player.getJerseyNumber()]
    #                 temp_positions.append(temp_player.get_position())
    #     for index, team in enumerate(temp_teams):
    #         for js in team:
    #             positions = team[js]
    #             total = 0.0
    #             for i in range(5):
    #                 x, y = positions[i]
    #                 p_x, p_y = positions[i+1]
    #                 total += math.sqrt(pow(x-p_x, 2) + pow(y-p_y, 2))
    #             team[js] = total
    #     return temp_teams


    def remove_all_draggable_visual_players(self):
        for visual_player in (self.visual_players):
            visual_player.remove()


    def setPositions(self, players):
        self.visual_idToPlayers = {}
        for player in players:
            visual_player = VisualPlayer(self.ax, player, self.current_time, self.sentio.game_instances)
            self.visual_idToPlayers[player.object_id] = visual_player

        self.govern_passes = DraggablePass(self.ax, self.visual_idToPlayers, self.fig)
        self.govern_passes.set_defined_passes(self.defined_passes_forSnapShot)
        self.govern_passes.set_passDisplayer(self.pass_info_page.logger)
        self.govern_passes.set_variables(self.heatmap_setup_page.heat_map, self.heatmap_setup_page.resolution,
                                        self.heatmap_setup_page.effectiveness)
        self.govern_passes.heatMap.set_color_bar(self.heatmap_setup_page.color_bar,
                                                self.heatmap_setup_page.colorbar_canvas)
        self.govern_passes.heatMap.set_color_bar_listeners((self.heatmap_setup_page.vmin_auto_rbutton,
                                                           self.heatmap_setup_page.vmin_custom_rbutton,
                                                           self.heatmap_setup_page.vmin_custom_entry),
                                                          (self.heatmap_setup_page.vmax_auto_rbutton,
                                                           self.heatmap_setup_page.vmax_custom_rbutton,
                                                           self.heatmap_setup_page.vmax_custom_entry),
                                                          self.heatmap_setup_page.colorbar_refresh_button)
        for visual_player in self.visual_idToPlayers.values():
            visual_player.draggable.setPassLogger(self.pass_info_page.logger)
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
                visual_player = VisualPlayer(self.ax, player, time, self.sentio.game_instances)
                self.visual_idToPlayers[player.object_id] = visual_player



    def remove_defined_passes(self):
        if self.govern_passes.passes_defined:
            for i in self.govern_passes.passes_defined: i.remove()
            del self.govern_passes.passes_defined[:]


    def remove_directionSpeedOfObjects(self):
        if self.directions_of_objects:
            for i in self.directions_of_objects:
                i.remove()
            del self.directions_of_objects[:]
            self.canvas.draw()


    def remove_allDefinedPassesForSnapShot(self):
        if self.defined_passes_forSnapShot:
            for pass_event in self.defined_passes_forSnapShot:
                pass_event.remove()
            del self.defined_passes_forSnapShot[:]
            self.canvas.draw()


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
                temp_pass_event_annotation = self.ax.annotate('', xy=pass_event_annotation.xy, xytext=pass_event_annotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=pass_event_annotation.arrowprops["fc"],
                                                  ec=pass_event_annotation.arrowprops["ec"], alpha=0.5))
                temp_pass_event_annotations.append(temp_pass_event_annotation)

            c_pass_annotation = self.pass_event_annotations[-1]
            temp_pass_event_annotations.append(self.ax.annotate('', xy=c_pass_annotation.xy, xytext=c_pass_annotation.xytext,
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
                trail_annotation.set_color(trail_annotation.player.getObjectColor())


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
        self.remove_directionSpeedOfObjects()
        self.remove_allDefinedPassesForSnapShot()
        self.removeEventAnnotation()
        self.removePassEventAnnotations()
        self.removeTrailAnnotations()
        self.removeEffectivenessAnnotation()
        self.pass_info_page.logger.Clear()








