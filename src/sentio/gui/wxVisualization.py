# coding=utf-8

from collections import OrderedDict


import numpy

import matplotlib
import operator
from src.sentio.file_io.reader.ReaderBase import ReaderBase

matplotlib.use('WXAgg')   # The recommended way to use wx with mpl is with the WXAgg backend.
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.patches import BoxStyle

from src.sentio import Parameters
from src.sentio.Parameters import *
from src.sentio.gui.CircleStyle import CircleStyle
from src.sentio.gui.DraggablePass import DraggablePass
from src.sentio.gui.DraggablePlayer import DraggablePlayer
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.gui.NoteBook import PageOne, PageTwo
from src.sentio.gui.SnapShot import SnapShot, adjust_arrow_size
from src.sentio.Time import Time
from src.sentio.file_io.Parser import Parser

import time as tm
import math
import os

import wx
import wx.media
from wx.lib.agw.shapedbutton import SBitmapButton



__author__ = 'emrullah'

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'source/bitmaps')


class wxVisualization(wx.Frame):

    dirname=''
    title = "Sport Analytics Tool - IDEA Lab"

    def __init__(self, sentio):
        wx.Frame.__init__(self, None, -1, self.title, pos=(0,20), size=(1200,750))

        self.sentio = sentio

        self.paused = True
        self.directions_of_objects = list()

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
        game_instance = self.sentio.game_instances.get((self.current_time.half, self.current_time.milliseconds))
        teams = ReaderBase.divideIntoTeams(game_instance.players)
        self.set_positions_of_objects(teams)

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

        self.Bind(wx.EVT_MENU, self.on_save_plot, m_save)
        self.Bind(wx.EVT_MENU, self.on_open_plot, m_open)
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.Bind(wx.EVT_MENU, self.on_debug_mode, debug_mode)
        self.Bind(wx.EVT_MENU, self.on_about, m_about)

        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_view, "&View")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)


    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()


    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_flash_status_off, self.timeroff)
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
        self.slider = wx.Slider(self.panel, -1, value=0, minValue=0, maxValue=len(self.sentio.game_instances)-1)

        self.upbmp = wx.Bitmap(os.path.join(bitmapDir, "play.png"), wx.BITMAP_TYPE_PNG)
        self.disbmp = wx.Bitmap(os.path.join(bitmapDir, "pause.png"), wx.BITMAP_TYPE_PNG)
        self.play_button = SBitmapButton(self.panel, -1, self.upbmp, (48, 48), size=(40,40))

        self.Bind(wx.EVT_RADIOBOX, self.on_mouse_action, self.rb)
        self.Bind(wx.EVT_BUTTON, self.on_play_button, self.play_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_play_button, self.play_button)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_slider_release, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_shift, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_play_speed_slider, self.play_speed_slider)


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
        self.hbox_play.Add(self.play_button, 0, border=3, flag=wx.ALIGN_CENTER)
        self.hbox_play.Add(self.slider, 1, border=3, flag=wx.ALIGN_CENTER | wx.EXPAND)
        self.hbox_play.Add(self.current_time_display, 0, border=3, flag=flags)
        self.vbox.Add(self.hbox_play, 1,  wx.EXPAND)

        self.panel.SetSizer(self.vbox)


    def draw_figure(self):
        self.canvas.draw()


    ##### handling menu events #####
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png|CSV (*.csv)|*.csv"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir="../../SampleScenarios",
            defaultFile="plot",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if ".png" in dlg.GetFilename():
                self.canvas.print_figure(path, dpi=self.dpi)
            else:
                defined_passes = self.govern_passes.passes_defined
                directions = self.getDirectionsOfPlayersFor(self.current_time)
                speeds = self.getSpeedsOfPlayersFor(self.current_time)

                snapShot = SnapShot(path)
                snapShot.saveSnapShot(self.draggable_visual_teams, defined_passes, directions, speeds)
            self.flash_status_message("Saved to %s" % path)


    def on_open_plot(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()

            try: self.removeAllAnnotations()
            except: pass

            snapShot = SnapShot(file_path)
            teams, list_of_directions = snapShot.loadSnapShot(self.ax)

            self.directions_of_objects.extend(list_of_directions)

            self.remove_all_draggable_visual_players()
            self.set_positions_of_objects(teams)

            all_defined_passes = snapShot.displayAllPasses(file_path, self.ax, self.draggable_visual_teams, self.pass_info_page.logger)
            self.defined_passes_forSnapShot.extend(all_defined_passes)

            for team in (self.draggable_visual_teams):
                for draggable_visual_player in team.values():
                    draggable_visual_player.setDefinedPasses(self.defined_passes_forSnapShot)
                    draggable_visual_player.setDraggableVisualTeams(self.draggable_visual_teams)

            self.current_time_display.SetLabel("Time = %s.%s.%s" %("--", "--", "--"))
            self.canvas.draw()
            self.flash_status_message("Opened file %s" % file_path)
        dlg.Destroy()


    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')


    def on_exit(self, event):
        self.Destroy()


    def on_debug_mode(self, e):
        Parameters.IS_DEBUG_MODE_ON = not Parameters.IS_DEBUG_MODE_ON
        print Parameters.IS_DEBUG_MODE_ON


    def on_about(self, event):
        msg = """ Sport Analytics Project
        UI Designer: Emrullah Delibaş (dktry_)

         we are still working on it!!! ;)
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    ##### handling slider events #####
    def on_slider_release(self, event):
        slider_index = self.slider.GetValue()
        half, milliseconds = self.sentio.slider_mapping[slider_index]
        temp_time = Time(half, milliseconds)

        self.removeAllAnnotations()
        self.visualizePositionsFor(temp_time)


    def on_slider_shift(self, event):
        slider_index = self.slider.GetValue()
        half, milliseconds = self.sentio.slider_mapping[slider_index]
        temp_time = Time(half, milliseconds)

        formatted_time = Time.time_display(temp_time)
        self.current_time_display.SetLabel(formatted_time)
        self.current_time = temp_time


    def on_play_speed_slider(self, event):
        speeds = {1:"0.5", 2:"1", 3:"2", 4:"3", 5:"4"}

        self.play_speed = self.play_speed_slider.GetValue()
        self.play_speed_box.SetLabel("Speed = %sx"%speeds[self.play_speed])


    ##### handling radioBox events #####
    def on_mouse_action(self, event):
        q = event.GetInt()
        if q == 0:
            if self.directions_of_objects:
                self.remove_directionSpeedOfObjects()
            for team in (self.draggable_visual_teams):
                for draggable_visual_player in team.values():
                    draggable_visual_player.disconnect()
            self.govern_passes.connect()
        elif q == 1:
            if self.directions_of_objects:
                self.remove_directionSpeedOfObjects()
            self.govern_passes.disconnect()
            for team in (self.draggable_visual_teams):
                for draggable_visual_player in team.values():
                    draggable_visual_player.connect()


    ##### handling button events #####
    def on_update_play_button(self, event):
        bitmap = (self.upbmp if self.paused else self.disbmp)
        self.play_button.SetBitmapLabel(bitmap)


    def refresh_ui(self):
        self.remove_allDefinedPassesForSnapShot()
        self.remove_directionSpeedOfObjects()

        # self.pass_info_page.logger.Clear()
        self.govern_passes.heatMap.clear()


    def on_play_button(self, event):
        self.refresh_ui()
        self.remove_defined_passes()

        self.paused = not self.paused
        while not self.paused:
            chosenSkip = 0
            if self.play_speed == 1: tm.sleep(0.1)
            elif self.play_speed == 2: chosenSkip = 0
            elif self.play_speed == 3: chosenSkip = 1
            elif self.play_speed == 4: chosenSkip = 2
            elif self.play_speed == 5: chosenSkip = 4

            for skipTimes in range(chosenSkip+1):
                self.current_time.next()

            self.current_time_display.SetLabel(Time.time_display(self.current_time))
            self.slider.SetValue(self.current_time.milliseconds / 2.)

            self.visualizePositionsFor(self.current_time)
            wx.Yield()


    def visualizePositionsFor(self, time):
        self.updatePositionsOfPlayersFor(time)
        self.annotateGameEventsFor(time)
        self.canvas.draw()


    def annotateGameEventsFor(self, time):
        game_instance  = self.sentio.game_instances.get((time.half, time.milliseconds))
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

                    p_visual_ball_holder = self.convertCoordinatePlayerToVisualPlayerIn(pass_event.pass_source)
                    p_visual_ball_holder.set_bbox(dict(boxstyle="circle,pad=0.3", fc=pass_event.pass_source.getObjectColor(),
                                                      ec=pass_event.pass_source.getObjectTypeColor(), alpha=0.5, linewidth=1))

                    c_visual_ball_holder = self.convertCoordinatePlayerToVisualPlayerIn(pass_event.pass_target)
                    c_visual_ball_holder.set_bbox(dict(boxstyle="circle,pad=0.3", fc=pass_event.pass_target.getObjectColor(),
                                                 ec="yellow", linewidth=2))

                    pass_event_annotation = self.ax.annotate('', xy=pass_event.pass_target.get_position(),
                                                             xytext=pass_event.pass_source.get_position(), size=20,
                                                             arrowprops=dict(arrowstyle="->", fc=pass_event.pass_source.getObjectColor(),
                                                                          ec=pass_event.pass_source.getObjectColor(), alpha=1.0))

                    effectiveness = self.govern_passes.displayDefinedPass(pass_event, self.pass_info_page.logger)
                    self.pass_event_annotations.append(pass_event_annotation)
                    self.updatePassEventAnnotations()

                    if Parameters.IS_DEBUG_MODE_ON:
                        self.risk_range.drawRangeFor(pass_event)

                    ultX = ((pass_event.pass_target.getX() + pass_event.pass_source.getY()) / 2.)
                    ultY = ((pass_event.pass_target.getX() + pass_event.pass_source.getY()) / 2.)

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


    def convertCoordinatePlayerToVisualPlayerIn(self, coordinate_player):
        try:
            if coordinate_player.isHomeTeamPlayer():
                draggable_visual_player = self.draggable_visual_teams[0][coordinate_player.getJerseyNumber()]
            else:
                draggable_visual_player = self.draggable_visual_teams[1][coordinate_player.getJerseyNumber()]
        except AttributeError:
            print "missing data"
            return None
        return draggable_visual_player.visual_player


    def annotateDirectionSpeedOfObjects_forGivenTime(self, time):
        teams_for_direction = self.getDirectionsOfPlayersFor(time)
        teams_for_speed = self.getSpeedsOfPlayersFor(time)
        for team1, team2 in zip(teams_for_direction, teams_for_speed):
            for player1, player2 in zip(team1, team2):
                current_x, next_x = player1.getX()
                current_y, next_y = player1.getY()
                speed = player2.speed

                next_x, next_y = adjust_arrow_size((current_x, current_y), (next_x, next_y), speed)
                passAnnotation = self.ax.annotate('', xy=(next_x,next_y), xycoords='data', xytext=(current_x,current_y),
                                                  textcoords='data',size=20, va="center", ha="center", arrowprops=dict(
                        arrowstyle="simple", connectionstyle="arc3",
                        fc="cyan", ec="b", lw=2))
                self.directions_of_objects.append(passAnnotation)
        self.canvas.draw()


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
        for team in (self.draggable_visual_teams):
            for draggable_visual_player in team.values():
                draggable_visual_player.visual_player.remove()


    def updatePositionsOfPlayersFor(self, time):
        game_instance = self.sentio.game_instances.get((time.half, time.milliseconds))
        teams = ReaderBase.divideIntoTeams(game_instance.players)
        pre_teams = self.draggable_visual_teams
        for index, current_team in enumerate((teams.home_team, teams.away_team, teams.referees, teams.unknowns)):
            pre_team = pre_teams[index]
            current_team_set, pre_team_set = set(current_team.getJerseyNumbersOfPlayers()), set(pre_team)
            if current_team_set != pre_team_set:
                if len(current_team_set) == len(pre_team_set):
                    current_only_js = current_team_set.difference(pre_team_set)
                    pre_only_js = pre_team_set.difference(current_team_set)
                    for js_index, current_js in enumerate(current_only_js):
                        pre_team[current_js] = pre_team.pop(tuple(pre_only_js)[js_index])
                        pre_team[current_js].visual_player.set_text(current_js) # set jersey number
                elif len(current_team_set) < len(pre_team_set):
                    pre_only_js = pre_team_set.difference(current_team_set)
                    print pre_only_js
                    for pre_js in pre_only_js:
                        pre_team[pre_js].visual_player.remove()
                        del pre_team[pre_js]
                else:
                    current_only_js = current_team_set.difference(pre_team_set)
                    for current_js in current_only_js:
                        player = current_team.getTeamPlayersWithJS().get(current_js)
                        visual_player = self.ax.text(player.getX(),player.getY(),player.getJerseyNumber(),
                            zorder=1, color="w", fontsize=(9 if len(str(player.getJerseyNumber()))==1 else 7),
                            picker=True, bbox=dict(boxstyle="circle,pad=0.3", fc=player.getObjectColor(),
                                                   ec=player.getObjectTypeColor(), alpha=0.5, linewidth=1))
                        visual_player.player = player
                        draggable_visual_player = DraggablePlayer(visual_player)
                        pre_team[current_js] = draggable_visual_player

            for js in current_team.getTeamPlayersWithJS():
                draggable_visual_player = pre_team.get(js)
                draggable_visual_player.visual_player.set_position(current_team.getTeamPlayersWithJS()[js].get_position())


    def set_positions_of_objects(self, teams):
        self.draggable_visual_teams = ({},{},{},{})
        BoxStyle._style_list["circle"] = CircleStyle
        for index, team in enumerate((teams.home_team, teams.away_team, teams.referees, teams.unknowns)):
            for player in team.getTeamPlayers():
                visual_player = self.ax.text(player.getX(),player.getY(),player.getJerseyNumber(), zorder=1,
                                color="w", fontsize=(9 if len(str(player.getJerseyNumber()))==1 else 7), picker=True,
                                bbox=dict(boxstyle="circle,pad=0.3", fc=player.getObjectColor(),
                                          ec=player.getObjectTypeColor(), alpha=0.5, linewidth=1))
                visual_player.player = player
                draggable_visual_player = DraggablePlayer(visual_player)
                self.draggable_visual_teams[index][player.getJerseyNumber()] = draggable_visual_player

        self.govern_passes = DraggablePass(self.ax, self.draggable_visual_teams, self.fig)
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
        for team in (self.draggable_visual_teams):
            for draggable_visual_player in team.values():
                draggable_visual_player.setPassLogger(self.pass_info_page.logger)
                draggable_visual_player.setDefinedPasses(self.govern_passes.passes_defined)
                draggable_visual_player.setDraggableVisualTeams(self.draggable_visual_teams)


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








