from src.sentio.Parameters import FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X, \
                                  FOOTBALL_FIELD_MAX_Y, FOOTBALL_FIELD_MIN_Y


import sys
import numpy as np
import matplotlib.tri
import matplotlib.path
from src.sentio.gui.Voronoi import Voronoi


__author__ = 'emrullah'



class DominantRegion:

    def __init__(self, ax):
        self.ax = ax

        self.voronoi_lines = None


    def circumcircle2(self, T):
        P1,P2,P3=T[:,0], T[:,1], T[:,2]
        b = P2 - P1
        c = P3 - P1
        d=2*(b[:,0]*c[:,1]-b[:,1]*c[:,0])
        center_x=(c[:,1]*(np.square(b[:,0])+np.square(b[:,1]))- b[:,1]*(np.square(c[:,0])+np.square(c[:,1])))/d + P1[:,0]
        center_y=(b[:,0]*(np.square(c[:,0])+np.square(c[:,1]))- c[:,0]*(np.square(b[:,0])+np.square(b[:,1])))/d + P1[:,1]
        return np.array((center_x, center_y)).T


    def check_outside(self, point, bbox):
        point=np.round(point, 4)
        return point[0]<bbox[0] or point[0]>bbox[2] or point[1]< bbox[1] or point[1]>bbox[3]


    def move_point(self, start, end, bbox):
        vector=end-start
        c=self.calc_shift(start, vector, bbox)
        if c>0 and c<1:
            start=start+c*vector
            return start


    def calc_shift(self, point, vector, bbox):
        c=sys.float_info.max
        for l,m in enumerate(bbox):
            a=(float(m)-point[l%2])/vector[l%2]
            if  a>0 and  not self.check_outside(point+a*vector, bbox):
                if abs(a)<abs(c):
                    c=a
        return c if c<sys.float_info.max else None


    def voronoi2(self, P, bbox=None):
        if not isinstance(P, np.ndarray):
            P=np.array(P)
        if not bbox:
            xmin=P[:,0].min()
            xmax=P[:,0].max()
            ymin=P[:,1].min()
            ymax=P[:,1].max()
            xrange=(xmax-xmin) * 0.3333333
            yrange=(ymax-ymin) * 0.3333333
            bbox=(xmin-xrange, ymin-yrange, xmax+xrange, ymax+yrange)
        bbox=np.round(bbox,4)

        D = matplotlib.tri.Triangulation(P[:,0],P[:,1])

        T = D.triangles
        n = T.shape[0]
        C = self.circumcircle2(P[T])

        segments = []
        for i in range(n):
            for j in range(3):
                k = D.neighbors[i][j]
                if k != -1:
                    #cut segment to part in bbox
                    start,end=C[i], C[k]
                    if self.check_outside(start, bbox):
                        start=self.move_point(start,end, bbox)
                        if  start is None:
                            continue
                    if self.check_outside(end, bbox):
                        end=self.move_point(end,start, bbox)
                        if  end is None:
                            continue
                    segments.append( [start, end] )
                else:
                    #ignore center outside of bbox
                    if self.check_outside(C[i], bbox) :
                        continue
                    first, second, third=P[T[i,j]], P[T[i,(j+1)%3]], P[T[i,(j+2)%3]]
                    edge=np.array([first, second])
                    vector=np.array([[0,1], [-1,0]]).dot(edge[1]-edge[0])
                    line=lambda p: (p[0]-first[0])*(second[1]-first[1])/(second[0]-first[0])  -p[1] + first[1]
                    orientation=np.sign(line(third))*np.sign( line(first+vector))
                    if orientation>0:
                        vector=-orientation*vector
                    c=self.calc_shift(C[i], vector, bbox)
                    if c is not None:
                        segments.append([C[i],C[i]+c*vector])
        return segments


    def draw(self, visual_players):
        lines=self.voronoi2(Voronoi.getPositions(visual_players),
                            (FOOTBALL_FIELD_MIN_X,FOOTBALL_FIELD_MIN_Y,
                             FOOTBALL_FIELD_MAX_X, FOOTBALL_FIELD_MAX_Y))

        lines = matplotlib.collections.LineCollection(lines, color='red')
        self.ax.add_collection(lines)
        self.voronoi_lines = lines


    def remove(self):
        if self.voronoi_lines:
            self.voronoi_lines.remove()
            self.voronoi_lines = None


    def update(self, visual_idToPlayers):
        self.remove()
        self.draw(visual_idToPlayers.values())