import itertools
from scipy import spatial
from src.sentio.gui.EventAnnotationManager import EventAnnotationManager
from src.sentio.gui.Voronoi import Voronoi

__author__ = 'emrullah'



import wx


class DominantRegionAnalysisNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax

        time_interval_box = wx.StaticBox(self, wx.ID_ANY, "Time Interval", style=wx.ALIGN_CENTER)
        self.interval_min = wx.TextCtrl(self, -1, "0", size=(50,-1))
        interval_text = wx.StaticText(self, label=" &&& ")
        self.interval_max = wx.TextCtrl(self, -1, "90", size=(50,-1))

        field_choice_text = wx.StaticText(self, label="Field Choice")
        field_choices = ["Whole Field", "HomeTeam Field", "AwayTeam Field"]
        self.field_choice = wx.ComboBox(self, size=(80,-1), choices=field_choices, style=wx.CB_READONLY)

        self.build_dataset_button = wx.Button(self, -1, "BUILD DATASET", size=(10,10))

        team_choice_text = wx.StaticText(self, label="Team Choice")
        team_choices = ["All Teams", "Home Team", "Away Team"]
        self.team_choice = wx.ComboBox(self, size=(80,-1), choices=team_choices, style=wx.CB_READONLY)

        time_point_choice_text = wx.StaticText(self, label="Time Point Choice")
        time_point_choices = ["all time points", "when HomeTeam has ball", "when AwayTeam has ball"]
        self.time_point_choice = wx.ComboBox(self, size=(80,-1), choices=time_point_choices, style=wx.CB_READONLY)

        self.run_button = wx.Button(self, -1, "RUN", size=(80,40))



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)

        time_interval_box_sizer = wx.StaticBoxSizer(time_interval_box, wx.HORIZONTAL)
        time_interval_box_sizer.Add(self.interval_min, 0, wx.EXPAND)
        time_interval_box_sizer.Add(interval_text, 0, wx.EXPAND)
        time_interval_box_sizer.Add(self.interval_max, 0, wx.EXPAND)
        vbox.Add(time_interval_box_sizer, 0, wx.EXPAND)

        vbox.Add(field_choice_text, 0, wx.EXPAND)
        vbox.Add(self.field_choice, 0, wx.EXPAND)

        vbox.Add(self.build_dataset_button, 1, wx.EXPAND)

        vbox.Add(team_choice_text, 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

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
        self.match.computeDominantRegions(
            interval_min=int(self.interval_min.GetValue()),
            interval_max=int(self.interval_max.GetValue()),
            field=self.field_choice.GetValue()
        )
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
            temp_results.append((team.team_name, ("Total Coverage", "Average Coverage", "Coverage Percentage")))
            for player in team.getTeamPlayers():
                temp_results.append((player.jersey_number, (player.dominant_region,
                                                            player.calculateAverageDRPerInstance(),
                                                            player.calculateDRPercentageInTotal())))
            results.append(temp_results)
        results = self.formatInfoToDisplay(results)
        EventAnnotationManager.annotateAnalysisResults(self.canvas, self.ax, results)


    def formatInfoToDisplay(self, results):
        print results
        q = ""

        if self.team_choice.GetValue() == "All Teams":
            for (home_js, home_stats), (away_js, away_stats) in itertools.izip(results[0], results[1]):
                total_coverage, average_coverage, coverage_percentage = home_stats
                total_coverage2, average_coverage2, coverage_percentage2 = away_stats
                try:
                    q += "%s %s %s %s | %s %s %s %s\n" %\
                         (("%.2f"%coverage_percentage).ljust(30), ("%.2f"%average_coverage).ljust(10),
                          ("%.2f"%total_coverage).ljust(10), str(home_js).center(10),
                          str(away_js).center(10), ("%.2f"%total_coverage2).rjust(10),
                          ("%.2f"%average_coverage2).rjust(10), ("%.2f"%coverage_percentage2).rjust(10))
                except:
                    q += "%s %s |%s %s\n" %(str(home_stats[::-1]).ljust(30), str(home_js).center(10),
                                             str(away_js).center(10), str(away_stats).rjust(30))
        else:
            for js, stats in results[0]:
                total_coverage, average_coverage, coverage_percentage = stats
                try:
                    q += "%s (%s %s %s)\n" %\
                         (str(js).center(10), ("%.2f"%total_coverage).rjust(15),
                          ("%.2f"%average_coverage).rjust(15), ("%.2f"%coverage_percentage).rjust(15))
                except:
                    q += "%s (%s %s %s)\n" %\
                         (str(js).center(10), str(total_coverage).rjust(15),
                          str(average_coverage).rjust(15), str(coverage_percentage).rjust(15))
        return q