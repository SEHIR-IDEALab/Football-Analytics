__author__ = 'emrullah'




import wx
import wx.grid



class TeamConfigTableNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 3)
        self.grid.SetColLabelValue(0, "js")
        self.grid.SetColLabelValue(1, "speed")
        self.grid.SetColLabelValue(2, "direction")

        # self.grid.SetDefaultColSize(60)
        self.grid.SetRowLabelSize(30)

        self.grid.SetColSize(0, 35)
        self.grid.SetColSize(1, 55)
        self.grid.SetColSize(2, 70)

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


    def update(self, visual_players, snapShot=False):
        self.resizeRows(len(visual_players))

        #- Populate the grid with new data:
        for i in range(len(visual_players)):
            visual_player = visual_players[i]
            
            if snapShot:
                visual_player.speed = visual_player.player.speed
                visual_player.direction = visual_player.player.direction
            else:
                visual_player.calculateSpeed()
                visual_player.calculateDirection()

            self.grid.SetCellValue(i, 0, str(visual_player.player.jersey_number))
            self.grid.SetCellValue(i, 1, str(visual_player.speed))
            self.grid.SetCellValue(i, 2, str(visual_player.direction))

            self.grid.SetCellBackgroundColour(i, 0, visual_player.getObjectColor())
            self.grid.SetReadOnly(i, 0, True)


    def resizeRows(self, number_of_players):
        current, new = (self.grid.GetNumberRows(), number_of_players)

        if new < current:
            #- Delete rows:
            self.grid.DeleteRows(0, current-new, True)

        if new > current:
            #- append rows:
            self.grid.AppendRows(new-current)


    def OnCellChange(self, evt):
        print "OnCellChange: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(), evt.GetPosition())

        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        value = self.grid.GetCellValue(evt.GetRow(), evt.GetCol())

        print value

        if value == 'no good':
            self.moveTo = evt.GetRow(), evt.GetCol()