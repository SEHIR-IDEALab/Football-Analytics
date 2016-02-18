import itertools
from scipy import spatial
from src.sentio.gui.EventAnnotationManager import EventAnnotationManager
from src.sentio.gui.Voronoi import Voronoi

__author__ = 'emrullah'



import wx


class DominantRegionAnalysisNotebook(wx.Panel):

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
        self.time_point_choice = wx.ComboBox(self, size=(80,-1), style=wx.CB_READONLY,
                                             choices=["all time points", "when HomeTeam has ball", "when AwayTeam has ball"])
        self.field_choice = wx.ComboBox(self, size=(80,-1), style=wx.CB_READONLY,
                                        choices=["Whole Field", "HomeTeam Field", "AwayTeam Field"])


        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)

        time_interval_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Time Interval", style=wx.ALIGN_CENTER), wx.HORIZONTAL)
        time_interval_box_sizer.Add(self.interval_min, 0, wx.EXPAND)
        time_interval_box_sizer.Add(wx.StaticText(self, label=" &&& "), 0, wx.EXPAND)
        time_interval_box_sizer.Add(self.interval_max, 0, wx.EXPAND)
        vbox.Add(time_interval_box_sizer, 0, wx.EXPAND)

        vbox.Add(wx.StaticText(self, label="Field Choice"), 0, wx.EXPAND)
        vbox.Add(self.field_choice, 0, wx.EXPAND)

        vbox.Add(self.build_dataset_button, 1, wx.EXPAND)

        vbox.Add(wx.StaticText(self, label="Team Choice"), 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

        vbox.Add(wx.StaticText(self, label="Time Point Choice"), 0, wx.EXPAND)
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
        self.analytics.clear()

        results = []
        for team in self.getChosenTeams():
            temp_results = []
            temp_results.append((team.team_name, ("Total Coverage", "Avg Coverage", "Coverage %")))
            for player in team.getTeamPlayers():
                temp_results.append((player.jersey_number, (player.dominant_region,
                                                            player.calculateAverageDRPerInstance(),
                                                            player.calculateDRPercentageInTotal())))
            results.append(temp_results)
        results = self.formatInfoToDisplay(results)
        self.analytics.results = EventAnnotationManager.annotateAnalysisResults(self.canvas, self.ax, results)


    def formatInfoToDisplay(self, results):
        print results
        q = ""

        if self.team_choice.GetValue() == "All Teams":
            for (home_js, home_stats), (away_js, away_stats) in itertools.izip(results[0], results[1]):
                total_coverage, average_coverage, coverage_percentage = home_stats
                total_coverage2, average_coverage2, coverage_percentage2 = away_stats
                try:
                    q += "%s %s %s %s | %s %s %s %s\n" %\
                         (("%.2f"%coverage_percentage).ljust(13), ("%.2f"%average_coverage).ljust(14),
                          ("%.2f"%total_coverage).ljust(15), str(home_js).center(5),
                          str(away_js).center(4), ("%.2f"%total_coverage2).rjust(16),
                          ("%.2f"%average_coverage2).rjust(14), ("%.2f"%coverage_percentage2).rjust(12))
                except:
                    q += "%s %s %s %s | %s %s %s %s\n" %\
                           (str(coverage_percentage).ljust(13), str(average_coverage).ljust(14),
                        str(total_coverage).ljust(15), str(home_js).center(5), str(away_js).center(4),
                        str(total_coverage2).rjust(16), str(average_coverage2).rjust(14),str(coverage_percentage2).rjust(12))
        else:
            for js, stats in results[0]:
                total_coverage, average_coverage, coverage_percentage = stats
                try:
                    q += "%s %s %s %s\n" %\
                         (str(js).center(10), ("%.2f"%total_coverage).rjust(12),
                          ("%.2f"%average_coverage).rjust(13), ("%.2f"%coverage_percentage).rjust(12))
                except:
                    q += "%s %s %s %s\n" %\
                         (str(js).center(10), str(total_coverage).rjust(12),
                          str(average_coverage).rjust(13), str(coverage_percentage).rjust(12))
        return q