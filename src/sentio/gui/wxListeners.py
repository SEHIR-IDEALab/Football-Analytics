# coding=utf-8

import wx
import time
from src.sentio import Parameters
from src.sentio.Parameters import GUI_FILE_DIALOG_DIRECTORY
from src.sentio.Time import Time
from src.sentio.gui.SnapShot import SnapShot

__author__ = 'emrullah'



class wxListeners:

    def __init__(self, wx_gui):
        self.wx_gui = wx_gui
        self.layouts = None


    ##### handling menu events #####
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png|XML (*.xml)|*.xml"

        dlg = wx.FileDialog(
            self.wx_gui,
            message="Save plot as...",
            defaultDir="../../SampleScenarios",
            defaultFile="plot",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            if ".png" in dlg.GetFilename():
                self.layouts.canvas.print_figure(file_path, dpi=self.layouts.dpi)
            else:
                SnapShot.save(file_path, self.wx_gui.visual_idToPlayers.values(), self.wx_gui.pass_manager.passes_defined)

            self.wx_gui.flash_status_message("Saved to %s" % file_path)


    def on_open_plot(self, event):
        dlg = wx.FileDialog(self.wx_gui, "Choose a file", GUI_FILE_DIALOG_DIRECTORY, "", "*.xml", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.wx_gui.snapShot = True
            file_path = dlg.GetPath()

            self.wx_gui.removeAllAnnotations()
            self.wx_gui.remove_visual_players()

            players, pass_events = SnapShot.load(file_path)
            self.wx_gui.setPositions(players, snapShot=self.wx_gui.snapShot)
            self.wx_gui.drawAndDisplayPassStats(pass_events)

            if Parameters.IS_SHOW_DIRECTIONS_ON:
                self.wx_gui.drawDirectionsWithSpeed()

            if Parameters.IS_VORONOI_DIAGRAM_ON:
                self.wx_gui.voronoi.update(self.wx_gui.getPositions())

            self.layouts.current_time_display.SetLabel("Time = %s.%s.%s" %("--", "--", "--"))
            self.layouts.canvas.draw()
            self.wx_gui.flash_status_message("Opened file %s" % file_path)
        dlg.Destroy()


    def on_flash_status_off(self, event):
        self.layouts.statusbar.SetStatusText('')


    def on_exit(self, event):
        self.wx_gui.Destroy()


    def on_debug_mode(self, e):
        Parameters.IS_DEBUG_MODE_ON = not Parameters.IS_DEBUG_MODE_ON
        print "debug mode: ", Parameters.IS_DEBUG_MODE_ON


    def on_show_directions(self, e):
        Parameters.IS_SHOW_DIRECTIONS_ON = not Parameters.IS_SHOW_DIRECTIONS_ON
        print "show directions: ", Parameters.IS_SHOW_DIRECTIONS_ON

        if Parameters.IS_SHOW_DIRECTIONS_ON:
            self.wx_gui.drawDirectionsWithSpeed()
        else:
            self.wx_gui.clearDirections()

        self.layouts.canvas.draw()


    def on_voronoi_diagram(self, e):
        Parameters.IS_VORONOI_DIAGRAM_ON = not Parameters.IS_VORONOI_DIAGRAM_ON
        print "voronoi diagram: ", Parameters.IS_VORONOI_DIAGRAM_ON

        if Parameters.IS_VORONOI_DIAGRAM_ON:
            self.wx_gui.voronoi.update(self.wx_gui.getPositions())
        else:
            self.wx_gui.voronoi.remove()

        self.layouts.canvas.draw()


    def on_about(self, event):
        msg = """ Sport Analytics Project
        UI Designer: Emrullah Delibaş (dktry_)

         we are still working on it!!! ;)
        """
        dlg = wx.MessageDialog(self.wx_gui, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    ##### handling slider events #####
    def on_slider_release(self, event):
        self.wx_gui.snapShot = False
        slider_index = self.layouts.slider.GetValue()
        temp_time = self.wx_gui.sentio.slider_mapping[slider_index]

        self.wx_gui.removeAllAnnotations()
        self.wx_gui.visualizePositionsFor(temp_time)


    def on_slider_shift(self, event):
        slider_index = self.layouts.slider.GetValue()
        temp_time = self.wx_gui.sentio.slider_mapping[slider_index]

        formatted_time = Time.time_display(temp_time)
        self.layouts.current_time_display.SetLabel(formatted_time)
        self.wx_gui.current_time = temp_time


    def on_play_speed_slider(self, event):
        speeds = {1:"0.5", 2:"1", 3:"2", 4:"3", 5:"4"}

        self.wx_gui.play_speed = self.layouts.play_speed_slider.GetValue()
        self.layouts.play_speed_box.SetLabel("Speed = %sx"%speeds[self.wx_gui.play_speed])

        if self.wx_gui.play_speed > 2:
            self.wx_gui.removeAllAnnotations()


    ##### handling radioBox events #####
    def on_mouse_action(self, event):
        q = event.GetInt()
        if q == 0:
            # if self.wx_gui.directions_of_objects:
            #     self.wx_gui.remove_directionSpeedOfObjects()
            for visual_player in self.wx_gui.visual_idToPlayers.values():
                visual_player.draggable.disconnect()
            self.wx_gui.pass_manager.connect()
        elif q == 1:
            # if self.wx_gui.directions_of_objects:
            #     self.wx_gui.remove_directionSpeedOfObjects()
            self.wx_gui.pass_manager.disconnect()
            for visual_player in self.wx_gui.visual_idToPlayers.values():
                visual_player.draggable.connect()


    ##### handling button events #####
    def on_update_play_button(self, event):
        bitmap = (self.layouts.upbmp if self.wx_gui.paused else self.layouts.disbmp)
        self.layouts.play_button.SetBitmapLabel(bitmap)


    def on_play_button(self, event):
        if self.wx_gui.snapShot:
            # self.wx_gui.removePassEventAnnotations()
            # self.layouts.pass_info_page.logger.Clear()
            self.wx_gui.removeAllAnnotations()
            self.wx_gui.snapShot = False

        self.wx_gui.removeManualPassEventAnnotations()
        self.wx_gui.pass_manager.heatMap.clear()

        self.wx_gui.paused = not self.wx_gui.paused
        while not self.wx_gui.paused:
            chosenSkip = 0
            if self.wx_gui.play_speed == 1: time.sleep(0.1)
            elif self.wx_gui.play_speed == 2: chosenSkip = 0
            elif self.wx_gui.play_speed == 3: chosenSkip = 1
            elif self.wx_gui.play_speed == 4: chosenSkip = 2
            elif self.wx_gui.play_speed == 5: chosenSkip = 4

            for skipTimes in range(chosenSkip+1):
                self.wx_gui.current_time.next()

            self.layouts.current_time_display.SetLabel(Time.time_display(self.wx_gui.current_time))
            self.layouts.slider.SetValue(self.getSliderValue())

            self.wx_gui.visualizePositionsFor(self.wx_gui.current_time, chosen_skip=chosenSkip)
            wx.Yield()


    def getSliderValue(self):
        total = 0
        if self.wx_gui.current_time.half != 1:
            for i in range(1, self.wx_gui.current_time.half):
                total += self.wx_gui.sentio.game_instances.getTotalNumberIn(i)
        return self.wx_gui.current_time.milliseconds / 2.0 + total


    def activate(self):
        self.wx_gui.Bind(wx.EVT_MENU, self.on_save_plot, self.layouts.m_save)
        self.wx_gui.Bind(wx.EVT_MENU, self.on_open_plot, self.layouts.m_open)
        self.wx_gui.Bind(wx.EVT_MENU, self.on_exit, self.layouts.m_exit)
        self.wx_gui.Bind(wx.EVT_MENU, self.on_debug_mode, self.layouts.debug_mode)
        self.wx_gui.Bind(wx.EVT_MENU, self.on_show_directions, self.layouts.show_directions)
        self.wx_gui.Bind(wx.EVT_MENU, self.on_voronoi_diagram, self.layouts.voronoi_diagram)
        self.wx_gui.Bind(wx.EVT_MENU, self.on_about, self.layouts.m_about)

        self.wx_gui.Bind(wx.EVT_RADIOBOX, self.on_mouse_action, self.layouts.rb)
        self.wx_gui.Bind(wx.EVT_BUTTON, self.on_play_button, self.layouts.play_button)
        self.wx_gui.Bind(wx.EVT_UPDATE_UI, self.on_update_play_button, self.layouts.play_button)
        self.wx_gui.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_slider_release, self.layouts.slider)
        self.wx_gui.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_shift, self.layouts.slider)
        self.wx_gui.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_play_speed_slider, self.layouts.play_speed_slider)



