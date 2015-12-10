import math
from matplotlib.patches import Polygon
from src.sentio.Parameters import FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X, \
                                  FOOTBALL_FIELD_MAX_Y, FOOTBALL_FIELD_MIN_Y

import numpy as np
from scipy import spatial



__author__ = 'emrullah'



class Voronoi:

    def __init__(self, ax=None):
        self.ax = ax

        self.voronoi_regions = []


    @staticmethod
    def getPositions(visual_players):
        q = []
        for visual_player in visual_players:
            x, y = visual_player.get_position()
            q.append(np.array([x,y]))
        return np.array(q)


    def computePolygons(self, players, draw=False):
        # compute Voronoi tesselation
        vor = spatial.Voronoi(Voronoi.getPositions(players))

        # plot
        regions, vertices = Voronoi.voronoi_finite_polygons_2d(vor)

        polygons = []
        for index, region in enumerate(regions):
            polygon = vertices[region]
            polygon = Voronoi.normalize(polygon)
            polygons.append(polygon)

            if draw:
                player = players[index]
                poly_patch = Polygon(polygon,
                                     alpha=0.4,
                                     color=player.getObjectColor())  # fc and ec
                self.ax.add_patch(poly_patch)
                self.voronoi_regions.append(poly_patch)
                # voronoi_region = self.ax.fill(*zip(*polygon), alpha=0.4, color=visual_player.getObjectColor())

        return polygons


    @staticmethod
    def isOutlier(point):
        x, y = point
        return not (FOOTBALL_FIELD_MIN_X <= x <= FOOTBALL_FIELD_MAX_X and
                FOOTBALL_FIELD_MIN_Y <= y <= FOOTBALL_FIELD_MAX_Y)


    @staticmethod
    def removeOutliers(points):
        for point in points[:]:  ## [:] is crucial for removing purposes
            if Voronoi.isOutlier(point):
                points.remove(point)
        return points


    @staticmethod
    def computeIntersectionsWithField(polygon):
        field_lines = [
            [(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MIN_Y),(FOOTBALL_FIELD_MIN_X,FOOTBALL_FIELD_MAX_Y)],
            [(FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MIN_Y),(FOOTBALL_FIELD_MAX_X,FOOTBALL_FIELD_MIN_Y)],
            [(FOOTBALL_FIELD_MAX_X, FOOTBALL_FIELD_MAX_Y),(FOOTBALL_FIELD_MAX_X,FOOTBALL_FIELD_MIN_Y)],
            [(FOOTBALL_FIELD_MAX_X, FOOTBALL_FIELD_MAX_Y),(FOOTBALL_FIELD_MIN_X,FOOTBALL_FIELD_MAX_Y)]
        ]

        from shapely import geometry
        shapely_poly = geometry.Polygon(polygon)

        intersection_lines = []
        for field_line in field_lines:
            shapely_line = geometry.LineString(field_line)
            intersection_line = shapely_poly.intersection(shapely_line)
            if intersection_line:
                intersection_line = list(intersection_line.coords)
                intersection_lines.extend(intersection_line)
        return intersection_lines


    @staticmethod
    def calculateArea(polygon):
        from shapely import geometry
        shapely_poly = geometry.Polygon(polygon)
        return shapely_poly.area


    def calculateTotalAreaOfField(self):
        return (FOOTBALL_FIELD_MAX_X - FOOTBALL_FIELD_MIN_X) * \
               (FOOTBALL_FIELD_MAX_Y - FOOTBALL_FIELD_MIN_Y)


    @staticmethod
    def orderByCentroid(points):
        # compute centroid
        cent=(sum([p[0] for p in points])/len(points),sum([p[1] for p in points])/len(points))
        # sort by polar angle
        points.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))
        return points


    @staticmethod
    def normalize(polygon):
        polygon = polygon.tolist()

        intersection_points = Voronoi.computeIntersectionsWithField(polygon)
        polygon = Voronoi.removeOutliers(polygon)
        polygon.extend(intersection_points)
        polygon = Voronoi.orderByCentroid(polygon)

        return np.array(polygon)


    def remove(self):
        if self.voronoi_regions:
            for voronoi_region in self.voronoi_regions:
                voronoi_region.remove()
            self.voronoi_regions = []


    def update(self, visual_idToPlayers, draw=True):
        self.remove()
        self.computePolygons(visual_idToPlayers.values(), draw)


    @staticmethod
    def voronoi_finite_polygons_2d(vor, radius=None):
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
