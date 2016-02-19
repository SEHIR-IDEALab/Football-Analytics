import math
import matplotlib.pyplot as plt
from src.sentio.Parameters import SOURCE_ANGLE,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT


__author__ = 'emrullah'


class RiskRange():

    def __init__(self, ax):
        self.ax = ax

        self.total_pass_count = 3
        self.temp_pass_count = 0

        self.risk_ranges = []


    @staticmethod
    def get_Point_Area(new_coords, p1, p2, p3):
        areas=[]
        xT1,yT1,xT2,yT2 = new_coords[1] # coordinates on the target circle
        xS1,yS1,xS2,yS2 = new_coords[0] ## coordinates on the source circle
        (x1,y1),(x2,y2),(x,y) = p1, p2, p3
        pointsList = [[(x,y,xS1,yS1,x1,y1),(x,y,xT1,yT1,x2,y2),(x,y,xS1,yS1,xT1,yT1),(x,y,x1,y1,x2,y2)],
                     [(x,y,xS2,yS2,x1,y1),(x,y,xT2,yT2,x2,y2),(x,y,xS2,yS2,xT2,yT2),(x,y,x1,y1,x2,y2)]]

        for index in [0,1]:
            sum_Area = 0
            for point in pointsList[index]:
                x1,y1,x2,y2,x3,y3=point
                sum_Area+=math.fabs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1-y2))/2.0)
            areas.append(sum_Area)
        return areas


    @staticmethod
    def isInRange(p1, p3, p2):

        new_coords,radius_source,radius_target = RiskRange.get_Coordinates_on_Circle(p1,p2)

        xT1,yT1,xT2,yT2=new_coords[1] # coordinates on the target circle
        xS1,yS1,xS2,yS2=new_coords[0] ## coordinates on the source circle

        (x_Sou_orijine,y_Sou_orijine),(x_Tar_orijine,y_Tar_orijine),(x,y)=p1,p2,p3

        radiusTarToP3 = math.sqrt(math.pow(x_Tar_orijine - x, 2) + math.pow(y_Tar_orijine - y, 2))
        radiusSouToP3 = math.sqrt(math.pow(x_Sou_orijine - x, 2) + math.pow(y_Sou_orijine - y, 2))

        cal_area1,cal_area2 = RiskRange.get_Point_Area(new_coords,p1,p2,p3)
        Area1=math.fabs((xS1*(yT1 - y_Sou_orijine) + xT1*(y_Sou_orijine - yS1) + x_Sou_orijine*(yS1-yT1))/2.0) +\
              math.fabs((x_Tar_orijine*(yT1 - y_Sou_orijine) + xT1*(y_Sou_orijine - y_Tar_orijine) + x_Sou_orijine*(y_Tar_orijine-yT1))/2.0)

        Area2=math.fabs((xS2*(yT2 - y_Sou_orijine) + xT2*(y_Sou_orijine - yS2) + x_Sou_orijine*(yS2-yT2))/2.0) +\
              math.fabs((x_Tar_orijine*(yT2 - y_Sou_orijine) + xT2*(y_Sou_orijine - y_Tar_orijine) + x_Sou_orijine*(y_Tar_orijine-yT2))/2.0)
        if (int(cal_area1) in [int(Area1) ,int(Area2)]) or (int(cal_area2) in [int(Area1) ,int(Area2)]) or (radiusSouToP3 <= radius_source) or (radiusTarToP3 <= radius_target):
            return True
        return False


    @staticmethod
    def get_Coordinates_on_Circle(p1,p2):
        index=None
        (x1,y1),(x2,y2)=p1,p2

        distance=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))
        # estimated_time = distance/22.35 # average speed of ball
        # radius_target = estimated_time*2.86*2 # average speed of player

        # radius_target = estimated_time*8.36

        radius_target = (math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/PASS_TARGET_RADIUS_COEFFICIENT

        radius_source = min(PASS_SOURCE_RADIUS,radius_target/2.0)
        # radius_source = PASS_SOURCE_RADIUS
        # radius_source2 = radius_target/2.0
        radius_source2=PASS_SOURCE_RADIUS

        # distance=radius_target*PASS_TARGET_RADIUS_COEFFICIENT
        #get the point on small circle
        dx = (0.01 if (x2-x1) == 0 else (x2-x1))
        slope=math.degrees(math.atan((y2-y1)/dx))


        tmp_angle, s_angle1, s_angle2, t_angle1, t_angle2 = 0,0,0,0,0
        if x2 > x1:
            if (y1 == y2) or (y2 > y1) or (y1 > y2):
                s_angle1=math.radians(180.0 - SOURCE_ANGLE + slope)
                s_angle2=math.radians(180.0 + SOURCE_ANGLE + slope)
                index=0
        elif x1 > x2:
            if (y1 == y2) or (y1 > y2) or (y2 >y1):
                s_angle1=math.radians(SOURCE_ANGLE +slope)
                s_angle2=math.radians(-SOURCE_ANGLE +slope)
                index=1
        elif x1 == x2:
            if y1 > y2: tmp_angle= 90.0
            elif y1 < y2: tmp_angle= -90.0
            s_angle1=math.radians(tmp_angle - SOURCE_ANGLE)
            s_angle2= math.radians(tmp_angle+ SOURCE_ANGLE)

        x1_on_s,x2_on_s = x1+(radius_source2)*round(math.cos(s_angle1),2),x1+(radius_source2)*round(math.cos(s_angle2),2)
        y1_on_s,y2_on_s = y1+(radius_source2)*round(math.sin(s_angle1),2),y1+(radius_source2)*round(math.sin(s_angle2),2)

        #angle on target circle
        ll=(math.sqrt(math.pow(x1_on_s - x2, 2) + math.pow(y1_on_s - y2, 2))) ## distance between p2 and new point on th small circle
        length=(math.sqrt(math.pow(ll, 2) - math.pow(radius_target, 2)))
        try:
            alfa1=math.degrees(math.atan(length/radius_target))
        except:
            alfa1=math.degrees(math.atan(length/1))
        try:
            alfa2=math.degrees(math.acos(((math.pow(radius_source2,2)) - math.pow(ll,2) - math.pow(distance,2))/(-2.0*ll*distance)))
        except:
            alfa2=math.degrees(math.acos(((math.pow(radius_source2,2)) - math.pow(ll,2) - math.pow(distance,2))/1))
        total_angle=alfa1+alfa2

        poss_angle=[(math.radians(180.0 - total_angle + slope),math.radians(180.0 + total_angle + slope)),
                    (math.radians(total_angle + slope),math.radians(-total_angle + slope))]
        if index != None: t_angle1,t_angle2=poss_angle[index]
        else: pass

        if x1 ==x2:
            if y1 > y2: tmp_angle=90.0
            elif y1 < y2: tmp_angle=270.0
            t_angle1=math.radians(tmp_angle + total_angle)
            t_angle2= math.radians(tmp_angle - total_angle)

        x1_on_t,x2_on_t = x2+(radius_target)*round(math.cos(t_angle1),2),x2+(radius_target)*round(math.cos(t_angle2),2)
        y1_on_t,y2_on_t = y2+(radius_target)*round(math.sin(t_angle1),2),y2+(radius_target)*round(math.sin(t_angle2),2)

        return [[x1_on_s,y1_on_s,x2_on_s,y2_on_s],[x1_on_t,y1_on_t,x2_on_t,y2_on_t]],radius_source,radius_target


    def drawRangeFor(self, pass_event):
        p1, p2 = pass_event.pass_source, pass_event.pass_target
        coord,sr,tr=RiskRange.get_Coordinates_on_Circle(p1.get_position(),p2.get_position())

        x1,x2=[coord[0][0],coord[1][0]],[coord[0][2],coord[1][2]]
        y1,y2=[coord[0][1],coord[1][1]],[coord[0][3],coord[1][3]]

        #lines
        self.line1 = self.ax.plot(x1,y1,c='r')
        self.line2 = self.ax.plot(x2,y2,c='r')

        (sx,sy)=p1.get_position()
        self.line3 = self.ax.plot([sx,x1[0]],[sy,y1[0]],c="r")
        self.line4 = self.ax.plot([sx,x2[0]],[sy,y2[0]],c="r")

        #circles
        self.circle1=plt.Circle(p1.get_position(),radius=sr,color='r',fill=False)
        self.circle2=plt.Circle(p2.get_position(),radius=tr,color='r',fill=False)
        self.ax.add_patch(self.circle1)
        self.ax.add_patch(self.circle2)

        self.risk_ranges.append([self.line1, self.line2, self.line3, self.line4, self.circle1, self.circle2])

        self.temp_pass_count += 1

        if self.temp_pass_count > self.total_pass_count:
            self.removeFILO()


    def removeFILO(self):
        for item in self.risk_ranges[0]:
            try: item.pop(0).remove()
            except: item.remove()
        del self.risk_ranges[0]


    def removeAll(self):
        if len(self.risk_ranges) != 0:
            for i in range(len(self.risk_ranges)):
                self.removeFILO()
