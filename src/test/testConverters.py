from matplotlib.offsetbox import DraggableBase


class DraggableAnnotation(DraggableBase):
    def __init__(self, annotation, use_blit=False):
        DraggableBase.__init__(self, annotation, use_blit=use_blit)
        self.annotation = annotation

    def save_offset(self):
        ann = self.annotation
        x, y = ann.xyann
        if isinstance(ann.anncoords, tuple):
            xcoord, ycoord = ann.anncoords
            x1, y1 = ann._get_xy(self.canvas.renderer, x, y, xcoord)
            x2, y2 = ann._get_xy(self.canvas.renderer, x, y, ycoord)
            ox0, oy0 = x1, y2
        else:
            ox0, oy0 = ann._get_xy(self.canvas.renderer, x, y, ann.anncoords)

        self.ox, self.oy = ox0, oy0
        self.annotation.anncoords = "figure pixels"
        self.update_offset(0, 0)

    def update_offset(self, dx, dy):
        ann = self.annotation
        ann.xyann = self.ox + dx, self.oy + dy
        x, y = ann.xyann

    def finalize_offset(self):
        loc_in_canvas = self.annotation.xyann
        self.annotation.anncoords = "axes fraction"
        pos_axes_fraction = self.annotation.axes.transAxes.inverted()
        pos_axes_fraction = pos_axes_fraction.transform_point(loc_in_canvas)
        self.annotation.xyann = tuple(pos_axes_fraction)