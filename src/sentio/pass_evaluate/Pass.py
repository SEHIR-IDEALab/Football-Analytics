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
        # coeff=RiskRange.get_coefficient()
        risk = 0.0
        coefficient={1.5: 3.922348484848485, 1.0: 3.5962752525252526, 2.0: 1.389520202020202, 3.0: 1.3036616161616161, 4.0: 0.5738636363636364, 5.0: 0.23042929292929293, 2.5: 1.4318181818181819, 7.0: 0.017992424242424244, 8.0: 0.0012626262626262627, 10.0: 0.0006313131313131314, 9.5: 0.0003156565656565657, 7.8: 0.0022095959595959595, 5.7: 0.11837121212121213, 2.3: 1.345959595959596, 5.5: 0.13415404040404041, 0.0: 1.1136363636363635, 6.0: 0.08175505050505051, 0.2: 4.065340909090909, 5.2: 0.1764520202020202, 4.3: 0.40940656565656564, 3.8: 0.6843434343434344, 7.4: 0.011363636363636364, 0.4: 3.1928661616161618, 5.1: 0.20107323232323232, 6.4: 0.03787878787878788, 3.3: 1.125, 3.5: 0.9551767676767676, 0.6: 3.053030303030303, 9.9: 0.000946969696969697, 3.7: 0.7585227272727273, 1.1: 3.845959595959596, 0.8: 3.148674242424242, 2.6: 1.4611742424242424, 3.6: 0.8383838383838383, 2.2: 1.321969696969697, 6.5: 0.032512626262626264, 1.3: 4.184027777777778, 1.2: 4.078914141414141, 1.6: 3.3405934343434343, 6.2: 0.06407828282828283, 9.3: 0.0003156565656565657, 0.5: 3.1186868686868685, 7.3: 0.017361111111111112, 2.4: 1.396780303030303, 3.2: 1.1934974747474747, 5.9: 0.08933080808080808, 7.7: 0.005366161616161616, 6.8: 0.025883838383838384, 5.4: 0.14741161616161616, 6.3: 0.05113636363636364, 0.3: 3.4835858585858586, 2.7: 1.444760101010101, 8.1: 0.0025252525252525255, 7.1: 0.02241161616161616, 5.6: 0.10353535353535354, 9.6: 0.0006313131313131314, 8.3: 0.0006313131313131314, 1.7: 2.6208964646464645, 4.8: 0.28188131313131315, 4.5: 0.35542929292929293, 6.1: 0.07796717171717171, 6.7: 0.02556818181818182, 6.9: 0.023042929292929292, 1.9: 1.5931186868686869, 3.1: 1.2414772727272727, 2.1: 1.3011363636363635, 4.4: 0.3854166666666667, 0.9: 3.483270202020202, 4.1: 0.5164141414141414, 0.1: 4.699179292929293, 1.4: 4.3188131313131315, 1.8: 1.97979797979798, 8.7: 0.0003156565656565657, 9.7: 0.0003156565656565657, 5.3: 0.1856060606060606, 2.8: 1.3652146464646464, 6.6: 0.028724747474747476, 3.4: 1.040719696969697, 3.9: 0.6256313131313131, 0.7: 3.180871212121212, 7.6: 0.008207070707070708, 4.6: 0.3229166666666667, 4.2: 0.4599116161616162, 4.7: 0.28440656565656564, 4.9: 0.2547348484848485, 8.2: 0.0022095959595959595, 8.8: 0.0003156565656565657, 8.4: 0.0006313131313131314, 7.2: 0.02462121212121212, 8.5: 0.0003156565656565657, 7.9: 0.003472222222222222, 2.9: 1.283459595959596, 7.5: 0.01167929292929293, 5.8: 0.10953282828282829}

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
        risk=(d1/d2)*coefficient[d_tmp_t]
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