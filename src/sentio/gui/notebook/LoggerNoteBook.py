__author__ = 'emrullah'


import wx



class LoggerNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.logger = wx.TextCtrl(self, size=(150,530), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font1 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, u'Tahoma')
        self.logger.SetFont(font1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.logger, 1, wx.EXPAND)

        self.SetSizer(vbox)
        #vbox.Fit(self)