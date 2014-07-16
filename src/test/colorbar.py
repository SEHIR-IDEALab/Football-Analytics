'''
Make a colorbar as a separate figure.
'''

from matplotlib import pyplot
import matplotlib as mpl

# Make a figure and axes with dimensions as desired.
fig = pyplot.figure(figsize=(8,3))
ax1 = fig.add_axes([0.05, 0.15, 0.9, 0.9])

# Set the colormap and norm to correspond to the data for which
# the colorbar will be used.
cmap = mpl.cm.hot
norm = mpl.colors.Normalize(vmin=5, vmax=10)

# ColorbarBase derives from ScalarMappable and puts a colorbar
# in a specified axes, so it has everything needed for a
# standalone colorbar.  There are many more kwargs, but the
# following gives a basic continuous colorbar with ticks
# and labels.
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                   norm=norm,
                                   orientation='horizontal')
cb1.set_label('Some Units')




pyplot.show()


"""
### colorbar canvas
        fig = Figure((5,0.5))
        ax1 = fig.add_axes([0, 0.4, 1, 1])
        self.colorbar_canvas = FigCanvas(self, -1, fig)

        cmap = matplotlib.cm.hot
        norm = matplotlib.colors.Normalize(vmin=5, vmax=10)

        cb1 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='horizontal')
"""