from analytics.BestShootPositionAnalysisNotebook import BestShootPositionAnalysisNotebook
from analytics.BallOwnershipAnalysisNotebook import BallOwnershipAnalysisNotebook
from analytics.RunningDistanceAnalysisNotebook import RunningDistanceAnalysisNotebook

__author__ = 'emrullah'


import wx


class AnalyticsNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        nb = wx.Notebook(self)

        # # create the page windows as children of the notebook
        self.best_shoot_position_analysis_page = BestShootPositionAnalysisNotebook(nb)
        self.ball_ownership_analysis_page = BallOwnershipAnalysisNotebook(nb)
        self.running_distance_analysis_page = RunningDistanceAnalysisNotebook(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.best_shoot_position_analysis_page, "BSPA")
        nb.AddPage(self.ball_ownership_analysis_page, "BOA")
        nb.AddPage(self.running_distance_analysis_page, "RDA")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)


    def setMatch(self, match):
        self.ball_ownership_analysis_page.setMatch(match)
        self.running_distance_analysis_page.setMatch(match)