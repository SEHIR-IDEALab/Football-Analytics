__author__ = 'aliuzun'

import os
import csv
import numpy
from sklearn import svm
import matplotlib.pyplot as plt
from src.sentio.Parameters import DATA_BASE_DIR
from src.sentio.file_io.reader.XMLreader import XMLreader


class HeatMapForPass():
    def __init__(self):
        pass

    def getPasses(self,PassStartingPoint):
        reader = XMLreader(os.path.join(DATA_BASE_DIR, 'output/sentio_data.xml'))
        game_instances, slider_mapping = reader.parse()

        # container = list()
        # container.extend(["Pass Starting Point(X)","Pass Starting Point(Y)","Pass Ending Point(X)","Pass Ending Point(Y)","is_significant"])
        # out = csv.writer(open("pass_table.csv","a"), delimiter='\t', quoting=csv.QUOTE_NONE)
        # out.writerow(container)
        # del container[:]

        points,statuses=[],[]
        for game_instance in game_instances.values():
            if game_instance.event and game_instance.event.isPassEvent():
                pass_event = game_instance.event.pass_event
                x1s,y1s = pass_event.pass_source.get_position()
                x2s,y2s = pass_event.pass_target.get_position()
                status = pass_event.isSuccessful()
                # print pass_source.get_position(), pass_target.get_position(),
                points.append([x1s,y1s,x2s,y2s])

                if status == True:statuses.append("T")
                else: statuses.append("F")


        # print points
        # print statuses

        s_x,s_y=PassStartingPoint

        clf=svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
            gamma=0.005, kernel='rbf', max_iter=-1, probability=True, random_state=None,
            shrinking=True, tol=0.001, verbose=False)

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

        scat_xf,scat_yf,scat_xt,scat_yt=[],[],[],[]

        for index,point in enumerate(points):
            x1,y1,x2,y2=point
            con1=(float(x1)>s_x-10.0 and float(x1) < s_x+10.0) and (float(y1)>s_y-10.0 and float(y1)<s_y+10.0)
            if con1:
                if statuses[index]==0:
                    scat_xf.append(x2)
                    scat_yf.append(y2)
                else:
                    scat_xt.append(x2)
                    scat_yt.append(y2)
        plt.matplotlib.pyplot.scatter(s_x,s_y,c='green')
        plt.matplotlib.pyplot.scatter(scat_xf,scat_yf,c='blue')
        plt.matplotlib.pyplot.scatter(scat_xt,scat_yt,c='red')
        im2=plt.imread('/Users/aliuzun/PycharmProjects/futbol-data-analysis/src/sentio/Sklearn/srcc/background.png',0)

        hm=plt.imshow(im2, extent=[-2.0, 107.0, 72.0, 0.0], aspect="auto")

        hm = plt.imshow(data, interpolation='bilinear', extent=[0.0, 105.0, 70.0, 0.0], alpha=0.8)

        plt.show()

        # if status == True:
        #     container.extend([x1s,y1s,x2s,y2s,"T"])
        # else:
        #     container.extend([x1s,y1s,x2s,y2s,"F"])
        #
        # # container.extend(status)
        # out.writerow(container)
        # del container[:]


if __name__ == "__main__":
    w=HeatMapForPass()
    print w.getPasses((52,35))



