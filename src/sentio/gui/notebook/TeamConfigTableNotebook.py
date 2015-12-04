__author__ = 'emrullah'




import wx
import wx.grid as gridlib



class TeamConfigTableNotebook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 3)
        self.grid.SetColLabelValue(0, "js")
        self.grid.SetColLabelValue(1, "speed")
        self.grid.SetColLabelValue(2, "direction")

        self.grid.SetDefaultColSize(60)
        self.grid.SetRowLabelSize(30)

        self.grid.SetColSize(0, 45)
        self.grid.SetColSize(1, 55)
        self.grid.SetColSize(2, 65)

        self.grid.EnableDragGridSize(False)
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()

        # self.grid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        # self.grid.SetCellTextColour(1, 1, wx.RED)
        # self.grid.SetCellBackgroundColour(2, 2, wx.CYAN)
        #
        # self.grid.SetReadOnly(3, 3, True)
        #
        # self.grid.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        # self.grid.SetCellValue(5, 0, "123")
        # self.grid.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        # self.grid.SetCellValue(6, 0, "123.34")
        # self.grid.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        #
        # self.grid.SetCellSize(11, 1, 3, 3)
        # self.grid.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        # self.grid.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)


    def resizeRows(self, number_of_players):
        current, new = (self.grid.GetNumberRows(), number_of_players)

        if new < current:
            #- Delete rows:
            self.grid.DeleteRows(0, current-new, True)

        if new > current:
            #- append rows:
            self.grid.AppendRows(new-current)


    def update(self, visual_players):
        self.resizeRows(len(visual_players))

        #- Populate the grid with new data:
        for i in range(len(visual_players)):
            visual_player = visual_players[i]
            self.grid.SetCellValue(i, 0, str(visual_player.player.jersey_number))
            self.grid.SetCellValue(i, 1, str(visual_player.calculateSpeed()))
            self.grid.SetCellValue(i, 2, str(visual_player.calculateDirection()))

            self.grid.SetCellBackgroundColour(i, 0, visual_player.getObjectColor())
            self.grid.SetReadOnly(i, 0, True)