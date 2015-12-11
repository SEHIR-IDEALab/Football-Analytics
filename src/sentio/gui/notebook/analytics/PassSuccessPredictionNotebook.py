__author__ = 'emrullah'


import wx
import wx.lib.scrolledpanel as scrolled



class PassSuccessPredictionNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax


        self.build_dataset_button = wx.Button(self, -1, "BUILD DATASET", size=(10,10))

        team_choice_text = wx.StaticText(self, label="Team Choice")
        team_choices = ["Home Team", "Away Team"]
        self.team_choice = wx.ComboBox(self, size=(80,-1), choices=team_choices, style=wx.CB_READONLY)

        range_choice_text = wx.StaticText(self, label="Range Choice")
        range_choices = ["0", "5", "10", "15", "20", "25", "30", "35"]
        self.range_choice = wx.ComboBox(self, size=(80,-1), choices=range_choices, style=wx.CB_READONLY)


        kernel_parameters_box = wx.StaticBox(self, wx.ID_ANY, "KERNEL PARAMETERS")

        c_text = wx.StaticText(self, label="C (float)")
        self.c = wx.TextCtrl(self, -1, "1.0", size=(50,-1))

        kernel_choice_text = wx.StaticText(self, label="Kernel Choice")
        kernel_choices = ["rbf", "linear", "poly", "sigmoid", "precomputed"]
        self.kernel_choice = wx.ComboBox(self, size=(80,-1), choices=kernel_choices, style=wx.CB_READONLY)

        degree_text = wx.StaticText(self, label="degree (int)")
        self.degree = wx.TextCtrl(self, -1, "3", size=(50,-1))

        gamma_text = wx.StaticText(self, label="gamma (float)")
        self.gamma = wx.TextCtrl(self, -1, "auto", size=(50,-1))

        coef_text = wx.StaticText(self, label="coef (float)")
        self.coef = wx.TextCtrl(self, -1, "0.0", size=(50,-1))

        probability_choice_text = wx.StaticText(self, label="probability choice")
        probability_choices = ["False", "True"]
        self.probability_choice = wx.ComboBox(self, size=(80,-1), choices=probability_choices, style=wx.CB_READONLY)

        shrinking_choice_text = wx.StaticText(self, label="shrinking choice")
        shrinking_choices = ["True", "False"]
        self.shrinking_choice = wx.ComboBox(self, size=(80,-1), choices=shrinking_choices, style=wx.CB_READONLY)

        tol_text = wx.StaticText(self, label="tol (float)")
        self.tol = wx.TextCtrl(self, -1, "1e-3", size=(50,-1))

        cache_size_text = wx.StaticText(self, label="cache_size (float)")
        self.cache_size = wx.TextCtrl(self, size=(50,-1))

        verbose_choice_text = wx.StaticText(self, label="verbose choice")
        verbose_choices = ["False", "True"]
        self.verbose_choice = wx.ComboBox(self, size=(80,-1), choices=verbose_choices, style=wx.CB_READONLY)

        max_iter_text = wx.StaticText(self, label="max_iter (int)")
        self.max_iter = wx.TextCtrl(self, -1, "-1", size=(50,-1))

        decision_function_shape_choice_text = wx.StaticText(self, label="decision_function_shape choice")
        decision_function_shape_choices = ["None", "ovo", "ovr"]
        self.decision_function_shape_choice = wx.ComboBox(self, size=(80,-1), choices=decision_function_shape_choices,
                                                          style=wx.CB_READONLY)

        self.run_button = wx.Button(self, -1, "RUN", size=(80,40))



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.build_dataset_button, 1, wx.EXPAND)

        vbox.Add(team_choice_text, 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

        vbox.Add(range_choice_text, 0, wx.EXPAND)
        vbox.Add(self.range_choice, 0, wx.EXPAND)

        kernel_parameters_box_sizer = wx.StaticBoxSizer(kernel_parameters_box, wx.VERTICAL)

        # Create the grid which will be scrollable:
        scrolledPanel = scrolled.ScrolledPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.c, 1, wx.EXPAND)
        sizer.Add(self.kernel_choice, 1, wx.EXPAND)
        sizer.Add(self.degree, 1, wx.EXPAND)
        sizer.Add(self.gamma, 1, wx.EXPAND)
        sizer.Add(self.coef, 1, wx.EXPAND)
        sizer.Add(self.probability_choice, 1, wx.EXPAND)
        sizer.Add(self.shrinking_choice, 1, wx.EXPAND)
        sizer.Add(self.tol, 1, wx.EXPAND)
        sizer.Add(self.cache_size, 1, wx.EXPAND)
        sizer.Add(self.verbose_choice, 1, wx.EXPAND)
        sizer.Add(self.max_iter, 1, wx.EXPAND)
        sizer.Add(self.decision_function_shape_choice, 1, wx.EXPAND)

        scrolledPanel.SetSizer(sizer)
        # scrolledPanel.Layout()
        scrolledPanel.SetupScrolling()
        # scrolledPanel.Scroll()

        kernel_parameters_box_sizer.Add(scrolledPanel, 0, wx.EXPAND)
        vbox.Add(kernel_parameters_box_sizer, 1, wx.EXPAND)
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
        self.match.buildMatchObjects()
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
        # for team in [self.match.getHomeTeam(), self.match.getAwayTeam()]:
        #     # if not results == "":
        #     #     results += "\n\n"
        #     temp_results = []
        #     temp_results.append((team.team_name, "Running Distance"))
        #     for player in team.getTeamPlayers():
        #         if self.game_stop_filter.GetValue() and self.speed_filter.GetValue():
        #             # print "with game_stop and speed filter: ", team_player.computeRunningDistanceWithGameStopAndSpeedFilter()
        #             result = player.computeRunningDistanceWithGameStopAndSpeedFilter()
        #         elif self.game_stop_filter.GetValue():
        #             # print "with game_stop filter: ", team_player.computeRunningDistanceWithGameStopFilter()
        #             result = player.computeRunningDistanceWithGameStopFilter()
        #         elif self.speed_filter.GetValue():
        #             # print "with speed filter: ", team_player.computeRunningDistanceWithSpeedFilter()
        #             result = player.computeRunningDistanceWithSpeedFilter()
        #         else:
        #             # print "without filter: ", team_player.computeRunningDistance()
        #             result = player.computeRunningDistance()
        #         temp_results.append((player.jersey_number, result))
        #     results.append(temp_results)
        # results = self.formatInfoToDisplay(results)
    #     EventAnnotationManager.annotateAnalysisResults(self.canvas, self.ax, results)
    #
    #
    # def formatInfoToDisplay(self, results):
    #     print results
    #     q = ""
    #     for (home_js, home_result), (away_js, away_result) in itertools.izip(results[0], results[1]):
    #         try:
    #             q += "%s %s | %s %s\n" %(("%.2f"%home_result).ljust(30), str(home_js).center(10),
    #                                      str(away_js).center(10), ("%.2f"%away_result).rjust(30))
    #         except:
    #             q += "%s %s | %s %s\n" %(str(home_result).ljust(30), str(home_js).center(10),
    #                                      str(away_js).center(10), str(away_result).rjust(30))
    #     return q

