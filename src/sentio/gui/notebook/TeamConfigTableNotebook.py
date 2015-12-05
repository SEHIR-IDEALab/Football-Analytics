from src.sentio import Parameters

__author__ = 'emrullah'




import wx
import wx.grid



class TeamConfigTableNotebook(wx.Panel):

    def __init__(self, parent, canvas):
        wx.Panel.__init__(self, parent)

        self.canvas = canvas

        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 4)
        self.grid.SetColLabelValue(0, "ID")
        self.grid.SetColLabelValue(1, "js")
        self.grid.SetColLabelValue(2, "speed")
        self.grid.SetColLabelValue(3, "direction")

        # self.grid.SetDefaultColSize(60)
        self.grid.SetRowLabelSize(30)

        self.grid.SetColSize(0, 0)
        self.grid.SetColSize(1, 35)
        self.grid.SetColSize(2, 55)
        self.grid.SetColSize(3, 70)

        self.grid.EnableDragGridSize(False)
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()

        # self.grid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        # self.grid.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        # self.grid.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        # self.grid.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        # self.grid.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnCellChange)


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
            self.grid.SetCellValue(i, 2, str(visual_player.speed))
            self.grid.SetCellValue(i, 3, str(visual_player.direction))

            self.grid.SetCellBackgroundColour(i, 1, visual_player.getObjectColor())
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

        if Parameters.IS_SHOW_DIRECTIONS_ON:
            visual_player.drawDirectionWithSpeed()
            self.canvas.draw()
