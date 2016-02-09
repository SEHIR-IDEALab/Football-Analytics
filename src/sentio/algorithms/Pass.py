import math

from src.sentio import Parameters
from src.sentio.Parameters import *
from src.sentio.analytics.Analyze import Analyze
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.analytics.prediction.OptimalShootingPointPrediction import OptimalShootingPointPrediction


__author__ = 'emrullah'


class Pass:

    def __init__(self, teams=None):
        self.teams = teams


    def risk(self, p1, p3, p2):
        risk = 0.0

        x1, y1 = p1.get_position()
        x2, y2 = p2.get_position()
        x3, y3 = p3.get_position()

        if not RiskRange.isInRange((x1,y1), (x3,y3), (x2,y2)):
            return risk
        try: slope = (y2 - y1) / (x2 - x1) # zero devision error gives
        except (ZeroDivisionError):  slope=100

        a,b,c = slope,-1,( ( slope * (-x1) ) + y1 )


        cond1,cond2 = min(x1,x2) <= x3 <= max(x1,x2) , min(y1,y2) <= y3 <= max(y1,y2)

        d1=math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
        hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
        try:
            sp1,sp2=((y3 - y1) / (x3 - x1)),((y3 - y2) / (x3 - x2))
            tmp_slope = min(sp1,sp2)
        except: (ZeroDivisionError)

        if x3==x1 or x3==x2:
            d1,d2= math.fabs((y3-y1)),0.1
            V2 = d2/(d1/average_speed_ball)
            d_tmp_t = float("{0:.1f}".format(V2))
            if d_tmp_t < 3.0:    tt=1.0
            elif d_tmp_t > 10.0: tt=0.0
            else:                tt=COEFFICIENTS[d_tmp_t]  # d1 is distance to point that p3 cross the line1to2 right angle

            risk=(d1/d2)*tt
            return risk

        if cond1 and cond2:
            d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        elif cond2 and not cond1:
            (math.pow(a, 2) + math.pow(b, 2))
            if tmp_slope < -1:
                d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            else:
                d2_a = math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b = math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2 = min([d2_a,d2_b])

        elif cond1 and not cond2:
            if tmp_slope > -1: d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            else:
                d2_a = math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b = math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2 = min([d2_a,d2_b])

        else:
            if (slope>0 and sp1 >0) or (slope<0 and sp1<0):
                d2_a=math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_b=math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2=min([d2_a,d2_b])
            else:
                d2_a = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
                d2_b = math.sqrt(math.pow((x3-x1),2) + math.pow((y3-y1),2))
                d2_c = math.sqrt(math.pow((x3-x2),2) + math.pow((y3-y2),2))
                d2 = min([d2_a,d2_b,d2_c])

                if d2 == d2_a:
                    d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))


        d2 = (0.1 if d2 <= 0.1 else d2)

        t1 = d1/average_speed_ball
        try:
            # V2 = d2/t1
            V2=d2/t1
        except ZeroDivisionError: V2=10.0

        d_tmp_t = float("{0:.1f}".format(V2))
        if d_tmp_t < 3.0:
            tt=1.0
        elif d_tmp_t > 10.0:
            tt=0.0
        else:
            tt=COEFFICIENTS[d_tmp_t]  # d1 is distance to point that p3 cross the line1to2 right angle


        risk=(d1/d2)*tt

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


    def gain(self, p1, p2):
        if p2.isHomeTeamPlayer(): opponent_team = self.teams.away_team
        else: opponent_team = self.teams.home_team

        gain = 0
        for p3 in opponent_team.getTeamPlayers():
            if Analyze.isBetween(p1, p3, p2):
                gain += 1
        if Analyze.isOpponentGoalKeeperLocationLeft(p2, self.teams):
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


    def goalChance(self, p1):
        goal_keeper = Analyze.detectGoalKeeperWithPositions(p1, self.teams)
        goal_keeper_x, goal_keeper_y = goal_keeper.get_position()

        d1 = math.sqrt(math.pow(goal_keeper_x - p1.getX(), 2) + math.pow(goal_keeper_y - p1.getY(), 2))
        angle = math.atan2(math.fabs(p1.getY() - goal_keeper_y), math.fabs(p1.getX() - goal_keeper_x)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, goal_keeper, goal_keeper=False)

        # q = (1 if q == 0 else q)
        d1 = (0.1 if d1 == 0 else d1)

        return (GOALPOST_LENGTH / d1) * (min(angle, (180 - angle)) / 90.) * (1. / (1 + q))


    def goalChanceWithOSPP(self, p1): ### goal chance with Optimal Shooting Point Prediction
        optimalShootingPointPrediction = OptimalShootingPointPrediction(self.teams)
        return optimalShootingPointPrediction.predict(p1, self.goalChance)[0]


    # def effectiveness(self, p1, p2):
    #     w1, w2, w3, w4 = 1, 1, 1, 1
    #     effectiveness = w1 * self.gain(p1, p2) + w3 * self.passAdvantage(p2)[0] + w4 * self.goalChanceWithOSPP(p2)
    #     if not self.isSuccessfulPass(p1, p2):
    #         if effectiveness < 0:
    #             return effectiveness*10
    #         return -effectiveness*10
    #     return effectiveness


    def effectiveness_withComponents(self, p1, p2, listeners=(True,True,True,True)):
        # print Parameters.W1, Parameters.W2, Parameters.W3, Parameters.W4
        gain = (Parameters.W1/max_gain) * self.gain(p1, p2)
        passAdvantage, pa_player = self.passAdvantage(p2)
        passAdvantage = (Parameters.W3/max_passAdvantage)*passAdvantage
        goalChance = (Parameters.W4/max_goalChance) * self.goalChance(p2) ########### goalChanceWithOSPP
        overallRisk = self.overallRisk(p1, p2)

        (gain_listener, effectiveness_listener, pass_advantage_listener, goal_chance_listener) = listeners

        effectiveness = 0
        comp_list = [overallRisk]
        if gain_listener:
            effectiveness += gain
            comp_list.append(gain)
        else:
            comp_list.append(None)
        if effectiveness_listener:
            pass
        if pass_advantage_listener:
            effectiveness += passAdvantage
            comp_list.append(passAdvantage)
            comp_list.append(pa_player)
        else:
            comp_list.append(None)
            comp_list.append(None)
        if goal_chance_listener:
            effectiveness += goalChance
            comp_list.append(goalChance)
        else:
            comp_list.append(None)

        if not Analyze.isSuccessfulPass(p1, p2):
            if effectiveness < 0:
                effectiveness *= 10
            else:
                effectiveness = -effectiveness * 10

        comp_list.append(effectiveness)
        return comp_list


    def __str__(self):
        pass


