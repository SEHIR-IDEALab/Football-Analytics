from matplotlib.patches import Polygon
from src.sentio.Parameters import FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X, \
                                  FOOTBALL_FIELD_MAX_Y, FOOTBALL_FIELD_MIN_Y


import sys
import numpy as np
import matplotlib.tri
from scipy import spatial
import matplotlib.path




__author__ = 'emrullah'



class Voronoi:

    def __init__(self, ax):
        self.ax = ax

        self.voronoi_lines = None
        self.voronoi_regions = []



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

        def getPositions(visual_players):
            q = []
            for visual_player in visual_players:
                x, y = visual_player.get_position()
                q.append(np.array([x,y]))
            return np.array(q)

        # def getPositions(visual_players):
        #     q = []
        #     for visual_player in visual_players:
        #         if visual_player.player.isPlayer():
        #             x, y = visual_player.get_position()
        #             q.append(np.array([x,y]))
        #     return np.array(q)


        # # print positions
        # lines=self.voronoi2(positions, (FOOTBALL_FIELD_MIN_X,FOOTBALL_FIELD_MIN_Y,
        #                              FOOTBALL_FIELD_MAX_X, FOOTBALL_FIELD_MAX_Y))
        #
        # # for line in lines:
        # #     self.ax.fill(*zip(*line), alpha=0.4, color="red")
        #
        #
        # # self.ax.scatter(points[:,0], points[:,1], color="blue")
        # print lines
        # lines = matplotlib.collections.LineCollection(lines, color='red')
        # self.ax.add_collection(lines)
        # # self.ax.axis((-20,120, -20,120))
        # # self.ax.show()
        # self.voronoi_lines = lines





        # compute Voronoi tesselation
        vor = spatial.Voronoi(getPositions(visual_players))

        # plot
        regions, vertices = self.voronoi_finite_polygons_2d(vor)
        # print "--"
        # print regions
        # print "--"
        # print vertices

        # colorize
        for index, region in enumerate(regions):
            polygon = vertices[region]
            visual_player = visual_players[index]
            # polygon = self.fill_normalizer(polygon)
            poly_patch = Polygon(polygon,
                                 alpha=0.4,
                                 color=visual_player.getObjectColor())  # fc and ec
            self.ax.add_patch(poly_patch)
            self.voronoi_regions.append(poly_patch)
            # voronoi_region = self.ax.fill(*zip(*polygon), alpha=0.4, color=visual_player.getObjectColor())


    def fill_normalizer(self, polygon):
        for index in range(len(polygon)):
            position = polygon[index]
            x, y = position
            if x < FOOTBALL_FIELD_MIN_X:
                x = FOOTBALL_FIELD_MIN_X
            elif x > FOOTBALL_FIELD_MAX_X:
                x = FOOTBALL_FIELD_MAX_X

            if y < FOOTBALL_FIELD_MIN_Y:
                y = FOOTBALL_FIELD_MIN_Y
            elif y > FOOTBALL_FIELD_MAX_Y:
                y = FOOTBALL_FIELD_MAX_Y
            polygon[index] = np.array([x,y])
        return polygon


    def remove(self):
        if self.voronoi_lines:
            self.voronoi_lines.remove()
            self.voronoi_lines = None

        if self.voronoi_regions:
            for voronoi_region in self.voronoi_regions:
                voronoi_region.remove()
            self.voronoi_regions = []


    def update(self, visual_players):
        self.remove()
        self.draw(visual_players)


    def voronoi_finite_polygons_2d(self, vor, radius=None):
        """
        Reconstruct infinite voronoi regions in a 2D diagram to finite
        regions.
        Parameters
        ----------
        vor : Voronoi
            Input diagram
        radius : float, optional
            Distance to 'points at infinity'.
        Returns
        -------
        regions : list of tuples
            Indices of vertices in each revised Voronoi regions.
        vertices : list of tuples
            Coordinates for revised Voronoi vertices. Same as coordinates
            of input vertices, with 'points at infinity' appended to the
            end.
        """

        if vor.points.shape[1] != 2:
            raise ValueError("Requires 2D input")

        new_regions = []
        new_vertices = vor.vertices.tolist()

        center = vor.points.mean(axis=0)
        if radius is None:
            radius = vor.points.ptp().max()*2

        # Construct a map containing all ridges for a given point
        all_ridges = {}
        for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
            all_ridges.setdefault(p1, []).append((p2, v1, v2))
            all_ridges.setdefault(p2, []).append((p1, v1, v2))

        # Reconstruct infinite regions
        for p1, region in enumerate(vor.point_region):
            vertices = vor.regions[region]

            if all(v >= 0 for v in vertices):
                # finite region
                new_regions.append(vertices)
                continue

            # reconstruct a non-finite region
            ridges = all_ridges[p1]
            new_region = [v for v in vertices if v >= 0]

            for p2, v1, v2 in ridges:
                if v2 < 0:
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge

                t = vor.points[p2] - vor.points[p1] # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counterclockwise
            vs = np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
            new_region = np.array(new_region)[np.argsort(angles)]

            # finish
            new_regions.append(new_region.tolist())

        return new_regions, np.asarray(new_vertices)
