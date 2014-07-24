# coding=utf-8

import matplotlib

matplotlib.use('WXAgg')

import time as tm
import math
from matplotlib.patches import BoxStyle
from wx.lib.agw.shapedbutton import SBitmapToggleButton, SBitmapButton
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
from matplotlib.widgets import RadioButtons, Slider
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar



__author__ = 'emrullah'

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, '../sentio/source/bitmaps')


class PageOne(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.pass_info_logger = wx.TextCtrl(self, size=(200,500), style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.pass_info_logger)

        self.SetSizer(vbox)
        #vbox.Fit(self)


class PageTwo(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.heat_map_label = wx.StaticText(self, label="Heatmap Type")
        self.resolution_label = wx.StaticText(self, label="Resolution")
        self.effectiveness_label = wx.StaticText(self, label="Display Value")

        heat_map_types = ['-----', 'defence position taking','position of target of pass', 'position of source of pass']
        self.heat_map = wx.ComboBox(self, size=(95, -1), choices=heat_map_types, style=wx.CB_DROPDOWN)
        self.resolution = wx.Slider(self, -1, value=2, minValue=0.5, maxValue=5,
                                    style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        comp_of_effectiveness = ["effectiveness", "gain", "pass advantage", "goal chance", "overall risk"]
        self.effectiveness = wx.ComboBox(self, size=(95, -1), choices=comp_of_effectiveness, style=wx.CB_DROPDOWN)

        self.vmin_auto_rbutton = wx.RadioButton(self, -1, label="auto")
        self.vmin_custom_rbutton = wx.RadioButton(self, -1, label="custom")
        self.vmin_custom_entry = wx.TextCtrl(self, size=(50,-1))

        self.vmax_auto_rbutton = wx.RadioButton(self, -1, label="auto")
        self.vmax_custom_rbutton = wx.RadioButton(self, -1, label="custom")
        self.vmax_custom_entry = wx.TextCtrl(self, size=(50,-1))

        ### colorbar canvas
        fig = Figure((0.5,3))
        ax1 = fig.add_axes([0, 0.03, 0.5,0.94])
        self.colorbar_canvas = FigCanvas(self, -1, fig)

        cmap = matplotlib.cm.hot
        norm = matplotlib.colors.Normalize(vmin=5, vmax=10)

        cb1 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='vertical')


        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.heat_map)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_resolution, self.resolution)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.effectiveness)


        vbox = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(8, 1, 0, 25)
        fgs.AddMany([(self.heat_map_label),
                     (self.heat_map, 1, wx.EXPAND),
                     (wx.StaticText(self), wx.EXPAND),
                     (self.resolution_label),
                     (self.resolution, 1, wx.EXPAND|wx.ALIGN_BOTTOM),
                     (wx.StaticText(self), wx.EXPAND),
                     (self.effectiveness_label),
                     (self.effectiveness, 1, wx.EXPAND)])
        vbox.Add(fgs, wx.ALIGN_LEFT)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(self, style=wx.HORIZONTAL, size=(150,2)), 0, wx.ALIGN_LEFT)
        vbox.AddSpacer(10)


        self.hbox_colorbar = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox_colorbar_options = wx.BoxSizer(wx.VERTICAL)

        colorbar_vmax_box = wx.StaticBox(self, wx.ID_ANY, "max")
        colorbar_vmax_box_sizer = wx.StaticBoxSizer(colorbar_vmax_box, wx.VERTICAL)
        colorbar_vmax_box_sizer.Add(self.vmax_auto_rbutton, wx.ALIGN_LEFT)
        hbox_max_custom = wx.BoxSizer(wx.VERTICAL)
        hbox_max_custom.Add(self.vmax_custom_rbutton)
        hbox_max_custom.Add(self.vmax_custom_entry, 0, wx.ALIGN_RIGHT)
        colorbar_vmax_box_sizer.Add(hbox_max_custom)
        self.vbox_colorbar_options.Add(colorbar_vmax_box_sizer, 0, wx.ALIGN_TOP)


        colorbar_vmin_box = wx.StaticBox(self, wx.ID_ANY, "min")
        colorbar_vmin_box_sizer = wx.StaticBoxSizer(colorbar_vmin_box, wx.VERTICAL)
        colorbar_vmin_box_sizer.Add(self.vmin_auto_rbutton, wx.ALIGN_LEFT)
        hbox_min_custom = wx.BoxSizer(wx.VERTICAL)
        hbox_min_custom.Add(self.vmin_custom_rbutton)
        hbox_min_custom.Add(self.vmin_custom_entry, 0, wx.ALIGN_RIGHT)
        colorbar_vmin_box_sizer.Add(hbox_min_custom)
        self.vbox_colorbar_options.Add(colorbar_vmin_box_sizer, wx.ALIGN_BOTTOM)

        self.hbox_colorbar.Add(self.vbox_colorbar_options, 1, wx.EXPAND)
        self.hbox_colorbar.Add(self.colorbar_canvas, 1, wx.EXPAND)

        vbox.Add(self.hbox_colorbar, 1, wx.EXPAND)

        self.SetSizer(vbox)
        #vbox.Fit(self)


    ##### handling comboBox events #####
    def EvtComboBox(self, event):
        pass
        #self.pass_info_logger.AppendText('EvtComboBox: %s\n' % event.GetString())


    def on_resolution(self, event):
        pass


