import itertools
from src.sentio.gui.EventAnnotationManager import EventAnnotationManager

__author__ = 'emrullah'


import wx


class RunningDistanceAnalysisNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax, analytics):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax
        self.analytics = analytics

        self.interval_min = wx.TextCtrl(self, -1, "0", size=(50,-1))
        self.interval_max = wx.TextCtrl(self, -1, "90", size=(50,-1))

        self.build_dataset_button = wx.Button(self, -1, "BUILD DATASET", size=(10,10))
        self.run_button = wx.Button(self, -1, "RUN", size=(80,40))

        self.team_choice = wx.ComboBox(self, size=(80,-1), style=wx.CB_READONLY,
                                       choices=["All Teams", "Home Team", "Away Team"])

        self.game_stop_filter = wx.CheckBox(self, -1, 'game stop')
        self.speed_filter = wx.CheckBox(self, -1, 'speed')


        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)

        time_interval_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Time Interval", style=wx.ALIGN_CENTER), wx.HORIZONTAL)
        time_interval_box_sizer.Add(self.interval_min, 0, wx.EXPAND)
        time_interval_box_sizer.Add(wx.StaticText(self, label=" &&& "), 0, wx.EXPAND)
        time_interval_box_sizer.Add(self.interval_max, 0, wx.EXPAND)

        vbox.Add(time_interval_box_sizer, 0, wx.EXPAND)
        vbox.Add(self.build_dataset_button, 1, wx.EXPAND)

        vbox.Add(wx.StaticText(self, label="Team Choice"), 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

        filters_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "FILTERS"), wx.VERTICAL)
        filters_box_sizer.Add(self.game_stop_filter, 0, wx.EXPAND)
        filters_box_sizer.Add(self.speed_filter, 0, wx.EXPAND)

        vbox.Add(filters_box_sizer, 1, wx.EXPAND)
        vbox.Add(self.run_button, 1, wx.EXPAND)

        self.SetSizer(vbox)
        # vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.build_dataset_button.Bind(wx.EVT_BUTTON, self.OnBuild)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnCompute)


    def setMatch(self, match):
        self.match = match


    def OnBuild(self, event):
        self.match.buildMatchObjects(int(self.interval_min.GetValue()), int(self.interval_max.GetValue()))
        print "data is built"


    def getChosenTeams(self):
        teams = None
        if self.team_choice.GetValue() == "All Teams":
            teams = [self.match.getHomeTeam(), self.match.getAwayTeam()]
        elif self.team_choice.GetValue() == "Home Team":
            teams = [self.match.getHomeTeam()]
        elif self.team_choice.GetValue() == "Away Team":
            teams = [self.match.getAwayTeam()]
        else:
            print "chosen team is missing!!!"
        return teams


    def OnCompute(self, event):
        self.analytics.clear()

        results = []
        for team in self.getChosenTeams():
            temp_results = []
            temp_results.append((team.team_name.upper(), "Running Distance"))
            for player in team.getTeamPlayers():

                ## filtering
                if self.game_stop_filter.GetValue() and self.speed_filter.GetValue():
                    result = player.computeRunningDistanceWithGameStopAndSpeedFilter()
                elif self.game_stop_filter.GetValue():
                    result = player.computeRunningDistanceWithGameStopFilter()
                elif self.speed_filter.GetValue():
                    result = player.computeRunningDistanceWithSpeedFilter()
                else:
                    result = player.computeRunningDistance()

                temp_results.append((player.jersey_number, result))
            results.append(temp_results)
        results = self.formatInfoToDisplay(results)
        self.analytics.results = EventAnnotationManager.annotateAnalysisResults(self.canvas, self.ax, results)


    def formatInfoToDisplay(self, results):
        print results
        q = ""
        if self.team_choice.GetValue() == "All Teams":
            for (home_js, home_result), (away_js, away_result) in itertools.izip(results[0], results[1]):
                if home_js != -1:
                    try:
                        q += "%s %s | %s %s\n" %(("%.2f"%home_result).ljust(30), str(home_js).center(10),
                                                 str(away_js).center(10), ("%.2f"%away_result).rjust(30))
                    except:
                        q += "%s %s | %s %s\n" %(str(home_result).ljust(30), str(home_js).center(10),
                                                 str(away_js).center(10), str(away_result).rjust(30))
        else:
            for js, result, in results[0]:
                if js != -1:
                    try:
                        q += "%s %s\n" %(str(js).center(10), str("%.2f"%result).rjust(30))
                    except:
                        q += "%s %s\n" %(str(js).center(10), str(result).rjust(30))
        return q[:-1]

