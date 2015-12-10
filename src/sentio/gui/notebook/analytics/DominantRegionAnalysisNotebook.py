from scipy import spatial
from src.sentio.gui.Voronoi import Voronoi

__author__ = 'emrullah'



import wx


class DominantRegionAnalysisNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # self.build_dataset_button = wx.Button(self, -1, "build dataset", size=(10,10))
        #
        # self.game_stop_filter = wx.CheckBox(self, -1, 'game stop')
        # self.speed_filter = wx.CheckBox(self, -1, 'speed')

        self.dominant_region_compute_button = wx.Button(self, -1, "calculate", size=(80,40))



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)
        # vbox.Add(self.build_dataset_button, 1, wx.ALIGN_TOP|wx.EXPAND)

        # filters_box = wx.StaticBox(self, wx.ID_ANY, "FILTERS")
        # filters_box_sizer = wx.StaticBoxSizer(filters_box, wx.VERTICAL)
        # filters_box_sizer.Add(self.game_stop_filter, 0, wx.EXPAND)
        # filters_box_sizer.Add(self.speed_filter, 0, wx.EXPAND)

        # vbox.Add(filters_box_sizer, 0, wx.EXPAND|wx.ALIGN_TOP)
        vbox.Add(self.dominant_region_compute_button, 1, wx.ALIGN_CENTER|wx.EXPAND)

        self.SetSizer(vbox)
        # vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        # self.running_distance_compute_button.Bind(wx.EVT_BUTTON, self.OnBuild)
        self.dominant_region_compute_button.Bind(wx.EVT_BUTTON, self.OnCompute)


    def setMatch(self, match):
        self.match = match


    # def OnBuild(self, event):
    #     self.match.buildMatchObjects()


    def OnCompute(self, event):
        self.match.computeDominantRegions()
        print "data is built"
        team_players = self.match.getHomeTeam().getTeamPlayers() + self.match.getAwayTeam().getTeamPlayers()

        for team_player in team_players:
            print team_player
            print "total coverage", team_player.dominant_region
            print "average DR per instance", team_player.calculateAverageDRPerInstance()
            print "DR percentage in total", team_player.calculateDRPercentageInTotal()