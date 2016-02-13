import itertools
import numpy
from src.sentio.algorithms.Pass import Pass
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.gui.EventAnnotationManager import EventAnnotationManager

__author__ = 'emrullah'


import wx


class PlayerEffectivenessAnalysisNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax, analytics):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax
        self.analytics = analytics

        time_interval_box = wx.StaticBox(self, wx.ID_ANY, "Time Interval", style=wx.ALIGN_CENTER)
        self.interval_min = wx.TextCtrl(self, -1, "0", size=(50,-1))
        interval_text = wx.StaticText(self, label=" &&& ")
        self.interval_max = wx.TextCtrl(self, -1, "90", size=(50,-1))

        team_choice_text = wx.StaticText(self, label="Team Choice")
        team_choices = ["All Teams", "Home Team", "Away Team"]
        self.team_choice = wx.ComboBox(self, size=(80,-1), choices=team_choices, style=wx.CB_READONLY)

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

        vbox.Add(team_choice_text, 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

        vbox.Add(self.run_button, 1, wx.EXPAND)

        self.SetSizer(vbox)
        vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.run_button.Bind(wx.EVT_BUTTON, self.OnCompute)


    def setMatch(self, match):
        self.match = match


    def getChosenTeams(self, players):
        teams = ReaderBase.divideIntoTeams(players)
        if self.team_choice.GetValue() == "All Teams":
            teams = [teams.home_team, teams.away_team]
        elif self.team_choice.GetValue() == "Home Team":
            teams = [teams.home_team]
        elif self.team_choice.GetValue() == "Away Team":
            teams = [teams.away_team]
        else:
            print "chosen team is missing!!!"
        return teams


    def OnCompute(self, event):
        self.analytics.clear()

        q = {}
        evaluate = Pass()
        for game_instance in self.match.sentio.game_instances.getAllInstances():
            try:
                if game_instance.event and game_instance.event.isPassEvent():
                    if int(self.interval_min.GetValue()) <= game_instance.time.convertToTime().minute <= int(self.interval_max.GetValue()):
                        pass_source = game_instance.event.pass_event.pass_source
                        pass_target = game_instance.event.pass_event.pass_target
                        evaluate.teams = ReaderBase.divideIntoTeams(game_instance.players)
                        temp_effectiveness = evaluate.effectiveness_withComponents(pass_source, pass_target)[-1]
                        if pass_source.jersey_number in q:
                            q[pass_source.jersey_number].effectiveness_scores.append(temp_effectiveness)
                        else:
                            pass_source.effectiveness_scores = [temp_effectiveness]
                            q[pass_source.jersey_number] = pass_source
            except AttributeError:
                print "event not found for game_instance"

        results = []
        for team in self.getChosenTeams(q.values()):
            temp_results = []
            temp_results.append((team.team_name, ("Effectiveness Score")))
            for player in team.getTeamPlayers():
                temp_results.append((player.jersey_number, (numpy.mean(player.effectiveness_scores))))
            results.append(temp_results)
        results = self.formatInfoToDisplay(results)
        self.analytics.results = EventAnnotationManager.annotateAnalysisResults(self.canvas, self.ax, results)


    def formatInfoToDisplay(self, results):
        print results
        q = ""

        if self.team_choice.GetValue() == "All Teams":
            for (home_js, home_stats), (away_js, away_stats) in itertools.izip(results[0], results[1]):
                effectiveness_score = home_stats
                effectiveness_score2 = away_stats
                try:
                    q += "%s %s | %s %s\n" %\
                         (("%.2f"%effectiveness_score).ljust(19), str(home_js).center(5),
                          str(away_js).center(4), ("%.2f"%effectiveness_score2).rjust(19))
                except:
                    q += "%s %s | %s %s\n" %\
                           (str(effectiveness_score).ljust(19), str(home_js).center(5),
                            str(away_js).center(4), str(effectiveness_score2).rjust(20))
        else:
            for js, stats in results[0]:
                effectiveness_score = stats
                try:
                    q += "%s %s\n" %\
                         (str(js).center(10), ("%.2f"%effectiveness_score).rjust(19))
                except:
                    q += "%s %s\n" %\
                         (str(js).center(10), str(effectiveness_score).rjust(20))
        return q