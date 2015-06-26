__author__ = 'aliuzun'

import math
import matplotlib.pyplot as plot
from matplotlib import pyplot

class Draw():

    def __init__(self):
        self.p_start=(0,0)
        self.p_end=(12.0,4.0)

    def get_shape(self,p1,p2,t):
        points=[]
        (x1,y1),(x2,y2)=p1,p2
        V=(math.sqrt((math.pow((x2-x1),2)) + (math.pow((y2-y1),2))))/1.0
        # print V
        if V < 2:
            t_r=1
        elif 2 <= V < 3.5:
            t_r=1.7
        elif 3.5 <= V < 5:
            t_r=2
        elif V >=5:
            t_r=3

        for i in range(0,181,1):
            # if i <=180:
            t_tmp=(t_r/180.0)*(i)
            distance=V*(t-t_tmp)
            points.append(self.get_poss_coord(p1,p2,distance,i))
            # print get_poss_coord(p1,distance,i),i
            t_tmp=(t_r/180.0)*(i)
            # print t_tmp,"---"
            distance=V*(t-t_tmp)

            points.append(self.get_poss_coord(p1,p2,distance,-i+360))


        return points


    def get_poss_coord(self,p,p2,x,angle):
        xo,yo=p
        xe,ye=p2
        angle+=math.degrees(math.atan((ye-yo)/(xe-xo)))
        x,y=x*math.cos(math.radians(angle)),x*math.sin(math.radians(angle))
        x=x+xo
        y=y+yo
        return (x,y)



    def draw_shape(self,t):
        all_data = self.get_shape(self.p_start,self.p_end,t)
        x = []
        y = []


        for i in xrange(len(all_data)):
            x.append(all_data[i][0])
            y.append(all_data[i][1])

        xs,ys=self.p_start
        xe,ye=self.p_end
        plot.scatter([xs,xe],[ys,ye],c='r',s=30)
        plot.plot([xs,xe],[ys,ye],marker='o',linestyle='->',color='r')
        plot.scatter(x,y)

        pyplot.show()

if __name__ == "__main__":
    w=Draw()
    print w.draw_shape(5)