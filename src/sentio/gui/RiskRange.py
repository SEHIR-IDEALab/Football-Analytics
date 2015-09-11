import math
import matplotlib.pyplot as plt
from src.sentio.Parameters import PASS_SOURCE_RADIUS, PASS_TARGET_RADIUS_COEFFICIENT,SOURCE_ANGLE


__author__ = 'doktoray'


class RiskRange():

    def __init__(self, ax):
        self.ax = ax

        self.total_pass_count = 3
        self.temp_pass_count = 0

        self.risk_range_info = []


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
        try:
            slope=math.degrees(math.atan((y2-y1)/(x2-x1)))
        except ZeroDivisionError:
            slope=90

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

        self.risk_range_info.append([self.line1, self.line2, self.line3, self.line4, self.circle1, self.circle2])

        self.temp_pass_count += 1

        if self.temp_pass_count > self.total_pass_count:
            self.remove()


    def remove(self):
        for item in self.risk_range_info[0]:
            try: item.pop(0).remove()
            except: item.remove()
        del self.risk_range_info[0]

