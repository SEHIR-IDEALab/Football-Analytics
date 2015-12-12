from src.sentio import Parameters

__author__ = 'emrullah'


import wx



class LoggerNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.logger = wx.TextCtrl(self, size=(150,530), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font1 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, u'Tahoma')
        self.logger.SetFont(font1)

        effectiveness_box = wx.StaticBox(self, wx.ID_ANY, "EFFECTIVENESS PARAMETERS", style=wx.ALIGN_CENTER)

        self.gain_comp = wx.CheckBox(self, -1, 'gain')
        self.w1 = wx.TextCtrl(self, -1, str(Parameters.W1), size=(50,-1))
        self.effectiveness_comp = wx.CheckBox(self, -1, 'effectiveness')
        self.w2 = wx.TextCtrl(self, -1, str(Parameters.W2), size=(50,-1))
        self.pass_advantage_comp = wx.CheckBox(self, -1, 'pass advantage')
        self.w3 = wx.TextCtrl(self, -1, str(Parameters.W3), size=(50,-1))
        self.goal_chance_comp = wx.CheckBox(self, -1, 'goal chance')
        self.w4 = wx.TextCtrl(self, -1, str(Parameters.W4), size=(50,-1))

        self.apply_button = wx.Button(self, -1, ">> APPLY <<")


        self.gain_comp.SetValue(True)
        self.effectiveness_comp.SetValue(True)
        self.pass_advantage_comp.SetValue(True)
        self.goal_chance_comp.SetValue(True)

        #########################
        ######## Layout #########
        #########################

        effectiveness_box_sizer = wx.StaticBoxSizer(effectiveness_box, wx.VERTICAL)
        effectiveness_box_sizer.Add(self.gain_comp, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.w1, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.effectiveness_comp, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.w2, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.pass_advantage_comp, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.w3, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.goal_chance_comp, 0, wx.EXPAND)
        effectiveness_box_sizer.Add(self.w4, 0, wx.EXPAND)
        effectiveness_box_sizer.AddSpacer(10)
        effectiveness_box_sizer.Add(self.apply_button, 0, wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.logger, 1, wx.EXPAND)
        vbox.Add(effectiveness_box_sizer, 0, wx.EXPAND)

        self.SetSizer(vbox)
        #vbox.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.gain_comp.Bind(wx.EVT_CHECKBOX, self.OnGainComp)
        self.effectiveness_comp.Bind(wx.EVT_CHECKBOX, self.OnEffectivenessComp)
        self.pass_advantage_comp.Bind(wx.EVT_CHECKBOX, self.OnPassAdvantageComp)
        self.goal_chance_comp.Bind(wx.EVT_CHECKBOX, self.OnGoalChanceComp)

        self.apply_button.Bind(wx.EVT_BUTTON, self.OnApply)


    def OnGainComp(self, event):
        if self.gain_comp.GetValue():
            self.w1.Enable()
        else:
            self.w1.Disable()


    def OnEffectivenessComp(self, event):
        if self.effectiveness_comp.GetValue():
            self.w2.Enable()
        else:
            self.w2.Disable()


    def OnPassAdvantageComp(self, event):
        if self.pass_advantage_comp.GetValue():
            self.w3.Enable()
        else:
            self.w3.Disable()


    def OnGoalChanceComp(self, event):
        if self.goal_chance_comp.GetValue():
            self.w4.Enable()
        else:
            self.w4.Disable()


    def OnApply(self, event):
        if self.gain_comp.GetValue():
            Parameters.W1 = float(self.w1.GetValue())
        if self.effectiveness_comp.GetValue():
            Parameters.W2 = float(self.w2.GetValue())
        if self.pass_advantage_comp.GetValue():
            Parameters.W3 = float(self.w3.GetValue())
        if self.goal_chance_comp.GetValue():
            Parameters.W4 = float(self.w4.GetValue())

        print Parameters.W1, Parameters.W2, Parameters.W3, Parameters.W4
