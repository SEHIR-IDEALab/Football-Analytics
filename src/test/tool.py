from matplotlib.widgets import RadioButtons
from pylab import figure, show, np

t = np.arange(0.0, 2.0, 0.01)
s1 = np.sin(2*np.pi*t)
fig = figure()
ax1 = fig.add_axes([0,0,1,1])

q = RadioButtons(ax1, labels=["a", "w"], activecolor="black")

show()