from scipy import spatial
from src.sentio.gui.Voronoi import Voronoi

__author__ = 'emrullah'



import wx


class DominantRegionAnalysisNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        time_interval_box = wx.StaticBox(self, wx.ID_ANY, "Time Interval", style=wx.ALIGN_CENTER)
        self.interval_min = wx.TextCtrl(self, -1, "0", size=(50,-1))
        interval_text = wx.StaticText(self, label=" &&& ")
        self.interval_max = wx.TextCtrl(self, -1, "90", size=(50,-1))

        self.build_dataset_button = wx.Button(self, -1, "BUILD DATASET", size=(10,10))

        team_choice_text = wx.StaticText(self, label="Team Choice")
        team_choices = ["All Teams", "Home Team", "Away Team"]
        self.team_choice = wx.ComboBox(self, size=(80,-1), choices=team_choices, style=wx.CB_READONLY)

        field_choice_text = wx.StaticText(self, label="Field Choice")
        field_choices = ["Whole Field", "HomeTeam Field", "AwayTeam Field"]
        self.field_choice = wx.ComboBox(self, size=(80,-1), choices=field_choices, style=wx.CB_READONLY)

        time_point_choice_text = wx.StaticText(self, label="Time Point Choice")
        time_point_choices = ["all time points", "when HomeTeam has ball", "when AwayTeam has ball"]
        self.time_point_choice = wx.ComboBox(self, size=(80,-1), choices=time_point_choices, style=wx.CB_READONLY)

        self.run_button = wx.Button(self, -1, "RUN", size=(80,40))



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)

        time_interval_box_sizer = wx.StaticBoxSizer(time_interval_box, wx.HORIZONTAL)
        time_interval_box_sizer.Add(self.interval_min, 1, wx.EXPAND)
        time_interval_box_sizer.Add(interval_text, 0, wx.EXPAND)
        time_interval_box_sizer.Add(self.interval_max, 1, wx.EXPAND)

        vbox.Add(time_interval_box_sizer, 1, wx.EXPAND|wx.ALIGN_CENTER)
        vbox.Add(self.build_dataset_button, 1, wx.EXPAND)

        vbox.Add(team_choice_text, 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

        vbox.Add(field_choice_text, 0, wx.EXPAND)
        vbox.Add(self.field_choice, 0, wx.EXPAND)

        vbox.Add(time_point_choice_text, 0, wx.EXPAND)
        vbox.Add(self.time_point_choice, 0, wx.EXPAND)

        vbox.Add(self.run_button, 1, wx.EXPAND)

        self.SetSizer(vbox)
        vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.build_dataset_button.Bind(wx.EVT_BUTTON, self.OnBuild)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnCompute)


    def setMatch(self, match):
        self.match = match


    def OnBuild(self, event):
        self.match.computeDominantRegions(int(self.interval_min.GetValue()), int(self.interval_max.GetValue()))
        print "data is built"


    def getChosenTeams(self):
        teams = None
        if self.team_choice.GetValue() == "All Players":
            teams = [self.match.getHomeTeam(), self.match.getAwayTeam()]
        elif self.team_choice.GetValue() == "Home Team":
            teams = [self.match.getHomeTeam()]
        elif self.team_choice.GetValue() == "Away Team":
            teams = [self.match.getAwayTeam()]
        else:
            print "chosen team is missing!!!"
        return teams


    def OnCompute(self, event):
        team_players = self.match.getHomeTeam().getTeamPlayers() + self.match.getAwayTeam().getTeamPlayers()

        for team_player in team_players:
            print team_player
            print "total coverage", team_player.dominant_region
            print "average DR per instance", team_player.calculateAverageDRPerInstance()
            print "DR percentage in total", team_player.calculateDRPercentageInTotal()