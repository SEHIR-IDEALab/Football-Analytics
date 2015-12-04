import os
import numpy
import wx
from wx.lib.agw.shapedbutton import SBitmapButton
from src.sentio.Parameters import FOOTBALL_FIELD_MIN_X, HOME_TEAM_NAME, AWAY_TEAM_NAME, BITMAP_DIRECTORY, \
    REFEREES_TEAM_NAME, UNKNOWNS_TEAM_NAME
from src.sentio.Parameters import FOOTBALL_FIELD_MAX_X
from src.sentio.Parameters import FOOTBALL_FIELD_MIN_Y
from src.sentio.Parameters import FOOTBALL_FIELD_MAX_Y

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
from src.sentio.gui.notebook.HeatMapNotebook import HeatMapNotebook
from src.sentio.gui.notebook.LoggerNotebook import LoggerNotebook


__author__ = 'emrullah'

class wxLayouts:

    def __init__(self, wx_gui):
        self.wx_gui = wx_gui

        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()


    def create_menu(self):
        menubar = wx.MenuBar()

        menu_file = wx.Menu()
        self.m_save = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.m_open = menu_file.Append(wx.ID_OPEN, "&Open"," Open a snapshot to display")
        menu_file.AppendSeparator()
        self.m_exit = menu_file.Append(-1, "&Exit\tCtrl-X", "Exit")

        menu_view = wx.Menu()
        self.debug_mode = menu_view.Append(-1, "&Debug Mode", kind=wx.ITEM_CHECK)
        self.show_directions = menu_view.Append(-1, "&Show Directions", kind=wx.ITEM_CHECK)
        self.voronoi_diagram = menu_view.Append(-1, "&Voronoi Diagram", kind=wx.ITEM_CHECK)

        menu_help = wx.Menu()
        self.m_about = menu_help.Append(-1, "&About\tF1", "About the tool")

        menubar.Append(menu_file, "&File")
        menubar.Append(menu_view, "&View")
        menubar.Append(menu_help, "&Help")
        self.wx_gui.SetMenuBar(menubar)


    def create_status_bar(self):
        self.statusbar = self.wx_gui.CreateStatusBar()


    def create_main_panel(self):
        self.panel = wx.Panel(self.wx_gui)

        ### main canvas
        self.dpi = 100
        self.fig = Figure((7,5), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        # self.toolbar = NavigationToolbar(self.canvas)

        self.ax = self.fig.add_axes([0.025, 0.03, 0.970, 0.925]) # x0, y0, x1, y1

        im = plt.imread('gui/source/background.png')
        self.ax.imshow(im, zorder=0, aspect='auto', extent=[FOOTBALL_FIELD_MIN_X-4.5, FOOTBALL_FIELD_MAX_X+4.5,
                                                            FOOTBALL_FIELD_MIN_Y-1.5, FOOTBALL_FIELD_MAX_Y+1.5])
        self.ax.grid()
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X+5, 5))
        self.ax.set_yticks(numpy.arange(FOOTBALL_FIELD_MIN_Y, FOOTBALL_FIELD_MAX_Y+5, 5))
        self.ax.tick_params(axis="both", labelsize=6)
        self.ax.autoscale(False)

        a,b,c,d, = plt.plot([],[],"bo",[],[],"ro",[],[],"yo",[],[],"ko", markersize=6)
        self.ax.legend([a,b,c,d], [HOME_TEAM_NAME, AWAY_TEAM_NAME, REFEREES_TEAM_NAME, UNKNOWNS_TEAM_NAME],
                       numpoints=1, fontsize=6, bbox_to_anchor=(0., 1.0, 1., .102),
                       loc=3, ncol=4, mode="expand", borderaxespad=0.5)

        self.current_time_display = wx.StaticText(self.panel, -1, "Time = 1_00:00:00")

        self.rb = wx.RadioBox(self.panel, label="Mouse Action", choices=['New Pass', 'Drag Object'],
                              majorDimension=1, style=wx.RA_SPECIFY_COLS)

        self.play_speed_slider = wx.Slider(self.panel, -1, value=2, minValue=1, maxValue=5)
        self.slider = wx.Slider(self.panel, -1, value=0, minValue=0, maxValue=self.wx_gui.sentio.game_instances.getTotalNumber()-1)

        self.upbmp = wx.Bitmap(os.path.join(BITMAP_DIRECTORY, "play.png"), wx.BITMAP_TYPE_PNG)
        self.disbmp = wx.Bitmap(os.path.join(BITMAP_DIRECTORY, "pause.png"), wx.BITMAP_TYPE_PNG)
        self.play_button = SBitmapButton(self.panel, -1, self.upbmp, (48, 48), size=(40,40))


    def layout_controls(self):
        # Layout with box sizers
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        p = wx.Panel(self.panel)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        self.pass_info_page = LoggerNotebook(nb)
        self.heatmap_setup_page = HeatMapNotebook(nb)

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
        # self.vbox_canvas.Add(self.toolbar, 0, wx.EXPAND)

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
