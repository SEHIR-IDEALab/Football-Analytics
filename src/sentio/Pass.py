import math
from src.sentio.Player_base import Player_base
from src.sentio.Parameters import *
from matplotlib.patches import Circle,Rectangle
import matplotlib.pyplot as plt

__author__ = 'emrullah'


class Pass:

    def __init__(self, coordinateDataOfObjects=None):
        self.allObjects = Player_base.convertTextsToPlayers(coordinateDataOfObjects)
        self.radius_source=None #this the radius of sources in a defined pass
        self.radius_target=None #this the radius of target in a defined pass


    @staticmethod
    def display_effectiveness(coordinates, components, logger):
        overall_risk, gain, pass_advantage, goal_chance, effectiveness = components

        logger.WriteText("\n(%.2f, %.2f)\n" %coordinates)
        logger.WriteText("overall_risk = %.2f\n" %overall_risk)
        logger.WriteText("gain = %.2f\n" %gain)
        logger.WriteText("pass_advantage = %.2f\n" %pass_advantage)
        logger.WriteText("goal_chance = %.2f\n" %goal_chance)
        logger.WriteText("effectiveness = %.2f\n" %effectiveness)

        logger.SetInsertionPoint(0)


    def displayDefinedPass(self, definedPass, passDisplayer):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords
        object_type1, object_id1, js1, (x1, y1) = p1.object_type, p1.object_id, p1.get_text(), p1.get_position()
        object_type2, object_id2, js2, (x2, y2) = p2.object_type, p2.object_id, p2.get_text(), p2.get_position()

        p1 = Player_base([object_type1, object_id1,js1, x1, y1])
        p2 = Player_base([object_type2, object_id2,js2, x2, y2])

        effectiveness = self.effectiveness(p1, p2)

        passDisplayer.WriteText("\n%s --> %s\n" %(p1.getJerseyNumber(), p2.getJerseyNumber()))
        passDisplayer.WriteText("overall_risk = %.2f\n" %(self.overallRisk(p1, p2)))
        passDisplayer.WriteText("gain = %.2f\n" %self.gain(p1, p2))
        passDisplayer.WriteText("pass_advantage = %.2f (%s)\n" %self.passAdvantage(p2))
        passDisplayer.WriteText("goal_chance = %.2f\n" %(self.goalChance(p2)))
        passDisplayer.WriteText("effectiveness = %.2f\n" %effectiveness)

        passDisplayer.SetInsertionPoint(0)

        return effectiveness

    def getAngle(self,p1,p2):
        angle1,angle2=None,None
        (x1,y1),(x2,y2)=p1,p2
        self.radius_target=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/2.0
        self.radius_source=(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))/4.0
        distance=self.radius_target*2.0
        length=(math.sqrt(math.pow(distance, 2) - math.pow((self.radius_target - self.radius_source), 2)))
        #print length
        try:
            t2=math.fabs(self.radius_target-self.radius_source)/length
            tmpAngle2=math.degrees(math.atan(t2))
        except (ZeroDivisionError):
            pass

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


    def Get_New_Coords(self,p1,p2):
        new_coord=[]
        add_angle1,add_angle2=self.getAngle(p1,p2)
        ang1,ang2=90  + add_angle1 + add_angle2 , 270 +add_angle1 - add_angle2
        rad1,rad2=math.radians(ang1),math.radians(ang2)
        #way1
        for point,radius in [(p1,self.radius_source),(p2,self.radius_target)]:
            x,y=point
            x1,x2=x+radius*round(math.cos(rad1),2),x+radius*round(math.cos(rad2),2)
            y1,y2=y+radius*round(math.sin(rad1),2),y+radius*round(math.sin(rad2),2)
            new_coord.append([x1,y1,x2,y2])
            # print (x1,y1),(x2,y2)
        return new_coord


    def isInRange(self,p1, p3, p2):
        (x_Sou_orijine,y_Sou_orijine),(x_Tar_orijine,y_Tar_orijine),(x,y)=p1,p2,p3

        new_coords=self.Get_New_Coords(p1,p2)

        xT1,yT1,xT2,yT2=new_coords[1] # coordinates on the target circle
        xS1,yS1,xS2,yS2=new_coords[0] ## coordinates on the source circle


        radiusTarToP3 = math.sqrt(math.pow(x_Tar_orijine - x, 2) + math.pow(y_Tar_orijine - y, 2))
        radiusSouToP3 = math.sqrt(math.pow(x_Sou_orijine - x, 2) + math.pow(y_Sou_orijine - y, 2))

        up=math.sqrt(math.pow(xS1 - xS2, 2) + math.pow(yS1 - yS2, 2))
        down=math.sqrt(math.pow(xT1 - xT2, 2) + math.pow(yT1 - yT2, 2))
        tt=(down-up)/2.0
        hipo=math.sqrt(math.pow(xS1 - xT1, 2) + math.pow(yS1 - yT1, 2))
        hight=math.sqrt(math.pow(hipo, 2) - math.pow(tt, 2))

        Area_Trapezoid=((up+down))*hight/2.0

        pointsList=[(x,y,xT1,yT1,xT2,yT2),(x,y,xT1,yT1,xS1,yS1),(x,y,xS1,yS1,xS2,yS2),(x,y,xS2,yS2,xT2,yT2)]
        sum_Area=0
        for point in pointsList:
            x1,y1,x2,y2,x3,y3=point
            sum_Area+=math.fabs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1-y2))/2.0)
        if (int(sum_Area)==int(Area_Trapezoid)) or (radiusSouToP3 <= self.radius_source) or (radiusTarToP3 <= self.radius_target):
            return True
        return False


    def risk(self, p1, p3, p2):
        risk = 0.0

        try: x1, y1 = p1.getPositionX(), p1.getPositionY()
        except AttributeError: x1, y1 = p1

        try: x2, y2 = p2.getPositionX(), p2.getPositionY()
        except AttributeError: x2, y2 = p2

        try: x3, y3 = p3.getPositionX(), p3.getPositionY()
        except AttributeError: x3, y3 = p3

        if not self.isInRange((x1,y1), (x3,y3), (x2,y2)): return risk

        slope = (y2 - y1) / (x2 - x1)
        a = slope
        b = -1
        c = ( ( slope * (-x1) ) + y1 )
        cond1= min(x1,x3) < x3 < max(x1,x2)
        cond2= min(y1,y2) < y3 < max(y1,y2)
        d1=math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))

        hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))

        if x1==x2 :
            if cond2:
                d2=math.fabs((x3-x1))
            else:
                d2_a=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b])

        elif y1==y2:
            if cond1:
                d2=math.fabs((y3-y1))
            else:
                d2_a=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b])

        elif cond1:
            d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))

            #d2 = math.fabs(x3 - x1)
        elif cond2:
            d2_a = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            d2_b=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
            d2_c=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
            d2=min([d2_a,d2_b,d2_c])

            if d2 == d2_a:
                d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        else:
            tmpslope=(y3 - y1) / (x3 - x1)
            if (slope>0 and tmpslope >0) or (slope<0 and tmpslope<0):
                d2_a=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b])
            else:
                d2_a = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
                d2_b=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_c=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b,d2_c])

                if d2 == d2_a:
                    d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        #print d1,d2
        if d2==0:
            # print (x1,y1),(x2,y2),(x3,y3)
            d2=0.01
        risk=d1/d2

        # try: risk = d1 / d2
        # except ZeroDivisionError: risk = d1

        return risk

    # def risk(self, p1, p3, p2):
    #     risk = 0.0
    #
    #     try: x1, y1 = p1.getPositionX(), p1.getPositionY()
    #     except AttributeError: x1, y1 = p1
    #
    #     try: x2, y2 = p2.getPositionX(), p2.getPositionY()
    #     except AttributeError: x2, y2 = p2
    #
    #     try: x3, y3 = p3.getPositionX(), p3.getPositionY()
    #     except AttributeError: x3, y3 = p3
    #     if not self.isInRange((x1,y1), (x3,y3), (x2,y2)): return risk
    #
    #     if x2 != x1:
    #         slope = (y2 - y1) / (x2 - x1)
    #         a = slope
    #         b = -1
    #         c = ( ( slope * (-x1) ) + y1 )
    #         d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
    #     else:
    #         d2 = math.fabs(x3 - x1)
    #     hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
    #     d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))
    #
    #     try: risk = d1 / d2
    #     except ZeroDivisionError: risk = d1
    #
    #
    #     return risk



    def overallRisk(self, p1, p2, goalKeeper=True):
        overallRisk = 0.0

        team1 = p1.getTypeName()

        try: js2 = p2.getJerseyNumber()
        except AttributeError: js2 = None

        if team1 == "home": opponent_players = self.allObjects[1]
        else: opponent_players = self.allObjects[0]

        if js2 != None:
            for p3 in opponent_players.values():
                if js2 != p3.getJerseyNumber():
                    if goalKeeper:
                        overallRisk += self.risk(p1, p3, p2)
                    else:
                        if not p3.isGoalKeeper():
                            overallRisk += self.risk(p1, p3, p2)
        else:
            for p3 in opponent_players.values():
                if goalKeeper:
                    overallRisk += self.risk(p1, p3, p2)
                else:
                    if not p3.isGoalKeeper():
                        overallRisk += self.risk(p1, p3, p2)

        return overallRisk


    def gain(self, p1, p2):
        x1, y1 = p1.getPositionX(), p1.getPositionY()

        x2, y2 = p2.getPositionX(), p2.getPositionY()
        team2 = p2.getTypeName()

        gain = 0
        left = False
        if team2 == "home": opponent_team = self.allObjects[1]
        else: opponent_team = self.allObjects[0]
        for p3 in opponent_team.values():
            x3, y3 = p3.get_position()
            if x1 <= x3 <= x2 or x2 <= x3 <= x1:
                gain += 1
            if p3.isGoalKeeper():
                if x3 <= x1 and x3 <= x2:
                    left = True
        if left:
            if x1 < x2: return -gain
            else: return gain
        else:
            if x1 < x2: return gain
            else: return -gain


    def passAdvantage(self, p1):
        team1 = p1.getTypeName()
        js1 = p1.getJerseyNumber()

        passAdvantages = {}
        if team1 == "home": own_team = self.allObjects[0]
        else: own_team = self.allObjects[1]
        for js2 in own_team:
            if js1 != js2:
                p2 = own_team[js2]
                pa = ((10 + self.gain(p1, p2)) / (10 + self.overallRisk(p1, p2)))
                passAdvantages[pa] = js2
        max_pass = max(passAdvantages.keys())
        return max_pass, passAdvantages[max_pass]


    def opponentGoalKeeperLocation_isLeft(self, p1):
        team1 = p1.getTypeName()
        goal_keeper_own, goal_keeper_opposite = None, None

        teams = self.allObjects[0].values() + self.allObjects[1].values()
        for p2 in teams:
            if p2.isGoalKeeper():
                team2 = p2.getTypeName()
                x2 = p2.getPositionX()
                if team1 == team2: goal_keeper_own = x2
                else: goal_keeper_opposite = x2

        if goal_keeper_opposite < goal_keeper_own:
            return True
        return False


    def goalChance(self, p1):
        x1, y1 = p1.getPositionX(), p1.getPositionY()

        if self.opponentGoalKeeperLocation_isLeft(p1): goalKeeperX = FOOTBALL_FIELD_MIN_X
        else: goalKeeperX = FOOTBALL_FIELD_MAX_X

        if y1 < GOALPOST_MIN_Y: goalKeeperY = GOALPOST_MIN_Y
        elif y1 > GOALPOST_MAX_Y: goalKeeperY = GOALPOST_MAX_Y
        else: goalKeeperY = y1

        d1 = math.sqrt(math.pow(goalKeeperX - x1, 2) + math.pow(goalKeeperY - y1, 2))
        d2 = GOALPOST_LENGTH
        angle = math.atan2(math.fabs(y1 - goalKeeperY), math.fabs(x1 - goalKeeperX)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, [goalKeeperX, goalKeeperY], goalKeeper=False)
        q = (1 if q == 0 else q)

        d1 = (1 if d1 == 0 else d1)
        return (d2 / d1) * (min(angle, (180 - angle)) / 90.) * (1. / (1 + q)) * GOAL_COEFFICIENT


    def isSuccessfulPass(self, p1, p2):
        team1 = p1.getTypeName()
        team2 = p2.getTypeName()
        if team1 == team2:
            return True
        return False


    def isInField(self, p1):
        if FOOTBALL_FIELD_MIN_X <= p1.getPositionX() <= FOOTBALL_FIELD_MAX_X and \
                                FOOTBALL_FIELD_MIN_Y <= p1.getPositionY() <= FOOTBALL_FIELD_MAX_Y:
            return True
        return False


    def effectiveness(self, p1, p2):
        w1, w2, w3, w4 = 1, 1, 1, 1
        effectiveness = w1 * self.gain(p1, p2) + w3 * self.passAdvantage(p2)[0] + w4 * self.goalChance(p2)
        if not self.isSuccessfulPass(p1, p2):
            if effectiveness < 0:
                return effectiveness*10
            return -effectiveness*10
        return effectiveness


    def effectiveness_withComponents(self, p1, p2):
        w1, w2, w3, w4 = 1, 1, 1, 1
        gain = w1 * self.gain(p1, p2)
        passAdvantage = w3 * self.passAdvantage(p2)[0]
        goalChance = w4 * self.goalChance(p2)
        overallRisk = self.overallRisk(p1, p2)
        effectiveness = gain + passAdvantage + goalChance
        if not self.isSuccessfulPass(p1, p2):
            if effectiveness < 0:
                effectiveness *= 10
            else:
                effectiveness = -effectiveness * 10

        return (overallRisk, gain, passAdvantage, goalChance, effectiveness)


    def __str__(self):
        pass