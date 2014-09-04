# coding=utf-8
import matplotlib
from src.sentio.Parameters import *

matplotlib.use('WXAgg')

import time as tm
import math
from matplotlib.patches import BoxStyle
from wx.lib.agw.shapedbutton import SBitmapButton
from src.sentio.CircleStyle import CircleStyle
from src.sentio.DraggablePass import DraggablePass
from src.sentio.DraggableText import DraggableText
from src.sentio.SnapShot import *
from src.sentio.Time import Time

import os
import wx
import wx.media

# The recommended way to use wx with mpl is with the WXAgg
# backend.
#

import numpy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar


__author__ = 'emrullah'

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'source/bitmaps')


class PageOne(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.logger = wx.TextCtrl(self, size=(150,530), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font1 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, u'Tahoma')
        self.logger.SetFont(font1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.logger, 1, wx.EXPAND)

        self.SetSizer(vbox)
        #vbox.Fit(self)


class PageTwo(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        heat_map_types = ['-----', 'defence position','position of target', 'position of source']
        comp_of_effectiveness = ["overall risk", "gain", "pass advantage", "goal chance", "effectiveness"]
        self.heat_map = wx.ComboBox(self, size=(80,-1), choices=heat_map_types, style=wx.CB_READONLY)
        self.effectiveness = wx.ComboBox(self, size=(80,-1), choices=comp_of_effectiveness, style=wx.CB_READONLY)
        self.resolution = wx.Slider(self, -1, value=2, minValue=0.5, maxValue=5)

        self.heat_map_label = wx.StaticText(self, label="Heatmap Type")
        self.resolution_label = wx.StaticText(self, label=("Resolution = %s"%self.resolution.GetValue()))
        self.effectiveness_label = wx.StaticText(self, label="Display Value")

        self.vmin_auto_rbutton = wx.RadioButton(self, -1, label="auto", style=wx.RB_GROUP)
        self.vmin_custom_rbutton = wx.RadioButton(self, -1, label="custom")
        self.vmin_custom_entry = wx.TextCtrl(self, size=(50,-1))

        self.colorbar_refresh_button = wx.Button(self, -1, "Refresh")

        self.vmax_auto_rbutton = wx.RadioButton(self, -1, label="auto", style=wx.RB_GROUP)
        self.vmax_custom_rbutton = wx.RadioButton(self, -1, label="custom")
        self.vmax_custom_entry = wx.TextCtrl(self, size=(50,-1))

        ### colorbar canvas
        fig = Figure((0.7,3))
        fig.set_facecolor((0.875, 0.875, 0.875, 1.0))
        ax1 = fig.add_axes([0, 0.03, 0.4,0.94])
        self.colorbar_canvas = FigCanvas(self, -1, fig)

        #cmap = matplotlib.cm.hot
        #norm = matplotlib.colors.Normalize(vmin=0, vmax=0)
        self.color_bar = matplotlib.colorbar.ColorbarBase(ax1, orientation='vertical')
        self.color_bar.ax.tick_params(labelsize=8)

        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_resolution, self.resolution)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_vmin_custom, self.vmin_custom_rbutton)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_vmax_custom, self.vmax_custom_rbutton)

        vbox = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(8, 1, 0, 25)
        fgs.AddMany([(self.heat_map_label),
                     (self.heat_map, 1, wx.EXPAND),
                     (wx.StaticText(self), wx.EXPAND),
                     (self.effectiveness_label),
                     (self.effectiveness, 1, wx.EXPAND),
                     (wx.StaticText(self), wx.EXPAND),
                     (self.resolution_label),
                     (self.resolution, 1, wx.EXPAND)])
        vbox.Add(fgs)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(self, style=wx.HORIZONTAL, size=(150,2)), 0, wx.ALIGN_CENTER)
        vbox.AddSpacer(10)

        color_logend_box = wx.StaticBox(self, wx.ID_ANY, "Color Legend")
        color_logend_box_sizer = wx.StaticBoxSizer(color_logend_box, wx.HORIZONTAL)

        self.vbox_colorbar_options = wx.BoxSizer(wx.VERTICAL)

        colorbar_vmax_box = wx.StaticBox(self, wx.ID_ANY, "max")
        colorbar_vmax_box_sizer = wx.StaticBoxSizer(colorbar_vmax_box, wx.VERTICAL)
        colorbar_vmax_box_sizer.Add(self.vmax_auto_rbutton)
        hbox_max_custom = wx.BoxSizer(wx.VERTICAL)
        hbox_max_custom.Add(self.vmax_custom_rbutton)
        hbox_max_custom.Add(self.vmax_custom_entry, 0, wx.ALIGN_RIGHT)
        colorbar_vmax_box_sizer.Add(hbox_max_custom)
        self.vbox_colorbar_options.Add(colorbar_vmax_box_sizer, 0, wx.ALIGN_TOP|wx.ALIGN_CENTER)

        self.vbox_colorbar_options.Add(self.colorbar_refresh_button, 1, wx.ALIGN_CENTER)

        colorbar_vmin_box = wx.StaticBox(self, wx.ID_ANY, "min")
        colorbar_vmin_box_sizer = wx.StaticBoxSizer(colorbar_vmin_box, wx.VERTICAL)
        colorbar_vmin_box_sizer.Add(self.vmin_auto_rbutton)
        hbox_min_custom = wx.BoxSizer(wx.VERTICAL)
        hbox_min_custom.Add(self.vmin_custom_rbutton)
        hbox_min_custom.Add(self.vmin_custom_entry, 0, wx.ALIGN_RIGHT)
        colorbar_vmin_box_sizer.Add(hbox_min_custom)
        self.vbox_colorbar_options.Add(colorbar_vmin_box_sizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER)

        color_logend_box_sizer.Add(self.vbox_colorbar_options, 1, wx.EXPAND)
        color_logend_box_sizer.Add(self.colorbar_canvas, 0, wx.EXPAND)

        vbox.Add(color_logend_box_sizer, 1, wx.EXPAND)
        self.SetSizer(vbox)
        #vbox.Fit(self)


    def on_vmin_custom(self, event):
        self.vmin_custom_entry.Enable()


    def on_vmax_custom(self, event):
        self.vmax_custom_entry.Enable()


    def on_resolution(self, event):
        q = ("Resolution = %s" % self.resolution.GetValue())
        self.resolution_label.SetLabel(q)


