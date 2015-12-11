import itertools
from src.sentio.gui.EventAnnotationManager import EventAnnotationManager

__author__ = 'emrullah'


import wx


class BallOwnershipAnalysisNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax

        time_interval_box = wx.StaticBox(self, wx.ID_ANY, "Time Interval", style=wx.ALIGN_CENTER)
        self.interval_min = wx.TextCtrl(self, -1, "0", size=(50,-1))
        interval_text = wx.StaticText(self, label=" &&& ")
        self.interval_max = wx.TextCtrl(self, -1, "90", size=(50,-1))

        self.build_dataset_button = wx.Button(self, -1, "BUILD DATASET")

        team_choice_text = wx.StaticText(self, label="Team Choice")
        team_choices = ["All Teams", "Home Team", "Away Team"]
        self.team_choice = wx.ComboBox(self, size=(80,-1), choices=team_choices, style=wx.CB_READONLY)

        self.run_button = wx.Button(self, -1, "RUN")



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
        self.match.buildMatchObjects(int(self.interval_min.GetValue()), int(self.interval_max.GetValue()))
        self.match.computeEventStats(int(self.interval_min.GetValue()), int(self.interval_max.GetValue()))
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
        results = []
        for team in self.getChosenTeams():
            temp_results = []
            temp_results.append((team.team_name, ("Ball Steal", "Ball Lose", "Ball Pass", "Ball Ownership Time")))
            for player in team.getTeamPlayers():
                temp_results.append((player.jersey_number, player.getStats()))
            results.append(temp_results)
        results = self.formatInfoToDisplay(results)
        EventAnnotationManager.annotateAnalysisResults(self.canvas, self.ax, results)


    def formatInfoToDisplay(self, results):
        print results
        q = ""

        if self.team_choice.GetValue() == "All Teams":
            for (home_js, home_stats), (away_js, away_stats) in itertools.izip(results[0], results[1]):
                ball_steal, ball_lose, ball_pass, ball_ownership_time = home_stats
                ball_steal2, ball_lose2, ball_pass2, ball_ownership_time2 = away_stats
                try:
                    q += "(%s %s %s %s) %s | %s (%s %s %s %s)\n" %\
                         (str(ball_ownership_time).ljust(30), str(ball_pass).ljust(10),str(ball_lose).ljust(10),
                          str(ball_steal).ljust(10), str(home_js).center(10),
                          str(away_js).center(10), str(ball_steal2).rjust(10), str(ball_lose2).rjust(10),
                          str(ball_pass2).rjust(10), str(ball_ownership_time2).rjust(30))
                except:
                    q += "%s %s | %s %s\n" %(str(home_stats[::-1]).ljust(30), str(home_js).center(10),
                                             str(away_js).center(10), str(away_stats).rjust(30))
        else:
            for js, stats in results[0]:
                ball_steal, ball_lose, ball_pass, ball_ownership_time = stats
                q += "%s (%s %s %s %s)\n" %\
                     (str(js).center(10), str(ball_steal).center(15), str(ball_lose).center(15),
                      str(ball_pass).center(15), str(ball_ownership_time).center(30))
        return q
