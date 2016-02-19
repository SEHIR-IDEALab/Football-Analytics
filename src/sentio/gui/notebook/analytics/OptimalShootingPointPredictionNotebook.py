from matplotlib.text import Text
from src.sentio.Parameters import PASS_SOURCE_RADIUS, PASS_TARGET_RADIUS_COEFFICIENT
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.analytics.prediction.OptimalShootingPointPrediction import OptimalShootingPointPrediction


__author__ = 'emrullah'


import wx



class OptimalShootingPointPredictionNotebook(wx.Panel):

    def __init__(self, parent, canvas, ax, fig):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas
        self.ax = ax
        self.fig = fig

        self.temp_ball_holder = None

        self.markPlayer_button = wx.Button(self, -1, "click and mark a player!", size=(10,10))
        self.run_button = wx.Button(self, -1, "RUN", size=(80,40))

        self.iteration_choice = wx.ComboBox(self, size=(80,-1), style=wx.CB_READONLY,
                                            choices=["0", "5", "10", "15", "20", "25", "30", "35"])
        self.step_size_choice = wx.ComboBox(self, size=(80,-1), style=wx.CB_READONLY,
                                            choices=["1", "2", "3", "4", "5"])


        #########################
        ######## Layout #########
        #########################

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(self.markPlayer_button, 1, wx.EXPAND)
        vbox.Add(wx.StaticText(self, label="Number of Iterations"), 0, wx.EXPAND)
        vbox.Add(self.iteration_choice, 0, wx.EXPAND)
        vbox.Add(wx.StaticText(self, label="Step Size"), 0, wx.EXPAND)
        vbox.Add(self.step_size_choice, 0, wx.EXPAND)

        risk_parameters_box = wx.StaticBox(self, wx.ID_ANY, "Risk Parameters", style=wx.ALIGN_CENTER)
        self.risk_parameter1 = wx.TextCtrl(self, -1, str(PASS_SOURCE_RADIUS), size=(50,-1))
        self.risk_parameter2 = wx.TextCtrl(self, -1, str(PASS_TARGET_RADIUS_COEFFICIENT), size=(50,-1))
        self.risk_parameter3 = wx.TextCtrl(self, -1, "---", size=(50,-1))

        risk_parameters_box_sizer = wx.StaticBoxSizer(risk_parameters_box, wx.VERTICAL)
        risk_parameters_box_sizer.Add(wx.StaticText(self, label="Pass source radius"), 0, wx.EXPAND)
        risk_parameters_box_sizer.Add(self.risk_parameter1, 0, wx.EXPAND)
        risk_parameters_box_sizer.Add(wx.StaticText(self, label="Pass target radius coefficient"), 0, wx.EXPAND)
        risk_parameters_box_sizer.Add(self.risk_parameter2, 0, wx.EXPAND)
        risk_parameters_box_sizer.Add(wx.StaticText(self, label="Shoot radius"), 0, wx.EXPAND)
        risk_parameters_box_sizer.Add(self.risk_parameter3, 0, wx.EXPAND)

        vbox.Add(risk_parameters_box_sizer, 0, wx.EXPAND)
        vbox.Add(self.run_button, 1, wx.EXPAND)

        self.SetSizer(vbox)
        # vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.markPlayer_button.Bind(wx.EVT_BUTTON, self.onMarkPlayer)
        self.run_button.Bind(wx.EVT_BUTTON, self.onCompute)




    def setWxGui(self, wx_gui):
        self.wx_gui = wx_gui


    def onMarkPlayer(self, event):
        self.cid = self.fig.canvas.mpl_connect('pick_event', self.onPick)


    def onPick(self, event):
        if isinstance(event.artist, Text):

            if self.wx_gui.ball_holder is not None:
                self.wx_gui.ball_holder.clearBallHolder()

            if self.temp_ball_holder is not None:
                self.temp_ball_holder.set_bbox(dict(boxstyle="circle,pad=0.3",
                                           fc=self.temp_ball_holder.team_color,
                                           ec=self.temp_ball_holder.player_color,
                                           alpha=0.5,
                                           linewidth=1))

            self.temp_ball_holder = event.artist
            self.temp_ball_holder.set_bbox(dict(boxstyle="circle,pad=0.3",
                                           fc=event.artist.team_color,
                                           ec="yellow",
                                           linewidth=2))

            self.canvas.draw()
            self.fig.canvas.mpl_disconnect(self.cid)


    def convertVisualPlayerToPlayer(self, visual_player):
        visual_player = self.wx_gui.visual_idToPlayers[visual_player.object_id]
        player = visual_player.player
        player.set_position(visual_player.get_position())
        return player


    def onCompute(self, event):
        teams = ReaderBase.divideIntoTeams(self.wx_gui.visual_idToPlayers.values())

        self.wx_gui.pass_logger.pass_evaluate.teams = teams
        optimalShootingPointPrediction = OptimalShootingPointPrediction(teams)

        best_goal_chance, scat_xr,scat_yr, s1x,s1y = optimalShootingPointPrediction.predict(
                                                            self.convertVisualPlayerToPlayer(self.temp_ball_holder),
                                                            self.wx_gui.pass_logger.pass_evaluate.goalChance,
                                                            iterate=15)

        self.ax.scatter(scat_xr,scat_yr,s=30,c='red',label = "Opponent Players")
        self.ax.scatter(s1x,s1y,s=30,c='blue',label = "ball owner")

        self.canvas.draw()

        # current_pass_event = PassEvent(self.convertVisualPlayerToPlayer(self.pass_event.textcoords),
        #                                            self.convertVisualPlayerToPlayer(self.pass_event.xycoords),
        #                                            ReaderBase.divideIntoTeams(self.visual_idToPlayers.values(),
        #                                                visual=True))