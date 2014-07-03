import math
from src.sentio.Player_base import Player_base
from src.sentio.Parameters import *

__author__ = 'emrullah'


class Pass:

    def __init__(self, coordinateDataOfObjects=None):
        self.allObjects = Player_base.convertTextsToPlayers(coordinateDataOfObjects)


    def displayDefinedPass(self, definedPass, passDisplayer):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords
        object_type1, object_id1, js1, (x1, y1) = p1.object_type, p1.object_id, p1.get_text(), p1.get_position()
        object_type2, object_id2, js2, (x2, y2) = p2.object_type, p2.object_id, p2.get_text(), p2.get_position()

        p1 = Player_base([object_type1, object_id1,js1, x1, y1])
        p2 = Player_base([object_type2, object_id2,js2, x2, y2])

        effectiveness = self.effectiveness(p1, p2)

        passDisplayer.insert("1.0", "goal_chance = %.2f\n" %self.goalChance(p2))
        passDisplayer.insert("1.0", "effectiveness = %.2f\n" %effectiveness)
        passDisplayer.insert("1.0", "pass_advantage = %.2f (%s)\n" %self.passAdvantage(p2))
        passDisplayer.insert("1.0", "gain = %.2f\n" %self.gain(p1, p2))
        passDisplayer.insert("1.0", "overall_risk(%s->%s) = %.2f\n" %(p1.getJerseyNumber(), p2.getJerseyNumber(),
                                                                      self.overallRisk(p1, p2)))
        passDisplayer.insert("1.0", "\n%s --> %s\n" %(p1.getJerseyNumber(), p2.getJerseyNumber()))

        return effectiveness


    def isInRange2(self, p1, p3, p2):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        additional_r = 1

        distance_1to2 = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        radius_x, radius_y = ((x1 + x2) / 2.), ((y1 + y2) / 2.)
        distance_radiusTo3 = math.sqrt(math.pow(radius_x - x3, 2) + math.pow(radius_y - y3, 2))
        radius = (distance_1to2 / 2.) + additional_r

        if distance_radiusTo3 <= radius:
            return True
        return False

    def getNewCoords(self,p1,p2):
        x1,y1=p1  # source of pass
        x2,y2=p2  # target of pass

        radius = (math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))/2.0

        if x2 !=x1 and y2 !=y1:
            m1=(y2-y1)/float(x2-x1)
            m2=-1/m1
            x_up,y_up=(x2+(radius)*(1/(math.pow(m2,2)+1)),y2+(radius)*(m2/(math.pow(m2,2)+1)))
            x_down,y_down=(x2-(radius)*(1/((math.pow(m2,2))+1)),y2-(radius)*(m2/((math.pow(m2,2))+1)))
        if x2==x1:
            x_up,y_up=x2+radius,y2
            x_down,y_down=x2-radius,y2
        if y2==y1:
            x_up,y_up=x2,y2+radius
            x_down,y_down=x2,y2-radius
        return (x_up,y_up,x_down,y_down)


    def getPoint(self,p1,p2,r=2):
        x1,y1=p1  # source of pass
        x2,y2=p2  # target of pass
        radius = (math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))/2.0
        distace=2.0*r
        Ux,Uy=(x2-x1)/(2*radius),(y2-y1)/(2*radius)
        x,y=x1-(distace*Ux),y1-(distace*Uy)
        return (x,y)



    def isInRange(self,p1, p3, p2):
        x_Sou_orijine,y_Sou_orijine=p1
        x_Tar_orijine,y_Tar_orijine=p2
        x,y=p3

        radiusT = (math.sqrt(math.pow(x_Tar_orijine - x_Sou_orijine, 2) + math.pow(y_Tar_orijine - y_Sou_orijine, 2)))/2.0
        radiusS=2
        xT1,yT1,xT2,yT2=self.getNewCoords(p1,p2) # coordinates on the target circle
        xS1,yS1,xS2,yS2=self.getNewCoords(self.getPoint(p1,p2,r=2),p1) ## coordinates on the source circle


        radiusTarToP3 = math.sqrt(math.pow(x_Tar_orijine - x, 2) + math.pow(y_Tar_orijine - y, 2))
        radiusSouToP3 = math.sqrt(math.pow(x_Sou_orijine - x, 2) + math.pow(y_Sou_orijine - y, 2))

        Area_Trapezoid=(2.0*(radiusS+radiusT))*radiusT

        pointsList=[(x,y,xT1,yT1,xT2,yT2),(x,y,xT1,yT1,xS1,yS1),(x,y,xS1,yS1,xS2,yS2),(x,y,xS2,yS2,xT2,yT2)]
        sum_Area=0
        for point in pointsList:
            x1,y1,x2,y2,x3,y3=point
            sum_Area+=math.fabs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1-y2))/2.0)
        if sum_Area==Area_Trapezoid or radiusSouToP3 <= radiusS or radiusTarToP3 <= radiusT:
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

        if x2 != x1:
            slope = (y2 - y1) / (x2 - x1)
            a = slope
            b = -1
            c = ( ( slope * (-x1) ) + y1 )
            d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
        else:
            d2 = math.fabs(x3 - x1)
        hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
        d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        try: risk = d1 / d2
        except ZeroDivisionError: risk = d1

        return risk


    def overallRisk(self, p1, p2, goalKeeper=True):
        overallRisk = 0.0

        team1 = p1.getTypeName()

        try: js2 = p2.getJerseyNumber()
        except AttributeError: js2 = None

        for p3 in self.allObjects:
            team3 = p3.getTypeName()

            if team3 not in [team1, "referee", "unknown"]:
                if js2 != None:
                    if js2 != p3.getJerseyNumber():
                        if goalKeeper:
                            overallRisk += self.risk(p1, p3, p2)
                        else:
                            if not p3.isGoalKeeper():
                                overallRisk += self.risk(p1, p3, p2)
                else:
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
        for p3 in self.allObjects:
            x3, y3 = p3.get_position()
            team3 = p3.getTypeName()
            if team3 not in [team2, "referee", "unknown"]:
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
        for p2 in self.allObjects:
            js2 = p2.getJerseyNumber()
            team2 = p2.getTypeName()

            if team2 == team1 and js2 != js1:
                pa = ((10 + self.gain(p1, p2)) / (10 + self.overallRisk(p1, p2)))
                passAdvantages[pa] = js2
        max_pass = max(passAdvantages.keys())
        return max_pass, passAdvantages[max_pass]


    def opponentGoalKeeperLocation_isLeft(self, p1):
        team1 = p1.getTypeName()

        goalKeeper_1, goalKeeper_2 = None, None
        for p2 in self.allObjects:
            x2, y2 = p2.getPositionX(), p2.getPositionY()
            team2 = p2.getTypeName()

            if p2.isGoalKeeper():
                if team2 == team1: goalKeeper_1 = x2
                else: goalKeeper_2 = x2

        if goalKeeper_2 < goalKeeper_1:
            return True
        return False


    def goalChance(self, p1):
        x1, y1 = p1.getPositionX(), p1.getPositionY()

        leftGoalKeeperX = 0.0
        rightGoalKeeperX = 105.0

        if self.opponentGoalKeeperLocation_isLeft(p1): goalKeeperX = leftGoalKeeperX
        else: goalKeeperX = rightGoalKeeperX

        if y1 < GOALPOST_MIN_Y: goalKeeperY = GOALPOST_MIN_Y
        elif y1 > GOALPOST_MAX_Y: goalKeeperY = GOALPOST_MAX_Y
        else: goalKeeperY = y1

        d1 = math.sqrt(math.pow(goalKeeperX - x1, 2) + math.pow(goalKeeperY - y1, 2))
        d2 = 8.5
        angle = math.atan2(math.fabs(y1 - goalKeeperY), math.fabs(x1 - goalKeeperX)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, [goalKeeperX, goalKeeperY], goalKeeper=False)
        q = (1 if q == 0 else q)
        goalCoefficient = 1000

        d1 = (1 if d1 == 0 else d1)
        return (d2 / d1) * (min(angle, (180 - angle)) / 90.) * (1. / (1 + q)) * goalCoefficient


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

        return (effectiveness, gain, passAdvantage, goalChance, overallRisk)


    def __str__(self):
        pass