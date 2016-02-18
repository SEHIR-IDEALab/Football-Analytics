from src.sentio import Parameters

__author__ = 'emrullah'




import wx
import wx.grid



class TeamConfigTableNotebook(wx.Panel):

    def __init__(self, parent, canvas):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas

        self.grid = wx.grid.Grid(self, size=(225, 200))
        self.grid.CreateGrid(0, 5)
        self.grid.SetColLabelValue(0, "ID")
        self.grid.SetColLabelValue(1, "js")
        self.grid.SetColLabelValue(2, "speed")
        self.grid.SetColLabelValue(3, "direc.")
        self.grid.SetColLabelValue(4, "acc.")

        # self.grid.SetDefaultColSize(60)
        self.grid.SetRowLabelSize(30)

        self.grid.SetColSize(0, 0)
        self.grid.SetColSize(1, 25)
        self.grid.SetColSize(2, 50)
        self.grid.SetColSize(3, 60)
        self.grid.SetColSize(4, 45)

        self.grid.EnableDragGridSize(False)
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()

        # self.grid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        # self.grid.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        # self.grid.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        # self.grid.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        # self.grid.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.global_speed = wx.CheckBox(self, -1, 'use global speed')
        speed_text = wx.StaticText(self, label="global speed")
        self.speed_entry = wx.TextCtrl(self, size=(50,-1))
        self.speed_entry.Disable()

        self.global_acceleration = wx.CheckBox(self, -1, 'use global acceleration')
        acceleration_text = wx.StaticText(self, label="global acceleration")
        self.acceleration_entry = wx.TextCtrl(self, size=(50,-1))

        self.globals_update_button = wx.Button(self, -1, "apply")

        self.speed_entry.Disable()
        self.acceleration_entry.Disable()


        #########################
        ######## Layout #########
        #########################

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND|wx.ALL)

        sizer.AddSpacer(5)

        globals_box = wx.StaticBox(self, wx.ID_ANY, "")
        globals_box_sizer = wx.StaticBoxSizer(globals_box, wx.VERTICAL)
        globals_box_sizer.Add(self.global_speed, 0, wx.EXPAND)

        speed_sizer = wx.BoxSizer(wx.HORIZONTAL)
        speed_sizer.Add(speed_text, 0, wx.EXPAND)
        speed_sizer.Add(self.speed_entry, 1, wx.EXPAND)

        globals_box_sizer.Add(speed_sizer, 0, wx.EXPAND)

        globals_box_sizer.AddSpacer(5)
        globals_box_sizer.Add(wx.StaticLine(self, style=wx.HORIZONTAL, size=(150,2)), 0, wx.ALIGN_CENTER)
        globals_box_sizer.AddSpacer(5)

        globals_box_sizer.Add(self.global_acceleration, 0, wx.EXPAND)

        acceleration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        acceleration_sizer.Add(acceleration_text, 0, wx.EXPAND)
        acceleration_sizer.Add(self.acceleration_entry, 1, wx.EXPAND)

        globals_box_sizer.Add(acceleration_sizer, 0, wx.EXPAND)
        globals_box_sizer.AddSpacer(5)
        globals_box_sizer.Add(wx.StaticLine(self, style=wx.HORIZONTAL, size=(100,2)), 0, wx.ALIGN_CENTER)
        globals_box_sizer.AddSpacer(5)
        globals_box_sizer.Add(self.globals_update_button, 0, wx.ALIGN_CENTER)

        sizer.Add(globals_box_sizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Fit(self)


        #####################
        ##### Binds #########
        #####################

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnCellChange)

        self.global_speed.Bind(wx.EVT_CHECKBOX, self.OnGlobalSpeed)
        self.global_acceleration.Bind(wx.EVT_CHECKBOX, self.OnGlobalAcceleration)

        self.globals_update_button.Bind(wx.EVT_BUTTON, self.OnGlobalsUpdate)


    def OnGlobalsUpdate(self, event):
        if self.global_speed.GetValue() or self.global_acceleration.GetValue():
            visual_players = self.visual_idToPlayers.values()
            for i in range(len(visual_players)):
                visual_player = visual_players[i]

                if self.global_speed.GetValue():
                    visual_player.speed = float(self.speed_entry.GetValue())

                if self.global_acceleration.GetValue():
                    visual_player.acceleration = float(self.acceleration_entry.GetValue())

                self.grid.SetCellValue(i, 2, self.displayMode(visual_player.speed))
                self.grid.SetCellValue(i, 4, self.displayMode(visual_player.acceleration))

                if Parameters.IS_SHOW_DIRECTIONS_ON:
                    visual_player.drawDirectionWithSpeed()
            self.canvas.draw()


    def chanceReadOnlyStatusForAndTo(self, column, status):
        for i in range(self.grid.GetNumberRows()):
            self.grid.SetReadOnly(i, column, status)


    def OnGlobalSpeed(self, event):
        if self.global_speed.GetValue():
            self.speed_entry.Enable()
            self.chanceReadOnlyStatusForAndTo(2, True)
        else:
            self.speed_entry.Disable()
            self.chanceReadOnlyStatusForAndTo(2, False)


    def OnGlobalAcceleration(self, event):
        if self.global_acceleration.GetValue():
            self.acceleration_entry.Enable()
            self.chanceReadOnlyStatusForAndTo(4, True)
        else:
            self.acceleration_entry.Disable()
            self.chanceReadOnlyStatusForAndTo(4, False)


    def update(self, visual_idToPlayers, snapShot=False):
        self.visual_idToPlayers = visual_idToPlayers
        self.resizeRows(len(self.visual_idToPlayers))

        #- Populate the grid with new data:
        visual_players = self.visual_idToPlayers.values()
        for i in range(len(visual_players)):
            visual_player = visual_players[i]

            if snapShot:
                visual_player.speed = visual_player.player.speed
                visual_player.direction = visual_player.player.direction
            else:
                visual_player.calculateSpeed()
                visual_player.calculateDirection()

            # self.grid.SetCellEditor(i, 0, wx.grid.GridCellNumberEditor())
            # self.grid.SetCellEditor(i, 2, wx.grid.GridCellFloatEditor())
            # self.grid.SetCellEditor(i, 3, wx.grid.GridCellFloatEditor())

            self.grid.SetCellValue(i, 0, str(visual_player.player.object_id))
            self.grid.SetCellValue(i, 1, str(visual_player.player.jersey_number))
            self.grid.SetCellValue(i, 2, self.displayMode(visual_player.speed))
            self.grid.SetCellValue(i, 3, self.displayMode(visual_player.direction))
            self.grid.SetCellValue(i, 4, self.displayMode(visual_player.acceleration))

            self.grid.SetCellBackgroundColour(i, 1, visual_player.getObjectColor())
            self.grid.SetCellTextColour(i, 1, "white")
            self.grid.SetReadOnly(i, 1, True)


    def resizeRows(self, number_of_players):
        current, new = (self.grid.GetNumberRows(), number_of_players)

        if new < current:
            #- Delete rows:
            self.grid.DeleteRows(0, current-new, True)

        if new > current:
            #- append rows:
            self.grid.AppendRows(new-current)


    def OnCellChange(self, evt):
        id = int(self.grid.GetCellValue(evt.GetRow(), 0))
        js = int(self.grid.GetCellValue(evt.GetRow(), 1))

        visual_player = self.visual_idToPlayers[id]
        value = float(self.grid.GetCellValue(evt.GetRow(), evt.GetCol()))

        if evt.GetCol() == 2:
            visual_player.speed = value
            print "speed changed for: ", js
        elif evt.GetCol() == 3:
            visual_player.direction = value
            print "direction changed for: ", js
        elif evt.GetCol() == 4:
            visual_player.acceleration = value
            print "acceleration changed for: ", js

        if Parameters.IS_SHOW_DIRECTIONS_ON:
            visual_player.drawDirectionWithSpeed()
            self.canvas.draw()


    def displayMode(self, value):
        return "{0:.1f}".format(value)

