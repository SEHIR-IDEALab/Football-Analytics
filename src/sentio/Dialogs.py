import wx

__author__ = 'emrullah'


def ask(parent=None, message=''):
    app = wx.App()
    dlg = wx.TextEntryDialog(parent,
                              message)
    res = dlg.ShowModal()
    if res == wx.ID_OK:
        value = dlg.GetValue()
        return value
    dlg.Destroy()
    app.MainLoop()
