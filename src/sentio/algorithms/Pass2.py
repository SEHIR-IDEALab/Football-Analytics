import math

from src.sentio.Parameters import *
from src.sentio.analytics.Analyze import Analyze
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.analytics.prediction.OptimalShootingPointPrediction import OptimalShootingPointPrediction


__author__ = 'emrullah'


class Pass:

    def __init__(self, teams=None):
        self.teams = teams
        self.pre_weight=None


    def risk(self, p1, p3, p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT):
        risk = 0.0

        x1, y1 = p1.get_position()
        x2, y2 = p2.get_position()
        x3, y3 = p3.get_position()

        if not RiskRange.isInRange((x1,y1), (x3,y3), (x2,y2),PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT):
            return risk
        dx = (0.01 if (x2-x1) == 0 else (x2-x1))
        slope = (y2 - y1) / dx # zero devision error gives

        a,b,c = slope,-1,( ( slope * (-x1) ) + y1 )


        cond1,cond2 = min(x1,x2) <= x3 <= max(x1,x2) , min(y1,y2) <= y3 <= max(y1,y2)

        d1=math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
        hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
        dx1 = (0.01 if (x3-x1) == 0 else (x3-x1))
        dx2 = (0.01 if (x3-x2) == 0 else (x3-x2))
        sp1,sp2=((y3 - y1) / dx1),((y3 - y2) / dx2)
        tmp_slope = min(sp1,sp2)

        if x3==x1 or x3==x2:
            d1,d2= math.fabs((y3-y1)),0.1
            if d1/average_speed_ball==0:   V2=10
            else:     V2 = d2/(d1/average_speed_ball)
            # V2 = d2/(d1/average_speed_ball)
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


    # def overallRisk(self, p1, p2,risk_ignore=False, goal_keeper=True):
    #     overallRisk = 0.0
    #     if risk_ignore==True: return overallRisk
    #
    #     else:
    #         if p1.isHomeTeamPlayer(): opponent_team = self.teams.away_team
    #         else: opponent_team = self.teams.home_team
    #
    #         if goal_keeper:
    #             for p3 in opponent_team.getTeamPlayers():
    #                 overallRisk += self.risk(p1, p3, p2)
    #         else:
    #             for p3 in opponent_team.getTeamPlayers():
    #                 if not p3.isGoalKeeper():
    #                     overallRisk += self.risk(p1, p3, p2)
    #
    #         return overallRisk

    def overallRisk(self, p1, p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT, risk_ignore,goal_keeper=True):
        overallRisk = 0.0

        if risk_ignore: return overallRisk

        try:
            if p1.isHomeTeamPlayer() == p2.isHomeTeamPlayer():
                if p1.isHomeTeamPlayer(): opponent_team = self.teams.away_team
                else: opponent_team = self.teams.home_team
            else:
                if p2.isHomeTeamPlayer(): opponent_team = self.teams.away_team
                else: opponent_team = self.teams.home_team


            if goal_keeper:
                for p3 in opponent_team.getTeamPlayers():
                    a=self.risk(p1, p3, p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT)
                    # print p3.getJerseyNumber(),a
                    #
                    if p3==p2:
                        overallRisk+=0

                    else:
                        # overallRisk += self.risk(p1, p3, p2,where)
                        overallRisk+=a
            else:
                for p3 in opponent_team.getTeamPlayers():
                    if not p3.isGoalKeeper():
                        overallRisk += self.risk(p1, p3, p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT)

            return overallRisk
        except AttributeError:
            return overallRisk


    # def gain(self, p1, p2,radius):
    #     if p2.isHomeTeamPlayer(): opponent_team = self.teams.away_team
    #     else: opponent_team = self.teams.home_team
    #
    #     gain = 0
    #     for p3 in opponent_team.getTeamPlayers():
    #         if Analyze.isBetween(p1, p3, p2):
    #             gain += 1
    #     if Analyze.isOpponentGoalKeeperLocationLeft(p2, self.teams):
    #         if p1.getX() < p2.getX(): return -gain
    #         else: return gain
    #     else:
    #         if p1.getX() < p2.getX(): return gain
    #         else: return -gain

    def getShootPoint(self,p1,G,shooting_radius):
        x1,y1=p1.getX(),p1.getY()
        x2,y2=G
        dx,dy=(x1-x2),(y1-y2)
        dx=(0.01 if dx==0 else dx)
        distance=math.sqrt(math.pow(dx,2)+math.pow(dy,2))

        # if distance < 2*shooting_radius:
        #     distance=shooting_radius[0]
        if distance > shooting_radius:
            distance-=shooting_radius

        alpha=math.degrees(math.atan(dy/dx))

        if y1 > y2: # above the line
            if x1>x2:
                xp,yp  = x1 - distance*round(math.cos(math.radians(alpha)),2),\
                               y1 - math.fabs(distance*round(math.sin(math.radians(alpha)),2))
            else:
                xp,yp  = x1 + distance*round(math.cos(math.radians(alpha)),2) ,\
                               y1 - math.fabs(distance*round(math.sin(math.radians(alpha)),2))
        else:
            if x1>x2:
                xp,yp  = x1 - distance*round(math.cos(math.radians(alpha)),2),\
                           y1 + math.fabs(distance*round(math.sin(math.radians(alpha)),2))
            else:
                xp,yp  = x1 + distance*round(math.cos(math.radians(alpha)),2) ,\
                               y1 + math.fabs(distance*round(math.sin(math.radians(alpha)),2))
        return (xp,yp)


    def get_gain(self,p,pG):
        gain=0
        dx,dy=(p.getX()-pG[0]),(p.getY()-pG[1])
        d1=math.sqrt(math.pow(dx,2)+math.pow(dy,2)) # distance of p to sh
        if p.isHomeTeamPlayer(): opponent_team = self.teams.away_team
        else: opponent_team = self.teams.home_team
        border=[p.getX(),pG[0]]
        border.sort()
        for p3 in opponent_team.getTeamPlayers():
            dx,dy=(p3.getX()-pG[0]),(p3.getY()-pG[1])
            d3=math.sqrt(math.pow(dx,2)+math.pow(dy,2)) # distance of p3 to sh
            if d3 <=d1 and not p3.isGoalKeeper():
                gain += 1
        return gain



    def gain(self,p1,p2,radius):
        target_loc={0:(0,35.0),1:(105.0,35.0)}
        if Analyze.isOpponentGoalKeeperLocationLeft(p1,self.teams):
            tp=target_loc[0]
        else:
            tp=target_loc[1]

        backPass=False
        dx1=p1.getX()-tp[0]
        dx2=p2.getX()-tp[0]
        if dx2 > dx1: backPass=True

        sx1,sy1=self.getShootPoint(p1,tp,radius)
        sx2,sy2=self.getShootPoint(p2,tp,radius)
        g1 = self.get_gain(p1,(sx1,sy1))
        g2 = self.get_gain(p2,(sx2,sy2))
        # print g1-g2
        if backPass:
            return -math.fabs(g1-g2)
        else: return math.fabs(g1-g2)

    def desicionTime(self,p1,p2):
        x1,y1=p2.get_position()
        team_p1 = ("home" if p1.isHomeTeamPlayer()==True else "away")
        team_p1 = (self.teams.away_team if team_p1=="home" else self.teams.home_team)
        team_p2 = ("home" if p1.isHomeTeamPlayer()==True else "away")
        team_p2 = (self.teams.away_team if team_p2=="home" else self.teams.home_team)
        d_min=126.0 # meters
        p_close=None
        if team_p1==team_p2:
            player_list=team_p2.getTeamPlayers()
            for p in player_list:
                x2,y2=p.get_position()
                d = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
                if d < d_min:
                    d_min = d
                    p_close=p.getJerseyNumber()
            t = d_min/10.0
        else:
            pass
        # print t,p_close,d_min,p1.getJerseyNumber(),p2.getJerseyNumber()
        return t



    #---------------------------------------------------------------------


    def passAdvantage(self, p1,radius,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,risk_ignore):
            if p1.isHomeTeamPlayer(): own_team = self.teams.home_team
            else: own_team = self.teams.away_team

            passAdvantages = {}

            for p2 in own_team.getTeamPlayers():
                if p1.getJerseyNumber() != p2.getJerseyNumber():
                    pa = ((10 + self.gain(p1, p2,radius)) / (10 + self.overallRisk(p1, p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,risk_ignore)))
                    passAdvantages[pa] = p2.getJerseyNumber()


            max_pass = max(passAdvantages.keys())
            return max_pass, passAdvantages[max_pass]



    def goalChance(self, p1,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,risk_ignore):
        goal_keeper = Analyze.detectGoalKeeperWithPositions(p1, self.teams)
        goal_keeper_x, goal_keeper_y = goal_keeper.get_position()

        d1 = math.sqrt(math.pow(goal_keeper_x - p1.getX(), 2) + math.pow(goal_keeper_y - p1.getY(), 2))
        angle = math.atan2(math.fabs(p1.getY() - goal_keeper_y), math.fabs(p1.getX() - goal_keeper_x)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, goal_keeper,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT, risk_ignore,goal_keeper=False)

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


    def effectiveness_withComponents(self, p1, p2,weights,risk_ignore):
        try:
            PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,sht_radius,w1,w2,w3,w4=weights
        except TypeError:
            PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,sht_radius,w1,w2,w3,w4=1,1,1,0,0,0,0
        # W1,W2,W3=weights
        # radius=weights
        # w1, w4, w2, w3 = W1, W2, W3, W4
        desicionTime = (w4/max_desicionTime)*self.desicionTime(p1,p2)
        gain = (w1/max_gain) * self.gain(p1, p2,sht_radius)

        if gain <0:
            gain=gain/(desicionTime+0.001)
        else: gain *= desicionTime

        passAdvantage, pa_player = self.passAdvantage(p2,sht_radius,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,risk_ignore)
        passAdvantage = (w2/max_passAdvantage)*passAdvantage
        # goalChance = (w3/max_goalChance) * self.goalChanceWithOSPP(p2)
        goalChance = (w3/max_goalChance) * self.goalChance(p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,risk_ignore)
        overallRisk = self.overallRisk(p1, p2,PASS_SOURCE_RADIUS,PASS_TARGET_RADIUS_COEFFICIENT,risk_ignore)

        effectiveness = gain + passAdvantage + goalChance


        return (overallRisk, gain, passAdvantage, pa_player, goalChance, effectiveness)


        # effectiveness = 0

        # comp_list = [overallRisk]
        # if gain_listener:
        #     effectiveness += gain
        #     comp_list.append(gain)
        # else:
        #     comp_list.append(None)
        # if effectiveness_listener:
        #     pass
        # if pass_advantage_listener:
        #     effectiveness += passAdvantage
        #     comp_list.append(passAdvantage)
        #     comp_list.append(pa_player)
        # else:
        #     comp_list.append(None)
        #     comp_list.append(None)
        # if goal_chance_listener:
        #     effectiveness += goalChance
        #     comp_list.append(goalChance)
        # else:
        #     comp_list.append(None)
        #
        # if not Analyze.isSuccessfulPass(p1, p2):
        #     if effectiveness < 0:
        #         effectiveness *= 10
        #     else:
        #         effectiveness = -effectiveness * 10
        #
        # comp_list.append(effectiveness)
        # return comp_list


    def __str__(self):
        pass