class wxVisualization(wx.Frame):

    dirname=''
    title = "Sport Analytics Tool - IDEA Lab"

    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title, pos=(0,20), size=(1200,750))

        self.paused = False

        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        self.layout_contols()

        self.draw_figure()


    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_save = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        m_open = menu_file.Append(wx.ID_OPEN, "&Open"," Open a snapshot to display")
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "&Exit\tCtrl-X", "Exit")

        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the demo")

        self.Bind(wx.EVT_MENU, self.on_save_plot, m_save)
        self.Bind(wx.EVT_MENU, self.on_open_plot, m_open)
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.Bind(wx.EVT_MENU, self.on_about, m_about)

        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)


    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()


    def create_main_panel(self):
        self.panel = wx.Panel(self)

        ### main canvas
        self.dpi = 100
        self.fig = Figure((10,7), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        #self.toolbar = NavigationToolbar(self.canvas)

        self.ax = self.fig.add_axes([0.015, 0.03, 0.990, 0.925])
        im = plt.imread('../sentio/source/background.png')
        self.ax.imshow(im, zorder=0, extent=[-6.5, 111.5, -1.5, 66.5])
        self.ax.grid()
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(0, 110, 5))
        self.ax.set_yticks(numpy.arange(0, 70, 5))
        self.ax.tick_params(axis="both", labelsize=6)

        a,b,c,d, = plt.plot([],[],"bo",[],[],"ro",[],[],"yo",[],[],"ko", markersize=6)
        self.ax.legend([a,b,c,d], ["QQQ", "WWW", 'Referees',
                                   'Unknown Objects'], numpoints=1, fontsize=6, bbox_to_anchor=(0., 1.0, 1., .102),
                       loc=3, ncol=4, mode="expand", borderaxespad=0.5)

        self.current_time = wx.StaticText(self.panel, -1, "Time = 0.0.0")

        radioList = ['New Pass', 'Drag Object']
        self.rb = wx.RadioBox(self.panel,label="Mouse Action",choices=radioList, majorDimension=2,
                              style=wx.RA_SPECIFY_COLS)

        self.play_speed_slider = wx.Slider(self.panel, -1, value=2, minValue=0.5, maxValue=5,
                                      style=wx.SL_AUTOTICKS | wx.SL_LABELS | wx.HORIZONTAL)
        self.slider = wx.Slider(self.panel, -1, value=0, minValue=1, maxValue=90,
                                      style=wx.SL_AUTOTICKS | wx.SL_LABELS | wx.HORIZONTAL)

        # The Rewind Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "play_back.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "play_back_disabled.png"), wx.BITMAP_TYPE_PNG)
        self.play_back_button = SBitmapToggleButton(self.panel, -1, upbmp, (48, 48))
        self.play_back_button.SetUseFocusIndicator(False)
        self.play_back_button.SetBitmapDisabled(disbmp)

        #The Play Button Is A Toggle Bitmap Button (SBitmapToggleButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "pause.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "pause_disabled.png"), wx.BITMAP_TYPE_PNG)
        self.pause_button = SBitmapButton(self.panel, -1, upbmp, (48, 48), size=(50,50))
        self.pause_button.SetUseFocusIndicator(False)
        self.pause_button.SetBitmapDisabled(disbmp)

        upbmp = wx.Bitmap(os.path.join(bitmapDir, "play.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "play_disabled.png"), wx.BITMAP_TYPE_PNG)
        self.play_button = SBitmapToggleButton(self.panel, -1, upbmp, (48, 48))
        self.play_button.SetUseFocusIndicator(False)
        self.play_button.SetBitmapDisabled(disbmp)

        self.Bind(wx.EVT_RADIOBOX, self.on_mouse_action, self.rb)
        self.Bind(wx.EVT_BUTTON, self.on_play_back_button, self.play_back_button)
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_BUTTON, self.on_play_button, self.play_button)
        #self.Bind(wx.EVT_UPDATE_UI, self.on_update_play_button, self.play_button)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.on_slider, self.slider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_play_speed_slider, self.play_speed_slider)


    def layout_contols(self):
        # Layout with box sizers
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        p = wx.Panel(self.panel)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = PageTwo(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Pass / Info")
        nb.AddPage(page2, "Heatmap Setup")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        vbox_rb_notebook = wx.BoxSizer(wx.VERTICAL)
        vbox_rb_notebook.Add(self.rb)
        vbox_rb_notebook.Add(p,1, wx.EXPAND)
        vbox_rb_notebook.Add(self.play_speed_slider)

        self.hbox.Add(vbox_rb_notebook)
        self.hbox.Add(self.canvas, 1, wx.EXPAND)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        #self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.vbox.Add(self.hbox, 1, wx.EXPAND)

        self.hbox_play = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_play.Add(self.play_back_button, 0, border=3, flag=wx.ALIGN_CENTER)
        self.hbox_play.Add(self.pause_button, 0, border=3, flag=wx.ALIGN_CENTER)
        self.hbox_play.Add(self.play_button, 0, border=3, flag=wx.ALIGN_CENTER)
        self.hbox_play.Add(self.slider, 1, border=3, flag=wx.ALIGN_CENTER | wx.EXPAND)
        self.hbox_play.Add(self.current_time, 0, border=3, flag=flags)
        self.vbox.Add(self.hbox_play, 0,  wx.EXPAND)

        self.panel.SetSizer(self.vbox)
        #self.vbox.Fit(self)



    def draw_figure(self):
        self.canvas.draw()


    ##### handling menu events #####
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)


    def on_open_plot(self, event):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            #self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()


    def on_exit(self, event):
        self.Close()


    def on_about(self, event):
        msg = """ Sport Analytics Project
        UI Designer: dktry_ (Emrullah Delibaş)

         we are still working on it!!! ;)
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()



    ##### handling button events #####
    def on_play_back_button(self, event):
        pass


    def on_pause_button(self, event):
        self.paused = not self.paused


    def on_play_button(self, event):
        self.paused = not self.paused


    def on_update_play_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.current_time.SetLabel(label)


    ##### handling slidir events #####
    def on_slider(self, event):
        pass


    def on_play_speed_slider(self, event):
        pass


    ##### handling radioBox events #####
    def on_mouse_action(self, event):
        pass

app = wx.App()
app.frame = wxVisualization()
app.frame.Show()
app.MainLoop()