class wxVisualization(wx.Frame):

    dirname=''
    title = "Sport Analytics Tool - IDEA Lab"

    def __init__(self, sentio, team_names):
        wx.Frame.__init__(self, None, -1, self.title, pos=(0,20), size=(1200,750))

        self.sentio = sentio
        self.team_names = team_names
        self.coordinatesData_byTime = self.sentio.getCoordinateData_byTime()
        self.event_id_explanation = self.sentio.get_ID_Explanation()

        self.paused = True
        self.directions_of_objects = list()

        self.current_time = Time(1,0,0,0)
        self.current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)

        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        self.layout_controls()

        self.definePasses = None
        self.definedPasses_forSnapShot = list()

        self.trailAnnotations, self.eventAnnotation, self.passAnnotations, self.passEffectivenessAnnotation = \
            [], None, [], None

        self.passEffectiveness_count = 0
        self.play_speed = 2

        teams = self.getObjectsCoords_forGivenTime(Time(1,0,0,0))
        self.set_positions_of_objects(teams)

        self.draw_figure()


    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_save = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        m_open = menu_file.Append(wx.ID_OPEN, "&Open"," Open a snapshot to display")
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "&Exit\tCtrl-X", "Exit")

        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the tool")

        self.Bind(wx.EVT_MENU, self.on_save_plot, m_save)
        self.Bind(wx.EVT_MENU, self.on_open_plot, m_open)
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.Bind(wx.EVT_MENU, self.on_about, m_about)

        self.menubar.Append(menu_file, "&File")
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

        im = plt.imread('source/background.png')
        self.ax.imshow(im, zorder=0, extent=[FOOTBALL_FIELD_MIN_X-4.5, FOOTBALL_FIELD_MAX_X+4.5,
                                             FOOTBALL_FIELD_MIN_Y-1.5, FOOTBALL_FIELD_MAX_Y+1.5])
        self.ax.grid()
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X+5, 5))
        self.ax.set_yticks(numpy.arange(FOOTBALL_FIELD_MIN_Y, FOOTBALL_FIELD_MAX_Y+5, 5))
        self.ax.tick_params(axis="both", labelsize=6)

        a,b,c,d, = plt.plot([],[],"bo",[],[],"ro",[],[],"yo",[],[],"ko", markersize=6)
        self.ax.legend([a,b,c,d], [self.team_names[0].decode("utf-8"), self.team_names[1].decode("utf-8"), 'Referees',
                                   'Unknown Objects'], numpoints=1, fontsize=6, bbox_to_anchor=(0., 1.0, 1., .102),
                       loc=3, ncol=4, mode="expand", borderaxespad=0.5)

        self.current_time_display = wx.StaticText(self.panel, -1, "Time = 1_00:00:00")

        radioList = ['New Pass', 'Drag Object']
        self.rb = wx.RadioBox(self.panel,label="Mouse Action",choices=radioList, majorDimension=1,
                              style=wx.RA_SPECIFY_COLS)

        self.play_speed_slider = wx.Slider(self.panel, -1, value=2, minValue=1, maxValue=5)
        self.slider = wx.Slider(self.panel, -1, value=0, minValue=0, maxValue=self.get_milliseconds_for_slider())

        self.upbmp = wx.Bitmap(os.path.join(bitmapDir, "play.png"), wx.BITMAP_TYPE_PNG)
        self.disbmp = wx.Bitmap(os.path.join(bitmapDir, "pause.png"), wx.BITMAP_TYPE_PNG)
        self.play_button = SBitmapButton(self.panel, -1, self.upbmp, (48, 48), size=(40,40))

        self.Bind(wx.EVT_RADIOBOX, self.on_mouse_action, self.rb)
        self.Bind(wx.EVT_BUTTON, self.on_play_button, self.play_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_play_button, self.play_button)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_slider_release, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_shift, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_play_speed_slider, self.play_speed_slider)


    def get_milliseconds_for_slider(self):
        total = 0
        q = Time.compute_minMaxOfHalf_inMilliseconds(self.sentio.minMaxOfHalf)
        for half in q:
            half_min_milliseconds, half_max_milliseconds = q[half]
            total += (half_max_milliseconds - half_min_milliseconds)/2. + 1
        return total - 1


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
                current_time = self.current_time
                defined_passes = self.definePasses.definedPasses
                directions = self.getDirectionOfObjects_forGivenTime(current_time)
                speeds = self.getSpeedOfObjects_forGivenTime(current_time)

                print directions
                print speeds

                snapShot = SnapShot(path)
                snapShot.saveSnapShot(self.team_names, self.texts, defined_passes, directions, speeds)
            self.flash_status_message("Saved to %s" % path)


    def on_open_plot(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            self.remove_directionSpeedOfObjects()
            self.remove_allDefinedPassesForSnapShot()
            self.remove_eventAnnotation()
            self.remove_passAnnotations()
            self.remove_trailAnnotations()
            self.remove_passEffectivenessAnnotation()
            self.pass_info_page.logger.Clear()

            snapShot = SnapShot(path)
            teams, list_of_directions = snapShot.loadSnapShot(self.ax)

            self.directions_of_objects.extend(list_of_directions)

            self.remove_all_objects()
            self.set_positions_of_objects(teams)

            all_defined_passes = snapShot.displayAllPasses(path, self.ax, self.texts, self.pass_info_page.logger)
            self.definedPasses_forSnapShot.extend(all_defined_passes)

            for team in self.texts:
                for js in team:
                    draggableText = team[js]
                    draggableText.set_definedPasses(self.definedPasses_forSnapShot)
                    draggableText.set_coordinatesOfObjects(self.texts)

            self.current_time_display.SetLabel("Time = %s.%s.%s" %("--", "--", "--"))
            self.canvas.draw()
            self.flash_status_message("Opened file %s" % path)
        dlg.Destroy()


    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')


    def on_exit(self, event):
        self.Destroy()


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
        milliseconds = self.slider.GetValue()
        time = Time()
        time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        time_adjust = time.milliseconds_to_time(milliseconds*2)
        self.visualizeCurrentPosition(time_adjust, skip_times=0)


    def on_slider_shift(self, event):
        milliseconds = self.slider.GetValue()
        time = Time()
        time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        time = time.milliseconds_to_time(milliseconds*2)

        formatted_time = Time.time_display(time)
        self.current_time_display.SetLabel(formatted_time)
        self.current_time = time


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
            for team in self.texts:
                for player_js in team.values():
                    player_js.disconnect()
            self.definePasses.connect()
        elif q == 1:
            if self.directions_of_objects:
                self.remove_directionSpeedOfObjects()
            self.definePasses.disconnect()
            for team in self.texts:
                for player_js in team.values():
                    player_js.connect()


    ##### handling button events #####
    def on_update_play_button(self, event):
        bitmap = (self.upbmp if self.paused else self.disbmp)
        self.play_button.SetBitmapLabel(bitmap)


    def refresh_ui(self):
        self.remove_allDefinedPassesForSnapShot()
        self.remove_directionSpeedOfObjects()

        #self.pass_info_page.logger.Clear()
        self.definePasses.heatMap.clear()


    def on_play_button(self, event):
        self.refresh_ui()

        self.paused = not self.paused

        current_time = self.current_time
        current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)

        self.remove_defined_passes()

        while not self.paused:
            chosenSkip = 0
            if self.play_speed == 1: tm.sleep(0.1)
            elif self.play_speed == 2: chosenSkip = 0
            elif self.play_speed == 3: chosenSkip = 1
            elif self.play_speed == 4: chosenSkip = 2
            elif self.play_speed == 5: chosenSkip = 4

            for skipTimes in range(chosenSkip+1):
                self.current_time  = current_time.next()

            self.current_time_display.SetLabel(Time.time_display(self.current_time))
            self.slider.SetValue(self.current_time.get_in_milliseconds() / 2.)

            self.visualizeCurrentPosition(self.current_time, chosenSkip)
            self.current_time.next()

            wx.Yield()


    def visualizeCurrentPosition(self, time, skip_times):
        teams = self.getObjectsCoords_forGivenTime(time)
        self.reposition_objects(teams)
        self.annotate_currentEvent(time, teams, skip_times)

        self.canvas.draw()


    def annotate_currentEvent_base(self, event_data, homeTeamPlayers, awayTeamPlayers):
        homeTeamName, awayTeamName = self.team_names
        teamName, js, eventID = event_data[0]
        player = None
        try:
            if teamName == homeTeamName: player = self.texts[0][js]
            elif teamName == awayTeamName: player = self.texts[1][js]
        except KeyError:
            print "missing data"

        if player != None: return (player.point, eventID)
        else: return (player, eventID)


    def annotate_currentEvent(self, time, teams, skip_times): # not completed
        homeTeamPlayers, awayTeamPlayers, referees, unknown_objects = teams
        eventData_current = self.sentio.get_currentEventData(time)
        player_current, eventID_current = self.annotate_currentEvent_base(eventData_current,
                                                                          homeTeamPlayers, awayTeamPlayers)
        if self.passEffectiveness_count != 0:
            self.passEffectiveness_count += 1
            if self.passEffectiveness_count == 5: self.remove_passEffectivenessAnnotation()
        self.remove_eventAnnotation()

        if eventID_current != 1:
            self.remove_ball_owner_annotation()
            self.eventAnnotation = self.ax.annotate(self.event_id_explanation[eventID_current], xy=(52.5,32.5),  xycoords='data',
                                                    va="center", ha="center", xytext=(0, 0), textcoords='offset points', size=20,
                                                    bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5), alpha=0.5))
            self.remove_passAnnotations()
            self.remove_trailAnnotations()
        else:
            eventData_previous = self.sentio.get_previousEventData(time, skip_times)
            player_previous, eventID_previous = self.annotate_currentEvent_base(eventData_previous,
                                                                                homeTeamPlayers, awayTeamPlayers)
            if player_current == None or player_previous == None:
                return

            if player_current != player_previous:
                if eventID_previous not in [2, 12]:
                    player_current.set_bbox(dict(boxstyle="circle,pad=0.3", fc=player_current.object_color,
                                             ec="yellow", linewidth=2))
                    player_previous.set_bbox(dict(boxstyle="circle,pad=0.3", fc=player_previous.object_color,
                                                  ec=player_previous.object_type_color, alpha=0.5, linewidth=1))

                    passAnnotation = self.ax.annotate('', xy=player_current.get_position(), xycoords=(player_current),
                                                      xytext=player_previous.get_position(), textcoords=(player_previous),
                                                      arrowprops=dict(fc=player_previous.object_color,
                                                                      ec=player_previous.object_color))

                    effectiveness = self.definePasses.displayDefinedPass(passAnnotation, self.pass_info_page.logger)
                    self.passAnnotations.append(passAnnotation)
                    self.adjust_passAnnotations()

                    ultX = ((player_current.get_position()[0] + player_previous.get_position()[0]) / 2.)
                    ultY = ((player_current.get_position()[1] + player_previous.get_position()[1]) / 2.)
                    self.remove_passEffectivenessAnnotation()
                    self.passEffectivenessAnnotation = self.ax.annotate(("effectiveness %.2f"%(effectiveness)),
                        xy=(ultX-10, ultY), xycoords="data", va="center", ha="center", xytext=(ultX-10, ultY),
                        textcoords="offset points", size=10, bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7),
                                                                       ec=(1., .5, .5), alpha=0.5))
                    self.passEffectiveness_count = 1


                    self.entire_trailX, self.entire_trailY = [player_current.get_position()[0]],[player_current.get_position()[1]]
                    trailAnnotation, = self.ax.plot(self.entire_trailX, self.entire_trailY, linestyle="--",
                                                         linewidth=2, color="yellow")
                    trailAnnotation.player = player_current
                    self.trailAnnotations.append(trailAnnotation)
                    self.adjust_trailAnnotations()
            else:
                if self.trailAnnotations != []:
                    self.entire_trailX.append(player_current.get_position()[0]), self.entire_trailY.append(player_current.get_position()[1])
                    c_trailAnnotation = self.trailAnnotations[-1]
                    c_trailAnnotation.set_data(self.entire_trailX, self.entire_trailY)
                else:
                    self.entire_trailX, self.entire_trailY = [player_current.get_position()[0]],[player_current.get_position()[1]]
                    trailAnnotation, = self.ax.plot(self.entire_trailX, self.entire_trailY, linestyle="--",
                                                         linewidth=2, color="yellow")
                    trailAnnotation.player = player_current
                    self.trailAnnotations.append(trailAnnotation)
                    self.adjust_trailAnnotations()


    def remove_ball_owner_annotation(self):
        teams = self.texts
        for team in teams:
            for js in team:
                player = team[js].point
                player.set_bbox(dict(boxstyle="circle,pad=0.3", fc=player.object_color,
                                              ec=player.object_type_color, alpha=0.5, linewidth=1))


    def annotateDirectionSpeedOfObjects_forGivenTime(self, time):
        list_of_directions_of_objects = self.getDirectionOfObjects_forGivenTime(time)
        teams = self.getSpeedOfObjects_forGivenTime(time)
        for index, team in enumerate(list_of_directions_of_objects):
            for js in team:
                player = team[js]
                current_x, next_x = player.getPositionX()
                current_y, next_y = player.getPositionY()
                speed = teams[index][js]

                next_x, next_y = adjust_arrow_size((current_x, current_y), (next_x, next_y), speed)
                passAnnotation = self.ax.annotate('', xy=(next_x,next_y), xycoords='data', xytext=(current_x,current_y),
                                                  textcoords='data',size=20, va="center", ha="center", arrowprops=dict(
                        arrowstyle="simple", connectionstyle="arc3",
                        fc="cyan", ec="b", lw=2))
                self.directions_of_objects.append(passAnnotation)
        self.canvas.draw()


    def getDirectionOfObjects_forGivenTime(self, time): # should be rewritten
        current_time = time
        current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(current_time)
        teams = [homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]
        for team in teams:
            for js in team:
                player_base = team[js]
                coordX, coordY = player_base.get_position()
                player_base.set_position(([coordX],[coordY]))
        next_time = current_time.next()
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(next_time)
        for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for js in team:
                    try:
                        player_base = team[js]
                        coordX, coordY= player_base.get_position()
                        ult_player_base = teams[index][js]
                        x, y = ult_player_base.getPositionX(), ult_player_base.getPositionY()
                        x.append(coordX), y.append(coordY)
                    except:
                        pass
        return teams


    def getSpeedOfObjects_forGivenTime(self, time): # should be rewritten
        current_time = time
        current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(current_time)
        teams = [homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]
        for team in teams:
            for js in team:
                player_base = team[js]
                coordX, coordY = player_base.get_position()
                player_base.set_position(([coordX],[coordY]))
        for i in range(5):
            pre_time = current_time.back()
            homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(pre_time)
            for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for js in team:
                    player_base = team[js]
                    coordX, coordY= player_base.get_position()
                    ult_player_base = teams[index][js]
                    x, y = ult_player_base.getPositionX(), ult_player_base.getPositionY()
                    x.append(coordX), y.append(coordY)
        for team in teams:
            for js in team:
                player_base = team[js]
                coordsX, coordsY = player_base.get_position()
                total = 0.0
                for i in range(5):
                    try:
                        x_current, y_current = coordsX[i], coordsY[i]
                        x_previous, y_previous = coordsX[i+1], coordsY[i+1]
                        total += math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                    except:
                        pass
                team[js] = total
        return teams


    def getObjectsCoords_forGivenTime(self, time):
        coordinatesData_current = self.coordinatesData_byTime[time.half][time.minute][time.second][time.millisecond]
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = {},{},{},{}
        for object_info in coordinatesData_current:
            player = Player_base(object_info)
            q = player.getObjectType()
            if q in [0,3]: homeTeamPlayers[player.getJerseyNumber()] = player
            elif q in [1,4]: awayTeamPlayers[player.getJerseyNumber()] = player
            elif q in [2,6,7,8,9]: referees[player.getJerseyNumber()] = player
            else: unknownObjects[player.getJerseyNumber()] = player
        teams = (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)
        return teams


    def reposition_objects(self, teams):
        pre_teams = self.texts
        current_teams = teams
        for index, current_team in enumerate(current_teams):
            pre_team = pre_teams[index]
            current_team_set, pre_team_set = set(current_team), set(pre_team)
            if current_team_set != pre_team_set:
                if len(current_team_set) == len(pre_team_set):
                    current_only_js = current_team_set.difference(pre_team_set)
                    pre_only_js = pre_team_set.difference(current_team_set)
                    for js_index, current_js in enumerate(current_only_js):
                        pre_team[current_js] = pre_team.pop(tuple(pre_only_js)[js_index])
                        pre_team[current_js].point.set_text(current_js) # set jersey number
                elif len(current_team_set) < len(pre_team_set):
                    pre_only_js = pre_team_set.difference(current_team_set)
                    print pre_only_js
                    for pre_js in pre_only_js:
                        pre_team[pre_js].point.remove()
                        del pre_team[pre_js]
                else:
                    current_only_js = current_team_set.difference(pre_team_set)
                    for current_js in current_only_js:
                        player = current_team[current_js]
                        temp_player = self.ax.text(player.getPositionX(),player.getPositionY(),player.getJerseyNumber(),
                            zorder=1, color="w", fontsize=(9 if len(str(player.getJerseyNumber()))==1 else 7),
                            picker=True, bbox=dict(boxstyle="circle,pad=0.3", fc=player.getObjectColor(),
                                                   ec=player.getObjectTypeColor(), alpha=0.5, linewidth=1))
                        temp_player.object_type = player.getObjectType()
                        temp_player.object_id = player.getObjectID()
                        temp_player.jersey_number = player.getJerseyNumber()
                        temp_player.object_color = player.getObjectColor()
                        temp_player.object_type_color = player.getObjectTypeColor()
                        dr = DraggableText(temp_player)
                        pre_team[current_js] = dr

            current_team = current_teams[index]
            for js in current_team:
                player = pre_team[js]
                player.point.set_position(current_team[js].get_position())


    def set_positions_of_objects(self, teams):
        self.texts = ( {}, {}, {}, {} )
        BoxStyle._style_list["circle"] = CircleStyle
        for index, team in enumerate(teams):
            current_team = self.texts[index]
            for js in team:
                player = team[js]
                player_js = self.ax.text(player.getPositionX(),player.getPositionY(),player.getJerseyNumber(), zorder=1,
                                color="w", fontsize=(9 if len(str(player.getJerseyNumber()))==1 else 7), picker=True,
                                bbox=dict(boxstyle="circle,pad=0.3", fc=player.getObjectColor(),
                                          ec=player.getObjectTypeColor(), alpha=0.5, linewidth=1))
                player_js.object_type = player.getObjectType()
                player_js.object_id = player.getObjectID()
                player_js.jersey_number = player.getJerseyNumber()
                player_js.object_color = player.getObjectColor()
                player_js.object_type_color = player.getObjectTypeColor()
                dr = DraggableText(player_js)
                current_team[player.getJerseyNumber()] = dr
        self.definePasses = DraggablePass(self.ax, self.texts, self.fig)
        self.definePasses.set_defined_passes(self.definedPasses_forSnapShot)
        self.definePasses.set_passDisplayer(self.pass_info_page.logger)
        self.definePasses.set_variables(self.heatmap_setup_page.heat_map, self.heatmap_setup_page.resolution,
                                        self.heatmap_setup_page.effectiveness)
        self.definePasses.heatMap.set_color_bar(self.heatmap_setup_page.color_bar,
                                                self.heatmap_setup_page.colorbar_canvas)
        self.definePasses.heatMap.set_color_bar_listeners((self.heatmap_setup_page.vmin_auto_rbutton,
                                                           self.heatmap_setup_page.vmin_custom_rbutton,
                                                           self.heatmap_setup_page.vmin_custom_entry),
                                                          (self.heatmap_setup_page.vmax_auto_rbutton,
                                                           self.heatmap_setup_page.vmax_custom_rbutton,
                                                           self.heatmap_setup_page.vmax_custom_entry),
                                                          self.heatmap_setup_page.colorbar_refresh_button)
        for team in self.texts:
            for js in team:
                draggableText = team[js]
                draggableText.set_passDisplayer(self.pass_info_page.logger)
                draggableText.set_definedPasses(self.definePasses.definedPasses)
                draggableText.set_coordinatesOfObjects(self.texts)


    def remove_defined_passes(self):
        if self.definePasses.definedPasses:
            for i in self.definePasses.definedPasses: i.remove()
            del self.definePasses.definedPasses[:]


    def remove_all_objects(self):
        teams = self.texts
        if teams:
            for team in teams:
                for player in team.values():
                    player = player.point
                    player.remove()
        self.texts = ({},{},{},{})


    def remove_directionSpeedOfObjects(self):
        if self.directions_of_objects:
            for i in self.directions_of_objects:
                i.remove()
            del self.directions_of_objects[:]
            self.canvas.draw()


    def remove_allDefinedPassesForSnapShot(self):
        if self.definedPasses_forSnapShot:
            for i in self.definedPasses_forSnapShot:
                i.remove()
            del self.definedPasses_forSnapShot[:]
            self.canvas.draw()


    def remove_eventAnnotation(self):
        if self.eventAnnotation != None:
            self.eventAnnotation.remove(); del self.eventAnnotation; self.eventAnnotation = None


    def remove_passAnnotations(self):
        if self.passAnnotations != []:
            for passAnnotation in self.passAnnotations:
                passAnnotation.remove()
            del self.passAnnotations[:]


    def adjust_passAnnotations(self):
        if self.passAnnotations != []:
            temp_passAnnotations = []
            for passAnnotation in self.passAnnotations[-3:-1]:
                temp_passAnnotation = self.ax.annotate('', xy=passAnnotation.xy, xytext=passAnnotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=passAnnotation.arrowprops["fc"],
                                                  ec=passAnnotation.arrowprops["ec"], alpha=0.5))
                temp_passAnnotations.append(temp_passAnnotation)

            c_passAnnotation = self.passAnnotations[-1]
            temp_passAnnotations.append(self.ax.annotate('', xy=c_passAnnotation.xy, xytext=c_passAnnotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=c_passAnnotation.arrowprops["fc"],
                                                  ec=c_passAnnotation.arrowprops["ec"], alpha=1.0)))

            for passAnnotation in self.passAnnotations: passAnnotation.remove()
            self.passAnnotations = temp_passAnnotations


    def adjust_trailAnnotations(self):
        if self.trailAnnotations != []:

            while len(self.trailAnnotations) > 3:
                self.trailAnnotations[0].remove()
                del self.trailAnnotations[0]

            for trailAnnotation in self.trailAnnotations[-3:-1]:
                trailAnnotation.set_alpha(0.5)
                trailAnnotation.set_color(trailAnnotation.player.object_color)


    def remove_trailAnnotations(self):
        if self.trailAnnotations !=[]:
            for trailAnnotation in self.trailAnnotations:
                trailAnnotation.remove()
            del self.trailAnnotations[:]


    def remove_passEffectivenessAnnotation(self):
        if self.passEffectivenessAnnotation != None:
            self.passEffectivenessAnnotation.remove(); del self.passEffectivenessAnnotation
            self.passEffectivenessAnnotation = None






