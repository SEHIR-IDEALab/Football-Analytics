from src.sentio.analytics.prediction.PassSuccessPrediction import PassSuccessPrediction

__author__ = 'emrullah'


import wx
import wx.lib.scrolledpanel as scrolled



class PassSuccessPredictionNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax, fig):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax
        self.fig = fig

        self.position = None


        self.mark_button = wx.Button(self, -1, "click and mark a point!", size=(10,10))

        team_choice_text = wx.StaticText(self, label="Team Choice")
        team_choices = ["Home Team", "Away Team"]
        self.team_choice = wx.ComboBox(self, size=(80,-1), choices=team_choices, style=wx.CB_READONLY)

        range_choice_text = wx.StaticText(self, label="Range Choice")
        range_choices = ["0", "5", "10", "15", "20", "25", "30", "35"]
        self.range_choice = wx.ComboBox(self, size=(80,-1), choices=range_choices, style=wx.CB_READONLY)


        kernel_parameters_box = wx.StaticBox(self, wx.ID_ANY, "KERNEL PARAMETERS")

        self.panel2 = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(600,200), style=wx.SIMPLE_BORDER)
        self.panel2.SetupScrolling()

        c_text = wx.StaticText(self.panel2, label="C (float)")
        self.c = wx.TextCtrl(self.panel2, -1, "1.0", size=(50,-1))
        #
        kernel_choice_text = wx.StaticText(self.panel2, label="Kernel Choice")
        kernel_choices = ["rbf", "linear", "poly", "sigmoid", "precomputed"]
        self.kernel_choice = wx.ComboBox(self.panel2, size=(80,-1), choices=kernel_choices, style=wx.CB_READONLY)

        degree_text = wx.StaticText(self.panel2, label="degree (int)")
        self.degree = wx.TextCtrl(self.panel2, -1, "3", size=(50,-1))

        gamma_text = wx.StaticText(self.panel2, label="gamma (float)")
        self.gamma = wx.TextCtrl(self.panel2, -1, "0.0005", size=(50,-1))

        coef_text = wx.StaticText(self.panel2, label="coef (float)")
        self.coef = wx.TextCtrl(self.panel2, -1, "0.0", size=(50,-1))

        probability_choice_text = wx.StaticText(self.panel2, label="probability choice")
        probability_choices = ["False", "True"]
        self.probability_choice = wx.ComboBox(self.panel2, size=(80,-1), choices=probability_choices, style=wx.CB_READONLY)

        shrinking_choice_text = wx.StaticText(self.panel2, label="shrinking choice")
        shrinking_choices = ["True", "False"]
        self.shrinking_choice = wx.ComboBox(self.panel2, size=(80,-1), choices=shrinking_choices, style=wx.CB_READONLY)

        tol_text = wx.StaticText(self.panel2, label="tol (float)")
        self.tol = wx.TextCtrl(self.panel2, -1, "0.001", size=(50,-1))

        # cache_size_text = wx.StaticText(self.panel2, label="cache_size (float)")
        # self.cache_size = wx.TextCtrl(self.panel2, size=(50,-1))

        verbose_choice_text = wx.StaticText(self.panel2, label="verbose choice")
        verbose_choices = ["False", "True"]
        self.verbose_choice = wx.ComboBox(self.panel2, size=(80,-1), choices=verbose_choices, style=wx.CB_READONLY)

        max_iter_text = wx.StaticText(self.panel2, label="max_iter (int)")
        self.max_iter = wx.TextCtrl(self.panel2, -1, "-1", size=(50,-1))

        # decision_function_shape_choice_text = wx.StaticText(self.panel2, label="decision_function_shape choice")
        # decision_function_shape_choices = ["None", "ovo", "ovr"]
        # self.decision_function_shape_choice = wx.ComboBox(self.panel2, size=(80,-1), choices=decision_function_shape_choices,
        #                                                   style=wx.CB_READONLY)


        self.run_button = wx.Button(self, -1, "RUN", size=(80,40))



        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.mark_button, 1, wx.EXPAND)

        vbox.Add(team_choice_text, 0, wx.EXPAND)
        vbox.Add(self.team_choice, 0, wx.EXPAND)

        vbox.Add(range_choice_text, 0, wx.EXPAND)
        vbox.Add(self.range_choice, 0, wx.EXPAND)

        kernel_parameters_box_sizer = wx.StaticBoxSizer(kernel_parameters_box, wx.VERTICAL)
        #
        # # Create the grid which will be scrollable:
        # scrolledPanel = scrolled.ScrolledPanel(self)
        #
        sizer = wx.BoxSizer(wx.VERTICAL)

        c_sizer = wx.BoxSizer(wx.HORIZONTAL)
        c_sizer.Add(c_text)
        c_sizer.Add(self.c)
        sizer.Add(c_sizer)

        kernel_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        kernel_choice_sizer.Add(kernel_choice_text)
        kernel_choice_sizer.Add(self.kernel_choice)
        sizer.Add(kernel_choice_sizer)

        degree_sizer = wx.BoxSizer(wx.HORIZONTAL)
        degree_sizer.Add(degree_text)
        degree_sizer.Add(self.degree)
        sizer.Add(degree_sizer)

        gamma_sizer = wx.BoxSizer(wx.HORIZONTAL)
        gamma_sizer.Add(gamma_text)
        gamma_sizer.Add(self.gamma)
        sizer.Add(gamma_sizer)

        coef_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coef_sizer.Add(coef_text)
        coef_sizer.Add(self.coef)
        sizer.Add(coef_sizer)

        probability_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        probability_choice_sizer.Add(probability_choice_text)
        probability_choice_sizer.Add(self.probability_choice)
        sizer.Add(probability_choice_sizer)

        shrinking_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        shrinking_choice_sizer.Add(shrinking_choice_text)
        shrinking_choice_sizer.Add(self.shrinking_choice)
        sizer.Add(shrinking_choice_sizer)

        tol_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tol_sizer.Add(tol_text)
        tol_sizer.Add(self.tol)
        sizer.Add(tol_sizer)

        # cache_size_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # cache_size_sizer.Add(cache_size_text)
        # cache_size_sizer.Add(self.cache_size)
        # sizer.Add(cache_size_sizer)

        verbose_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        verbose_choice_sizer.Add(verbose_choice_text)
        verbose_choice_sizer.Add(self.verbose_choice)
        sizer.Add(verbose_choice_sizer)

        max_iter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        max_iter_sizer.Add(max_iter_text)
        max_iter_sizer.Add(self.max_iter)
        sizer.Add(max_iter_sizer)

        # decision_function_shape_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # decision_function_shape_choice_sizer.Add(decision_function_shape_choice_text)
        # decision_function_shape_choice_sizer.Add(self.decision_function_shape_choice)
        # sizer.Add(decision_function_shape_choice_sizer)

        self.panel2.SetSizer(sizer)

        kernel_parameters_box_sizer.Add(self.panel2, 0, wx.EXPAND)
        vbox.Add(kernel_parameters_box_sizer, 1, wx.EXPAND)
        vbox.Add(self.run_button, 1, wx.EXPAND)

        self.SetSizer(vbox)
        # vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.mark_button.Bind(wx.EVT_BUTTON, self.OnMark)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnCompute)




    def setMatch(self, match):
        self.match = match

        self.pass_success_prediction = PassSuccessPrediction(self.canvas, self.ax, self.fig)
        self.pass_success_prediction.setMatch(self.match)


    def OnMark(self, event):
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)


    def onclick(self, event):
        self.position = event.xdata, event.ydata
        self.ax.plot([event.xdata], [event.ydata], 'x', mew=5, ms=15, color="black")
        self.canvas.draw()
        self.fig.canvas.mpl_disconnect(self.cid)


    def setWxGui(self, wx_gui):
        self.wx_gui = wx_gui


    def OnCompute(self, event):
        self.wx_gui.removeAllAnnotations()
        self.wx_gui.removeVisualPlayers()

        self.pass_success_prediction.getPasses(self.position, float(self.range_choice.GetValue()), self.team_choice.GetValue(),
                    float(self.c.GetValue()),
                    str(self.kernel_choice.GetValue()),
                    int(self.degree.GetValue()),
                    (float(self.gamma.GetValue()) if self.gamma.GetValue() != "auto" else str(self.gamma.GetValue())),
                    float(self.coef.GetValue()),
                    bool(self.probability_choice.GetValue()),
                    bool(self.shrinking_choice.GetValue()),
                    float(self.tol.GetValue()),
                    bool(self.verbose_choice.GetValue()),
                    int(self.max_iter.GetValue()))
        self.canvas.draw()

        # results = []
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

