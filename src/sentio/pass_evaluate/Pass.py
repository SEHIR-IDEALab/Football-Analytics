import math
from src.sentio import Parameters
from src.sentio.Parameters import *
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.object.PlayerBase import PlayerBase


__author__ = 'emrullah'


class Pass:

    def __init__(self):
        self.teams = None


    @staticmethod
    def display_effectiveness(coordinates, components, logger):
        overall_risk, gain, pass_advantage, goal_chance, effectiveness = components

        logger.WriteText("\n(%.1f, %.1f)\n" %coordinates)
        logger.WriteText("overall_risk = %.2f\n" %overall_risk)
        logger.WriteText("gain = %.2f\n" %gain)
        logger.WriteText("pass_advantage = %.2f\n" %pass_advantage)
        logger.WriteText("goal_chance = %.2f\n" %goal_chance)
        logger.WriteText("effectiveness = %.2f\n" %effectiveness)

        logger.SetInsertionPoint(0)


    def displayDefinedPass(self, defined_pass, pass_logger, draggable=False, visual=False):
        if draggable:
            p1 = defined_pass.textcoords.player; p2 = defined_pass.xycoords.player
            p1.set_position(defined_pass.textcoords.get_position()); p2.set_position(defined_pass.xycoords.get_position())
        else:
            if visual: p1 = defined_pass.pass_source.player; p2 = defined_pass.pass_target.player
            else: p1 = defined_pass.pass_source; p2 = defined_pass.pass_target

        self.teams = defined_pass.teams
        effectiveness = self.effectiveness(p1, p2)

        if Parameters.IS_DEBUG_MODE_ON:
            (x1,y1) = p1.get_position(); (x2,y2) = p2.get_position()
            pass_logger.WriteText("\n(%.1f, %.1f) --> (%.1f, %.1f)\n" %(x1,y1,x2,y2))
        else:
            pass_logger.WriteText("\n")
        pass_logger.WriteText("%s --> %s\n" %(p1.getJerseyNumber(), p2.getJerseyNumber()))
        pass_logger.WriteText("overall_risk = %.2f\n" %(self.overallRisk(p1, p2)))
        pass_logger.WriteText("gain = %.2f\n" %self.gain(p1, p2))
        pass_logger.WriteText("pass_advantage = %.2f (%s)\n" %self.passAdvantage(p2))
        pass_logger.WriteText("goal_chance = %.2f\n" %(self.goalChance(p2)))
        pass_logger.WriteText("effectiveness = %.2f\n" %effectiveness)

        pass_logger.SetInsertionPoint(0)

        return effectiveness


    def get_Point_Area(self,new_coords,p1,p2,p3):
        areas=[]
        xT1,yT1,xT2,yT2=new_coords[1] # coordinates on the target circle
        xS1,yS1,xS2,yS2=new_coords[0] ## coordinates on the source circle
        (x1,y1),(x2,y2),(x,y)=p1,p2,p3
        pointsList=[[(x,y,xS1,yS1,x1,y1),(x,y,xT1,yT1,x2,y2),(x,y,xS1,yS1,xT1,yT1),(x,y,x1,y1,x2,y2)],
                     [(x,y,xS2,yS2,x1,y1),(x,y,xT2,yT2,x2,y2),(x,y,xS2,yS2,xT2,yT2),(x,y,x1,y1,x2,y2)]]

        for index in [0,1]:
            sum_Area=0
            for point in pointsList[index]:
                x1,y1,x2,y2,x3,y3=point
                sum_Area+=math.fabs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1-y2))/2.0)
            areas.append(sum_Area)
        return areas


    def isInRange(self,p1, p3, p2):

        new_coords,radius_source,radius_target= RiskRange.get_Coordinates_on_Circle(p1,p2)

        xT1,yT1,xT2,yT2=new_coords[1] # coordinates on the target circle
        xS1,yS1,xS2,yS2=new_coords[0] ## coordinates on the source circle

        (x_Sou_orijine,y_Sou_orijine),(x_Tar_orijine,y_Tar_orijine),(x,y)=p1,p2,p3

        radiusTarToP3 = math.sqrt(math.pow(x_Tar_orijine - x, 2) + math.pow(y_Tar_orijine - y, 2))
        radiusSouToP3 = math.sqrt(math.pow(x_Sou_orijine - x, 2) + math.pow(y_Sou_orijine - y, 2))

        cal_area1,cal_area2=self.get_Point_Area(new_coords,p1,p2,p3)
        Area1=math.fabs((xS1*(yT1 - y_Sou_orijine) + xT1*(y_Sou_orijine - yS1) + x_Sou_orijine*(yS1-yT1))/2.0) +\
              math.fabs((x_Tar_orijine*(yT1 - y_Sou_orijine) + xT1*(y_Sou_orijine - y_Tar_orijine) + x_Sou_orijine*(y_Tar_orijine-yT1))/2.0)

        Area2=math.fabs((xS2*(yT2 - y_Sou_orijine) + xT2*(y_Sou_orijine - yS2) + x_Sou_orijine*(yS2-yT2))/2.0) +\
              math.fabs((x_Tar_orijine*(yT2 - y_Sou_orijine) + xT2*(y_Sou_orijine - y_Tar_orijine) + x_Sou_orijine*(y_Tar_orijine-yT2))/2.0)

        if (int(cal_area1) in [int(Area1) ,int(Area2)]) or (int(cal_area2) in [int(Area1) ,int(Area2)]) or (radiusSouToP3 <= radius_source) or (radiusTarToP3 <= radius_target):
            return True
        return False


    def risk(self, p1, p3, p2):
        risk = 0.0

        x1, y1 = p1.get_position()
        x2, y2 = p2.get_position()
        x3, y3 = p3.get_position()

        if not self.isInRange((x1,y1), (x3,y3), (x2,y2)):
            return risk

        slope = (y2 - y1) / (x2 - x1)
        a,b,c = slope,-1,( ( slope * (-x1) ) + y1 )
        cond1,cond2 = min(x1,x2) < x3 < max(x1,x2),min(y1,y2) < y3 < max(y1,y2)

        d1=math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
        hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))

        if x1==x2 :
            if cond2: d2=math.fabs((x3-x1))
            else:
                d2_a=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b])

        elif y1==y2:
            if cond1: d2=math.fabs((y3-y1))
            else:
                d2_a=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b])

        elif cond1 or cond2:
            d2_a = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            d2_b=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
            d2_c=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
            d2 = min([d2_a,d2_b,d2_c])

            if d2==d2_a: d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

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

                if d2 == d2_a: d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        if cond1 and cond2:
            d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        if d2==0: d2=0.01


        # cal1 = (math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2)))/22.35
        cal1=d1/22.35
        d_tmp_t = float("{0:.1f}".format(cal1))
        risk=(d1/d2)*COEFFICIENTS[d_tmp_t]
        # risk =d1/d2
        return risk


    def overallRisk(self, p1, p2, goal_keeper=True):
        overallRisk = 0.0

        if p1.isHomeTeamPlayer(): opponent_team = self.teams.away_team
        else: opponent_team = self.teams.home_team

        if goal_keeper:
            for p3 in opponent_team.getTeamPlayers():
                overallRisk += self.risk(p1, p3, p2)
        else:
            for p3 in opponent_team.getTeamPlayers():
                if not p3.isGoalKeeper():
                    overallRisk += self.risk(p1, p3, p2)

        return overallRisk


    def isBetween(self, p1, p3, p2):
        return p1.getX() <= p3.getX() <= p2.getX() or \
               p2.getX() <= p3.getX() <= p1.getX()


    def gain(self, p1, p2):
        if p2.isHomeTeamPlayer(): opponent_team = self.teams.away_team
        else: opponent_team = self.teams.home_team

        gain = 0
        for p3 in opponent_team.getTeamPlayers():
            if self.isBetween(p1, p3, p2):
                gain += 1
        if self.isOpponentGoalKeeperLocationLeft(p2):
            if p1.getX() < p2.getX(): return -gain
            else: return gain
        else:
            if p1.getX() < p2.getX(): return gain
            else: return -gain


    def passAdvantage(self, p1):
        if p1.isHomeTeamPlayer(): own_team = self.teams.home_team
        else: own_team = self.teams.away_team

        passAdvantages = {}
        for p2 in own_team.getTeamPlayers():
            if p1.getJerseyNumber() != p2.getJerseyNumber():
                pa = ((10 + self.gain(p1, p2)) / (10 + self.overallRisk(p1, p2)))
                passAdvantages[pa] = p2.getJerseyNumber()
        max_pass = max(passAdvantages.keys())
        return max_pass, passAdvantages[max_pass]


    def isOpponentGoalKeeperLocationLeft(self, p1):
        if p1.isHomeTeamPlayer():
            own_goal_keeper = self.teams.home_team.getGoalKeeper()
            opponent_goal_keeper = self.teams.away_team.getGoalKeeper()
        else:
            own_goal_keeper = self.teams.away_team.getGoalKeeper()
            opponent_goal_keeper = self.teams.home_team.getGoalKeeper()

        return own_goal_keeper.getX() > opponent_goal_keeper.getX()


    def goalChance(self, p1):
        if self.isOpponentGoalKeeperLocationLeft(p1): goal_keeper_x = GOALPOST_MIN_X
        else: goal_keeper_x = GOALPOST_MAX_X

        if p1.getY() < GOALPOST_MIN_Y: goal_keeper_y = GOALPOST_MIN_Y
        elif p1.getY() > GOALPOST_MAX_Y: goal_keeper_y = GOALPOST_MAX_Y
        else: goal_keeper_y = p1.getY()

        goal_keeper = PlayerBase()
        goal_keeper.set_position((goal_keeper_x, goal_keeper_y))
        goal_keeper.setJerseyNumber("goal_keeper")

        d1 = math.sqrt(math.pow(goal_keeper_x - p1.getX(), 2) + math.pow(goal_keeper_y - p1.getY(), 2))
        angle = math.atan2(math.fabs(p1.getY() - goal_keeper_y), math.fabs(p1.getX() - goal_keeper_x)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, goal_keeper, goal_keeper=False)
        q = (1 if q == 0 else q)

        d1 = (1 if d1 == 0 else d1)
        return (GOALPOST_LENGTH / d1) * (min(angle, (180 - angle)) / 90.) * (1. / (1 + q)) * GOAL_COEFFICIENT


    def isSuccessfulPass(self, p1, p2):
        return p1.getTypeName() == p2.getTypeName()


    def isInField(self, p1):
        return FOOTBALL_FIELD_MIN_X <= p1.getX() <= FOOTBALL_FIELD_MAX_X and \
               FOOTBALL_FIELD_MIN_Y <= p1.getY() <= FOOTBALL_FIELD_MAX_Y


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