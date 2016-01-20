
__author__ = 'aliuzun'
import math
import numpy
from sklearn import svm
from src.sentio.Parameters import \
    FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X, \
    FOOTBALL_FIELD_MAX_Y, FOOTBALL_FIELD_MIN_Y



class PassSuccessPrediction:
    def __init__(self, canvas, ax, fig):
        self.canvas = canvas
        self.ax = ax
        self.fig = fig


    def setMatch(self, match):
        self.match = match


    def extractPassFeatures(self, team_choice):
        coordinates, statusus = [], []
        for game_instance in self.match.sentio.game_instances.getAllInstances():
            try:
                if game_instance.event and game_instance.event.isPassEvent():
                    pass_event = game_instance.event.pass_event
                    x1s,y1s = pass_event.pass_source.get_position()
                    x2s,y2s = pass_event.pass_target.get_position()

                    if pass_event.pass_source.getTeamSide() == team_choice:
                        coordinates.append([x1s,y1s,x2s,y2s])
                        statusus.append([("T" if pass_event.isSuccessful() else "F")])
            except AttributeError:
                print "event not found for game_instance"
        return coordinates, statusus


    def getPasses(self,PassStartingPoint,radius,team_choice,
                  C, kernel, degree, gamma, coef, probability, shrinking,
                  tol, verbose, max_iter):
        for i in [C, kernel, degree, gamma, coef, probability, shrinking, tol, verbose, max_iter]:
            print type(i)
        F_point,T_point,F_status,T_status=[],[],[],[]
        points,statuses=self.extractPassFeatures(team_choice)
        for index in range(len(statuses)):

            if statuses[index]=="T":
                T_point.append(points[index])
                T_status.append(statuses[index])
            else:
                T_point.append(points[index])
                T_status.append(statuses[index])
        points=T_point+ F_point
        statuses=T_status+ F_status

        s_x,s_y = PassStartingPoint

        clf=svm.SVC(C=C, coef0=coef, degree=degree,
            gamma=gamma, kernel=kernel, max_iter=max_iter, probability=probability,
            shrinking=shrinking, tol=tol, verbose=verbose)

        clf.fit(points,statuses)

        x_points, y_points = 210,140
        x_coord = numpy.linspace(0, 70, x_points)
        y_coord = numpy.linspace(0, 105, y_points)

        data=[]

        for y in y_coord:
            val=[]
            for x in x_coord:
                v=(numpy.array(clf.predict_proba([s_x,s_y,x,y])).tolist())
                val.append(v[0][1])
            data.append(val)
        # print min(data[0]),max(data[0])

        scat_xf,scat_yf,scat_xt,scat_yt=[],[],[],[]

        for index,point in enumerate(points):
            x1,y1,x2,y2 = float(point[0]),float(point[1]),float(point[2]),float(point[3])
            r = math.sqrt(math.pow((s_x-x1),2) + math.pow((s_y-y1),2))
            if r <= radius:
                if statuses[index] == "F":
                    scat_xf.append(x2)
                    scat_yf.append(y2)
                else:
                    scat_xt.append(x2)
                    scat_yt.append(y2)

        self.ax.scatter(scat_xf,scat_yf,s=30,c='blue',label = "Unsuccessful Pass")
        self.ax.scatter(scat_xt,scat_yt,s=30,c='red',label = "Successful Pass")

        q = self.ax.imshow(data,
                           interpolation='bilinear',
                           extent=[FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MAX_X,
                                   FOOTBALL_FIELD_MAX_Y, FOOTBALL_FIELD_MIN_Y],
                           alpha=0.8)

        # divider = make_axes_locatable(self.ax)
        # cax = divider.append_axes("right", size="0.5%", pad=0.02)

        # self.fig.colorbar(q)
        self.ax.legend(ncol=2,fontsize=8, bbox_to_anchor=(0., 1.0, 1., .102), loc=3, borderaxespad=0.5, mode="expand")



