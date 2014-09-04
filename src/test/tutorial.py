__author__ = 'aliuzun'
import math
import numpy
from matplotlib.patches import Circle,Rectangle  # $matplotlib/patches.py
import matplotlib.pyplot as plt
import matplotlib.lines as lines

p1=(5.97,33.11)
p2=(33.73,36.42)

x1,y1=p1
x2,y2=p2

r2=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/2.0
r1=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/4.0

def getAngle(p1,p2):
    angle1,angle2=None,None
    (x1,y1),(x2,y2)=p1,p2
    distance=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))
    #r2=distance/2.0
    #r1=distance/4.0
    length=(math.sqrt(math.pow(distance, 2) - math.pow((r2-r1), 2)))
    t2=math.fabs(r2-r1)/length
    tmpAngle2=math.degrees(math.atan(t2))
    if (x1==x2 and y1==y2):
        angle1,angle2=0,0

    if x1==x2:
        angle1=90
        if (y2>y1) :
            angle2=tmpAngle2
        elif (y1>y2):
            angle2=-tmpAngle2
    else:
        t1=(y2-y1)/(x2-x1)
        angle1=math.degrees(math.atan(t1))

    if (y1==y2):
        angle1=0
        if (x2>x1) :
            angle2=tmpAngle2
        elif (x1>x2) :
            angle2=-tmpAngle2

    if x2 > x1:
        if (y1>y2) or (y2>y1):
            angle2=tmpAngle2
    elif x1>x2:
        if (y2>y1) or (y1>y2):
            angle2=-tmpAngle2 #--
    return angle1,angle2


def Ftry(p1,p2):
    new_coord=[]
    #x1,y1=p1
    #x2,y2=p2
    add_angle1,add_angle2=getAngle(p1,p2)
    #r2=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/2.0
    #r1=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/4.0

    ang1,ang2=90  + add_angle1 + add_angle2 , 270 +add_angle1 - add_angle2
    rad1,rad2=math.radians(ang1),math.radians(ang2)

    #way1
    for point,radius in [(p1,r1),(p2,r2)]:
        x,y=point
        x1,x2=x+radius*round(math.cos(rad1),2),x+radius*round(math.cos(rad2),2)
        y1,y2=y+radius*round(math.sin(rad1),2),y+radius*round(math.sin(rad2),2)
        new_coord.append([x1,y1,x2,y2])
        print (x1,y1),(x2,y2)
    return new_coord



def draw(p1,p2):
    coords=Ftry(p1,p2)
    xs1,ys1,xs2,ys2=coords[0]
    xt1,yt1,xt2,yt2=coords[1]

    line1=[(xs1,ys1),(xt1,yt1)]
    line2=[(xs2,ys2),(xt2,yt2)]

    (line1_xs, line1_ys) = zip(*line1)
    (line2_xs, line2_ys) = zip(*line2)

    e = Circle( p1, radius=r1,alpha=0.3,facecolor="blue" )
    e1 = Circle( p2, radius=r2,alpha=0.3,facecolor="blue" )
    ax = plt.gca()  # ax = subplot( 1,1,1 )
    ax.add_artist(e)
    ax.add_artist(e1)
    e.set_clip_box(ax.bbox)
    e1.set_clip_box(ax.bbox)

    im= plt.imread("background.png")
    ax.imshow(im,extent=[0,100,70,0])
    ax.set_xticks(numpy.arange(0,100+5, 5))
    ax.set_yticks(numpy.arange(0,70+5, 5))

    ax.add_line(lines.Line2D(line1_xs, line1_ys, linewidth=1, color='blue',alpha=0.3))
    ax.add_line(lines.Line2D(line2_xs, line2_ys, linewidth=1, color='blue',alpha=0.3))

    plt.show()



draw(p1,p2)

p3=(0,0)

def isInRange(p1, p3, p2):
        x_Sou_orijine,y_Sou_orijine=p1
        x_Tar_orijine,y_Tar_orijine=p2
        x,y=p3

        new_coords=Ftry(p1,p2)

        xT1,yT1,xT2,yT2=new_coords[1] # coordinates on the target circle
        xS1,yS1,xS2,yS2=new_coords[0] ## coordinates on the source circle



        radiusTarToP3 = math.sqrt(math.pow(x_Tar_orijine - x, 2) + math.pow(y_Tar_orijine - y, 2))
        radiusSouToP3 = math.sqrt(math.pow(x_Sou_orijine - x, 2) + math.pow(y_Sou_orijine - y, 2))

        Area_Trapezoid=(2.0*(r1+r2))*r2

        pointsList=[(x,y,xT1,yT1,xT2,yT2),(x,y,xT1,yT1,xS1,yS1),(x,y,xS1,yS1,xS2,yS2),(x,y,xS2,yS2,xT2,yT2)]
        sum_Area=0
        for point in pointsList:
            x1,y1,x2,y2,x3,y3=point
            sum_Area+=math.fabs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1-y2))/2.0)
        if (int(sum_Area)==int(Area_Trapezoid)) or (radiusSouToP3 <= r1) or (radiusTarToP3 <= r2):
            print  True
        print False



## old version of risk

 # def risk(self, p1, p3, p2):
 #        risk = 0.0
 #
 #        try: x1, y1 = p1.getPositionX(), p1.getPositionY()
 #        except AttributeError: x1, y1 = p1
 #
 #        try: x2, y2 = p2.getPositionX(), p2.getPositionY()
 #        except AttributeError: x2, y2 = p2
 #
 #        try: x3, y3 = p3.getPositionX(), p3.getPositionY()
 #        except AttributeError: x3, y3 = p3
 #        point=[[x1,y1],[x2,y2]]
 #        if not self.isInRange((x1,y1), (x3,y3), (x2,y2)): return risk
 #        cond1=x3< min(point[0][0]) and x3> max(point[1][0])
 #        cond2=y3< min(point[0][1]) and y3> max(point[1][1])
 #        if cond1:
 #            if x2 != x1:
 #                slope = (y2 - y1) / (x2 - x1)
 #                a = slope
 #                b = -1
 #                c = ( ( slope * (-x1) ) + y1 )
 #                d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
 #            else:
 #                d2 = math.fabs(x3 - x1)
 #            hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
 #            d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))
 #
 #            try: risk = d1 / d2
 #            except ZeroDivisionError: risk = d1
 #
 #
 #
 #        return risk
