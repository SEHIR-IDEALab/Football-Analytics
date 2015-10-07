__author__ = 'doktoray'

import wx
from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas



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
        vbox.Add(fgs, 1, wx.ALIGN_CENTER)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(self, style=wx.HORIZONTAL, size=(170,2)), 0, wx.ALIGN_CENTER)
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
