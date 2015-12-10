__author__ = 'emrullah'


import wx


class BallOwnershipAnalysisNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.ball_ownership_compute_button = wx.Button(self, -1, "run")



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.ball_ownership_compute_button, 1, wx.EXPAND)

        self.SetSizer(vbox)
        vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.ball_ownership_compute_button.Bind(wx.EVT_BUTTON, self.OnCompute)


    def setMatch(self, match):
        self.match = match


    def OnBuild(self, event):
        self.match.buildMatchObjects()


    def OnCompute(self, event):
        self.match.buildMatchObjects()
        self.match.computeEventStats()
        print "data is built"
        team_players = self.match.getHomeTeam().getTeamPlayers() + self.match.getAwayTeam().getTeamPlayers()

        for team_player in team_players:
            print team_player.printStats()
