__author__ = 'emrullah'


import wx


class RunningDistanceAnalysisNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.build_dataset_button = wx.Button(self, -1, "build dataset")

        self.game_stop_filter = wx.CheckBox(self, -1, 'game stop')
        self.speed_filter = wx.CheckBox(self, -1, 'speed')

        self.running_distance_compute_button = wx.Button(self, -1, "calculate")



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.build_dataset_button, 0, wx.EXPAND)

        filters_box = wx.StaticBox(self, wx.ID_ANY, "FILTERS")
        filters_box_sizer = wx.StaticBoxSizer(filters_box, wx.VERTICAL)
        filters_box_sizer.Add(self.game_stop_filter, 0, wx.EXPAND)
        filters_box_sizer.Add(self.speed_filter, 0, wx.EXPAND)

        vbox.Add(filters_box_sizer, 0, wx.EXPAND)
        vbox.Add(self.running_distance_compute_button, 0, wx.EXPAND)

        self.SetSizer(vbox)
        vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.running_distance_compute_button.Bind(wx.EVT_BUTTON, self.OnBuild)
        self.running_distance_compute_button.Bind(wx.EVT_BUTTON, self.OnCompute)


    def setMatch(self, match):
        self.match = match


    def OnBuild(self, event):
        self.match.buildMatchObjects()


    def OnCompute(self, event):
        self.match.buildMatchObjects()
        print "data is built"
        team_players = self.match.getHomeTeam().getTeamPlayers() + self.match.getAwayTeam().getTeamPlayers()

        for team_player in team_players:
            if self.game_stop_filter.GetValue() and self.speed_filter.GetValue():
                print "with game_stop and speed filter: ", team_player.computeRunningDistanceWithGameStopAndSpeedFilter()
            elif self.game_stop_filter.GetValue():
                print "with game_stop filter: ", team_player.computeRunningDistanceWithGameStopFilter()
            elif self.speed_filter.GetValue():
                print "with speed filter: ", team_player.computeRunningDistanceWithSpeedFilter()
            else:
                print "without filter: ", team_player.computeRunningDistance()
