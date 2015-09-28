from matplotlib.path import Path
from matplotlib.patches import BoxStyle
from src.sentio.Parameters import VISUAL_PLAYER_RADIUS


class CircleStyle(BoxStyle._Base):
    """
    A simple box.
    """

    def __init__(self, pad=0.3):

        self.pad = pad
        super(CircleStyle, self).__init__()

    def transmute(self, x0, y0, width, height, mutation_size):

        # padding
        # pad = mutation_size * self.pad

        cx, cy = x0+.5*width, y0+.5*height # center
        
        # width and height with padding added.
        # width, height = width + 2.*pad, height + 2.*pad,

        # get radius
        # radius = (width**2 + height**2)**.5 * .5

        radius = VISUAL_PLAYER_RADIUS

        cir_path = Path.unit_circle()
        vertices = radius*cir_path.vertices + (cx, cy)

        # a path of the circle
        path = Path(vertices, cir_path.codes)

        return path
