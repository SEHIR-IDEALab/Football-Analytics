from wx.lib.agw import aui
from analytics.OptimalShootingPointPredictionNotebook import OptimalShootingPointPredictionNotebook
from analytics.BallOwnershipAnalysisNotebook import BallOwnershipAnalysisNotebook
from analytics.RunningDistanceAnalysisNotebook import RunningDistanceAnalysisNotebook
from src.sentio.gui.notebook.analytics.BallOwnershipPredictionNotebook import BallOwnershipPredictionNotebook
from src.sentio.gui.notebook.analytics.DominantRegionAnalysisNotebook import DominantRegionAnalysisNotebook
from src.sentio.gui.notebook.analytics.PassSuccessPredictionNotebook import PassSuccessPredictionNotebook

__author__ = 'emrullah'


import wx



class AnalyticsNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax, fig):
        wx.Panel.__init__(self, parent)

        style = aui.AUI_NB_DEFAULT_STYLE
        style &= ~(aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)

        nb = aui.AuiNotebook(self, agwStyle=style)

        # # create the page windows as children of the notebook
        self.ball_ownership_analysis_page = BallOwnershipAnalysisNotebook(nb, canvas, ax)
        self.running_distance_analysis_page = RunningDistanceAnalysisNotebook(nb, canvas, ax)
        self.dominant_region_analysis_page = DominantRegionAnalysisNotebook(nb, canvas, ax)
        self.optimal_shooting_point_prediction_page = OptimalShootingPointPredictionNotebook(nb, canvas, ax, fig)
        self.pass_success_prediction_page = PassSuccessPredictionNotebook(nb, canvas, ax, fig)
        self.ball_ownership_prediction_page = BallOwnershipPredictionNotebook(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.ball_ownership_analysis_page, "Ball Ownership A.")
        nb.AddPage(self.running_distance_analysis_page, "Running Distance A.")
        nb.AddPage(self.dominant_region_analysis_page, "Dominant Region A.")
        nb.AddPage(self.optimal_shooting_point_prediction_page, "Optimal Shooting Point P.")
        nb.AddPage(self.pass_success_prediction_page, "Pass Success P.")
        nb.AddPage(self.ball_ownership_prediction_page, "Ball Ownership P.")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)


    def setMatch(self, match):
        self.ball_ownership_analysis_page.setMatch(match)
        self.running_distance_analysis_page.setMatch(match)
        self.dominant_region_analysis_page.setMatch(match)
        ########
        self.pass_success_prediction_page.setMatch(match)